try:
    from exceptions import Exception
except ImportError:
    pass
import ckan.logic as logic
import ckan.authz as authz
import ckan.plugins.toolkit as t
_ = t._
c = t.c
import ckan.model as model

ValidationError = logic.ValidationError
NotFound = logic.NotFound

def _getOriginalPackage(context,data_dict):
    model = context['model']
    name_or_id = data_dict.get('id') or data_dict.get('name')
    if name_or_id is None:
        raise ValidationError({'id': _('Missing value')})

    pkg = model.Package.get(name_or_id)
    if pkg is None:
        raise NotFound(_('Package was not found.'))
    context["package"] = pkg

    return pkg

def users_role_for_group_or_org(user_name, org_id):
    ''' Returns the user's role for the group. (Ignores privileges that cascade
    in a group hierarchy.)

    '''

    user_id = authz.get_user_id_for_username(user_name, allow_none=True)
    if not user_id:
        return None
    # get any roles the user has for the group
    q = model.Session.query(model.Member) \
        .filter(model.Member.table_name == 'user') \
        .filter(model.Member.group_id == org_id) \
        .filter(model.Member.state == 'active') \
        .filter(model.Member.table_id == user_id)
    # return the first role we find
    for row in q.all():
        return row.capacity
    return None

def _get_user(username):
    ''' Try to get the user from c, if possible, and fallback to using the DB '''
    if not username:
        return None
    # See if we can get the user without touching the DB
    try:
        if c.userobj and c.userobj.name == username:
            return c.userobj
    except AttributeError:
        # c.userobj not set
        pass
    except TypeError:
        # c is not available
        pass
    # Get user from the DB
    return model.User.get(username)

def is_sysadmin(username):
    authz.is_sysadmin(username)

def is_admin_of_org(username, owner_org):
    ''' Returns True is username is admin of an organization '''
    return users_role_for_group_or_org(username, owner_org) == 'admin'

def can_publish_in_org(username, owner_id):
    return is_sysadmin(username) or is_admin_of_org(username, owner_id)


def package_publish(context, data_dict):
    if not data_dict:
        return {'success': False, 'msg': _('missing parameter data_dict')}

    if len(data_dict) != 2 or u'private' not in data_dict or u'id' not in data_dict:
        return {'success': False, 'msg': _('data_dict must be in this form {id : 53535, private : True}')}

    pkg = _getOriginalPackage(context, data_dict)

    if authz.is_sysadmin(context[u"user"]) and pkg.private == True:
        return {'success': True}

    if not pkg.owner_org:
        return {'success': False, 'msg': _('Can\'t publish without an organization')}

    admin = users_role_for_group_or_org(context[u'user'], pkg.owner_org) == 'admin'
    if not admin:
        return {'success': False, 'msg': 'Not allowed to publish wrong role or api'}

    elif pkg.private == True and pkg.private != data_dict[u'private']:
        return {'success': True}

    return {'success': False, 'msg': 'Wrong state, package is already published'}

def package_unpublish(context, data_dict):
    if not data_dict:
        return {'success': False, 'msg': _('missing parameter data_dict')}

    if len(data_dict) != 2 or u'private' not in data_dict or u'id' not in data_dict:
        return {'success': False, 'msg': _('data_dict must be in this form {id : 53535, private : True}')}

    pkg = _getOriginalPackage(context, data_dict)

    if authz.is_sysadmin(context[u"user"]) and pkg.private == False:
        return {'success': True}

    if not pkg.owner_org:
        return {'success': False, 'msg': _('Can\'t unpublish without an organization')}

    admin = users_role_for_group_or_org(context[u'user'], pkg.owner_org) == 'admin'
    if not admin:
        return {'success': False, 'msg': 'Not allowed to unpublish wrong role or api'}
    elif pkg.private == False and pkg.private != data_dict[u'private']:
        return {'success': True}

    return {'success': False, 'msg': 'Wrong state, package is already unpublished'}

def package_update_barrier(context, data_dict):
    # TODO throw exception if data_dict not defined
    if not data_dict:
        raise Exception(_('missing parameter data_dict'))

    pkg = _getOriginalPackage(context, data_dict)

    if 'private' not in data_dict:
        data_dict['private'] = pkg.private

    if pkg.private != data_dict[u'private']:
        return {'success': False, 'msg': 'Not allowed to publish wrong role or api'}
    else:
        return {'success': True}

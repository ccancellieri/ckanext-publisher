# encoding: utf-8

import logging
import datetime
import time
import json

from ckan.common import config
import ckan.common as converters
import six
from six import text_type

import ckan.lib.helpers as h
import ckan.plugins as plugins
import ckan.logic as logic
from ckanext.publisher.logic.auth import can_publish_in_org
import ckan.logic.schema as schema_
import ckan.lib.dictization as dictization
import ckan.lib.dictization.model_dictize as model_dictize
import ckan.lib.dictization.model_save as model_save
import ckan.lib.navl.dictization_functions
import ckan.lib.navl.validators as validators
import ckan.lib.plugins as lib_plugins
import ckan.lib.email_notifications as email_notifications
import ckan.lib.search as search
import ckan.lib.uploader as uploader
import ckan.lib.datapreview
import ckan.lib.app_globals as app_globals
from ckan.common import _, request
import inspect as inspect
log = logging.getLogger(__name__)

# Define some shortcuts
# Ensure they are module-private so that they don't get loaded as available
# actions in the action API.
_validate = ckan.lib.navl.dictization_functions.validate
_get_action = logic.get_action
_check_access = logic.check_access
NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
_get_or_bust = logic.get_or_bust



@plugins.toolkit.chained_action
def package_create(next_auth, context, data_dict):
    # For the UI, we are not sending the private flag so let's add to it
    if 'private' not in data_dict: #or ('private' in data_dict and data_dict['private'] == False):
            data_dict['private'] = True

     # Let's check for the type private field should be a boolean
    elif type(data_dict['private']) != bool:
        raise ValidationError({'private': _('The private flag must be a boolean not a string')})

    # The data dict contains the private flag
    # Let's check if it's properly set and if we are allowed to use it
    org_id = logic.converters.convert_group_name_or_id_to_id(data_dict['owner_org'], context)
    can_publish = can_publish_in_org(context['user'], org_id)
    publish = data_dict['private'] == False
    if publish and not can_publish:
        # https://github.com/ckan/ckan/blob/master/ckan/views/api.py#L294-L350
        raise NotAuthorized(_('User not authorized to create a public metadata.'))

    # delegate to the next action
    return next_auth(context, data_dict)

@plugins.toolkit.chained_action
def package_update(next_auth, context, data_dict):
    _check_access('package_update_barrier', context, data_dict)
    return next_auth(context,data_dict)

@plugins.toolkit.chained_action
def package_patch(next_auth, context, data_dict):
    _check_access('package_update_barrier', context, data_dict)
    # delegate to the next action
    return next_auth(context,data_dict)


def package_publish(context, data_dict):
    _check_access('package_publish', context, data_dict)
    return ckan.logic.action.patch.package_patch(context,data_dict)

def package_unpublish(context, data_dict):
    _check_access('package_unpublish', context, data_dict)
    return ckan.logic.action.patch.package_patch(context, data_dict)



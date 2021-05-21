# encoding: utf-8
from ckan.lib.plugins import DefaultPermissionLabels
import ckan.plugins.toolkit as toolkit
import logging
import ckan.plugins as p
import ckan.logic as logic
import ckanext.publisher.logic.action as action
import ckanext.publisher.logic.auth as auth
_check_access = logic.check_access
_get_action = logic.get_action
log = logging.getLogger(__name__)

class PublisherPlugin(p.SingletonPlugin, DefaultPermissionLabels):
    p.implements(p.IActions)
    p.implements(p.IAuthFunctions)
    p.implements(p.IConfigurer)

    # IConfigurer
    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')
        toolkit.add_resource('fanstatic', 'publisher')

    # IActions

    def get_actions(self):
        actions = {
            'package_publish': action.package_publish,
            'package_unpublish': action.package_unpublish,
            'package_update': action.package_update,
            'package_create': action.package_create,
            'package_patch': action.package_patch
        }
        return actions

    # IAuthFunctions

    def get_auth_functions(self):
        return {
            'package_publish': auth.package_publish,
            'package_unpublish': auth.package_unpublish,
            'package_update_barrier': auth.package_update_barrier
        }
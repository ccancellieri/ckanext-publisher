import ckan.plugins
import pytest
import ckan.tests.factories as factories
import ckan.tests.helpers as helpers
import ckan.logic as logic
from ckan.plugins.toolkit import NotAuthorized


class TestPublisher(object):
    publisher = None
    package = None
    context = None
    owner_org = None
    owner_org_two = None

    @classmethod
    def setup_class(cls):
        helpers.reset_db()
        # Test code should use CKAN's plugins.load() function to load plugins
        # to be tested.
        if not ckan.plugins.plugin_loaded('publisher'):
            ckan.plugins.load('publisher')
        # Create user and package
        cls.syadmin = factories.Sysadmin()
        cls.publisher = factories.User()
        cls.editor = factories.User()
        cls.member = factories.User()
        cls.context = {
            'ignore_auth': False,
            'user': cls.publisher['name']
        }
        cls.editor_context = {
            'ignore_auth': False,
            'user': cls.editor['name']
        }
        cls.owner_org = factories.Organization(
            users=[{'name': cls.publisher['id'], 'capacity': 'admin'}, {'name': cls.editor['id'], 'capacity': 'editor'},
                   {'name': cls.member['id'], 'capacity': 'member'}]
        )
        cls.owner_org_two = factories.Organization(
            users=[{'name': cls.publisher['id'], 'capacity': 'admin'}, {'name': cls.editor['id'], 'capacity': 'editor'},
                   {'name': cls.member['id'], 'capacity': 'member'}]
        )

    def setup_method(self):
        self.package = factories.Dataset(owner_org=self.owner_org['id'])

    def test_as_admin_I_can_publish_a_created_metadata(self, app):
        new_context = {
            'ignore_auth': False,
            'user': self.publisher['name']
        }
        res = helpers.call_action('package_publish', new_context, id=self.package['id'], private=False)
        assert res['private'] == False, 'Publisher is not able to publish'

    def test_as_admin_I_can_unpublish_a_created_metadata(self):
        new_context = {
            'ignore_auth': False,
            'user': self.publisher['name']
        }
        # Publish package
        helpers.call_action('package_publish', new_context, id=self.package['id'], private=False)
        # Test
        res = helpers.call_action('package_unpublish', new_context, id=self.package['id'], private=True)
        assert res['private'] == True, 'Publisher is not able to unpublish'

    def test_as_admin_I_can_not_publish_a_published_metadata(self):
        # Publish package
        helpers.call_action('package_publish', self.context, id=self.package['id'], private=False)
        # Test
        new_context = {
            'ignore_auth': False,
            'user': self.publisher['name']
        }
        with pytest.raises(NotAuthorized):
            helpers.call_action('package_publish',
                                new_context,
                                id=self.package['id'], private=False)

    def test_its_not_possible_to_call_package_publish_or_package_unpublish_with_wrong_arguments(self):
        new_context = {'ignore_auth': False, 'user': self.publisher['name']}
        with pytest.raises(NotAuthorized):
            helpers.call_action('package_publish', new_context, id=self.package['id'], private=False,
                                wrong_argu="wrong argment")

    def test_as_member_I_can_not_publish_or_unpublish_metada_in_my_organization_using_action_package_publish_and_package_unpublish(
            self):
        new_context = {'ignore_auth': False, 'user': self.publisher['name']}
        with pytest.raises(NotAuthorized):
            helpers.call_action('package_unpublish',
                                new_context,
                                id=self.package['id'], private=False)

        with pytest.raises(NotAuthorized):
            helpers.call_action('package_publish',
                                new_context,
                                id=self.package['id'], private=True)

    def test_as_member_I_can_not_publish_or_unpublish_metada_in_my_organization_using_action_package_update(self):
        new_context = {
            'ignore_auth': False,
            'user': self.member['name']
        }
        with pytest.raises(NotAuthorized):
            helpers.call_action('package_update',
                                new_context,
                                id=self.package['id'], private=False)

        with pytest.raises(NotAuthorized):
            helpers.call_action('package_update',
                                new_context,
                                id=self.package['id'], private=True)

    def test_as_sys_admin_Im_able_unpublish_and_publish_metadata(self):
        new_context = {
            'ignore_auth': False,
            'user': self.syadmin['name']
        }
        res = helpers.call_action('package_unpublish', new_context, id=self.package['id'], private=False)
        assert res['private'] == False, 'Publisher is not able to unpublish'

        res = helpers.call_action('package_unpublish', new_context, id=self.package['id'], private=True)
        assert res['private'] == True, 'Publisher is not able to unpublish'

    def test_metadata_can_not_be_published_outiside_an_organization(self):
        new_context = {
            'ignore_auth': False,
            'user': self.publisher['name']
        }
        with pytest.raises(NotAuthorized):
            helpers.call_action('package_publish',
                                new_context,
                                id=self.package['id'], private=False, owner_org='notexist')

    def test_as_admin_I_can_publish_metada_in_my_organization_using_action_package_publish(self):
        res = helpers.call_action('package_publish', self.context, id=self.package['id'], private=False)
        assert res['private'] == False, 'Publisher is not able to publish'

    def test_as_admin_I_can_not_publish_metadata_in_my_organization_using_action_package_update(self):
        new_context = {
            'ignore_auth': False,
            'user': self.publisher['name']
        }
        with pytest.raises(NotAuthorized):
            helpers.call_action('package_update', context=new_context,
                                id=self.package['id'],
                                private=False)

    def _test_as_editor_I_can_not_unpublish_metada_in_my_organization_using_action_package_update(self):
        # Make package public
        # Context is admin
        helpers.call_action('package_publish',
                            self.context,
                            id=self.package['id'], private=False)
        new_context = {
            'ignore_auth': False,
            'user': self.editor['name']
        }
        with pytest.raises(NotAuthorized):
            helpers.call_action('package_update',
                                new_context,
                                id=self.package['id'], private=True)

        with pytest.raises(NotAuthorized):
            helpers.call_auth('package_update',
                                new_context,
                                id=self.package['id'], private=False)

    def test_as_editor_I_can_not_publish_metadata_in_my_organization_using_action_package_patch(self):
        package = helpers.call_action('package_create', self.context, **self.package)
        new_context = {
            'ignore_auth': False,
            'user': self.editor['name']
        }
        with pytest.raises(NotAuthorized):
            helpers.call_action('package_update', context=new_context,
                                id=package['id'],
                                private=False)

    def test_as_editor_I_can_not_publish_metadata_in_my_organization_using_action_package_patch(self):
        new_context = {
            'ignore_auth': False,
            'user': self.editor['name']
        }
        with pytest.raises(NotAuthorized):
            helpers.call_action('package_update', context=new_context,
                                id=self.package['id'],
                                private=True)

    def test_as_editor_I_can_not_publish_metada_in_my_organization_using_action_package_publish(self):
        new_context_ = {
            'ignore_auth': False,
            'user': self.editor['name']
        }
        with pytest.raises(NotAuthorized):
            helpers.call_action('package_publish',
                                new_context_,
                                id=self.package['id'], private=False)

    def test_as_editor_I_can_not_unpublish_metada_in_my_organization_using_action_package_unpublish(self):
        new_context = {
            'ignore_auth': False,
            'user': self.editor['name']
        }
        with pytest.raises(NotAuthorized):
            helpers.call_action('package_unpublish',
                                new_context,
                                id=self.package['id'], private=True)

    def test_as_editor_is_able_to_create_resources_and_delete_resources(self):
        resource = factories.Resource(package_id=self.package['id'])
        assert logic.check_access('resource_create', {'user': self.editor['name']}, resource)
        assert logic.check_access('resource_delete', {'user': self.editor['name']},
                                  {'id': resource['id']})

    def test_as_admin_is_able_to_create_resources_and_delete_resources(self):
        resource = factories.Resource(package_id=self.package['id'])
        assert logic.check_access('resource_create', {'user': self.publisher['name']}, resource)
        assert logic.check_access('resource_delete', {'user': self.publisher['name']},
                                  {'id': resource['id']})

    def test_as_member_is_Im_not_able_to_create_resources_and_delete_resources(self):
        new_context = {
            'ignore_auth': False,
            'user': self.member['name']
        }
        resource = factories.Resource(package_id=self.package['id'])
        with pytest.raises(NotAuthorized):
            helpers.call_action('resource_create',
                                new_context,
                                package_id=self.package['id'])

        with pytest.raises(NotAuthorized):
            helpers.call_action('resource_delete',
                                new_context,
                                id=resource['id'])

    def test_as_editor_is_able_to_update_resource(self):
        # Create resource
        new_context = {
            'ignore_auth': False,
            'user': self.editor['name']
        }
        resource = factories.Resource(package_id=self.package['id'])
        res = helpers.call_action('resource_patch', new_context, id=resource['id'], name='new_name')
        assert res['name'] == 'new_name', 'Editor can not edit the resource'

    def test_as_admin_is_able_to_update_resource(self):
        # Create resource
        new_context = {
            'ignore_auth': False,
            'user': self.publisher['name']
        }
        resource = factories.Resource(package_id=self.package['id'])
        res = helpers.call_action('resource_patch', new_context, id=resource['id'], name='new_name')
        assert res['name'] == 'new_name', 'Editor can not edit the resource'

    def test_admin_of_two_organization_can_move_metadata_between_adminstered_organizations(self):
        new_context = {
            'ignore_auth': False,
            'user': self.publisher['name']
        }
        res = helpers.call_action('package_patch', new_context, id=self.package['id'],
                                  owner_org=self.owner_org_two['id'])
        assert res['owner_org'] == self.owner_org_two['id'], 'Admin unable to move dataset'

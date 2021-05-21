import ckan.plugins
import pytest
import ckan.tests.factories as factories
import ckan.tests.helpers as helpers
from ckan.plugins.toolkit import NotAuthorized, ValidationError


class TestPublisherCreation(object):
    publisher = None
    package = None
    context = None
    owner_org = None
    owner_org_two = None

    @classmethod
    def setup_class(cls):
        helpers.reset_db()
        '''Nose runs this method once to setup our test class.'''
        # Test code should use CKAN's plugins.load() function to load plugins
        # to be tested.
        if not ckan.plugins.plugin_loaded('publisher'):
            ckan.plugins.load('publisher')
        # Create user and package
        cls.syadmin = factories.Sysadmin()
        cls.publisher = factories.User()
        cls.editor = factories.User()
        cls.member = factories.User()
        sysadmin_context = {
            'ignore_auth': False,
            'user': cls.syadmin['name']
        }
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

    def test_as_sysadmin_I_can_publish_a_created_metadata(self, app):
        new_context = {
            'ignore_auth': False,
            'user': self.syadmin['name']
        }
        res = helpers.call_action('package_publish', new_context, id=self.package['id'], private=False)
        assert res['private'] == False, 'Sysadmin is not able to publish'

    def test_as_admin_I_can_create_metadata_private_set_to_False(self):
        res = helpers.call_action('package_create', self.context, name='test_package', owner_org=self.owner_org['id'],
                                  private=False)
        assert res['private'] == False, 'Publisher is not able to create package set to False'

    def test_as_editor_I_can_not_create_metadata_private_set_to_False(self):
        new_context = {
            'ignore_auth': False,
            'user': self.editor['name']
        }
        with pytest.raises(NotAuthorized):
            helpers.call_action('package_create', new_context, name='test_package', owner_org=self.owner_org['id'],
                                private=False)

    def test_I_can_not_create_metadata_with_private_as_a_string(self):
        new_context = {
            'ignore_auth': False,
            'user': self.publisher['name']
        }
        with pytest.raises(ValidationError):
            helpers.call_action('package_create', new_context, name='test_package',
                                owner_org=self.owner_org['id'],
                                private='False')

    def test_as_member_I_can_not_create_metadata_private_set_to_False(self):
        new_context = {
            'ignore_auth': False,
            'user': self.member['name']
        }
        with pytest.raises(NotAuthorized):
            helpers.call_action('package_create', new_context, name='test_package',
                                owner_org=self.owner_org['id'],
                                private=False)

    def test_as_member_I_can_not_create_metadata(self):
        new_context = {
            'ignore_auth': False,
            'user': self.member['name']
        }
        with pytest.raises(ValidationError):
            helpers.call_action('package_create', new_context, name='test_package',
                                owner_org=self.owner_org['id'],
                                private='False')

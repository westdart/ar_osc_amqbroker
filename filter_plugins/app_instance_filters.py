#
# Filter functions defining naming standard for AMQ and Interconnect instances
#

def app_common_name(app_instance):
    return app_instance['name'].lower()

def app_namespace(app_instance, deployment_phase):
    if 'namespace' in app_instance:
        return app_instance['namespace'].lower()

    name = app_common_name(app_instance)
    phase = deployment_phase.lower()
    if 'parent' in app_instance:
        return app_instance['parent'].lower() + "-" + phase
    return name + "-" + phase

def application_name(app_instance):
    name = app_common_name(app_instance)
    return name + "-broker"

def config_map_name(app_instance):
    return application_name(app_instance) + "-config-map"

def secrets_name(app_instance):
    return application_name(app_instance) + "-secrets"

class FilterModule(object):
    '''
    custom jinja2 filters for working with collections
    '''

    def filters(self):
        return {
            'app_namespace': app_namespace,
            'app_common_name': app_common_name,
            'application_name': application_name,
            'config_map_name': config_map_name,
            'secrets_name': secrets_name,
        }

'''
Testing
'''
import unittest


class TestAppInstanceFilters(unittest.TestCase):
    app_instance = {
        'name': "TRG001"
      }
    app_instance_with_parent = {
        'name':   "TRG002",
        'parent': "TRG001"
    }

    app_instances = [app_instance, app_instance_with_parent]

    def test_app_namespace(self):
        self.assertEqual('trg001-dev', app_namespace(self.app_instance, 'dev'))

    def test_app_namespace_with_parent(self):
        self.assertEqual('trg001-dev', app_namespace(self.app_instance_with_parent, 'dev'))

    def test_application_name(self):
        self.assertEqual('trg001-aspera', application_name(self.app_instance))

    def test_application_name_with_parent(self):
        self.assertEqual('trg002-aspera', application_name(self.app_instance_with_parent))

    def test_config_map_name(self):
        self.assertEqual('trg001-aspera-config-map', config_map_name(self.app_instance))

    def test_secrets_name(self):
        self.assertEqual('trg001-aspera-secrets', secrets_name(self.app_instance))


if __name__ == '__main__':
    unittest.main()

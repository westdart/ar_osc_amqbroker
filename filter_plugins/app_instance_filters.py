#
# Filter functions defining naming standard for AMQ and Interconnect instances
#
import re
def app_var(app_instance, name, default):
    if name in app_instance:
        return app_instance[name]
    return default

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

def broker_application_name(app_instance):
    name = app_common_name(app_instance)
    return name + "-broker"

class FilterModule(object):
    '''
    custom jinja2 filters for working with collections
    '''

    def filters(self):
        return {
            'broker_application_name': broker_application_name,
            'app_namespace': app_namespace,
            'app_common_name': app_common_name
        }

'''
Testing
'''
import unittest


class TestAppInstanceFilters(unittest.TestCase):
    app_instance = {
        'name': "TRG001",
        'incomingAddressList': ['addr_TRG001_1', 'addr_TRG001_2', 'addr_TRG001_3']
      }
    app_instance_with_parent = {
        'name':   "TRG002",
        'parent': "TRG001",
        'cert_locale': 'Else',
        'amq_ic_domain': 'test.com',
        'incomingAddressList': ['addr_TRG002_1', 'addr_TRG002_2', 'addr_TRG002_3']
    }

    app_instances = [app_instance, app_instance_with_parent]

    def test_something(self):
        self.assertEqual('', '')


if __name__ == '__main__':
    unittest.main()

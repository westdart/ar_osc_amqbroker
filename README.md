# ar_osc_amqbroker
Ansible Role for OpenShift Config targeting the AMQ Broker application

## amqbroker_config

Generate the config files required to build out AMQ Broker 
nodes

## Requirements


## Role Variables
The following details:
- the parameters that should be passed to the role (aka vars)
- the defaults that are held
- the secrets that should generally be sourced from an ansible vault.

### Parameters:
| Variable                        | Description                             | Default |
| --------                        | -----------                             | ------- |
| ar_osc_amqbroker_ns             | Openshift Namespace / Project           | None    |
| ar_osc_amqbroker_name           | Application name                        | None    |
| ar_osc_amqbroker_instance       | The amq broker instance var (see below) | None    |
| ar_osc_amqbroker_user_roles     | Array of name/role pairs (see below)    | None    |
| ar_osc_amqbroker_admin_username | The amq broker admin user               | None    |
| ar_osc_amqbroker_admin_password | The amq broker admin user password      | None    |

The 'ar_osc_amqbroker_instance' variable is an object that contains the details on each instance required.

The structure is:
```
  {
    name: <the name>,
    namespace: <the namespace>,
    incomingAddressList: [<list of queues where this broker is the terminus>],
    sendToDLAOnNoRoute: '<true|false>',
    broker_node_port: <node-port>, # Optional - for direct connection to the broker from outside the cluster
  }
```

For user / role pairs the structure is:
```
  [
    { name: "name1", role: "user" },
    { name: "name2", role: "viewer" },
    { name: "name3", role: "admin" },
  ]
```
This shows the three possible roles. Note, the admin user defined in 
'ar_osc_amqbroker_admin_username' within the secrets is added to the
'admin' group automatically and does not need to be defined in the 
'ar_osc_amqbroker_user_roles' array.
The names of the users in 'ar_osc_amqbroker_user_roles' array must match
with those provided in the secrets provided in the key/value form:
<username>=<password>

### Defaults
| Variable                      | Description                             | Default                   |
| --------                      | -----------                             | -------                   |
| ar_osc_amqbroker_k8s_template | The Broker application template         | 'amq-broker-72-basic.yml' |
| ar_osc_amqbroker_config_dest  | Area in which to generate config        | '/tmp'                    |
| ar_osc_amqbroker_xml_template | The template to generate amq xml config | 'amq7-template.xml.j2'    |


### Globals
The following are variable used within the role:

| Variable           | Description                    | Default         |
| --------           | -----------                    | -------         |
| amqbroker_image    | The AMQ Broker Image           | None            |
| amqbroker_image_ns | The AMQ Broker Image Namespace | 'openshift'     |
| amqbroker_data_dir | The AMQ Broker data directory  | '/opt/amq/data' |


## Dependencies

- openshift-applier

## Example Playbook

To create AMQ Broker:
```
- name: Build AMQ Broker
  hosts: localhost
  tasks:
    - name: "Create AMQ Broker"
      include_role:
        name: ar_osc_amqbroker
      vars:
        ar_osc_amqbroker_ns:              "my-namespace"
        ar_osc_amqbroker_name:            "my-broker"
        ar_osc_amqbroker_config_dest:     "/tmp/my-broker"
        ar_osc_amqbroker_k8s_template:    "amq-broker-72-basic.yml"
        ar_osc_amqbroker_admin_username:  "admin"
        ar_osc_amqbroker_admin_password:  "password"
        ar_osc_amqbroker_user_roles:      [{ name: "systemuser", role: "user"   },
                                           { name: "viewer",     role: "viewer" }]        
        systemuser:                       "systemuser-password"
        viewer:                           "viewer-password" 
```


## License

BSD

## Author Information

dstewart@redhat.com

# ar_osc_amqbroker
Ansible Role for OpenShift deployment of the AMQ Broker application

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
    amqbroker_image: <the image>, # Optional, can be defined globally
    incomingAddressList: [<list of queues where this broker is the terminus>],
    sendToDLAOnNoRoute: '<true|false>',
    broker_node_port: <node-port>, # Optional - for direct connection to the broker from outside the cluster
  }
```

For user / role pairs defined in the 'ar_osc_amqbroker_user_roles' variable, the structure is:
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
| Variable                                   | Description                                                                | Default                                                                                                                                                                                 |
| --------                                   | -----------                                                                | -------                                                                                                                                                                                 |
| ar_osc_amqbroker_image                     | The full name for the docker image to use                                  | 'amqbroker_image' taken from the 'ar_osc_amqbroker_instance' or global ansible variable namespace                                                                                       |
| ar_osc_amqbroker_k8s_template              | The Broker application kubernetes template                                 | 'amq-broker-72-basic.yml'                                                                                                                                                               |
| ar_osc_amqbroker_config_dest               | Area in which to generate config                                           | '/tmp'                                                                                                                                                                                  |
| ar_osc_amqbroker_xml_template              | The template to generate amq xml config                                    | 'amq7-template.xml.j2'                                                                                                                                                                  |
| ar_osc_amqbroker_pvc                       | Definition for the storage to be used by the broker                        | 1Gi mounted at '/opt/amq/data' with ;ReadWriteOnce' access mode                                                                                                                         |
| ar_osc_amqbroker_container_max_memory      | The maximum memory limit for the container                                 | 'container_max_mem' taken either from the 'ar_osc_amqbroker_instance' or global ansible variable namespace, otherwise '5G'                                                              |
| ar_osc_amqbroker_java_max_memory_ratio     | Ratio of maximum container memory defining the maximum for Java ('Xmx')    | 'java_max_mem_ratio' taken either from the 'ar_osc_amqbroker_instance' or global ansible variable namespace, otherwise '0' (ensuring that memory params are not specified for Java)     |
| ar_osc_amqbroker_java_initial_memory_ratio | Ratio of maximum Java memory ('Xmx') defining the minimum for Java ('Xms') | 'java_initial_mem_ratio' taken either from the 'ar_osc_amqbroker_instance' or global ansible variable namespace, otherwise '0' (ensuring that memory params are not specified for Java) |
| ar_osc_amqbroker_global_max_size           | Limit of amount of memory the Broker can use before it starts paging       | 'global_max_size' taken either from the 'ar_osc_amqbroker_instance' or global ansible variable namespace, otherwise 'ar_osc_amqbroker_default_global_max_size'                          |
| ar_osc_amqbroker_default_global_max_size   | Default for 'ar_osc_amqbroker_global_max_size'                             | A 5th of 'Xmx', i.e. ((ar_osc_amqbroker_container_max_memory * ar_osc_amqbroker_java_max_memory_ratio ) / (100 * 5))                                                                    |
| ar_osc_amqbroker_openshift_login_url       | The Openshift cluster to connect to                                        | 'oc_login_url' taken either from the 'ar_osc_amqbroker_instance' or global ansible variable namespace                                                                                   |

For the 'ar_osc_amqbroker_pvc' variable, the structure is:
```
  {
    accessModes: <List of modes to assign to this pvc>,
    size: '<Size required by the pvc',
    mountPath: '<mount path for the pvc (default: /opt/amq/data)>',
    storageClass: '<optional: some storage class>',
    volumeName: '<optional: some name>',
    name: '<optional: the PVC name>',
    oc_login_url: "<optional: The Openshift management endpoint URL>"
  }
```

### Globals
The following are variable used within the role:

| Variable           | Description                                                                          | Default         |
| --------           | -----------                                                                          | -------         |
| amqbroker_image    | The AMQ Broker Image                                                                 | None            |
| amqbroker_data_dir | The AMQ Broker data directory                                                        | '/opt/amq/data' |
| oc_login_url       | The Openshift management endpoint URL (Can also be provided as an instance variable) | None            |


## Dependencies
- ar_os_common
- ar_os_seed
- casl-ansible/roles/openshift-labels

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
        ar_osc_amqbroker_image:           "docker-registry-default.t2.training.local/imgns/amq-broker-72-openshift:1.2"
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

MIT / BSD

## Author Information

This role was created in 2020 by David Stewart (dstewart@redhat.com)

aspera_config
=============

Generate the config files required to build out Aspera file transfer 
nodes

Requirements
------------


Role Variables
--------------
The following details:
a. the parameters that should be passed to the role (aka vars)
b. the defaults that are held
c. the secret that should generally be sourced from an ansible vault.


| Variable                                | Description                                                                         | Default                   |
| --------                                | -----------                                                                         | -------                   |
| aspera_instance                         | Object defining the Aspera instance (see below)                                     | None                      |
| aspera_config_ssh_port                  | Port that SSHD will listen on                                                       | 22                        |
| aspera_config_dest                      | Path to where generated config files are placed                                     | /tmp                      |
| aspera_config_docker_registry           | The docker registry to push built images to                                         | None                      |
| aspera_config_docker_registry_dest_path | The path under the registry where images are pushed (typically a k8s namespace)     | 'openshift'               |
| aspera_config_package_base_url          | Base URL to where the RPM files can be found (if not using a subscribed base image) | None                      |
| aspera_config_license_file              | Path to the Aspera license file for the instance                                    | 'aspera_license_file' var |

The 'aspera_instance' variable is an object that contains the details on each instance required.

The structure is:
```
  {
    name: "<the name>",
    aspera_image: "<the image tag to use>",
    aspera_license_file: "<path to the Aspera license file>",
    aspera_node_port: <the node port to use to connect over ssh to Aspera>
  }
```

Secrets:
--------
| Variable                                     | Description                                 | Default |
| --------                                     | -----------                                 | ------- |
| amq_broker_config_admin_username             | The admin username                          | None    |
| amq_broker_config_admin_password             | The admin username                          | None    |
| amq_broker_config_aditional_users[user_name] | Array of uasername/Password key value pairs | None    |

Default Variables
----------------- 

| Variable                             | Description                                                                 | Default                                                           |
| --------                             | -----------                                                                 | -------                                                           |
| aspera_config_namespace              | Openshift Namespace / Project                                               | fn: app_namespace                                                 |
| aspera_config_common_name            | Application name                                                            | aspera_instance.name                                              |
| aspera_config_sshd_config_file       | The generated SSHD config path                                              | aspera_config_dest + '/sshd_config'                               |
| aspera_config_file                   | The generated Aspera config path                                            | aspera_config_dest + '/aspera_config'                             |
| aspera_config_launch_script          | The script executed to start Aspera and related processes                   | role_path + '/files/launch.sh'                                    |
| aspera_config_k8s_template           | The k8s template to use                                                     | 'aspera-app-1.yml'                                                |
| aspera_config_username               | The Aspera username                                                         | 'aspera'                                                          |
| aspera_config_version                | The version to ascribe to images created                                    | '1.0'                                                             |
| aspera_config_sshd_internal_port     | The SSHD internal port the Aspera Pod listens on                            | '33001'                                                           |
| aspera_config_server_package         | The Aspera Server package to use                                            | aspera_config_package_base_url + '/dummy-1-0.noarch.rpm'          |
| aspera_config_endpoint_package       | The Aspera Endpoint package to use                                          | aspera_config_package_base_url + '/dummy-1-0.noarch.rpm'          |
| aspera_config_have_rhel_subscription | Boolean marking if th base image is subscribed to RedHat satellite channels | false                                                             |
| aspera_config_package_dependencies   | Direct Aspera package dependencies                                          | ```['openssh-server', 'perl', 'perl-Data-Dumper', 'nmap-ncat']``` |
| aspera_config_rhel_base_image_name   | The image name given to the RHEL 7 image + dependent packages               | 'aspera-rhel7-base'                                               |
| aspera_config_package_list           | The complete list of package dependencies                                   | (see dependencies)                                                |

Dependencies
------------

The following are RPM dependencies for the deployment of Aspera.
These should be either available through subscription-manager or direct
via a web site defined by the variable 'aspera_config_package_base_url'
```
tcp_wrappers-libs-7.6-77.el7.x86_64.rpm
fipscheck-lib-1.4.1-6.el7.x86_64.rpm
fipscheck-1.4.1-6.el7.x86_64.rpm
openssh-7.4p1-21.el7.x86_64.rpm
openssh-server-7.4p1-21.el7.x86_64.rpm
groff-base-1.22.2-8.el7.x86_64.rpm
perl-5.16.3-294.el7_6.x86_64.rpm
perl-Carp-1.26-244.el7.noarch.rpm
perl-Data-Dumper-2.145-3.el7.x86_64.rpm
perl-Encode-2.51-7.el7.x86_64.rpm
perl-Exporter-5.68-3.el7.noarch.rpm
perl-File-Path-2.09-2.el7.noarch.rpm
perl-File-Temp-0.23.01-3.el7.noarch.rpm
perl-Filter-1.49-3.el7.x86_64.rpm
perl-Getopt-Long-2.40-3.el7.noarch.rpm
perl-HTTP-Tiny-0.033-3.el7.noarch.rpm
perl-PathTools-3.40-5.el7.x86_64.rpm
perl-Pod-Escapes-1.04-294.el7_6.noarch.rpm
perl-Pod-Perldoc-3.20-4.el7.noarch.rpm
perl-Pod-Simple-3.28-4.el7.noarch.rpm
perl-Pod-Usage-1.63-3.el7.noarch.rpm
perl-Scalar-List-Utils-1.27-248.el7.x86_64.rpm
perl-Socket-2.010-4.el7.x86_64.rpm
perl-Storable-2.45-3.el7.x86_64.rpm
perl-Text-ParseWords-3.29-4.el7.noarch.rpm
perl-Time-HiRes-1.9725-3.el7.x86_64.rpm
perl-Time-Local-1.2300-2.el7.noarch.rpm
perl-constant-1.27-2.el7.noarch.rpm
perl-libs-5.16.3-294.el7_6.x86_64.rpm
perl-macros-5.16.3-294.el7_6.x86_64.rpm
perl-parent-0.225-244.el7.noarch.rpm
perl-podlators-2.5.1-3.el7.noarch.rpm
perl-threads-1.87-4.el7.x86_64.rpm
perl-threads-shared-1.43-6.el7.x86_64.rpm
dumb-init-1.2.0-1.20170802gitd283f8a.el6.x86_64.rpm
libpcap-1.5.3-11.el7.x86_64.rpm
nmap-ncat-6.40-19.el7.x86_64.rpm"
```

Example Playbook
----------------

To create Docker images:
```
- name: Build Aspera Docker images
  hosts: localhost
  tasks:
    - name: Build and Push Aspera images
      include_role:
        name: aspera_config
        tasks_from: docker
      vars:
        aspera_config_dest: "/tmp/docker"
        aspera_config_docker_registry: "docker-registry-default.my-openshift.local"
        aspera_config_package_base_url: "http://localhost:8081/artifactory/dump"
          
```

To create Aspera Config:
```
- name: Build Aspera Docker images
  hosts: localhost
  vars:
    aspera_instance: {
      name: "my-aspera-instance"
      aspera_image: "aspera-hsts:latest",
      aspera_license_file: "/tmp/aspera-license-server",
      aspera_node_port: 30022
    }
    
  tasks:
    - name: "Build Aspera Config"
      include_role:
        name: aspera_config
      vars:
        aspera_config_ssh_port:     "33001"
        aspera_config_dest:         "/tmp/templates/{{ aspera_instance.name }}"
        aspera_config_k8s_template: "aspera-app-1.yml"          
```

Outputs
-------
Files:
- "{{ ar_osc_amqbroker_config_dest }}/amq-broker-cm.yml"
- "{{ ar_osc_amqbroker_config_dest }}/amq-broker-nodeport-service.yml"
- "{{ ar_osc_amqbroker_config_dest }}/amq-broker-k8s-template.yml"
- "{{ ar_osc_amqbroker_config_dest }}/amq-broker-files-secret.yml"


Docker Instructions
-------------------
To build the docker images the rhel7 base image registry must be 
available on the local machine and the operating user must also be able
to execute docker commands as their own user.

To setup docker to do this see the docker documentation. For the version
under test the following has to be undertaken:

1. The docker config file is changed to reference the 'dockerroot' unix
group (note the name of this group changes to 'docker' in later 
versions).
2. Add the user to the 'dockerroot' unix group

On completions, the user should be able to execute docker commands 
without the use of 'sudo'.


License
-------

BSD

Author Information
------------------

dstewart@redhat.com

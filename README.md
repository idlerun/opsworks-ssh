Connecting to OpsWorks instance with SSH can be can be problematic. Here is a script which generates an SSH config file containing an entry for each host in the OpsWorks stack.

There are two problems to be solved when connecting to OpsWorks instances:

1. The instances may be started and stopped, so the IP addresses will change frequently.
2. Some instances may not be publicly accessible and must be accessed via a tunnel through a bastion server.

## Setup

The only requirement for this script is that each OpsWorks stack have a custom JSON setting *stack_id* which is a short name to prefix any ssh hostnames (to ensure uniqueness and allow wildcards). For the examples below, the stack_id is `dev`

### `~/.ssh/config`
Add a bastion server configuration through which you can connect to any private-IP instances in the OpsWorks stack.
Also configure a wildcard config entry for {stack_id}.* which indicates for all matching hosts to use the bastion server to connect.

The generator script will fill in the specific host entries as `dev.host1`, `dev.host2`, etc. This will make them use the wildcard configuration as a starting point.

For example:

~~~ text
Host dev-nat
  User ec2-user
  HostName YOUR_ENTRYPOINT_PUBLIC_IP_HERE
  IdentityFile ~/.ssh/aws.pem

Host dev.*
  StrictHostKeyChecking no
  UserKnownHostsFile=/dev/null
  User ec2-user
  IdentityFile ~/.ssh/aws.pem
  ProxyCommand ssh dev-nat nc %h %p
~~~

## Script

This script adds a generated section to the `~/.ssh/config` which contains entries for each host in the OpsWorks stack.
After running the script, you can use a simple ssh command to connect:

~~~ bash
ssh dev.host1
~~~

#### [generate_sshconfig.py](https://github.com/idlerun/opsworks-ssh/blob/master/generate_sshconfig.py)

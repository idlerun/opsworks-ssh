#!/usr/bin/env python3

import boto
import boto.opsworks
import json

from os.path import expanduser

print("Reading previous ~/.ssh/config")
DELIM ="######## AUTO GENERATED BY generate_sshconfig.py"

path = '%s/.ssh/config' % expanduser("~")
config_file = open(path, 'r')
in_skip = False
config_lines = []
# read lines, but skip everything in the DELIM block that was previously auto-generated
for line in config_file:
  line = line.strip()
  if line == DELIM:
    in_skip = not in_skip
  else:
    if not in_skip:
      config_lines.append(line)
config_file.close()

# now write the unfiltered lines to config file
config_file = open(path, 'w')
for line in config_lines:
  config_file.write(line + "\n")

# start the the auto-generated section
config_file.write(DELIM + "\n")


print("Reading stack info")
# East is correct here, boto.opsworks.regions() is only us-east-1 right now.
# ops.describe_stacks will return stacks from all regions
ops = boto.opsworks.connect_to_region('us-east-1')

st = ops.describe_stacks()
UP_STATUSES = ['booting','online','pending','rebooting','requested','running_setup','setup_failed']
for stack in st['Stacks']:
  print("Reading instances for stack %s" % stack['Name'])

  config = json.loads(stack['CustomJson'])
  # custom stack id for ssh prefix
  name = config['stack_id']
  instances = filter(lambda inst: inst['Status'] in UP_STATUSES, ops.describe_instances(stack_id=stack['StackId'])['Instances'])
  for instance in instances:
    host = "%s.%s" % (name, instance['Hostname'])
    print("Writing instance config for %s" % host)
    config_file.write("Host %s\n  HostName %s\n" % (host, instance['PrivateIp']))

config_file.write(DELIM + "\n")
config_file.close()
print("Done")
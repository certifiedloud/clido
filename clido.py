import argparse
import json
import sys
from os.path import expanduser


try:
    from dopy.manager import DoManager

except ImportError:
    print("dopy is required. pip install dopy and try again")

# Set the API token for authenticated interaction
#IDEA cycle through a list of tokens to avoid rate limiting
config_file= expanduser('~') + '/.clido.cfg'
f = open(config_file, 'r')
api_token = f.readline().split('=')[1]

# Initialize the API
do = DoManager(None, api_token, api_version=2)

# Use argparse to set all of the CLI options
description = """
Interact with your DigitalOcean account through their API.
When run without any arguments, you simply get a list of
all the active droplets in the specified account
"""
parser = argparse.ArgumentParser(description = description)
parser.add_argument('-s', '--show', help="Show details of droplet. Use the ID number of the droplet")
args = parser.parse_args()

# Show the details of a single droplet and exit
if args.show:
    droplets = do.show_droplet(args.show)
    print(json.dumps(droplets, sort_keys=True, indent=4))
    sys.exit(0)

# If the program hasn't exited by now, just show a list of active droplets
for droplet in do.all_active_droplets():
    print("{} {}".format(droplet['name'], droplet['id']))

import argparse
import json
import sys
from os.path import expanduser


try:
    from dopy.manager import DoManager

except ImportError:
    print("dopy is required. pip install dopy and try again")

# Set the API token for authenticated interaction
# IDEA cycle through a list of tokens to avoid rate limiting
config_file = expanduser('~') + '/.clido.cfg'
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
parser = argparse.ArgumentParser(description=description)
parser.add_argument('-l', '--list-droplet-details',
                    help="Show details of droplet. Use the"
                    "ID number of the droplet")
parser.add_argument('--all-domains', action="store_true",
                    help="List all domains on the account")
parser.add_argument('--all-regions', action="store_true",
                    help="Show all regions availalbe")
parser.add_argument('--all-images', action="store_true",
                    help="Show all images availalbe")
parser.add_argument('--all-ssh-keys', action="store_true",
                    help="Show all ssh keys availalbe")
parser.add_argument('--all-sizes', action="store_true",
                    help="Show all sizes availalbe")
parser.add_argument('-c', '--create-droplet', action="store_true",
                    help="create droplet. -c  -n <name> -s <size>"
                    "-i <image> -r <region>")
parser.add_argument('-n', '--name',
                    help="name of droplet to create")
parser.add_argument('-s', '--size',
                    help="size-slug of droplet to create")
parser.add_argument('-i', '--image',
                    help="image-slug of droplet to create")
parser.add_argument('-r', '--region',
                    help="region-slug of droplet to create")
args = parser.parse_args()

# Ensure that all required args are present for droplet creation
if args.create_droplet:
    if args.name is None or args.size is None or \
            args.image is None or args.region is None:
        parser.error("When using -c, you must specify -n <name>"
                     "-s <size> -i <image> and -r <region>")

# Print a list of domains
if args.all_domains:
    print(json.dumps(do.all_domains(), sort_keys=True, indent=4))

# Print a detailed list of available regions
if args.all_regions:
    print(json.dumps(do.all_regions(), sort_keys=True, indent=4))
    sys.exit(0)

# Print a detailed list of available images
if args.all_images:
    print(json.dumps(do.all_images(), sort_keys=True, indent=4))
    sys.exit(0)

# Print a detailed list of available ssh keys
if args.all_ssh_keys:
    print(json.dumps(do.all_ssh_keys(), sort_keys=True, indent=4))
    sys.exit(0)

# Print a detailed list of available droplet sizes
if args.all_sizes:
    print(json.dumps(do.sizes(), sort_keys=True, indent=4))
    sys.exit(0)

# Show the details of a single droplet and exit
if args.list_droplet_details:
    droplets = do.show_droplet(args.list_droplet_details)
    print(json.dumps(droplets, sort_keys=True, indent=4))
    sys.exit(0)

if args.create_droplet:
    do.new_droplet(args.name, args.size, args.image, args.region)

# If the program hasn't exited by now, just show a list of active droplets
for droplet in do.all_active_droplets():
    print("{} {}".format(droplet['name'], droplet['id']))

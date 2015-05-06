import argparse
import sys
from os.path import expanduser

try:
    import digitalocean

except ImportError:
    print("python-digitalocean is required. pip install it and try again")

# Set the API token for authenticated interaction
# TODO cycle through a list of tokens to avoid rate limiting
config_file = expanduser('~') + '/.clido.cfg'
f = open(config_file, 'r')
api_token = f.readline().split('=')[1].strip()

# Initialize the API
do = digitalocean.Manager(token=api_token)

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
parser.add_argument('--destroy-droplet',
                    help="destroy droplet by <id>")
parser.add_argument('-n', '--name',
                    help="name of droplet to create")
parser.add_argument('-s', '--size',
                    help="size-slug of droplet to create")
parser.add_argument('-i', '--image',
                    help="image-slug of droplet to create")
parser.add_argument('-r', '--region',
                    help="region-slug of droplet to create")
parser.add_argument('-k', '--ssh-keys', default=[], nargs='+', type=int,
                    help="list of ssh key id's to add to new droplets")
args = parser.parse_args()

# Ensure that all required args are present for droplet creation when -c is used
if args.create_droplet:
    if args.name is None or args.size is None or \
            args.image is None or args.region is None:
        parser.error("When using -c, you must specify -n <name>"
                     "-s <size> -i <image> and -r <region>")

# Print a list of domains
if args.all_domains:
    domains = do.get_all_domains()
    for domain in domains:
        print("{} {}".format(domain.id, domain))
    sys.exit(0)

# Print a detailed list of available regions
if args.all_regions:
    regions = do.get_all_regions()
    for region in regions:
        print("{}({})".format(region, region.slug))
    sys.exit(0)

# Print a detailed list of available images
if args.all_images:
    images = do.get_all_images()
    for image in images:
        print("{}({})".format(image, image.slug))
    sys.exit(0)

# Print a detailed list of available ssh keys
if args.all_ssh_keys:
    keys = do.get_all_sshkeys()
    for key in keys:
        print(key)
    sys.exit(0)

# Print a detailed list of available droplet sizes
if args.all_sizes:
    sizes = do.get_all_sizes()
    for size in sizes:
        print(size)
    sys.exit(0)

# Show the details of a single droplet and exit
if args.list_droplet_details:
    # This should be more verbose
    print(do.get_droplet(args.list_droplet_details))
    sys.exit(0)

# Create a droplet based on the given arguments
if args.create_droplet:
    # TODO add other options such as ssh keys, backups, etc.
    try:
        new_droplet = digitalocean.Droplet(token=api_token,
                                           name=args.name,
                                           image=args.image,
                                           region=args.region,
                                           size_slug=args.size,
                                           ssh_keys=args.ssh_keys)
        new_droplet.create()
        print("Successfuly created {}({})"
              .format(new_droplet.name, new_droplet.id))
        sys.exit(0)

    except Exception as e:
        print("Unable to create droplet: {}".format(e))
        sys.exit(1)

if args.destroy_droplet:
    try:
        droplet_to_destroy = do.get_droplet(args.destroy_droplet)
        droplet_to_destroy.destroy()
        sys.exit(0)
    except Exception as e:
        print("Unable to destroy droplet: {}".format(e))
        sys.exit(1)

# If the program hasn't exited by now, just show a list of active droplets
droplets = do.get_all_droplets()
for droplet in droplets:
    print(droplet)

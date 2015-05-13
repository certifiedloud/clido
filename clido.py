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
parser.add_argument('operand',
                    help="specify one of the following: "\
                    "droplets, domains, images, sizes, regions, keys.")
parser.add_argument('-c', '--create-droplet', action="store_true",
                    help="create droplet. -c  -n <name> -s <size>"
                    "-i <image> -r <region>")
parser.add_argument('-d', '--destroy',
                    help="destroy <operand> by <id>")
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

# Check that all required args are present for droplet creation when -c is used
if args.create_droplet:
    if args.name is None or args.size is None or \
            args.image is None or args.region is None:
        parser.error("When using -c, you must specify -n <name>"
                     "-s <size> -i <image> and -r <region>")

if args.operand == 'sizes':
    sizes = do.get_all_sizes()
    for size in sizes:
        print(size)

if args.operand == 'regions':
    # Print a detailed list of available regions
    regions = do.get_all_regions()
    for region in regions:
        print("{}({})".format(region, region.slug))
    sys.exit(0)

if args.operand == 'keys':
    keys = do.get_all_sshkeys()
    for key in keys:
        print(key)

if args.operand == 'images':
    images = do.get_all_images()
    for image in images:
        print("{}({})".format(image, image.slug))

if args.operand == 'droplets':
    # check if we want to destroy a droplet
    if args.destroy:
        try:
            droplet_to_destroy = do.get_droplet(args.destroy)
            droplet_to_destroy.destroy()
            sys.exit(0)
        except Exception as e:
            print("Unable to destroy droplet: {}".format(e))
            sys.exit(1)

    droplets = do.get_all_droplets()
    for droplet in droplets:
        print(droplet)

if args.operand == 'domains':
    domains = do.get_all_domains()
    for domain in domains:
        print(domain)

else:
    print("{} is not a valid operand, please choose one of the following:"
            .format(args.operand))
    print("droplets, domains, keys, regions, sizes, images.")

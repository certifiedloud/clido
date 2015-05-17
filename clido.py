import argparse
from tabulate import tabulate
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
                    help="specify one of the following: "
                    "droplets, domains, images, sizes, regions, keys.")
parser.add_argument('-c', '--create', action="store_true",
                    help="create droplet. -c  -n <name> -s <size>"
                    "-i <image> -r <region>")
parser.add_argument('-d', '--destroy',
                    help="destroy <operand> by <id>")
parser.add_argument('-n', '--name',
                    help="name of droplet to create")
parser.add_argument('-u', '--update-domain', action="store_true",
                    help="update specifc domain with a record")
parser.add_argument('-a', '--ip-address',
                    help="Specify ip address for domain creation")
parser.add_argument('-s', '--size',
                    help="size-slug of droplet to create")
parser.add_argument('-i', '--image',
                    help="image-slug of droplet to create")
parser.add_argument('-r', '--region',
                    help="region-slug of droplet to create")
parser.add_argument('-k', '--ssh-keys', default=[], nargs='+', type=int,
                    help="list of ssh key id's to add to new droplets")
parser.add_argument('-l', '--lookup',
                    help="lookup details of <operand> by <id>")
args = parser.parse_args()

if args.operand == 'sizes':
    sizes = do.get_all_sizes()
    for size in sizes:
        print(size)

elif args.operand == 'regions':
    # Print a detailed list of available regions
    regions = do.get_all_regions()
    for region in regions:
        print("{}({})".format(region, region.slug))
    sys.exit(0)

elif args.operand == 'keys':
    keys = do.get_all_sshkeys()
    for key in keys:
        print(key)

elif args.operand == 'images':
    images = do.get_all_images()
    for image in images:
        print("{}({})".format(image, image.slug))

elif args.operand == 'droplets':
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

elif args.operand == 'domains':
    # check if we want to create a domain
    if args.create:
        if not args.name and not args.ip_address:
            parser.error("In order to create a domain you must specify both "
                         "--name and --ip-address")
            sys.exit(1)
        else:
            try:
                domain = digitalocean.Domain(token=api_token,
                                             name=args.name,
                                             ip_address=args.ip_address).create()
                sys.exit(0)
            except Exception as e:
                print("Unable to create domain: {}".format(e))
                sys.exit(1)

    # check if we want to destroy a domain
    if args.destroy:
        try:
            digitalocean.Domain(token=api_token,
                                name=args.destroy).destroy()
            sys.exit(0)
        except Exception as e:
            print("Couldn't destroy domain: {}".format(e))
            sys.exit(1)

    # Check if we want to update existing domain
    if args.update_domain:
        if not args.name:
            print("You must specify -n, which domain to update")
            sys.exit(1)
    # TODO finish domain record updating

    if args.lookup:
        domain = digitalocean.Domain(token=api_token,
                                     name=args.lookup)
        records = domain.get_records()
        record_list = []
        for record in records:
            record_list.append({"Type": record.type,
                                "Priority": record.priority,
                                "Name": record.name,
                                "Data": record.data,
                                "ID": record.id})
        print(tabulate(record_list, headers='keys', stralign='center'))
        sys.exit(0)

    # If nothing else, just print a list of domains
    domains = do.get_all_domains()
    for domain in domains:
        print(domain)

else:
    print("{} is not a valid operand, please choose one of the following:"
          .format(args.operand))
    print("droplets, domains, keys, regions, sizes, images.")

import argparse
from os.path import expanduser

try:
    from dopy.manager import DoManager

except ImportError:
    print("dopy is required. pip install dopy and try again")

# TODO Use argparse to set all of the CLI options
parser = argparse.ArgumentParser(
    description = "Interact with your DigitalOcean account through their API")
#parser.add_argument
parser.parse_args()

# TODO set the API token for authenticated interaction
config_file= expanduser('~') + '/.clido.cfg'
f = open(config_file, 'r')
api_token = f.readline().split('=')[1]

# TODO run the command from dopy based on the given args
do = DoManager(None, api_token, api_version=2)
do.all_active_droplets()

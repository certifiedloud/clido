import argparse

try:
    import dopy

except ImportError:
    print("dopy is required. pip install dopy and try again")

# TODO Use argparse to set all of the CLI options
parser = argparse.ArgumentParser(
    description = "Interact with your DigitalOcean account through their API")
parser.add_argument

# TODO set the API token for authenticated interaction

# TODO run the command from dopy based on the given args

import argparse

def list_of_strings(arg):
    return arg.split(',')

parser = argparse.ArgumentParser()

parser.add_argument("--str-list", type=list_of_strings)

args = parser.parse_args()

samples = args.str_list

if samples:
    print(len(samples))
else:
    print("NO samples", samples)
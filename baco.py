import argparse
import os
import os.path as p
from subprocess import call

parser = argparse.ArgumentParser()

parser.add_argument('input_format', type=str,
                    help='''The format to be converted from''')
parser.add_argument('output_format', type=str,
                    help='''The format to be converted to''')

args = parser.parse_args()

if not args.input_format.startswith('.'):
    args.input_format = '.' + args.input_format
if not args.output_format.startswith('.'):
    args.output_format = '.' + args.output_format


def convert(target: str):
    call(['ffmpeg', '-i', target, p.splitext(target)[0] + args.output_format])


def main():
    contents = os.listdir()
    targets = []
    for i in contents:
        if not p.isfile(i):
            continue
        if i.endswith(args.input_format):
            targets.append(i)
    for t in targets:
        convert(t)


if __name__ == '__main__':
    
    main()
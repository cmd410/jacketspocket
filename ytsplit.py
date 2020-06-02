"""Lil script in snake language to download a video(audio) from youtube
And the RIP IT INTO TINY LITTLE PIECES according to timetags file you provide

timetag format is:
SECTION NAME 00:00:00
or
00:00:00 SECTION NAME
or
SECTION 00:00:00 NAME
doesent matter really where you put time.

youtube-dl and ffmpeg ARE REQUIRED"""

import argparse
import string
import os.path as p
from os import system

parser = argparse.ArgumentParser('ytsplit.py')


parser.add_argument('--timetags', '-t', type=str, required=True,
                    help='File that contains timetags for video')
parser.add_argument('--author', '-au', type=str, default='unknown',
                    help='Author of the album.')
parser.add_argument('--album', '-a', type=str, default='unknown',
                    help='Album name')
parser.add_argument('--output', '-o', type=str, default='./',
                   help='Output directory name, if not defined files are saved in current working directory.')
parser.add_argument('--format', '-f', type=str, default='ogg',
                    help='Prefered format of output file')
parser.add_argument('url', type=str,
                    help='Video url')

args = parser.parse_args()


def format_filename(s):
    valid_chars = "-_.([]/\\,) %s%s" % (string.ascii_letters, string.digits)
    valid_chars += 'йцукенгшщзхъфывапролджэячсмитьбю'
    filename = ''.join(c for c in s if c.lower() in valid_chars)
    print(filename)
    return filename


def ytdl(artist, album, ext, url):
    outputfile = p.join(args.output, format_filename(f'{artist} - {album}[ALBUM].webm'))
    if p.exists(outputfile): return outputfile
    if system(f'youtube-dl -f bestaudio --output "{outputfile}" {url}'): raise Exception('Failed to download video.')
    return outputfile

def get_timetags(filename):
    data = ''
    with open(filename, 'r') as file:
        data = file.read()
    if not data: raise ValueError

    lines = data.split('\n')
    tags = []
    for track in lines:
        tag = ''
        for word in track.split(' '):
            if word.replace(':', '').isdigit():
                tag = word
                break
        if not tag: continue
        name = format_filename(track.replace(tag, '').strip())
        tags.append((tag, name))
    intervals = []
    prev = None
    while tags:
        item = tags.pop()
        intervals.append((item[0], prev, item[1]))
        prev = item[0]
    return reversed(intervals)

def ffmpeg(file, timetags, artist, album):
    timetags = get_timetags(timetags)
    track_number = 1
    for start, end, name in timetags:
        print()
        print(start, end, name, args.format)
        new_file_name = p.join(args.output, f'{artist} - {name}.{args.format}')
        meta = f'-metadata author="{artist}" '
        meta += f'-metadata album_artist="{artist}" '
        meta += f'-metadata album="{album}" '
        meta += f'-metadata track={track_number} '
        meta += f'-metadata title="{name}" '
        if not end:
            system(f'ffmpeg -i "{file}" {meta}-ss {start} "{new_file_name}"')
            continue
        system(f'ffmpeg -i "{file}" {meta}-ss {start} -to {end} "{new_file_name}"')
        track_number += 1

if __name__ == '__main__':
    filename = ytdl(args.author, args.album, args.format, args.url)
    ffmpeg(filename, args.timetags, args.author, args.album)
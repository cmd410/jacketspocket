"""Lil script in snake language to download a video(audio) from youtube
And then RIP IT INTO TINY LITTLE PIECES according to time_tags file you provide

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
from sys import platform
from subprocess import call

parser = argparse.ArgumentParser('ytsplit.py')


parser.add_argument('--time_tags', '-t', type=str, required=True,
                    help='File that contains time_tags for video')
parser.add_argument('--author', '-au', type=str, default='unknown',
                    help='Author of the album.')
parser.add_argument('--album', '-al', type=str, default='unknown',
                    help='Album name')
parser.add_argument('--output', '-o', type=str, default='./',
                   help='Output directory name, if not defined files are saved in current working directory.')
parser.add_argument('--format', '-f', type=str, default='ogg',
                    help='Prefered format of output file')
parser.add_argument('url', type=str,
                    help='Video url')

args = parser.parse_args()


def format_file_name(s, remove_separators=False):
    if 'win' in platform.lower():
        invalid_chars = ':*?"<>|;'
    else:
        invalid_chars = ''
    if remove_separators:
        invalid_chars += '\\/'
    file_name = ''.join(c for c in s if c.lower() not in invalid_chars)
    return file_name

meta_author = args.author
meta_album = args.album

args.author = format_file_name(args.author, True)
args.album = format_file_name(args.album, True)
args.output = format_file_name(args.output)
args.format = format_file_name(args.format).replace('.','')


def ytdl(author, album, ext, url):
    output_file = p.join(args.output, f'{author} - {album}[ALBUM].webm')
    if p.exists(output_file):
        return output_file
    if call(['youtube-dl', '-f', 'bestaudio', '--output', output_file, url]):
        raise Exception('Failed to download video.')
    return output_file


def get_time_tags(file_name):
    data = ''
    with open(file_name, 'r') as file:
        data = file.read()
    if not data:
        raise ValueError

    lines = data.split('\n')
    tags = []
    for track in lines:
        tag = ''
        for word in track.split(' '):
            if word.replace(':', '').isdigit():
                tag = word
                break
        if not tag: continue
        name = track.replace(tag, '').strip()
        tags.append((tag, name))
    intervals = []
    prev = None
    while tags:
        item = tags.pop()
        intervals.append((item[0], prev, format_file_name(item[1])))
        prev = item[0]
    return reversed(intervals)


def ffmpeg(file, time_tags, author, album):
    time_tags = get_time_tags(time_tags)
    track_number = 1
    for track_number, (start, end, name) in enumerate(time_tags, 1):
        print()
        print(start, end, name, args.format)
        new_file_name = p.join(args.output, f'{author} - {name}.{args.format}')
        meta = ['-metadata', f'artist={meta_author}',
                '-metadata', f'album_artist={meta_author}',
                '-metadata', f'track={track_number}',
                '-metadata', f'title={name}',
                '-metadata', f'album={meta_album}']
        if not end:
            call(['ffmpeg', '-i', file] + meta + ['-ss', start, new_file_name])
            continue
        call(['ffmpeg', '-i', file] + meta \
             + ['-ss', start, '-to', end, new_file_name])


if __name__ == '__main__':
    file_name = ytdl(args.author, args.album, args.format, args.url)
    ffmpeg(file_name, args.time_tags, args.author, args.album)


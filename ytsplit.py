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
from sys import platform
from subprocess import call

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
    if 'win' in platform.lower():
        invalid_chars = '\\/:*?"<>|;'
    else:
        invalid_chars = '\\/'
    filename = ''.join(c for c in s if c.lower() not in invalid_chars)
    return filename



def ytdl(artist, album, ext, url):
    outputfile = p.join(args.output, f'{artist} - {album}[ALBUM].webm')
    outputfile = format_filename(output_file)
    if p.exists(outputfile):
        return outputfile
    if call(['youtube-dl', '-f', 'bestaudio', '--output', outputfile, url]):
        raise Exception('Failed to download video.')
    return outputfile

def get_timetags(filename):
    data = ''
    with open(filename, 'r') as file:
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
        intervals.append((item[0], prev, item[1]))
        prev = item[0]
    return reversed(intervals)

def ffmpeg(file, timetags, artist, album):
    timetags = get_timetags(timetags)
    track_number = 1
    for track_number, (start, end, name) in enumerate(timetags, 1):
        print()
        print(start, end, name, args.format)
        new_file_name = p.join(args.output, f'{artist} - {name}.{args.format}')
        new_file_name = format_filename(new_file_name)
        meta = ['-metadata', f'author={artist!r}',
                '-metadata', f'album_artist={artist!r}',
                '-metadata', f'track={track_number:d}',
                '-metadata', f'title={name!r}']
        if not end:
            call(['ffmpeg', '-i', file] + meta + ['-ss', start, new_file_name])
            continue
        call(['ffmpeg', '-i', file] + meta \
             + ['-ss', start, '-to', end, new_file_name])

if __name__ == '__main__':
    filename = ytdl(args.author, args.album, args.format, args.url)
    ffmpeg(filename, args.timetags, args.author, args.album)


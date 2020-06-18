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
import re
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
parser.add_argument('--start-number', '-sn', type=int, default=1,
                    help='A number from which to start counting tracks in album, defaults to 1')
parser.add_argument('-y', action='store_true',
                    help='Overwrite existing files.')
parser.add_argument('-d', '--deduce', type=str,
                    help='''A format string of deducing author/song title/album from time tags list.
                    Example: author - song [album]''')
parser.add_argument('url', type=str,
                    help='Video url')


args = parser.parse_args()


def get_info(string: str):
    deduce = args.deduce
    m = dict()
    for s in [r'author', r'song', r'album']:
        match = re.search(s, deduce)
        if match is None:
            continue
        m[s] = match.span()
    l = sorted([i for i in m.items()], key=lambda item: item[1][0] + item[1][1])

    indexes = (l[0][1][0], l[-1][1][1])
    offsets = (indexes[0], len(deduce) - indexes[1])
    splitters = []
    for i, item in enumerate(l):
        if i == len(l)-1:
            break
        sep = deduce[item[1][1]:l[i + 1][1][0]]
        splitters.append(sep)

    info = dict()
    ending = deduce[-offsets[1]:]
    if string.endswith(ending):
        string = string[offsets[0]:-offsets[1]]
    else:
        string = string[offsets[0]:]
    print(string)
    sep_index = 0
    for i in l:
        subject = i[0]
        if splitters:
            sep = splitters.pop(0)
            sep_index = string.find(sep)
            if sep_index == -1:
                value = string
            else:
                value = string[:sep_index]
                string = string[sep_index+len(sep):]
        else:
            if sep_index == -1:
                break
            value = string[string.find(sep) + 1:]
        info[subject] = value
    return info


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


def get_meta(name, n=1):
    info = dict()
    if not args.deduce:
        meta = ['-metadata', f'artist={meta_author}',
                '-metadata', f'album_artist={meta_author}',
                '-metadata', f'track={n + args.start_number - 1}',
                '-metadata', f'title={name}',
                '-metadata', f'album={meta_album}']
    else:
        info = get_info(name)
        meta = ['-metadata', f'artist={info.get("author") or "Unknown"}',
                '-metadata', f'album_artist={info.get("author") or "Unknown"}',
                '-metadata', f'track={n + args.start_number - 1}',
                '-metadata', f'title={info.get("song") or "Unknown"}',
                '-metadata', f'album={info.get("album") or "Unknown"}']

    return meta, info


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
        meta, info = get_meta(name, track_number)
        new_file_name = p.join(args.output, f'{ info.get("author", author) } - {info.get("song", name)}.{args.format}')
        if not end:
            print(new_file_name)
            call(['ffmpeg', '-y' if args.y else '-n', '-i', file] + meta + ['-ss', start, new_file_name])
            continue
        call(['ffmpeg', '-y' if args.y else '-n', '-i', file] + meta + ['-ss', start, '-to', end, new_file_name])


if __name__ == '__main__':
    file_name = ytdl(args.author, args.album, args.format, args.url)
    ffmpeg(file_name, args.time_tags, args.author, args.album)


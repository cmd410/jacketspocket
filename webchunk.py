'''
Script that opens sites from given presets.
Presets are defined in config file with structure like:

[preset name]
example.com
python.org
...and so on

Script searches for web.list(or any given filename in -l) in following directories:
1. Current working directory
2. User directory
3. Script directory
Until it finds one or raises an exception
'''
import webbrowser as web
import configparser
import argparse
from os.path import join, exists, dirname, expanduser

parser = argparse.ArgumentParser(description='Open web pages in from presets.')

parser.add_argument('-l','--list', default='web.list',
                    help='List of presets')

parser.add_argument('preset_name', 
                    help='Name of preset you want to open.')

def read_presets(list_name):
    for d in ['./', expanduser('~'), dirname(__file__)]:
        p = join(d, list_name)
        if exists(p):
            list_name = p
            break
    if not exists(list_name):
        raise Exception(f'Preset file not found {list_name}')
    preset_list = configparser.ConfigParser(allow_no_value=True)
    preset_list.optionxform = str
    preset_list.read(list_name)
    return preset_list

def choose_preset(preset_list, preset_name):
    return preset_list[preset_name]

def main():
    args = parser.parse_args()
    presets = read_presets(args.list)
    preset = choose_preset(presets, args.preset_name)
    for i, site in enumerate(preset.keys()):
        if site in {'http','https', 'file'}:
            site = f'{site}:{preset[site]}'
        else:
            site = f'http://{site}'
        print(f'Opening {site}...')
        if i == 0:
            web.get().open_new(site)
        else:
            web.get().open(site)

if __name__ == '__main__':
    main()

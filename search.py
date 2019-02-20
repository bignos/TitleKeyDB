#!/usr/bin/env python3

# This module search on Wii U title key data
# [STATE]   : POC ( Development )
# [AUTHOR]  : bignos@gmail.com
#

# coding=utf-8

import argparse
import textwrap

from modules import transform2JSON  # Local module import to load data from JSON file

# -[ Consts ]-
funkiiu_exec = './funkiiu'

# -[ Command line argument ]-
parser = argparse.ArgumentParser(description='Search on Title key',
                                    formatter_class=argparse.RawDescriptionHelpFormatter,
                                    epilog=textwrap.dedent('''\
Example:
    - Search all titles with mario from europe and with type eshop:
        search.py -n mario -r eur -t eshop\
                                    '''))
parser.add_argument('-n','-name', action='store', dest='name', default='',
                    help='the title name to search')
parser.add_argument('-r', '-region', action='store', dest='region', default='',
                    help='the region to search')
parser.add_argument('-t', '-type', action='store', dest='ttype', metavar='TYPE', default='',
                    help='the type to search')
parser.add_argument('-i', '-install', action='store_true', dest='install',
                    help='display install command line')
parser.set_defaults(install=False)

# -[ Private function ]-

def _debug(message):
    print("[DEBUG]: {}".format(message))

def _print_if_ok(title_key, name, region, ttype):
    if _is_present(name):
        if not _get_if(title_key.name, name):
            return False
    if _is_present(region):
        if not _get_if(title_key.region, region):
            return False
    if _is_present(ttype):
        if not _get_if(title_key.ttype, ttype):
            return False
    return True

def _is_present(value):
    return True if value != '' else False

def _get_if(title_key_value, value):
    if title_key_value.lower().find(value.lower()) != -1:
        return True
    else:
        return False

def _get_install(title_key):
    return '''\
################################################################################
{exec} -title {title} -key {key}
{exec} -title {title} -onlinekeys
{exec} -title {title} -onlinetickets
################################################################################
'''.format(exec=funkiiu_exec, title=title_key.tid, key=title_key.key)

# -[ Main ]-

if __name__ == '__main__':
    title_list = transform2JSON.WiiUTitlekeyList.loadFromJSON(transform2JSON.wiiu_title_key_json)
    arguments = parser.parse_args()

    name        = arguments.name
    region      = arguments.region
    ttype       = arguments.ttype
    install     = arguments.install

    for title_key in title_list.wii_u_title_key_list:
        if _print_if_ok(title_key, name, region, ttype):
            print(title_key)
            if install:
                print(_get_install(title_key))

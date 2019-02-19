# This module search on Wii U title key data
# [STATE]   : POC ( Development )
# [AUTHOR]  : bignos@gmail.com
#

# coding=utf-8

from modules import transform2JSON  # Local module import to load data from JSON file

# -[ Main ]-

if __name__ == '__main__':
    title_list = transform2JSON.WiiUTitlekeyList.loadFromJSON(transform2JSON.wiiu_title_key_json)

    for title_key in title_list.wii_u_title_key_list:
        print(title_key)

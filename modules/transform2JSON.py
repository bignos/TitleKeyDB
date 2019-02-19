# This module extract Wii U Title key from HTML file and tranform it to JSON
# [STATE]   : POC ( Development )
# [AUTHOR]  : bignos@gmail.com
#

# coding=utf-8

import sys              # for exit()
import os               # for path and basename
import lxml.html        # for parse XML
import json             # for JSON dump and load

# -[ Data ]-

wiiu_title_key_html = './resources/html/WiiU Title Key.html'
wiiu_title_key_json = './resources/json/WiiU Title Key.json'


# -[ Class ]-

class WiiUTitlekeyList():

    def __init__(self, wii_u_title_key_list):
        """ Default constructor, but not very usefull
        """
        self.wii_u_title_key_list = wii_u_title_key_list

    # -[ Static ]-

    def loadFromHTML(path):
        """ Static method to load a WiiUTitlekeyList object from an HTML file
            path:   {str}               Path of the HTML file
            Return: {WiiUTitlekeyList}  list of WiiUTitlekey from the HTML file
        """
        try:
            html_document = _read_html_file(path)
        except FileNotFoundError as exception:
            print('File not found: {}'.format(exception.filename))
            sys.exit()
        except PermissionError as exception:
            print('Permission denied: {}'.format(exception.filename))
            sys.exit()
        
        # Extract data
        title_key_tree = lxml.html.fromstring(html_document)
        result = list()
        
        for table in title_key_tree.xpath('//table[@class="table table-bordered"]'):
            for tr in table.xpath('./tr'):
                tid    = tr.xpath('./td[1]/text()')[0].strip()
                key    = tr.xpath('./td[2]/text()')[0].strip()
                name   = tr.xpath('./td[3]/text()')[0].replace('\n', ' ') if len(tr.xpath('./td[3]/text()')) > 0 else ''
                region = tr.xpath('./td[4]/text()')[0] if len(tr.xpath('./td[4]/text()')) > 0 else ''
                ttype  = tr.xpath('./td[5]/text()')[0].strip()

                result.append(WiiUTitlekey(tid, key, name, region, ttype))

        return WiiUTitlekeyList(result)

    def loadFromJSON(path):
        """ Static method to build a WiiUTitlekeyList from a JSON file
            path:   {str}       Path of the JSON file
            Return: {Framedata} WiiUTitlekeyList object with information of the JSON file
            Throw FileNotFoundError if the file in path is not found
            Throw PermissionError if you don't have permission to read the file
        """
        with open(path, 'r') as json_file:
            json_content = json.load(json_file)

        wii_u_title_key_list = list()

        for wii_u_title_key in json_content:
            wii_u_title_key_list.append(WiiUTitlekeyList._create_wii_u_title_key_from_json(wii_u_title_key))

        return WiiUTitlekeyList(wii_u_title_key_list)

    # -[ Public ]-

    def saveToJSON(self, path):
        """ Save the WiiUTitlekeyList object to a JSON file
            path:   {str}   Path of the JSON file
            Return: None
        """
        with open(path, 'w') as json_file:
            json.dump(self.wii_u_title_key_list, json_file, indent=4, separators=(',', ': '), sort_keys=False, cls=WiiUTitlekeyListEncoder)

    # -[ Private ]-
    
    def _create_wii_u_title_key_from_json(json):
        """ Private method to create a WiiUTitlekey instance with a JSON WiiUTitlekey node
            json:       {dict}  The JSON node
            Return:     {WiiUTitlekey}  The WiiUTitlekey instance from the JSON node
        """
        return WiiUTitlekey(json['tid'],
                            json['key'],
                            json['name'],
                            json['region'],
                            json['ttype'])


class WiiUTitlekey():
    """ WiiUTitlekey structure
        - tid       {str}           id of the Title
        - key       {str}           key of the Title
        - name      {str}           name of the Title
        - region    {str}           region of the Title
        - ttype     {str}           type of the Title
    """

    # -[ Internals ]-

    def __init__(self, tid, key, name, region, ttype):
        self.tid    = tid
        self.key    = key
        self.name   = name
        self.region = region
        self.ttype  = ttype

    def __repr__(self):
        """ Return: {str}   String representation of WiiUTitlekey instance """
        return """--------------------------------------------------------------------------------
Name   : {}
Region : {}
Type   : {}
ID     : {}
Key    : {}
--------------------------------------------------------------------------------
""".format(self.name, self.region, self.ttype, self.tid, self.key)


class WiiUTitlekeyListEncoder(json.JSONEncoder):
    """ Encode to JSON WiiUTitlekeyList instance object """

    def default(self, wii_u_title_key_list):
        if isinstance(wii_u_title_key_list, WiiUTitlekeyList):
            return wii_u_title_key_list
            
        return WiiUTitlekeyEncoder.default(self, wii_u_title_key_list)

class WiiUTitlekeyEncoder(json.JSONEncoder):
    """ Encode to JSON WiiUTitlekey instance object """

    def default(self, wii_u_title_key):
        if isinstance(wii_u_title_key, WiiUTitlekey):
            result = dict()
            result['name']   = wii_u_title_key.name
            result['region'] = wii_u_title_key.region
            result['ttype']  = wii_u_title_key.ttype
            result['tid']    = wii_u_title_key.tid
            result['key']    = wii_u_title_key.key

            return result

        return json.JSONEncoder.default(self, wii_u_title_key)


# -[ Private Function ]-

def _read_html_file(path):
    """ Private function read file and return content on a string
        path:   {str}   Path of the character file
        Return: {str}   The content of the file
        Throw FileNotFoundError if the file in path is not found
        Throw PermissionError if you don't have permission to read the file
    """
    with open(path, 'rt', encoding='utf-8') as document:
        result = document.read()
    return result

def _html_to_json(source_html, dest_json):
    """ Private function transform Wii U title key html files to json
        source_html:    {str}   Source path of the HTML file
        dest_json:      {str}   Destination path of the JSON file
        Return: None
    """
    title_list = WiiUTitlekeyList.loadFromHTML(wiiu_title_key_html)
    title_list.saveToJSON(wiiu_title_key_json)

# -[ Main ]-

if __name__ == '__main__':
    title_list = WiiUTitlekeyList.loadFromJSON(wiiu_title_key_json)

    for title_key in title_list.wii_u_title_key_list:
        print(title_key)

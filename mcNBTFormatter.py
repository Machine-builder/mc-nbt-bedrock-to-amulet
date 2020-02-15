'''
A python module to convert nbt data from the bedrock module

available at : https://github.com/BluCodeGH/bedrock

into nbt data for the amulet_nbt module

available at : https://github.com/Amulet-Team/Amulet-NBT
'''

'''
{"upside_down_bit": 1b, "weirdo_direction": 3}

compound is {}
list is []
int is 1
byte is 1b
short is 1s
string is "1"
'''

import re

def search_for_multisubstring(s,substrings=[],return_min=True):
    indices = []
    for substring in substrings:
        if substring in s:
            indices.append(s.index(substring))
    return (min(indices) if return_min else indices)

class TAG():
    def __init__(self, tag_type, payload):
        self.type = tag_type
        self.payload = payload

def bedrock_nbt_to_amulet_nbt(bedrock_nbt_string):
    '''recursively convert bedrock nbt into amulet-nbt'''

    bnbts = bedrock_nbt_string

    # check how many tags there are, and then find the index of all of them
    tagsc = bnbts.count("TAG_")
    tags_indices = [m.start() for m in re.finditer('TAG_', bnbts)]
    
    # debug messages
    print("Amount of tags :", tagsc)
    print("Tags found :", len(tags_indices))

    # temporary nbt data storage
    output_data = {  }

    # loop through every tag index that was found earlier with regex
    for tag_index in tags_indices:
        # get the text after the tag index
        after_tag_bit = bnbts[tag_index:]
        # get the index of the end of the tag id
        tag_after_index = after_tag_bit.index('-')
        # get the tag id
        tag_type_string = after_tag_bit[:tag_after_index]
        # get the real tag type
        real_tag_type = tag_type_string.replace('TAG_','')
        # get the index after the tag name
        name_after_tag_index = after_tag_bit.index(':')
        # get the tag name
        real_tag_name = after_tag_bit[tag_after_index+1:name_after_tag_index]
        # get the content of the tag
        rtt = real_tag_type.lower()
        tag_content = None
        if rtt in ['int', 'byte', 'short']:
            addtable = {
                'int': '',
                'byte': 'b',
                'short': 's'
            }
            # the tag is a number of sorts
            after_tag_section = after_tag_bit[name_after_tag_index+1:]
            next_index = search_for_multisubstring(after_tag_section,[']',','])
            tag_content = after_tag_section[:next_index]+addtable[rtt]

        if rtt == 'string':
            # the tag is type string
            after_tag_section = after_tag_bit[name_after_tag_index+1:]
            next_index = search_for_multisubstring(after_tag_section,[']',','])
            tag_content = '"'+after_tag_section[:next_index]+'"'

        if rtt == 'compound':
            # the tag is type compound
            # TODO : read and count open and closed brackets to work out what data is 'inside' this set
            inside_data = ''
            after_tag_section = after_tag_bit[name_after_tag_index+2:]
            open_brackets = 1
            for character in after_tag_section:
                if character == '[':
                    open_brackets += 1
                if character == ']':
                    open_brackets -= 1
                    if open_brackets == 0:
                        break
                inside_data += character
            tag_content = inside_data

        print(real_tag_type.ljust(9), '::', real_tag_name.ljust(10), '>>', tag_content)
        # output_data[real_tag_name]


class BedrockNBT():
    '''A class designed to read nbt data from Bedrock and convert it to be used with Amulet-NBT'''
    def __init__(self, nbt):
        self.rawnbt = nbt
        self.strnbt = str(nbt)

    def into_amulet_nbt(self):
        '''turn the current bedrock nbt data into amulet nbt data'''

        # record the string of operation, for debugging
        new = self.strnbt
        open("ian_step1.txt", 'w').write(new)

        bedrock_nbt_to_amulet_nbt( new )
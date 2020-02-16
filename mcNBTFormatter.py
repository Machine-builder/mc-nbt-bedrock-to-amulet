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
    try: return (min(indices) if return_min else indices)
    except: return len(s)+2

def bedrock_nbt_to_universal_nbt(bedrock_nbt_string):
    '''recursively convert bedrock nbt into universal nbt'''

    # copy the bedrock_nbt_string variable to bnbts
    bnbts = bedrock_nbt_string

    # if there is no tag type starter, assume it's a compound
    if bnbts.startswith('[') and bnbts.endswith(']'):
        bnbts = 'TAG_Compound-properties:'+bnbts

    # check how many tags there are, and then find the index of all of them
    tags_indices = []

    # track open brackets to find tag indices within layer 0 of recursion
    ob = 0
    for text_position,character in enumerate(bnbts):
        if character == '[': ob += 1
        elif character == ']': ob -= 1
        if ob == 0:
            left_over = bnbts[text_position:]
            if left_over.startswith('TAG_'): tags_indices.append(text_position)

    # temporary nbt data storage
    output_data = []

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
            tag_content = bedrock_nbt_to_universal_nbt( inside_data )

        if rtt == 'list':
            # the tag is type list
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
            tag_content = bedrock_nbt_to_universal_nbt( inside_data )

        # save the data
        output_data.append([real_tag_type,real_tag_name,tag_content])
    
    return output_data

'''

compound is {}
list is []
int is 1
byte is 1b
short is 1s
string is "1"

'''

def universal_nbt_to_amulet_nbt(universal_nbt,is_list=False):
    '''recursively convert universal nbt into amulet nbt'''
    
    # store the final string
    final_string = ''

    for datatagindex, datatag in enumerate( universal_nbt ):
        tag_type, tag_name, tag_content = datatag
        
        # check if this is the last tag, if it is, don't put a comma after it
        is_last_tag = not datatagindex < len(universal_nbt)-1

        if tag_name!='' and not is_list:
            final_string += tag_name+': '

        if tag_type == 'Int':
            final_string += str(tag_content)

        if tag_type == 'Byte':
            final_string += str(tag_content)

        if tag_type == 'Short':
            final_string += str(tag_content)

        if tag_type == 'String':
            final_string += str(tag_content)

        if tag_type == 'Compound':
            final_string += '{' + universal_nbt_to_amulet_nbt( tag_content ) + '}'

        if tag_type == 'List':
            final_string += '[' + universal_nbt_to_amulet_nbt( tag_content, is_list=True ) + ']'

        final_string += (', ' if not is_last_tag else '')

    return final_string

import json

def represent_tags(data, recursion_level = 1):
    for dat in data:
        tt,tn,tc = dat # tag type, tag name, tag content
        print("   "*recursion_level, "TAG_"+str(tt).title()+'-'+str(tn))
        if type(tc)==list:
            represent_tags(tc,recursion_level+1)

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

        univ_nbt = bedrock_nbt_to_universal_nbt( new )
        represent_tags( univ_nbt )

        amulet_nbt = universal_nbt_to_amulet_nbt( univ_nbt )
        print("AMULET-NBT")
        print(amulet_nbt)
        print()

'''
TAG_Compound-:[
  TAG_Byte-Findable:0,
  TAG_List-Items:[
    TAG_Compound-0:[
      TAG_Byte-Count:1,
      TAG_Short-Damage:0,
      TAG_String-Name:minecraft:stone_sword,
      TAG_Byte-Slot:0, 
      TAG_Compound-tag:[
        TAG_Int-Damage:0,
        TAG_List-ench:[
          TAG_Compound-0:[
            TAG_Short-id:9,
            TAG_Short-lvl:2
          ]
        ]
      ]
    ]
  ],
  TAG_String-id:Chest,
  TAG_Byte-isMovable:1
]

Findable
Items
    0
        Count
        Damage
        Name
        Slot
        tag
        Damage
        ench
            0
                id
                lvl
id
isMovable
'''

if __name__ == '__main__':
    print("RUNNING TEST")
    bedrocknbtx = '[TAG_Int-facing_direction:4]'
    print(bedrocknbtx)

    r = BedrockNBT( bedrocknbtx )
    r.into_amulet_nbt()
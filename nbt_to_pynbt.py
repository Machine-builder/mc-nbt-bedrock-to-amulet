import bedrock

import mcNBTFormatter as nbtformat

'''
turn this :
[TAG_Byte-upside_down_bit:1, TAG_Int-weirdo_direction:3]

into this :
{"upside_down_bit": 1b, "weirdo_direction": 3}
'''

with bedrock.World("C:\\Users\\josh\\AppData\\Local\\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang\\minecraftWorlds\\lEdaXSWuAgA=") as world:
    print(world)
    block = world.getBlock( 10,4,14 ) # z = 13-stair, 14-chest
    bnbt = block.nbt
    props = block.properties

    print("nbt type :", type(bnbt))
    print("properties type :", type(props))

    if bnbt: dat = bnbt
    else: dat = props
    sdat = str(dat)
    open('f_decoded_world_block.txt', 'w').write(sdat)

    if bnbt:
        print("NBT -")
        print(bnbt)
        print("program out :")

        NBTDATA = nbtformat.BedrockNBT( bnbt )
        NBTDATA.into_amulet_nbt()
    
    if props:
        print("PROPERTIES -")
        print(props)
        print("program out :")

        PROPERTIESDATA = nbtformat.BedrockNBT( props )
        PROPERTIESDATA.into_amulet_nbt()
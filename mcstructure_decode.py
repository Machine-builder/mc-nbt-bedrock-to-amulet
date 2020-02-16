import amulet_nbt.amulet_py_nbt as pynbt
import json

dat = pynbt.load( input("fname >> ")+".mcstructure", compressed=False, little_endian=True )
sdat = (dat.to_snbt())

open('f_decoded_mcstructure.txt', 'w').write( sdat )
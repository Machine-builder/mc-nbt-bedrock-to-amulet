import amulet_nbt.amulet_py_nbt as pynbt
import json

dat = pynbt.load( 'inp.mcstructure', compressed=False, little_endian=True )
sdat = (dat.to_snbt())

open('sdata.txt', 'w').write( sdat )
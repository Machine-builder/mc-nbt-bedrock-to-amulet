import amulet_nbt.amulet_py_nbt as pynbt

sdat = open("sdata.txt", 'r').read()

dat = pynbt.from_snbt(sdat)
pynbt.NBTFile(dat).save_to("out.mcstructure", compressed=False, little_endian=True)


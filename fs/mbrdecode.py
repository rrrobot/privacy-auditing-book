# mbrdecode.py:
# This program opens a disk image in binary mode,
# reads the first sector, verifies the MBR signature bytes,
# and then prints the value of the four slots in the standard
# partition table. Notice the use of struct.unpack() to unpack
# the little endian Byte and Long values

if __name__=="__main__":
    import argparse,sys,struct
    parser = argparse.ArgumentParser(description="Print the MBR")
    parser.add_argument("image",help="Image file",type=str)
    args = parser.parse_args()

    with open(args.image,"rb") as img:
        img.seek(0)             # not necessary, as image opens to seek(0)
        mbr = img.read(512)     # read a block
        if mbr[510:512]!=b'\x55\xaa':
            raise RuntimeError(img.name + " is not an MBR image")
        for i in range(0,4):
            loc = 446+i*16
            ptype = struct.unpack('<B',mbr[loc+4:loc+5])[0] 
            lba_s = struct.unpack('<L',mbr[loc+8:loc+12])[0] 
            print("Partition {} offset: {:X}h type: {:3} LBA Start: {:8}".format(
                    i+1,loc,ptype,lba_s))

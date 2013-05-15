if __name__=="__main__":
    import argparse,sys
    parser = argparse.ArgumentParser(description="Print FAT disk metadata")
    parser.add_argument("-o","--offset",help="Starting block number",type=int,default=0)
    parser.add_argument("-b","--blocksize",help="Specify block size",type=int,default=512)
    parser.add_argument("image",help="Image file",type=str)
    args = parser.parse_args()

    with open(args.image,"rb") as img:
        offset = args.offset * args.blocksize
        img.seek(offset)
        bss = img.read(512)
        print("oemname: ",bss[3:11].decode('latin1',errors='replace'))
        print("ssize:   ",bss[11:13])

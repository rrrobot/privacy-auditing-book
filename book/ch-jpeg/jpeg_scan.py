#!/usr/bin/env python3
# http://stackoverflow.com/questions/1557071/the-size-of-a-jpegjfif-image/1602428#1602428
# http://gvsoft.homedns.org/exif/exif-explanation.html

RST = ['\xff\xd0','\xff\xd1','\xff\xd2','\xff\xd3','\xff\xd4',
       '\xff\xd5','\xff\xd6','\xff\xd7','\xff\xd8']
def validate_jpeg(fn):
    import struct
    data = open(fn,"rb").read()
    cc = 0
    # print(fn)
    while True:
        if cc+2 > len(data):
            print("{}   RAN OFF END ".format(fn));
            return

        # print("  Found marker {} {} at {}".format(hex(data[cc]),hex(data[cc+1]),cc))
        # assert(data[cc]==255)

        if data[cc:cc+2]==b'\xff\xd8':     # SOI
            cc += 2
            continue
        if data[cc:cc+2]==b'\xff\x01':     # TEM
            cc += 2
            continue
        
        if (data[cc:cc+2] in RST):
            cc += 2
            continue
        
        if data[cc:cc+2]==b'\xff\xd9':     # EOI
            return                         # validated!

        if data[cc:cc+2]==b'\xff\xda':  # SOS
            # Found a start of stream. Scan for the EOI
            
            # experiment: any repeated characters?
            for i in range(cc,len(data)-4):
                if data[i]==data[i+1]==data[i+2]==data[i+3]:
                    print("{} len={} repeated data at {}: {}".format(fn,len(data),i,data[i]))
            
            eoi_loc = data.find(b'\xff\xd9',cc)
            if eoi_loc and eoi_loc+2 == len(data):
                return                  # validates
            if eoi_loc==-1:             # incomplete
                print("{} INCOMPLETE".format(fn))
                return
            print("{}  eoi_loc={}  len={}  EXTRA BYTES: {}".format(fn,eoi_loc,len(data),len(data)-eoi_loc))
            return

        l = struct.unpack('>H',data[cc+2:cc+4])[0]
        # print("      Found variable length len={}".format(l))
        cc += 2 + l


if __name__=="__main__":
    import argparse,os

    parser = argparse.ArgumentParser(description="Search and process JPEGs in local file system")
    parser.add_argument("path",help="Path to search",type=str)
    
    args = parser.parse_args()

    for (dirpath, dirnames, filenames) in os.walk(args.path):
        for name in filter(lambda chk:chk.lower().endswith(".jpg") or chk.lower().endswith(".jpeg"),filenames):
            fn = os.path.join(dirpath,name)
            validate_jpeg(fn)

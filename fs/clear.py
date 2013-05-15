if __name__=="__main__":
    import argparse,sys
    parser = argparse.ArgumentParser(description="Clear a raw disk partition")
    parser.add_argument("-b","--blocksize",help="Specify block size",type=int,default=512)
    parser.add_argument("device",help="Device",type=str)
    args = parser.parse_args()

    count = 0
    zbuf  = '\000' * args.blocksize
    with open(args.device,"wb") as f:
        while not f.eof():
            f.write(zbuf)
            count += 1
    print("{:,} sectors ({:,} MB) were cleared".format(count,count*args.blocksize/1e6))

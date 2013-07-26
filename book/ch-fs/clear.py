if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Clear a raw disk partition")
    parser.add_argument("-b","--blocksize",type=int,default=512,
                        help="Specify block size")
    parser.add_argument("device",help="Device",type=str)
    args = parser.parse_args()

    count = 0
    with open(args.device,"wb") as f:
        while not f.eof():
            f.write('\000' * args.blocksize)
            count += 1
    print("{:,} sectors ({:,} MB) were cleared"
          .format(count,count*args.blocksize/1e6))

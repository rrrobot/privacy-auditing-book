#!/usr/bin/env python3

# jpeg_scan reworked to store results in a database
# This program builds on what we learned from jpeg_scan.py:
# - Truncated JPEGs are rare

import mmap,struct,sqlite3

# Schema using SQLLite foreign key support introduction in SQLite 3.6.19
# http://sqlite.org/foreignkeys.html

dbfile = 'jpegs.sqlite3'
schema = """
CREATE TABLE jpegs (fileid INTEGER PRIMARY KEY ASC,filename TEXT UNIQUE,filesize INTEGER);
CREATE TABLE markers (trackid INTEGER PRIMARY KEY ASC, 
           fileid INTEGER,marker INTEGER,offset INTEGER,len INTEGER, 
           FOREIGN KEY (fileid) REFERENCES jpegs(fileid));
CREATE TABLE comments (commentid INTEGER PRIMARY KEY ASC,fileid INTEGER,comment TEXT,
           FOREIGN KEY (fileid) REFERENCES jpegs(fileid));
CREATE TABLE extra (extraid INTEGER PRIMARY KEY ASC,fileid INTEGER,len INTEGER,
           FOREIGN KEY (fileid) REFERENCES jpegs(fileid));
"""

import os

if not os.path.exists(dbfile):
    print("Creating database "+dbfile)
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    for stmt in schema.split(";"):
        c.execute(stmt)
else:
    conn = sqlite3.connect(dbfile)
    c = conn.cursor()
    

def validate_jpeg(fn):
    c.execute("SELECT fileid FROM jpegs WHERE filename=?",(fn,))
    if c.fetchone():
        print(fn,"in database")
        return     # already in database
    f = open(fn,"rb")
    data = f.read()
    c.execute("INSERT INTO jpegs (filename,filesize) VALUES (?,?)",(fn,len(data)))
    fileid = c.lastrowid
    print(fn,fileid)
    pos = 0
    markers = []                # array of (offset,marker) elements
    while pos+2 <= len(data):
        if data[pos] != 0xFF:
            break;              # end of image data
        marker = data[pos+1]
        markers.append((pos,marker)) # record offset and marker

        # Decode the fixed-size markers
        if marker==0xD8:  # SOI
            pos += 2;
            continue

        if (marker >= 0xD0 and marker <= 0xD8): # RSTn
            pos += 2;
            continue
        
        if marker==0xD9: # EOI
            extra = len(data)-(pos+2)
            if extra:
                c.execute("INSERT INTO extra (fileid,len) VALUES (?,?)",(fileid,extra))
            break

        # Decode the SOS segment
        if marker==0xDA: # Found SOS; scan for the EOI
            eoi_loc = data.find(b'\xFF\xD9',pos)
            if eoi_loc>0:
                pos = eoi_loc;
                continue 
            pos = len(data)     # go to end
            break               # no EOI?

        # Get the length, add it, then loop
        try:
            segment_len = struct.unpack('>H',data[pos+2:pos+4])[0]
            if marker==0xFE:
                c.execute("INSERT INTO comments (fileid,comment) VALUES (?,?)",(fileid,data[pos+4:pos+2+segment_len]))
            # Additional decoding could go here
            pos += 2 + segment_len
        except struct.error:
            break               # end of file?

    # Now put all of the markers into the database
    for i in range(len(markers)-1):
        c.execute("INSERT INTO markers (fileid,marker,offset,len) VALUES (?,?,?,?)",
                  (fileid,markers[i][1],markers[i][0],markers[i+1][0]-markers[i][0]))
        # Add the final marker
    if len(markers)>0:
        c.execute("INSERT INTO markers (fileid,marker,offset,len) VALUES (?,?,?,?)",
                  (fileid,markers[-1][1],markers[-1][0],len(data)-markers[-1][0]))
    conn.commit()


if __name__=="__main__":
    import argparse,os

    parser = argparse.ArgumentParser(description="Search and process JPEGs in local file system")
    parser.add_argument("path",nargs="+",help="Path to search")
    args = parser.parse_args()

    def is_jpeg_fn(fn):
        return os.path.splitext(fn)[1].lower() in ['.jpg','.jpeg']

    
    for fn in args.path:
        if os.path.isdir(fn):
            for (dirpath, dirnames, filenames) in os.walk(fn):
                print(dirpath)
                for name in filter(is_jpeg_fn,filenames):
                    validate_jpeg(os.path.join(dirpath,name))
        else:
            validate_jpeg(fn)


import hashlib
import os
import glob

def md5_for_file(filename, block_size=2**6):
    md5 = hashlib.md5()
    f = open(filename, "rb")
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.digest()

def generate_md5_dict(directory):
    d = {}
    for f in glob.glob("%s/*.msg" % directory):
        d[f] = md5_for_file(f)
    return d

if __name__ == "__main__":
    p = "c:/Code/python/email-db/email"
    md5_dict = generate_md5_dict(p)
    for d in md5_dict.keys():
        print "%s: %s" % (d, md5_dict[d])
        
	

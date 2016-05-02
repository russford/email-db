import os
import hashlib
import glob
import sqlite3
import ExtractMsg

def md5_for_file(filename, block_size=2**6):
    md5 = hashlib.md5()
    f = open(filename, "rb")
    while True:
        data = f.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()

def create_db (directory):
    con = sqlite3.connect('%s/email-db' % directory)
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS email")
    cur.execute('''CREATE TABLE email (
subject TEXT,
sender TEXT,
names_from TEXT,
names_cc TEXT,
body TEXT,
sent_date TEXT,
attachments TEXT,
file_location TEXT,
md5 TEXT)''')
    con.commit()
    return con
    
def msg_data (msg_file):
    md5 = md5_for_file (msg_file)
    msg = ExtractMsg.Message(msg_file)
    attachment_str = '\n'.join(a.longFilename for a in msg.attachments)
    db_data = [ msg.subject, msg.to, msg.sender, msg.cc, msg.body, msg.date, attachment_str, msg_file, md5 ]
    return db_data

def generate_db (directory):
    con = create_db (directory)
    cur = con.cursor()
    i = 0
    err_action = "s"
    for msg_file in glob.glob("%s/*.msg" % directory):
        try:
            db_data = msg_data (msg_file)
            cur.execute ("INSERT INTO email VALUES (?,?,?,?,?,?,?,?,?)", db_data)
        except:
            print "error in file %s" % msg_file
            if err_action <> "c":
                print "i for ignore, c to ignore all, s to stop:"
                err_action = raw_input()
                if err_action == "s":
                    break
				
        i = i+1
        if i%10 == 0: print "%s completed"%i
    con.commit()       
        
if __name__ == "__main__":
    a = generate_db("c:/email/2015-11 to 12")
    

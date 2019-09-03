# Import python modules
from ftplib import FTP
from main_ import *

# FTP transfer including error handling
# which would otherwise break the code
def ftp_upload(filename):
    try:
        print("ftp_upload: " + filename)
        ftp = FTP('ftp.mediaculturalstudies.com')
        ftp.login('pi@mississippistudies.org','pain77?Piece')
        ftp.retrlines('LIST')
        ftp.storbinary("STOR " + filename, open(filename, 'rb'))
        ftp.quit()
    except:
        msg_handler("Error: ftp_upload()", "in FTP_.py")





------author--->black-perl-------
------written @ 17-10-2013---




from gdata.spreadsheet.service import *
from getopt import getopt,error
from getpass import getpass
import sys
from prompter import CRUD


#defining gloabal variables
_id=" "
_password=" "
client=None

def userCredentials():
    try:
      opts,arguments=getopt(sys.argv[1:]," ",["user="])#username,opt are locals for functions
    except error:
                       print "----RUN AS: python spreadsheets_connect.py --user [username]"
                       sys.exit()
    if len(opts)>0:#because if not argument given to --user error is there
     for user,username in opts:
        
        
        
       
        if user!="--user":
            print "----RUN AS: python spreadsheets_connect.py --user [username]"
            sys.exit()

        else:
         
         global _id
         _id=username

    elif len(opts)==0:
         print "----RUN AS: python spreadsheets_connect.py --user [username]"
         sys.exit()

         
def promptForPassword():
    global _password
    _password=getpass("enter password for:{0}---->".format(_id))
    
def connect(userid,password):
    global client#we need to define client to global
    client=SpreadsheetsService()
    client.email=userid
    client.password=password
    client.source = 'Spreadsheets GData Sample'
    client.ProgrammaticLogin()

def clientConnect():
    userCredentials()
    if "@"  not in _id:
         print"----RUN AS: python spreadsheets_connect.py --user [username] and enter valid username"
         sys.exit()
    else:
        promptForPassword()
    connect(_id,_password)
    print "----connection established------"
    return client

if __name__=="__main__":
    a=clientConnect()
    mycrud=CRUD(a)
    mycrud.run()
    
    
        

    
    
    

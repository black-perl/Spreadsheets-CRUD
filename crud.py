from gdata.spreadsheet import *
from gdata.spreadsheet.service import *
import string



class CRUD:
    def __init__(self,clientConnect):
        self.client=clientConnect#referring to a global function here and i think it first search the name of the attributte in class namespace and then in global namespace
        self.sheet_key=" "
        self.wk_key=" "

    def spreadsheetsFeed(self):
        feed=self.client.GetSpreadsheetsFeed()#returns an instance of class Spreadsheets Spreadsheets Feed and that is the no. of spreadsheets
        self.printFeed(feed)#remember that printfeed is an object atribute and for an  instantiated object we have to use its name that's why we have used a self with it
        choice=raw_input("Enter the no. :-")
        #now we will find the key for our selected spreadsheet
        sheet_id=feed.entry[string.atoi(choice)-1].id.text.split("/")
        self.sheet_key=sheet_id[len(sheet_id)-1]
        
    def worksheetsFeed(self):
        feed=self.client.GetWorksheetsFeed(self.sheet_key)#we specify the spreadsheet id for which we need the worksheet feed
        self.printFeed(feed)
        choice=raw_input("Enter the no. :-")
        sheet_id=feed.entry[string.atoi(choice)-1].id.text.split("/")
        self.wk_key=sheet_id[len(sheet_id)-1]#getting the worksheet key


    def actionPrompt(self):
        mylist=["   ---->show","  ---->insert","  ---->delete","  ---->update"]
        choices=enumerate(mylist,1)
        for i,j in choices:
            print i,j
        while True:
           user_choice=raw_input("enter:-")
           if int(user_choice) in range(1,5):
               return user_choice
               break#a break statement does not matter here as return will take out of the function yield v/s return
            
        
    def cellsOperations(self):
        choice=self.actionPrompt()
        if choice=="1":
            feed=self.client.GetCellsFeed(self.sheet_key,self.wk_key)#returns cells feed
            # returns an instance of the class SpreadsheetsCellsFeed
            self.printFeed(feed)
            self.run()
        elif choice=="2":
            print "addding a new cell value is not supported"
            self.run()
        elif choice=="4":
          #try:
            print "use the format---> update {row} {col} {value} \n eg. update 4 5 ankush"
            command=raw_input("Enter the command:-").split(" ")
            while True:
                if command[0]=="update":
                    #try:
                        entry=self.client.UpdateCell(row=command[1], col=command[2], inputValue=command[3], key=self.sheet_key, wksht_id=self.wk_key)
                        if isinstance(entry,SpreadsheetsCell):
                                       print 'Updated!'
                                       self.run()
                                       break

                    #except Error:
                        print "your command is in wrong format"
                        command=raw_input("Enter the command:-").split("")
          #except:
            print "follow the proper format"
            self.run()

        else:
            print "delete command is also not supported"
            self.run()

    def listOperations(self):
        choice=self.actionPrompt()
        if choice=="1":
            feed=self.client.GetListFeed(self.sheet_key,self.wk_key)
            self.printFeed(feed)
            self.run()
        elif choice=="2":
         data={}

         try:
          print "add a new row using -> insert {values} \n eg.- insert  name=ankush sub=sharma"
          while True:
            command=raw_input("enter-->").split(" ")
            if command[0]=="insert":
                for i in range(len(command)-1):
                    dummy=command[i+1].split("=")
                    data[dummy[0]]=dummy[1]
                
                entry=self.client.InsertRow(data,self.sheet_key,self.wk_key)
                if isinstance(entry,SpreadsheetsList):
                        print "inserted"
                        self.run()
                        break
            else:
                pass
         except:
            print "follow the correct format"
            self.run()

        elif choice=="4":
            print "update a row using the format ---> update {row} {new-data}"
            while True:
                data={}
                command=raw_input("enter-->").split(" ")
                if command[0]=="update":
                  try:
                    index=command[1]
                    for i in range(len(command)-2):
                        dummy=command[i+2].split("=")
                        data[dummy[0]]=dummy[1]

                    old_feed=self.client.GetListFeed(self.sheet_key,self.wk_key)
                    old_entry=old_feed.entry[string.atoi(index)-1]
                    
                    entry=self.client.UpdateRow(old_entry,data)
                    if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
                                  print 'Updated!'
                                  self.run()
                                  break
                  except :#general except will catch any error
                            print "enter in the correct format"
                            self.run()

        else:
             while True:
              try:
               print "enter in the format--> delete {row}"
               command=raw_input("enter-->").split(" ")
               if command[0]=="delete":
                    index=command[1]
                    old_feed=self.client.GetListFeed(self.sheet_key,self.wk_key)
                    old_entry=old_feed.entry[string.atoi(index)-1]
                    self.client.DeleteRow(old_entry)
                    print "deleted"
                    self.run()
                    break

               else:pass
              except:
                print "please follow the proper format"
                self.run()


    def printFeed(self,feed):
        data=enumerate(feed.entry,1)
        for i,entry in data:
            #now we can have multiple instances of feed
            if isinstance(feed,SpreadsheetsSpreadsheetsFeed):
                print "You have the following spreadsheets:"
                print "{0}  -->  {1} \n".format(i,entry.title.text)

            elif isinstance(feed,SpreadsheetsWorksheetsFeed):
                print "You have the following Worksheets:"
                print "{0}  -->  {1} \n".format(i,entry.title.text)

            elif isinstance(feed,SpreadsheetsCellsFeed):
                print "{0}  ----> {1} \n".format(entry.title.text,entry.content.text)
            else:
                print '%s %s %s' % (i, entry.title.text, entry.content.text)
                # Print this row's value for each column (the custom dictionary is
                # built using the gsx: elements in the entry.)
                print 'Contents:'
                for key in entry.custom:  
                   print '  %s: %s' % (key, entry.custom[key].text) 
                   print '\n',
                   
             
                
            



    def run(self):
        self.spreadsheetsFeed()
        self.worksheetsFeed()
        while True:
         choice=raw_input("On what you want to operate -- list(enter 1) or cells(enter2)")
         if choice=="1":
            self.listOperations()
            break
         elif choice=="2":
            self.cellsOperations()
            break
        
    

            
        
        
    

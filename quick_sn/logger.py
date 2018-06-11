#Efficiency Tip:
# from test.test_import import PycRewritingTests
# every time you write something to a csv, it deletes everything in the csv, because of this, in order to log 
# something you must first record everything already in the csv, then write everything that used to be in the
# csv plus what you are trying to log.  If you are dealing with a csv with a lot of data, recording then re-writing 
# it all will take a lot of time.  Because of this, the most efficient way to do logging is to build up a big list
# of all the data you want to log, then logging it all at once.  Therefore you should try to always use
# logList() instead of logSingle() 

import csv
import os.path


# use this to get path
# import os
#   
# full_path = os.path.realpath(__file__)
# csvPath =  os.path.dirname(full_path) + '\\NEW_CSV_MADE_BY_LOGGER.csv'

#------------------------------------------------------PUBLIC------------------------------------------------------#

#logs a list of dicts, each dict = one row, dict = {columb header: data}
#ex:
# tweetLogDictList = [{'Time/Date': '11:34pm on monday',
#                      'User_Name': '@bob',     
#                      'Tweet':     'my name is bob and this is a test'},
#                     
#                     {'Time/Date': '12:35pm on tuesday',
#                      'User_Name': '@jill',     
#                      'Tweet':     'my name is jill and im the worst'}]
def logList(dataDictList, csvPath, wantBackup = True):       
    #read the csv into a list of dicts (one dict for each row)
    csvData = readCSV(csvPath)  
    
    #check to make sure the csv's fieldnames matches the headerList, if not, create backup before overwriting
    if not formatsMatch(dataDictList[0], csvData):
        if wantBackup == True:
            backup(csvData, csvPath)
        csvData = []
     
    #add the data to be logged to the list of csv data
    for dataDict in dataDictList:
            #make sure data wont cause a unicode error - not efficient!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        for key, data in dataDict.items():
            if type(data) == str:
                data = data.encode('ascii', 'ignore')
        csvData.append(dataDict) 
        
    
        
    #write it all back to the csv    
    write2CSV(csvData, csvPath)       


#should try not to use much, its not very efficient, same thing as logList() but one dict at a time
#ex:
# tweetLogDict = {'Time/Date': '11:47pm on saterday',
#                 'User_Name': '@sagman',     
#                 'Tweet':     'my name is sagman bardlileriownoaosnfo'}


def logSingle(dataDict, csvPath, wantBackup = True):
    #check if file already exists, if not, make it
    try:#try is safer than isfile()
        #read the csv into a list of dicts (one dict for each row) 
        csvData = readCSV(csvPath)  
        
        #check to make sure the csv's fieldnames matches the headerList, if not, create backup before overwriting
        if not formatsMatch(dataDict, csvData):
            if wantBackup == True:
                backup(csvData, csvPath)
            csvData = []  
               
    except:
        csvData = []
        
    #make sure data wont cause a unicode error - not efficient!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    for key, data in dataDict.items():
        if type(data) == str:
            data = data.encode('ascii', 'ignore')
        
    #add the data to be logged to the list of csv data
    csvData.append(dataDict) 
        
    #write it all back to the csv    
    write2CSV(csvData, csvPath) 


#returns a list of dicts
#each element of the list is dict with entries like {header_name: data}
def readCSV(csvPath):
    dataDictList = []
    
    with open(csvPath, 'rt') as csvfile:#, encoding='utf8'
        csvReader = csv.DictReader(csvfile)
             
        for row in csvReader:
            rowDict = {}
            for header in csvReader.fieldnames:         
                #convert string to dict
                dataStr = row[header]
                rowDict[header] = dataStr
                #headerDataDict = ast.literal_eval(headerdataStr)   
            dataDictList.append(rowDict)              
    return dataDictList


def write2CSV(logDictList, csvPath):
    with open(csvPath, 'wt') as csvfile:#, encoding='utf8'
        fieldnames = []
        for header, data in logDictList[0].items():
            fieldnames.append(header)

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator = '\n')
        writer.writeheader()
        
        #build rowDictList
        rowDictList = []
        rdlPos = 0
        for logDict in logDictList:
            for header, data in logDict.items():
                                    
                if rowDictList == [] or rdlPos > (len(rowDictList) - 1):
                    rowDictList.append({})
                rowDictList[rdlPos][header] = data
            rdlPos +=1
        #write rows
        for rowDict in rowDictList:
            writer.writerow(rowDict)
    csvfile.close()
       

def backup(csvData, csvPath):
    backupCount = 0
    sp = csvPath.split(".")
    backupPath = '_BACKUP_' + sp[0] + '_BACKUP_' + str(backupCount) + '.' + sp[1]
    
    while(os.path.isfile(backupPath)):
        backupCount += 1
        backupPath = sp[0] + '_BACKUP_' + str(backupCount) + '.' + sp[1]
    
    write2CSV(csvData, backupPath)
              
              
def formatsMatch(dataDict, csvData):
    #if the csv is empty, no need for a backup
    if csvData == []:
        return True
    
    for header, data in dataDict.items():
        if header not in csvData[0]:
            return False
    return True
 
# full_path = os.path.realpath(__file__)
# csvPath =  os.path.dirname(full_path) + '\\tweet_log.csv' 
# 
# tweetLogDict = {'Time/Date': '11:47pm on saterday',
#                 'User_Name': '@sagmanblablatest3',     
#                 'Tweet':     'my name is sagman'}
#  
# tweetLogDictList = [{'Time/Date': '11:34pm on monday',
#                      'User_Name': '@bob',     
#                      'Tweet':     'my name is bob and this is a test'},
#                      
#                     {'Time/Date': '12:35pm on tuesday',
#                      'User_Name': '@jill',     
#                      'Tweet':     'my name is jill and im the worst'}] 
#           
# logList(tweetLogDictList, csvPath)         
# logSingle(tweetLogDict, csvPath)
          
#         
        
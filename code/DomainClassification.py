import nltk

import configparser
import datetime
from nltk.corpus import stopwords
en_stops = set(stopwords.words('english'))
en_stops.update(['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}','*','â€™','|'])

from DataAccess import DataAccess
from Classifier import Classifier as classifier

parameter = configparser.ConfigParser()
parameter.read('../config/parameter.config')

class DomainClassification():
    def processCleanText(self, transactionData):
         nltk_tokens = nltk.word_tokenize(transactionData)
         cleanTextList = []
         for word in nltk_tokens: 
             if word not in en_stops:
                 cleanTextList.append(word.lower())
         print(cleanTextList)
         return cleanTextList
      
  
    def trainModel(self):
        url=parameter.get("database","url")
        masterKey=parameter.get("database","masterkey")
        dbName=parameter.get("database","db")
        collName=parameter.get("database","collection")
        
        obj = DataAccess(url,masterKey,dbName)
        documentlist = obj.findAll(collName)
        arr = [] 
        for doc in documentlist:
            temp = {}
            temp ['domain'] = doc['$v']['domain']['$v']
            temp ['keywords'] = doc['$v']['keywords']['$v']
            arr.append(temp)

        print('***train data***',arr)
        now = datetime.datetime.now()
        dateTime = str(now.day)+'_'+str(now.month)+'_'+str(now.year)+'_'+str(now.hour)+'_'+str(now.minute)+'_'+str(now.second)
        classifier.saveModel(arr,'../model/backup/wbg'+'_'+dateTime)
        classifier.saveModel(arr,'../model/wbg')
        return 'process completed'
    
    
    def classifyDomain(self,transaction_data_utterance): 
         # load training data
         trainList = classifier.loadModel('../model/wbg')
         cleanTextList = self.processCleanText(transaction_data_utterance)
         lengthOfCleanText = len(cleanTextList)
         tempDict = {} 
         for i in cleanTextList:
             for j in trainList:
                 domain = j.get('domain')
                 keywords = j.get('keywords')
                 keywords = keywords.lower()
                 if i in keywords.split(','): #if word matches push it in tempDict dictionary
                     if domain in tempDict.keys(): #if domain present increment the count by 1
                         tempDict[domain] = 1 + tempDict.get(domain)
                     else: #if not present set the count to 1
                         tempDict[domain] = 1
         
         result = self.formatOutputResult(tempDict,lengthOfCleanText)
         return result

    def formatOutputResult(self,obj,lengthOfText):
        finalList = []
        finalResultObj = {}
        if len(obj) > 0:
             tempList = []
             for key, value in obj.items():
                 tempObj = {}
                 tempObj['name'] = key
                 tempObj['score'] = value/lengthOfText
                 print(key+' -> '+str(value)+'/'+str(lengthOfText)+' = '+str(value/lengthOfText))
                 tempList.append(tempObj)
             finalResultObj['domains'] = sorted(tempList, key = lambda k:k['score'], reverse=True)
        else:
            finalResultObj['domains'] = finalList
        
        return finalResultObj
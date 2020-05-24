import pandas as pd
import pymongo


def mongoInit():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["discordText"]
    print(myclient.list_database_names())

def startListening(author):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["discordText"]
    mycol = mydb["trackedUsers"]
    if(userExists(author)):
        print('turning on message tracking')
        query = { "username": author.name + '#' + author.discriminator }
        tracking = { "$set": {"tracking": True } }
        mycol.update_one(query, tracking)
    else:
        userDict = { "username": author.name + '#' + author.discriminator, "tracking": True}
        mycol.insert_one(userDict)

def stopListening(author):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["discordText"]
    mycol = mydb["trackedUsers"]
    if(userExists(author)):
        print('turning off message tracking')
        query = { "username": author.name + '#' + author.discriminator }
        tracking = { "$set": {"tracking": False } }
        mycol.update_one(query, tracking)
    else:
        userDict = { "username": author.name + '#' + author.discriminator, "tracking": False }
        mycol.insert_one(userDict)

def userExists(author):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["discordText"]
    mycol = mydb["trackedUsers"]
    query = { "username": author.name + '#' + author.discriminator}
    user = mycol.find(query)
    if(user.count() == 1):
        return True
    elif(user.count() == 0):
        return False
    print("Error")

def userIsTracking(author):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["discordText"]
    mycol = mydb["trackedUsers"]
    query = { "username": author.name + '#' + author.discriminator, "tracking": True}
    user = mycol.find(query)
    if(user.count() == 1):
        return True
    else:
        return False

def trackMessage(message):
    if(userIsTracking(message.author)):
        print("Storing message")
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["discordText"]
        mycol = mydb["messages"]
        query = { "username": message.author.name + '#' + message.author.discriminator, "message": message.content}
        mycol.insert_one(query)

    else:
        print("Ignoring message")

def getMessages(author):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["discordText"]
    mycol = mydb["messages"]
    query = { "username": author.name + '#' + author.discriminator }
    messages = mycol.find(query)
    print(messages)
    return messages  

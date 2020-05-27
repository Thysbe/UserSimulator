import pymongo
from pymongo import MongoClient


class UserManager:

    def __init__(self):
        self.my_client: MongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.my_client["discordText"]
        self.tracked_col = self.mydb["trackedUsers"]
        self.messages_col = self.mydb["messages"]
        print(self.my_client.list_database_names())

    def startListening(self, author):
        if self.userExists(author):
            print('turning on message tracking')
            query = {"username": author.name + '#' + author.discriminator}
            tracking = {"$set": {"tracking": True}}
            self.tracked_col.update_one(query, tracking)
        else:
            userDict = {"username": author.name + '#' + author.discriminator, "tracking": True, "userId": author.id}
            self.tracked_col.insert_one(userDict)

    def stopListening(self, author):
        if self.userExists(author):
            print('turning off message tracking')
            query = {"username": author.name + '#' + author.discriminator}
            tracking = {"$set": {"tracking": False}}
            self.tracked_col.update_one(query, tracking)
        else:
            userDict = {"username": author.name + '#' + author.discriminator, "tracking": False, "userId": author.id}
            self.tracked_col.insert_one(userDict)

    def userExists(self, author):
        query = {"username": author.name + '#' + author.discriminator}
        user = self.tracked_col.find(query)
        if user.count() == 1:
            return True
        elif user.count() == 0:
            return False
        print("Error")

    def userIsTracking(self, author):
        query = {"username": author.name + '#' + author.discriminator, "tracking": True}
        user = self.tracked_col.find(query)
        if user.count() == 1:
            return True
        else:
            return False

    def trackMessage(self, message):
        if self.userIsTracking(message.author):
            print("Storing message")
            username = message.author.name + '#' + message.author.discriminator
            # {'$push': {"messages": message.content}})
            self.tracked_col.update({'username': username}, {'$push': {'messages': message.content}})
        else:
            print("Ignoring message")

    def getMessages(self, userId):
        query = {'userId': userId}
        print(userId)
        print(query)
        user = self.tracked_col.find(query)
        print(query)
        print(user)
        for message in user[0].messages:
            print(message)
        return user[0].messages
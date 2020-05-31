import pymongo
from pymongo import MongoClient
from enum import Enum


# class TrackingLevel(Enum):
#    NONE: 0
#    LIMITED: 1
#    FULL: 2

# class ChannelTrackingLevel(Enum):
#    NOT_TRACKED: 0  # Channel doesn't store messages
#    FULL_TRACKING: 1  # Channel stores messages from users with limited and full tracking
#    LIMTED_TRACKING: 2  # Channel stores messages from users with full tracking


class UserManager:

    def __init__(self):
        self.my_client: MongoClient = pymongo.MongoClient(
            "mongodb://localhost:27017/")
        self.mydb = self.my_client["discordText"]
        self.tracked_col = self.mydb["trackedUsers"]
        self.channels_col = self.mydb["channels"]
        self.userTrackingLevels = ['NONE', 'LIMITED', 'FULL']
        self.channelTrackingLevels = [
            'NOT_TRACKED', 'FULL_TRACKING', 'LIMITED_TRACKING']
        print(self.my_client.list_database_names())

    def updateTrackingLevel(self, userId, trackingLevel, username):
        if self.userExists(userId):
            print('updating user record')
            query = {"userId": userId}
            tracking = {"$set": {"trackingLevel": trackingLevel}}
            self.tracked_col.update_one(query, tracking)
        else:
            print('creating user record')
            userDict = {"trackingLevel": trackingLevel,
                        "userId": userId, "username": username}
            self.tracked_col.insert_one(userDict)

    def userExists(self, userId):
        query = {"userId": userId}
        user = self.tracked_col.find(query)
        if user.count() == 1:
            return True
        elif user.count() == 0:
            return False
        print("Error")

    def getUserName(self, userId):
        query = {"userId": userId}
        user = self.tracked_col.find(query)
        return user[0]['username']

    def userTrackingLevel(self, userId):
        if(self.userExists(userId)):
            query = {"userId": userId}
            user = self.tracked_col.find(query)
            return user[0]['trackingLevel']
        return 'NONE'

    # user tracking none - dont store message
    # user tracking limted - store if channel is full tracking
    # user tracking full - store if channel is not NOT_TRACKED
    def trackMessage(self, message):
        trackingLevel = self.userTrackingLevel(message.author.id)
        channelTrackingLevel = self.channelTracking(message.channel.id)
        if(trackingLevel == 'NONE'):
            print("Ignoring message")
            return
        elif(trackingLevel == 'LIMITED'):
            if(channelTrackingLevel == 'FULL_TRACKING'):
                print("Storing Message")
                self.storeMessage(message.author.id, message.content)
                return
            else:
                print("Ignoring message")
                return
        elif(trackingLevel == 'FULL'):
            if(channelTrackingLevel == 'NOT_TRACKED'):
                print("Ignoring message")
                return
            else:
                print("Storing Message")
                self.storeMessage(message.author.id, message.content)
                return
        else:
            print("error tracking level not referenced")

    def storeMessage(self, userId, messageContent):
        query = {'userId': userId}
        operation = {'$push': {'messages': messageContent}}
        self.tracked_col.update(query, operation)
        return

    # returns array of all users messages
    def getMessages(self, userId):
        query = {'userId': userId}
        user = self.tracked_col.find(query)
        return user[0]['messages']

    # if channel doesn't exist, return limted tracking
    def channelTracking(self, channelId):
        if(self.channelExists(channelId)):
            query = {'channelId': channelId}
            channel = self.channels_col.find(query)
            return channel[0]['trackingLevel']
        return 'LIMITED_TRACKING'

    def updateChannelTracking(self, channelId, trackingLevel):
        if self.channelExists(channelId):
            print("channel exists, updating record")
            query = {"channelId": channelId}
            tracking = {"$set": {"trackingLevel": trackingLevel}}
            self.channels_col.update_one(query, tracking)
        else:
            print("channel doesnt exist, creating record")
            channel = {"trackingLevel": trackingLevel, "channelId": channelId}
            self.channels_col.insert_one(channel)

    def channelExists(self, channelId):
        query = {"channelId": channelId}
        channel = self.channels_col.find(query)
        if channel.count() == 1:
            return True
        elif channel.count() == 0:
            return False
        print("Error")

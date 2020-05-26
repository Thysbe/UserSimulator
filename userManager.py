import pymongo
from pip._internal.utils.misc import enum
from pymongo import MongoClient


class UserManager:

    def __init__(self):
        self.my_client: MongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.my_client["discordText"]
        self.tracked_col = self.mydb["trackedUsers"]
        self.messages_col = self.mydb["messages"]
        self.user_query = lambda name, disc: {"username": name + "#" + disc}
        self.user_t_query = lambda name, disc, t: {"username": name + "#" + disc, "tracking": t}
        self.set_tracking = lambda track_b: {"$set": {"tracking": track_b}}

        print(self.my_client.list_database_names())

    def create_user(self, author, t_bool) -> None:
        user_enum: enumerate = enum(
            {
            "username": author.name + '#' + author.discriminator,
            "tracking": t_bool,
            "userId": author.id
             }
        )
        self.tracked_col.insert_one(user_enum)

    def update_tracking(self, author, t_bool: bool) -> None:
        if t_bool:
            print('turning on message tracking')
        elif not t_bool:
            print('turning off message tracking')
        query = self.user_query(author.name, author.discriminator)
        tracking: dict = self.set_tracking(t_bool)
        self.tracked_col.update_one(query, tracking)

    def startListening(self, author, p_level: int) -> None:
        if p_level == 1:

        elif p_level == 2:
            self

        elif p_level == 3:
            if self.userExists(author):
                self.update_tracking(True)
            else:
                self.create_user(self, author, True)

    def stopListening(self, author) -> None:
        if self.userExists(author):
            self.update_tracking(False)
        else:
            self.create_user(author, False)

    def userExists(self, author) -> bool:
        query = self.user_query(author.name, author.discriminator)
        user = self.tracked_col.find(query)
        if user.count() == 1:
            return True
        elif user.count() == 0:
            return False
        print("Error")

    def userIsTracking(self, author) -> bool:
        query = self.user_t_query(author.name, author.discriminaotr, True)
        user = self.tracked_col.find(query)
        if user.count() == 1:
            return True
        else:
            return False

    def trackMessage(self, message) -> None:
        if self.userIsTracking(message.author):
            print("Storing message")
            username = message.author.name + '#' + message.author.discriminator
            # {'$push': {"messages": message.content}})
            self.tracked_col.update({'username': username}, {'$push': {'messages': message.content}})
        else:
            print("Ignoring message")

    def getMessages(self, author) -> str:
        query = self.user_query(author.name, author.discriminator)
        user = self.tracked_col.find(query)
        for message in user[0].messages:
            print(message)
        return user[0].messages

import pymongo
from pymongo import MongoClient


class UserManager:

    def __init__(self):
        self.my_client: MongoClient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.my_client["discordText"]
        self.tracked_col = self.mydb["trackedUsers"]
        self.messages_col = self.mydb["messages"]
        self.user_query = lambda name, disc: {"username": name + "#" + disc}
        # t_l = tracking level
        self.user_t_query = lambda name, disc, t_l, t: {"username": name + "#" + disc, str(t_l): t}
        self.set_tracking = lambda t_l, track_b: {"$set": {t_l: track_b}}
        self.tracking_level = ["tracking-low", "tracking-mid", "tracking"]

        print(self.my_client.list_database_names())

    def create_user(self, author, all_bool: bool, l_bool: bool, m_bool: bool) -> None:
        user_dict = {
            "username": author.name + '#' + author.discriminator,
            "tracking": all_bool,
            "userId": author.id,
            "tracking_mid": m_bool,
            "tracking_low": l_bool,

        }
        self.tracked_col.insert_one(user_dict)

    def update_tracking(self, author, t_l: str, t_bool: bool) -> None:
        if t_bool:
            print('turning on message tracking')
        elif not t_bool:
            print('turning off message tracking')
        query = self.user_query(author.name, author.discriminator)
        tracking: dict = self.set_tracking(t_l, track_b=t_bool)
        self.tracked_col.update_one(query, tracking)

    def startListening(self, author, p_level) -> None:
        if 1 == int(p_level):
            if self.userExists(author):
                self.update_tracking(author,
                                     t_l="tracking_mid",
                                     t_bool=False
                                     )
                self.update_tracking(author,
                                     t_l="tracking_low",
                                     t_bool=True
                                     )
                self.update_tracking(author,
                                     t_l="tracking",
                                     t_bool=False
                                     )
            else:
                self.create_user(author,
                                 all_bool=False,
                                 m_bool=False,
                                 l_bool=True
                                 )

        if 2 == int(p_level):
            # we want lot and test to track messages
            if self.userExists(author):
                self.update_tracking(author,
                                     t_l="tracking_mid",
                                     t_bool=True
                                     )
                self.update_tracking(author,
                                     t_l="tracking_low",
                                     t_bool=False
                                     )
                self.update_tracking(author,
                                     t_l="tracking",
                                     t_bool=False
                                     )

            else:
                self.create_user(author,
                                 all_bool=False,
                                 m_bool=True,
                                 l_bool=False)
        if 3 == int(p_level):
            # we want to track all messages
            if self.userExists(author):
                self.update_tracking(author,
                                     t_l="tracking_mid",
                                     t_bool=False
                                     )
                self.update_tracking(author,
                                     t_l="tracking_low",
                                     t_bool=False
                                     )
                self.update_tracking(author,
                                     t_l="tracking",
                                     t_bool=True
                                     )
            else:
                self.create_user(author,
                                 all_bool=True,
                                 m_bool=False,
                                 l_bool=False)

    def stopListening(self, author) -> None:
        if self.userExists(author):
            for level in self.tracking_level:
            self.update_tracking(author,
                                 t_l=level,
                                 t_bool=False
                                 )
        else:
            self.create_user(author,
                             all_bool=False,
                             m_bool=False,
                             l_bool=False
                             )

    def userExists(self, author) -> bool:
        query = self.user_query(author.name, author.discriminator)
        user = self.tracked_col.find(query)
        if user.count() == 1:
            return True
        elif user.count() == 0:
            return False
        print("Error")

    def userIsTracking(self, author, tracking_level) -> bool:
        query = self.user_t_query(author.name,
                                  author.discriminator,
                                  tracking_level, True)
        user = self.tracked_col.find(query)
        if user.count() == 1:
            return True
        else:
            return False

    def trackMessage(self, message) -> None:
        for level in self.tracking_level:
            if self.userIsTracking(message.author, level):
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

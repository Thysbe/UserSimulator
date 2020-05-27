from enum import Enum


class AuthorEnum(Enum):
    def __init__(self, author, t_bool: bool):
        self.author = author
        self.username = author.name + '#' + author.discriminator
        self.tracking = t_bool
        self.userId = author.id

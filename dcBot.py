import discord
from userManager import UserManager
from simulator import simulateUser
from messageUtil import parseTaggedUser
import env


def runBot():
    TOKEN = env.TOKEN()
    user_manager = UserManager()

    client = discord.Client()

    @client.event
    async def on_message(message):
        # we do not want the bot to reply to itself
        if message.author == client.user:
            return
        elif message.content.startswith('!hello'):
            await message.channel.send('I heard you!')
        elif message.content.startswith('!startListening'):
            # for console debugging we will neeed to ask user
            level = input("Please input a level of participation low 1-3 high")
            p = level
            user_manager.startListening(message.author, p_level=p)
        elif message.content.startswith('!stopListening'):
            user_manager.stopListening(message.author)
        elif message.content.startswith('!simulate'):
            simulatedUser = parseTaggedUser(message)
            messages = user_manager.getMessages(simulatedUser)
            simulatedMessage = simulateUser(messages)
            await message.channel.send(simulatedMessage)
        else:
            user_manager.trackMessage(message)

    @client.event
    async def on_ready():
        print('Logged in as')

        print(client.user.name)
        print(client.user.id)
        print('------')

    client.run(TOKEN)

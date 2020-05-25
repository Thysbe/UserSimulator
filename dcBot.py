import discord
from userManager import UserManager
from simulator import Simulator
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
            user_manager.startListening(message.author)
        elif message.content.startswith('!stopListening'):
            user_manager.stopListening(message.author)
        elif message.content.startswith('!simulate'):
            simulatedUser = parseTaggedUser(message.content)
            simulatedMessage = Simulator.simulateUser(simulatedUser)
            await message.channel.send(simulatedMessage)
        elif message.content.startswith('!testGet'):
            user_manager.getMessages(message.author)
        else:
            user_manager.trackMessage(message)

    @client.event
    async def on_ready():
        print('Logged in as')

        print(client.user.name)
        print(client.user.id)
        print('------')

    client.run(TOKEN)


def parseTaggedUser(messageContent):
    print(messageContent)

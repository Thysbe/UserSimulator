import discord
import userManager
import env

def init():
    userManager.mongoInit()

def runBot():
    TOKEN = env.TOKEN()

    client = discord.Client()

    @client.event
    async def on_message(message):
        # we do not want the bot to reply to itself
        if message.author == client.user:
            return
        elif message.content.startswith('!hello'):
            await message.channel.send('I heard you!')
        elif message.content.startswith('!startListening'):
            userManager.startListening(message.author)
        elif message.content.startswith('!stopListening'):
            userManager.stopListening(message.author)
        elif message.content.startswith('!simulate'):
            simulatedUser = parseTaggedUser(message.content)
            # userManager.getMessages(simulatedUser)
        else:
            userManager.trackMessage(message)

    @client.event
    async def on_ready():
        print('Logged in as')

        print(client.user.name)
        print(client.user.id)
        print('------')

    client.run(TOKEN)

def parseTaggedUser(messageContent):
    print(messageContent)

import discord
from userManager import UserManager
from simulator import simulateUser
from messageUtil import parseTaggedUser
import env


def runBot():
    TOKEN = env.TOKEN()
    user_manager = UserManager()

    client = discord.Client()

    async def adminControls(message):
        if message.content.startswith('!trackUser'):
            print("Turning on full tracking")
            taggedUserId = parseTaggedUser(message.content)
            print('tagged userId')
            print(taggedUserId)
            user_manager.updateTrackingLevel(
                taggedUserId, 'FULL', message.author.name)
            return
        if message.content.startswith('!ignoreChannel'):
            print("Ignoring channel")
            user_manager.updateChannelTracking(
                message.channel.id, 'NOT_TRACKED'
            )
            await message.channel.send('Ignoring channel')
            return
        if message.content.startswith('!listenToChannel'):
            print("Turning on full channel tracking")
            user_manager.updateChannelTracking(
                message.channel.id, 'FULL_TRACKING'
            )
            await message.channel.send('Tracking channel')
            return
        if message.content.startswith('!resetChannel'):
            print("Setting channel tracking to default")
            user_manager.updateChannelTracking(
                message.channel.id, 'LIMITED_TRACKING'
            )
            await message.channel.send('Tracking channel')
            return

    @client.event
    async def on_message(message):
        # we do not want the bot to reply to itself
        if message.author == client.user:
            return
        elif message.author.id == (165683808685785088):  # Thysbe or eeyeseeu
            await adminControls(message)
        if message.content.startswith('!hello'):
            await message.channel.send('I heard you!')
        elif message.content.startswith('!startListening'):
            user_manager.updateTrackingLevel(
                message.author.id, 'LIMITED', message.author.name)
            await message.channel.send('limited listening on')
        elif message.content.startswith('!stopListening'):
            user_manager.updateTrackingLevel(
                message.author.id, 'NONE', message.author.name)
            await message.channel.send('no longer tracking')
        elif message.content.startswith('!simulate'):
            simulatedUser = parseTaggedUser(message.content)
            messages = user_manager.getMessages(simulatedUser)
            username = user_manager.getUserName(simulatedUser)
            simulatedMessage = simulateUser(messages)
            await message.channel.send(username + "Bot says: " + simulatedMessage)
        # ignores admin control messages
        elif message.content.startswith('!'):
            return
        else:
            user_manager.trackMessage(message)

    @client.event
    async def on_ready():
        print('Logged in as')

        print(client.user.name)
        print(client.user.id)
        print('------')

    client.run(TOKEN)

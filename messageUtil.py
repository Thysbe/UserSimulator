def parseTaggedUser(message):
    print('Message ')
    parseString = message.content
    parsedString = parseString.split('@')
    parsedString = parsedString[1]
    parsedString = parsedString.split('!')
    parsedString = parsedString[1]
    parsedString = parsedString.split('>')
    parsedString = parsedString[0]
    return parsedString

def parseTaggedUser(message):
    parseString = message
    parsedString = parseString.split('@')
    parsedString = parsedString[1]
    parsedString = parsedString.split('!')
    parsedString = parsedString[1]
    parsedString = parsedString.split('>')
    parsedString = parsedString[0]
    return int(parsedString)

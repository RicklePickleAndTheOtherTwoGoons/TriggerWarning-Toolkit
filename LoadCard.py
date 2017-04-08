#LoadCard loads the specified decks 
import csv
import requests

class card:                                     #card object
    def __init__(self):                          
        self.text = ""                          #card text (required)
        self.draw = 0                           #draw value if applicable
        self.pick = 0                           #pick value if applicable
        self.cType = "ERROR"                         #card type (required)
with open("MainCH.tsv") as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter="\t")
    cardSet = [] 
    for row in tsvreader:
        if row[14] == "v1.7":
            newCard = card()
            if row[0] == "Prompt":                  #Prompt
                newCard.text = row[1]
                newCard.cType = "black"
                if row[2] != "":
                    if ", " in row[2]:              #Prompt with Draw and Pick
                        newCard.draw = row[2][5]
                        newCard.pick = row[2][13]
                    elif "DRAW" in row[2]:          #Prompt with Draw
                        newCard.draw = row[2][5]
                    elif "PICK" in row[2]:          #Prompt with Pick
                        newCard.pick = row[2][5]
                cardSet.append(newCard)
            elif "Response" in row[0]:                #Response 
                newCard.text = row[1]
                newCard.cType = "white"
                cardSet.append(newCard)
    #create card set and get ID
        r = requests.post("https://triggerwarning.herokuapp.com/api/cardsets", data = {'name': 'BasePack'}, files = dict(foo = 'bar'))
        response = (r.text).split('id":"')
        cardSetID = response[1][0:24]
    #print(cardSetID)
        for p in cardSet:                           #iterate through all cards
            data = {
                'text' : p.text,
                'draw' : p.draw,
                'pick' : p.pick,
                'type' : p.cType}
            re = requests.post("https://triggerwarning.herokuapp.com/api/cards", data = data, files = dict(foo = 'bar')) 
            response = (re.text).split('id":"')
            cardID = response[1][0:24]
            #print(cardID)
            url = "https://triggerwarning.herokuapp.com/api/cardsets/" + cardSetID + "/add/" + cardID
            requests.get(url)
        #returns cardset object
        #save id from cardset
        #for each card create card to api cards and add card to cardset
tsvfile.close()

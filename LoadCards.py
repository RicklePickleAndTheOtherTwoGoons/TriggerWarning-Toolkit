#!/usr/local/bin/python
#LoadCard loads Main Deck given its filename 
import csv
import requests
import sys
class card:                                     #card object
    def __init__(self):                          
        self.text = ""                          #card text (required)
        self.draw = 0                           #draw value if applicable
        self.pick = 0                           #pick value if applicable
        self.cType = "ERROR"                         #card type (required)
filenames = str(sys.argv[1])
if ".tsv" in filenames:
    with open(filenames) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        cardSet = [] 
        for row in tsvreader:                        #iterates through lines
            if "Prompt" in row[0]:                   #is prompt card
                if "v1.7" in row[14]:                #check current US version
                    newCard = card()                 #create card object
                    newCard.text = row[1]            #text in second column
                    newCard.cType = "black"          #prompts are black cards
                    if row[2] != "":                 #if has pick or draw
                        if ", " in row[2]:              #Prompt with Draw and Pick
                            newCard.draw = row[2][5]
                            newCard.pick = row[2][13]
                        elif "DRAW" in row[2]:          #Prompt with Draw
                            newCard.draw = row[2][5]
                        elif "PICK" in row[2]:          #Prompt with Pick
                            newCard.pick = row[2][5]
                    cardSet.append(newCard)
            elif "Response" in row[0]:                #Response 
                if row[14] == "v1.7":
                    newCard = card()
                    newCard.text = row[1]           #text in second column
                    newCard.cType = "white"         #responses are white    
                    cardSet.append(newCard)         #add card to list
    #create card set and get ID
        print("Loading in ", len(cardSet), "cards.")                         #550
        r = requests.post("https://triggerwarning.herokuapp.com/api/cardsets", data = {'name': filenames}, files = dict(foo = 'bar'))
        response = (r.text).split('id":"')
        cardSetID = response[1][0:24]
        for p in cardSet:                           #iterate through all cards
            data = {                                #set variables for upload
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
else:
    print("ERROR: file has wrong type or was not provided please download a\n\t .tsv of the main deck and pass it as the argument")


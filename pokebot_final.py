from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
from tkinter.ttk import Treeview
from tkinter import filedialog

from PIL import ImageTk,Image
import json
import os
import pandas as pd
import requests
from io import BytesIO

'''

--------------------
PokeBot Deck Builder
--------------------
By:
Muhammad Akbar Zanucky - 2301934594
Ignatius Christanto - 2301918224 
Raditya Rahmaldi Triputra - 2301948492
Hocky Harijanto - 2301848640

'''

setList = {"smp": "Sun & Moon Black Star Promos.json",
       "sm1": "Sun & Moon.json",
       "sm2": "Guardians Rising.json",
       "sm3": "Burning Shadows.json",
       "sm35": "Shining Legends.json",
       "sm4": "Crimson Invasion.json",
       "sm5": "Ultra Prism.json",
       "sm6": "Forbidden Light.json",
       "sm7": "Celestial Storm.json",
       "sm75": "Dragon Majesty.json",
       "sm8": "Lost Thunder.json",
       "sm9": "Team Up.json",
       "sm10": "Unbroken Bonds.json",
       "sm11": "Unified Minds.json",
       "sm115": "Hidden Fates.json",
       "sm12": "Cosmic Eclipse.json",
       "det1": "Detective Pikachu.json",
       "swshp": "SWSH Black Star Promos.json",
       "swsh1": "Sword & Shield.json",
       "swsh2": "Rebel Clash.json",
       "swsh3": "Darkness Ablaze.json",
       "swsh35": "Champions Path.json",
       "swsh4": "Vivid Voltage.json"}

energyList = {  "Grass": "sm1-164",
                "Fire": "sm1-165",
                "Water": "sm1-166",
                "Lightning": "sm1-167",
                "Psychic": "sm1-168",
                "Fighting": "sm1-169",
                "Darkness": "sm1-170",
                "Metal": "sm1-171",
                "Fairy": "sm1-172"}

dataBase = []
ndataBase = []
pokeList = []
pokeListNum = []
pokeListPoke = []
pokeListTrainer = [[], [], []]
pokeListEnergy = []

img_url = "https://upload.wikimedia.org/wikipedia/en/3/3b/Pokemon_Trading_Card_Game_cardback.jpg"
currDir = os.getcwd()

#console log print
def printInfo():
    print()
    print("Main List:", pokeList)
    print("Qty List:", pokeListNum)
    print("Poke List:", pokeListPoke)
    print("Trainer List:", pokeListTrainer)
    print("Energy List:", pokeListEnergy)

#update backend list
def updateList(card_id, num):
    global pokeList, pokeListNum, pokeListPoke, pokeListTrainer, pokeListEnergy, setList
    # print("Updating for:", card_id)
    dump = card_id.split('-')
    f = open("json/cards/{0}".format(setList[dump[0]]))
    db = json.load(f)
    for i in db:
        if i["id"] == card_id:
            cType = fixName(i["supertype"])
            if cType == "Trainer" or cType == "Energy":
                sType = fixName(i["subtype"])
                if sType == "Pokemon Tool":
                    sType = "Item"
                if sType == "Basic":
                    sType = "Energy"
                updateSpecificList(card_id, sType, num)
            else:
                updateSpecificList(card_id, cType, num)

#get index from frontend
def getIndex(card_id):
    global pokeList, pokeListNum, pokeListPoke, pokeListTrainer, pokeListEnergy, setList
    x = card_id + '#' + getCardName(card_id)
    if x in pokeListPoke:
        return pokeListPoke.index(x)
    elif x in pokeListTrainer:
        return pokeListTrainer.index(x) + len(pokeListPoke)
    elif x in pokeListEnergy:
        return pokeListEnergy.index(x) + len(pokeListPoke) + len(pokeListTrainer)
    else:
        return 0

#update specific backend list
def updateSpecificList(card_id, type, num):
    global pokeList, pokeListPoke, pokeListTrainer, pokeListEnergy
    nCard = fixName(getCardName(card_id))
    x = card_id + '#' + nCard
    num = int(num)
    if x not in pokeList:
        pokeList.append(x)
        if "◇" in nCard:
            if num > 1:
                num = 1
        pokeListNum.append(num)
        if type == "Pokemon":
            pokeListPoke.append(x)
        elif type == "Supporter":
            pokeListTrainer[0].append(x)
        elif type == "Item":
            pokeListTrainer[1].append(x)
        elif type == "Stadium":
            pokeListTrainer[2].append(x)
        elif type == "Energy" or type == "Special":
            pokeListEnergy.append(x)
    else:
        #update entry
        id1 = pokeList.index(x)
        if num > 0:
            #add card, energy exception >4
            pokeListNum[id1] += num
            if type != "Energy":
                if pokeListNum[id1] > 4:
                    pokeListNum[id1] = 4
            if "◇" in nCard:
                if pokeListNum[id1] > 1:
                    pokeListNum[id1] = 1

        elif num < 0:
            #remove card, must be -1
            if pokeListNum[id1] > 1:
                pokeListNum[id1] += num
            else:
                if type == "Pokemon":
                    id2 = pokeListPoke.index(x)
                    pokeListPoke.pop(id2)
                elif type == "Supporter":
                    id2 = pokeListTrainer[0].index(x)
                    pokeListTrainer[0].pop(id2)
                elif type == "Item":
                    id2 = pokeListTrainer[1].index(x)
                    pokeListTrainer[1].pop(id2)
                elif type == "Stadium":
                    id2 = pokeListTrainer[2].index(x)
                    pokeListTrainer[2].pop(id2)
                elif type == "Energy" or type == "Special":
                    id2 = pokeListEnergy.index(x)
                    pokeListEnergy.pop(id2)
                pokeList.pop(id1)
                pokeListNum.pop(id1)
    refreshMyDeck()

#refresh frontend
def refreshMyDeck():
    global pokeList, pokeListNum, pokeListPoke, pokeListTrainer, pokeListEnergy
    def updateTreeView():
        counter = 1
        for i in range(len(pokeListPoke)):
            id1 = pokeList.index(pokeListPoke[i])
            dump = pokeListPoke[i].split('#')
            cid = dump[0]
            cName = getCardName(cid)
            qty = pokeListNum[id1]
            my_deck.insert(parent='', index=END, iid=counter, text="", values=(cid, cName, qty))
            counter += 1
        for i in range(len(pokeListTrainer[0])):
            id1 = pokeList.index(pokeListTrainer[0][i])
            dump = pokeListTrainer[0][i].split('#')
            cid = dump[0]
            cName = getCardName(cid)
            qty = pokeListNum[id1]
            my_deck.insert(parent='', index=END, iid=counter, text="", values=(cid, cName, qty))
            counter += 1
        for i in range(len(pokeListTrainer[1])):
            id1 = pokeList.index(pokeListTrainer[1][i])
            dump = pokeListTrainer[1][i].split('#')
            cid = dump[0]
            cName = getCardName(cid)
            qty = pokeListNum[id1]
            my_deck.insert(parent='', index=END, iid=counter, text="", values=(cid, cName, qty))
            counter += 1
        for i in range(len(pokeListTrainer[2])):
            id1 = pokeList.index(pokeListTrainer[2][i])
            dump = pokeListTrainer[2][i].split('#')
            cid = dump[0]
            cName = getCardName(cid)
            qty = pokeListNum[id1]
            my_deck.insert(parent='', index=END, iid=counter, text="", values=(cid, cName, qty))
            counter += 1
        for i in range(len(pokeListEnergy)):
            id1 = pokeList.index(pokeListEnergy[i])
            dump = pokeListEnergy[i].split('#')
            cid = dump[0]
            cName = getCardName(cid)
            qty = pokeListNum[id1]
            my_deck.insert(parent='', index=END, iid=counter, text="", values=(cid, cName, qty))
            counter += 1
    temp = str()
    if my_deck.focus():
        foc = my_deck.focus()
        dvalue = my_deck.item(foc, 'values')
        temp = dvalue[0]
    for i in my_deck.get_children():
        my_deck.delete(i)
    updateTreeView()
    if temp:
        if len(pokeList) > 0:
            idx = getIndex(temp) + 1
            my_deck.focus(idx)
            my_deck.selection_set(idx)

#top counter
def updateDeckCount(newV):
    deckCount = sum(pokeListNum)
    if deckCount > 60:
        Label2.config(fg='red')
    else:
        Label2.config(fg='black')
    newCount = '{deckNum}/60'.format(deckNum = deckCount)
    newV.set(newCount)
    return deckCount

#fix name from json
def fixName(name):
    name = name.replace("Ã©", "e")
    name = name.replace("â€”", "-")
    name = name.replace("â—‡", "◇")
    name = name.replace("PRISM STAR", "◇")
    return name

#file to listbox
def inputDB(poke):
    global setList
    files = ['sm1', 'sm2', 'sm3', 'sm35', 'sm4', 'sm5', 'sm6', 'sm7', 'sm75', 'sm8', 'sm9', 'sm10',
             'sm11', 'sm115', 'sm12', 'smp', 'det1', 'swsh1', 'swsh2', 'swsh3', 'swsh35', 'swsh4', 'swshp']
    for x in files:
        f = open('json/cards/{0}'.format(setList[x]))
        data = json.load(f)
        for i in data:
            dataid = i["id"]
            dataname = fixName(i["name"])
            ndataBase.append([dataid, dataname])
        f.close()

    count = 0
    for record in ndataBase:
        my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1]))
        count += 1

#search card menu
def searchCard(event=None):
    simg_url = "https://upload.wikimedia.org/wikipedia/en/3/3b/Pokemon_Trading_Card_Game_cardback.jpg"
    top = Toplevel()
    top.title("Search Results")
    top.iconbitmap("database/rsc/pokebot.ico")

    searchResult = []
    searchInput = search.get()
    toSearch = searchInput.lower()
    for i in range(len(ndataBase)):
        if toSearch in ndataBase[i][0].lower():
            searchResult.append(ndataBase[i])
        elif toSearch in ndataBase[i][1].lower():
            searchResult.append(ndataBase[i])
    print(searchResult)

    def searchSelect():
        global inputSearch
        e.delete(0, END)
        curItem = searchTree.focus()
        dvalue = searchTree.item(curItem, 'values')
        if dvalue == '':
            print("Nothing is selected!")
            popupmsg()
        else:
            value = dvalue[0]
            updateList(value, 1)
            printInfo()
            updateDeckCount(countDeck)
            recBox()

        print(pokeList)

    def updatePic(event):
        curItem = searchTree.focus()
        dvalue = searchTree.item(curItem, 'values')
        print(dvalue)
        nvalue = dvalue[0]
        dump = nvalue.split('-')
        global setList
        f = open("json/cards/{0}".format(setList[dump[0]]))
        db = json.load(f)
        simg_url = str()
        for i in db:
            if i["id"] == nvalue:
                simg_url = i["imageUrl"]
        f.close()
        print(simg_url)

        response = requests.get(simg_url)
        img_data = response.content
        img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)).resize((240, 336), Image.ANTIALIAS))
        spokePic.config(image=img)
        spokePic.image = img
        spokePic.update()

    response = requests.get(simg_url)
    simg_data = response.content
    simg = ImageTk.PhotoImage(Image.open(BytesIO(simg_data)).resize((240, 336), Image.ANTIALIAS))
    spokePic = Label(top, image=simg)
    print(simg_url)
    spokePic.grid(row=0, column=1)
    spokePic.config(image=simg)
    spokePic.image = simg
    spokePic.update()


    frms = Frame(top)
    frms.grid(row=0, column=0, padx=8, pady=8)

    searchTree: Treeview = ttk.Treeview(frms, height=20)
    searchTree['columns'] = ("ID", "Name")
    searchTree.bind('<Double-1>', updatePic)

    searchTree.column('#0', width=0, minwidth=0)
    searchTree.column('ID', anchor=W, width=100)
    searchTree.column("Name", anchor=W, width=200)

    searchTree.heading("#0", text="", anchor=W)
    searchTree.heading("ID", text="ID", anchor=W)
    searchTree.heading("Name", text="Name", anchor=CENTER)

    searchTree.pack(side='left', fill='y')

    sbls = Scrollbar(frms, orient="vertical", width=20)
    sbls.pack(side='right', fill='y')
    searchTree.configure(yscrollcommand=sbls.set)
    sbls.configure(command=searchTree.yview)

    insButt = Button(top, text='Insert Card', command=searchSelect).grid(row=1, column=0, pady=8)

    count=0
    for record in searchResult:
        searchTree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1]))
        count += 1

#get name from id (json)
def getCardName(card_id): #Converting Card ID to NAME
    global setList
    # print("Searching name:", card_id)
    dump = card_id.split('-')
    # print("opening", setList[dump[0]])
    f = open("json/cards/{0}".format(setList[dump[0]]))
    db = json.load(f)
    for i in db:
        if i["id"] == card_id:
            i["name"] = fixName(i["name"])
            return i["name"]
    f.close()

#get recommend, one card
def getRec(card_id, deck):
    f = open("database/rsc/supportLayer.txt")
    supportLayer = []
    for lines in f:
        temp = lines.split()
        supportLayer.append(temp[0])
    f.close()
    cid = card_id.split('#')
    nCid = cid[0]
    if nCid in supportLayer:
        print("Excluding", getCardName(nCid))
        return [-1, "None"]
    else:
        fname = "database/{0}.csv".format(nCid)
        if not os.path.exists(fname):
            return [-1, "None"]
        df = pd.read_csv(fname)
        high = 0
        rec = str()
        rate = int()
        for index in df.index:
            freq = int(df.loc[index]["Frequency"])
            div = int(df.loc[index]["Distribution"])
            rate = freq / div
            thiscard = df.loc[index]["ID"] + '#' + getCardName(df.loc[index]["ID"])
            if thiscard in deck:
                continue
            elif rate > high:
                rec = df.loc[index]["ID"]
                high = rate
        if not rec:
            rate = -1
            rec = "None"
        card = [rate, rec]
        return card

#get recommend from decklist
def fullRecommend(deck): #Get recommendation
    if len(deck) == 0:
        return "None"
    rec = []
    for cards in deck:
        rec.append(getRec(cards, deck))
    high = 0
    card = str()
    for i in range(len(rec)):
        if rec[i][0] > high:
            card = rec[i][1]
            high = rec[i][0]
    if not card:
        card = "None"
    return card

#recommend box (right)
def recBox():
    e.config(state=NORMAL)
    e.delete(0, END)
    rec = fullRecommend(pokeList)
    if rec != "None":
        x = getCardName(rec)
        print("Current recommendation:", rec, x)
        e.insert(0, x)
        e.config(state=DISABLED)
    else:
        e.insert(0, "No Recommendation")
        print("No recommendation")
        e.config(state=DISABLED)

#get selected card info - listbox
def CurSelect(event):
    global img_url
    global setList
    curItem = my_tree.focus()
    dvalue = my_tree.item(curItem, 'values')
    nvalue = dvalue[0]
    dump = nvalue.split('-')
    f = open("json/cards/{0}".format(setList[dump[0]]))
    db = json.load(f)
    for i in db:
        if i["id"] == nvalue:
            img_url = i["imageUrl"]
    f.close()
    print(img_url)

    response = requests.get(img_url)
    img_data = response.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)).resize((240, 336), Image.ANTIALIAS))
    pokePic.config(image=img)
    pokePic.image=img
    pokePic.update()

#get selected card info - deck
def CurSelectDeck(event):
    global img_url
    global setList
    curItem = my_deck.focus()
    dvalue = my_deck.item(curItem, 'values')
    nvalue = dvalue[0]
    dump = nvalue.split('-')
    f = open("json/cards/{0}".format(setList[dump[0]]))
    db = json.load(f)
    for i in db:
        if i["id"] == nvalue:
            img_url = i["imageUrl"]
    f.close()
    print('URL : ', img_url)

    response = requests.get(img_url)
    img_data = response.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)).resize((240, 336), Image.ANTIALIAS))
    pokePic.config(image=img)
    pokePic.image = img
    pokePic.update()

#BUTTONS

#add card from searchbox
def addCardSearch():
    curItem = my_tree.focus()
    dvalue = my_tree.item(curItem, 'values')
    if dvalue == '':
        print("Nothing is selected!")
        popupmsg()
    else:
        value = dvalue[0]
        updateList(value, 1)

        printInfo()
        updateDeckCount(countDeck)
        recBox()

#add card from recommendbox
def addCardRecom():
    value = fullRecommend(pokeList)
    if value != 'None':
        qty = spbox.get()
        updateList(value, qty)
        printInfo()
        updateDeckCount(countDeck)
        recBox()
    else:
        mb.showinfo("!", "No Recommended Card!")
        print("no card")

#add card from add trainer
def addCardSup():
    global setList
    timg_url = "https://upload.wikimedia.org/wikipedia/en/3/3b/Pokemon_Trading_Card_Game_cardback.jpg"

    path = 'database/rsc/trainer/'

    trainerSet = []
    trainerSetQty = []

    trainerSetCardList = []
    trainerSetCardQty = []
    for fname in os.listdir(path):
        file = fname.replace(".txt", "")
        trainerSet.append(file)
        setlist = []
        setqty = []
        total = 0
        f = open("{0}{1}".format(path, fname))
        for lines in f:
            lines = lines.strip()
            qty = int(lines[0])
            card = lines[3::]
            card_id = card.split('#')
            setlist.append(card_id[1])
            setqty.append(qty)
            total += qty
        trainerSetCardList.append(setlist)
        trainerSetCardQty.append(setqty)
        trainerSetQty.append(total)

    def CurSelectTrainer(event):  # Get selected card info
        global timg_url
        curItem = my_deckT.focus()
        dvalue = my_deckT.item(curItem, 'values')
        nvalue = dvalue[0]
        dump = nvalue.split('-')
        f = open("json/cards/{0}".format(setList[dump[0]]))
        db = json.load(f)
        for i in db:
            if i["id"] == nvalue:
                timg_url = i["imageUrl"]
        f.close()
        print('URL : ', timg_url)

        responseT = requests.get(timg_url)
        timg_data = responseT.content
        timg = ImageTk.PhotoImage(Image.open(BytesIO(timg_data)).resize((240, 336), Image.ANTIALIAS))
        tpokePic = Label(trainer, image=timg)
        tpokePic.grid(row=0, column=8, columnspan=2, rowspan=3, padx=8, pady=8)
        tpokePic.config(image=timg)
        tpokePic.image = timg
        tpokePic.update()

    def CurSelectTrainerSet(event):  # Get selected card info
        curItem = my_treeT.focus()
        id1 = int(curItem)
        for i in my_deckT.get_children():
            my_deckT.delete(i)
        for i in range(len(trainerSetCardList[id1])):
            cid = trainerSetCardList[id1][i]
            nCard = getCardName(cid)
            qty = trainerSetCardQty[id1][i]
            my_deckT.insert(parent='', index=END, iid=i,
                            text="", values=(cid, nCard, qty))

    def insertTrainerToDeck():
        for i in my_deckT.get_children():
            dump = my_deckT.item(i, 'values')
            value = dump[0]
            tqty = int(dump[2])
            updateList(value, tqty)
            printInfo()
        recBox()
        updateDeckCount(countDeck)
        trainer.destroy()

    trainer = Toplevel()
    trainer.title("Trainer")
    trainer.iconbitmap("database/rsc/pokebot.ico")

    mainSize()


    logo = Label(trainer, text='Add Pre-made Sets')  # LOGO
    logo.grid(row=0, column=0, padx=8, sticky='s')

    frm = Frame(trainer)
    frm.grid(row=2, column=0, rowspan=5, padx=8, pady=8)

    my_treeT: Treeview = ttk.Treeview(frm, height=15)
    my_treeT['columns'] = ("Trainer Set", "Qty")
    my_treeT.bind('<Double-1>', CurSelectTrainerSet)

    my_treeT.column('#0', width=0, minwidth=0)
    my_treeT.column('Trainer Set', anchor=W, width=180)
    my_treeT.column("Qty", anchor=CENTER, width=60)

    my_treeT.heading("#0", text="", anchor=W)
    my_treeT.heading("Trainer Set", text="Trainer Set", anchor=W)
    my_treeT.heading("Qty", text="Qty", anchor=CENTER)

    my_treeT.pack(side='left', fill='y')

    Label1 = Label(trainer, text='Trainer list:')  # explanatory
    Label1.grid(row=0, column=4, padx=8, sticky='s')

    frm1 = Frame(trainer)
    frm1.grid(row=2, column=4, rowspan=5, padx=8, pady=8)

    my_deckT = ttk.Treeview(frm1, height=15)
    my_deckT['columns'] = ("ID", "Name", "Qty")
    my_deckT.bind('<Double-1>', CurSelectTrainer)

    my_deckT.column('#0', width=0, minwidth=0)
    my_deckT.column('ID', anchor=W, width=80)
    my_deckT.column("Name", anchor=W, width=180)
    my_deckT.column("Qty", anchor=W, width=50)

    my_deckT.heading("#0", text="", anchor=W)
    my_deckT.heading("ID", text="ID", anchor=W)
    my_deckT.heading("Name", text="Name", anchor=W)
    my_deckT.heading("Qty", text="Qty", anchor=W)

    my_deckT.pack(side='left', fill='y')

    responseT = requests.get(timg_url)
    timg_data = responseT.content
    timg = ImageTk.PhotoImage(Image.open(BytesIO(timg_data)).resize((240, 336), Image.ANTIALIAS))
    tpokePic = Label(trainer, image=timg)
    tpokePic.grid(row=0, column=8, columnspan=2, rowspan=3, padx=8, pady=8)
    tpokePic.config(image=timg)
    tpokePic.image = timg
    tpokePic.update()

    # createDeck(pokeList)

    # inputDB(x)

    # scrollbar for list

    sbl1 = Scrollbar(frm, orient="vertical", width=20)
    sbl1.pack(side='right', fill='y')
    my_treeT.configure(yscrollcommand=sbl1.set)
    sbl1.configure(command=my_treeT.yview)

    sbl2 = Scrollbar(frm1, orient="vertical", width=20)
    sbl2.pack(side='right', fill='y')
    my_deckT.configure(yscrollcommand=sbl2.set)
    sbl2.configure(command=my_deckT.yview)

    # ALL THE BUTTONS
    OkButt = Button(trainer, text="Ok", command=insertTrainerToDeck, height=2)
    OkButt.grid(row=4, column=8, rowspan=3, columnspan=2, padx=8, pady=8, sticky='nswe')

    for i in range(len(trainerSet)):
        my_treeT.insert(parent='', index=END, iid=i, text="", values=(trainerSet[i], trainerSetQty[i]))

    # for i in range(len(trainerSetCardList)):
    #     cid = trainerSetCardList[i]
    #     nCard = getCardName(cid)
    #     qty = trainerSetQty[i]
    #     my_deckT.insert(parent='', index=END, iid=len(trainerSetCardList),
    #                     text="", values=(cid, nCard, qty))

#add card from add energy
def addCardEng():
    global energyList
    top = Toplevel()
    top.title("Add Energy Card(s)")
    top.iconbitmap("database/rsc/pokebot.ico")
    top.wm_geometry("")

    def getvalue():
        etype = clicked.get()
        eqty = spboxE.get()
        value = energyList[etype]
        updateList(value, eqty)
        recBox()
        updateDeckCount(countDeck)
        top.destroy()

    infoEng = Label(top, text = "Choose Energy Type: ").pack()
    Energy = ['Grass', 'Fire', 'Water', 'Lightning', 'Psychic', 'Fighting', 'Darkness', 'Metal', 'Fairy']
    clicked = StringVar()
    clicked.set(Energy[0])
    enopt = OptionMenu(top, clicked, *Energy)
    enopt.pack()
    t1 = Label(top, text="How many cards:").pack()
    qty = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
           16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    spboxE = Spinbox(top, values=qty, width=10)
    spboxE.pack()
    button1 = Button(top,
                        text='OK!',
                        fg='White',
                        bg='dark green', height=1, width=10, command=getvalue).pack(pady=10)

#remove selected card from deck
def remCard():
    curItem = my_deck.focus()
    avalue = my_deck.item(curItem, 'values')
    if avalue == '':
        print("Nothing is selected!")
        popupmsg()
    else:
        dvalue = avalue[0]
        updateList(dvalue, -1)
    updateDeckCount(countDeck)
    printInfo()
    recBox()

#view recommended card
def viewCard():
    global img_url
    nvalue = fullRecommend(pokeList)
    if nvalue != "None":
        dump = nvalue.split('-')
        f = open("json/cards/{0}".format(setList[dump[0]]))
        db = json.load(f)
        for i in db:
            if i["id"] == nvalue:
                img_url = i["imageUrl"]
        f.close()
        print('URL : ', img_url)
        response = requests.get(img_url)
        img_data = response.content
        img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)).resize((240, 336), Image.ANTIALIAS))
        pokePic.config(image=img)
        pokePic.image = img
        pokePic.update()
    else:
        mb.showinfo("!", "No Recommended Card!")
        print("no card")

#save deck to txt
def save():
    if sum(pokeListNum) > 60:
        print("Too many cards!")
        return
    txt_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir=currDir, title="Select file",
                                           filetypes=(("Text Files", "*.txt"), ("all files", "*.*")))
    if txt_file:
        name = txt_file
        name = name.replace("C:/gui", "")
        print(txt_file)
        f = open(name, 'w')
        for i in range(len(pokeList)):
            dump = pokeList[i].split('#')
            x = str(pokeListNum[i]) + ' ' + dump[0] + '#' + dump[1].replace("◇", "PRISM STAR") + '\n'
            f.write(x)
        print("Save deck success")
        f.close()

#open saved deck
def load():
    txt_file = filedialog.askopenfilename(initialdir=currDir, title="Select file",
                                                   filetypes=(("Text Files", "*.txt"), ("all files", "*.*")))
    try:
        f = open(txt_file, 'r')
    except FileNotFoundError:
        print("Load deck cancelled")
        return
    pokeList.clear()
    pokeListNum.clear()
    pokeListPoke.clear()
    pokeListTrainer[0].clear()
    pokeListTrainer[1].clear()
    pokeListTrainer[2].clear()
    pokeListEnergy.clear()
    for i in my_deck.get_children():
        my_deck.delete(i)
    for lines in f:
        temp = lines.strip()

        if temp[1] == " ":
            x = temp[2::]
            num = int(temp[0])
        else:
            x = temp[3::]
            num = int(temp[0]) * 10
            num += int(temp[1])
        dump = x.split('#')
        cid = dump[0]
        print(cid, num)
        updateList(cid, num)
    print("Load deck success")
    f.close()

    e.delete(0, END)
    recBox()
    updateDeckCount(countDeck)

# WARNING
def popupmsg(): #Show msg if no card is selected when trying to add
    mb.showinfo("!", "No Card Selected!")

def deleteDeck():
    MsgBox = mb.askquestion ('Delete Deck','Are you sure you want to delete your deck?',icon = 'warning')
    if MsgBox == 'yes':
        pokeList.clear()
        pokeListNum.clear()
        pokeListPoke.clear()
        pokeListTrainer[0].clear()
        pokeListTrainer[1].clear()
        pokeListTrainer[2].clear()
        pokeListEnergy.clear()
        for i in my_deck.get_children():
            my_deck.delete(i)
        updateDeckCount(countDeck)
    else:
        return

#BODY STARTS HERE

def mainSize():
    sizex = 1050
    sizey = 600
    posx = 40
    posy = 20
    window.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))

window = Tk()
window.title("PokeBot UI")
window.iconbitmap("database/rsc/pokebot.ico")
mainSize()


#LEFT
#listbox
logo = Label(window, text='PokeBot Deck Builder') #LOGO
logo.grid(row=0,column=0, padx=8, sticky='s')

search = Entry(window, text='searchbox', width=53) #SearchBar
search.bind('<Return>', searchCard)
search.grid(row=1,column=0, padx=8, pady=8,sticky=W)

frm = Frame(window)
frm.grid(row=2, column=0,rowspan=5, padx=8, pady=8,sticky=W)

my_tree: Treeview = ttk.Treeview(frm,height=24)
my_tree['columns'] = ("ID", "Name")
my_tree.bind('<Double-1>',CurSelect)

my_tree.column('#0', width=0, minwidth=0)
my_tree.column('ID', anchor=W, width=100)
my_tree.column("Name",anchor=W, width=220)

my_tree.heading("#0", text="", anchor=W)
my_tree.heading("ID", text="ID", anchor=W)
my_tree.heading("Name", text="Name", anchor=W)

my_tree.pack(side='left', fill='y')

#Scrollbar
sbl1 = Scrollbar(frm, orient="vertical", width=20)
sbl1.pack(side='right', fill='y')
my_tree.configure(yscrollcommand=sbl1.set)
sbl1.configure(command=my_tree.yview)

Label1 = Label(window, text='Your Deck:') #explanatory
Label1.grid(row=1,column=4,sticky='es')

countDeck= StringVar()
Label2 = Label(window, textvariable=countDeck) #card counter
Label2.grid(row=1,column=5, sticky='sw')
updateDeckCount(countDeck)
#########################

#MIDDLE
#DECK

frm1 = Frame(window)
frm1.grid(row=1, column=4,columnspan=2, rowspan=6, padx=8, pady=8, sticky=S)

my_deck = ttk.Treeview(frm1, height=24)
my_deck['columns'] = ("ID", "Name", "Qty")
my_deck.bind('<Double-1>', CurSelectDeck)

my_deck.column('#0', width=0, minwidth=0)
my_deck.column('ID', anchor=W, width=80)
my_deck.column("Name", anchor=W, width=180)
my_deck.column("Qty", anchor=W, width=50)

my_deck.heading("#0", text="", anchor=W)
my_deck.heading("ID", text="ID", anchor=W)
my_deck.heading("Name", text="Name", anchor=W)
my_deck.heading("Qty", text="Qty", anchor=W)

my_deck.pack(side='left', fill='y')

sbl2 = Scrollbar(frm1, orient="vertical", width=20)
sbl2.pack(side='right', fill='y')
my_deck.configure(yscrollcommand=sbl2.set)
sbl2.configure(command=my_deck.yview)
#####################

# RIGHT
# IMAGE
response = requests.get(img_url)
img_data = response.content
img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)).resize((240,336), Image.ANTIALIAS))
pokePic = Label(image=img)
pokePic.grid(row=0, column=7, columnspan=3, rowspan=3, padx=8, pady=8, sticky='w')


# RECOMMEND SECTION
e = Entry(window, width=30) # RECOMMEND BOX
e.grid(row=4,column=8, padx=8,pady=8, sticky='e')
e.insert(0, 'No Recommended Card')

qty=[1, 2, 3, 4]
spbox = Spinbox(window, values=qty, width=5)
spbox.grid(row=4,column=8, padx=8,pady=8, sticky='e')

# createDeck(pokeList)
inputDB(dataBase)

rText = Label(window, text='Recommended Card:')
rText.grid(row=3, column=8, columnspan=2)

# ALL THE BUTTONS
#LOAD ICON
trashPhoto = PhotoImage(file = r"database/rsc/Bin.png")
rtphoto = trashPhoto.subsample(2, 2)

#BUTTONS
addButton = Button(window, text=">>", command=addCardSearch, bg='green', height=1)
addButton.grid(row=2, column=3)

removeButton = Button(window, text="<<", command=remCard, bg='red', height=1)
removeButton.grid(row=4, column=3)

addButton1 = Button(window, text="<<", command=addCardRecom, bg='green', height=1)
addButton1.grid(row=4, column=6)

addButton2 = Button(window, text="Add Trainer", command=addCardSup, width=13, height=2)
addButton2.grid(row=5, column=8, sticky='w')

addButton3 = Button(window, text="Add Energy", command=addCardEng, width=13, height=2)
addButton3.grid(row=6, column=8, sticky='w')

addButton4 = Button(window, text="  Save", command=save, width=13, height=2)
addButton4.grid(row=5, column=8, sticky='e')

addButton5 = Button(window, text=" Load", command=load, width=13, height=2)
addButton5.grid(row=6, column=8, sticky='e')

addButton6 = Button(window, text='Clear Deck', image=rtphoto, command=deleteDeck) #clear button
addButton6.grid(row=3,column=6, sticky='s')

addButton7 = Button(window, text="View", command=viewCard) #clear button
addButton7.grid(row=4,column=9)


window.mainloop()
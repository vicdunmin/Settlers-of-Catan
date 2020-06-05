# Mode Demo
from tkinter import *
from tkinter import font
import random
import math
import gameSetup
import resourceClass
import json
import socket
import threading
import playerClass
import buildClass
from queue import Queue

# Citation; This code is get from the socket tutorial by wonderful 112 TAs
HOST = ""  # put your IP address here if playing on multiple computers
PORT = 50002

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((HOST, PORT))
print("connected to server")


def handleServerMsg(server, serverMsg):
    server.setblocking(1)
    msg = ""
    command = ""
    while True:
        msg += server.recv(10).decode("UTF-8")
        command = msg.split("\n")
        while (len(command) > 1):
            readyMsg = command[0]
            msg = "\n".join(command[1:])
            serverMsg.put(readyMsg)
            command = msg.split("\n")

####################################
# init
####################################


class Bar(object):

    def __init__(self, x0, y0, x1, y1, fill=None):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.fill = fill

    def draw(self, canvas, text='', font='Chalkduster 15'):
        canvas.create_rectangle(self.x0, self.y0, self.x1,
                                self.y1, fill=self.fill, width=3)
        canvas.create_text((self.x0 + self.x1) / 2,
                           (self.y0 + self.y1) / 2, text=text, font=font)

    def inBar(self, x, y):
        return self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1


def init(data):
    data.mode = "menu"
    data.score = 0
    data.turn = 0
    data.dice = 0
    data.ready = False
    data.underConstruction = False
    data.helpOnMapSelection = False
    data.me = None
    data.rollable = True
    data.tradeStart = False
    data.moveMob = False
    data.gameOver = False
    data.winnerID = None
    data.gameMoveMode = None
    data.buildMode = None
    data.tradeMode = None
    data.otherPlayers = dict()
    data.otherReady = dict()
    data.playerList = []
    data.settlementList = []
    data.cityList = []
    data.roadList = []
    data.roadPoint = []
    data.numList = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
    data.colorList = ['OliveDrab1', 'brown4', 'gold', 'grey',
                      'chartreuse4'] * 3 + ['OliveDrab1', 'gold', 'chartreuse4']
    data.playerColorList = [None, 'yellow', 'white', 'blue', 'pink']
    data.menuBar1 = Bar(data.width / 3, data.height / 3,
                        data.width / 3 * 2, data.height / 2)
    data.menuBar2 = Bar(data.width / 3, data.height / 2,
                        data.width / 3 * 2, data.height / 3 * 2)
    data.helpOnMapSelectionBar = Bar(data.width / 10 * 8 - data.width / 100, data.height / 5,
                                     data.width / 40 * 39 + data.width / 100, data.height / 6 * 5, 'SkyBlue1')
    data.mapConfirm = Bar(data.width / 8 * 3, data.height / 7 * 6,
                          data.width / 8 * 5, data.height / 7 * 6.5, 'SkyBlue1')
    data.returnMenu = Bar(data.width / 20, data.height /
                          15, data.width / 10 * 3, data.height / 10, 'SkyBlue1')
    data.helpOnMap = Bar(data.width / 10 * 7, data.height /
                         15, data.width / 20 * 19, data.height / 10, 'SkyBlue1')
    data.turnBar = Bar(data.width / 20, data.height / 15,
                       data.width / 10 * 3, data.height / 10, 'SkyBlue1')
    data.diceBar = Bar(data.width / 10 * 8, data.height / 15,
                       data.width / 20 * 19, data.height / 10, 'SkyBlue1')
    data.buildBar = Bar(data.width / 20, data.height / 7 * 6,
                        data.width / 5, data.height / 7 * 6.5, 'SkyBlue1')
    data.tradeBar = Bar(data.width / 10 * 3, data.height / 7 * 6,
                        data.width / 20 * 9, data.height / 7 * 6.5, 'SkyBlue1')
    data.useBar = Bar(data.width / 20 * 11, data.height / 7 * 6,
                      data.width / 10 * 7, data.height / 7 * 6.5, 'SkyBlue1')
    data.endBar = Bar(data.width / 5 * 4, data.height / 7 * 6,
                      data.width / 20 * 19, data.height / 7 * 6.5, 'SkyBlue1')
    data.resourceBar = Bar(data.width / 10 * 8 - data.width / 100, data.height / 5,
                           data.width / 40 * 39 + data.width / 100, data.height / 6 * 5, 'SkyBlue1')
    data.playSelectionBar = Bar(
        data.width / 40, data.height / 5, data.width / 5, data.height / 6 * 5, 'SkyBlue1')
    data.buildRoadSelectionBar = Bar(
        data.width / 40, data.height / 5, data.width / 5, data.height / 120 * 43, 'SkyBlue1')
    data.buildSettlementSelectionBar = Bar(
        data.width / 40, data.height / 120 * 43, data.width / 5, data.height / 60 * 31, 'SkyBlue1')
    data.buildCitySelectionBar = Bar(
        data.width / 40, data.height / 60 * 31, data.width / 5, data.height / 40 * 27, 'SkyBlue1')
    data.buildDevelopSelectionBar = Bar(
        data.width / 40, data.height / 40 * 27, data.width / 5, data.height / 6 * 5, 'SkyBlue1')
    data.bankTradeBar = Bar(data.width / 40, data.height / 5,
                            data.width / 5, data.height / 120 * 43, 'SkyBlue1')
    data.portTradeBar = Bar(data.width / 40, data.height / 120 *
                            43, data.width / 5, data.height / 60 * 31, 'SkyBlue1')
    data.playerTradeBar = Bar(data.width / 40, data.height /
                              60 * 31, data.width / 5, data.height / 40 * 27, 'SkyBlue1')
    data.closeTradeBar = Bar(data.width / 40, data.height /
                             40 * 27, data.width / 5, data.height / 6 * 5, 'SkyBlue1')
    data.moveMobBar = Bar(data.width / 40, data.height / 5,
                          data.width / 5, data.height / 120 * 43, 'SkyBlue1')
    data.feastBar = Bar(data.width / 40, data.height / 120 *
                        43, data.width / 5, data.height / 60 * 31, 'SkyBlue1')
    data.extraVPBar = Bar(data.width / 40, data.height / 60 *
                          31, data.width / 5, data.height / 40 * 27, 'SkyBlue1')
    data.closeUseBar = Bar(data.width / 40, data.height /
                           40 * 27, data.width / 5, data.height / 6 * 5, 'SkyBlue1')
    data.woolBar = None
    data.brickBar = None
    data.grainBar = None
    data.oreBar = None
    data.lumberBar = None
    data.tradewP1Bar = None
    data.tradewP2Bar = None
    data.tradewP3Bar = None
    data.tradewP4Bar = None
    data.choose1Bar = None
    data.choose2Bar = None
    data.choose3Bar = None
    data.choose4Bar = None
    data.choose5Bar = None
    data.feastGet = None
    data.tradePID = None
    data.tradedPID = None
    data.giveOut = None
    data.giveOutQuantity = 0
    data.takeIn = None
    data.takeInQuantity = 0
    data.tradeNotification = False
    data.tradeAccepted = None
    data.tradeRefused = None
    data.resourceList = gameSetup.generateMap(data)


def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**(1 / 2)


def readFile(path):
    with open(path, "rt") as f:
        return f.read()


def mousePressed(event, data):
    if data.gameOver == True:
        msg = 'Gameover now\n'
        if (msg != ""):
            print("sending: ", msg,)
            data.server.send(msg.encode())
    if not data.gameOver:
        if data.mode == 'menu':
            menuMousePressed(event, data)
        if data.mode == 'mapSelection':
            mapSelectionMousePressed(event, data)
        if data.mode == 'gamePlay':
            gamePlayMousePressed(event, data)
        msg = 'Mode %s\n' % (data.mode)
        if (msg != ""):
            print("sending: ", msg,)
            data.server.send(msg.encode())


def keyPressed(event, data):
    msg = ''
    if event.keysym == 'h':
        contentsRead = readFile('help.txt')
        print(contentsRead)
    # Handle The trade
    if data.tradeNotification:
        if data.me.resource[data.takeIn] - data.takeInQuantity < 0:
            msg = 'Request Refused from %s to %s\n' % (
                data.me.PID, data.tradePID)
            data.tradeNotification = False
        elif event.keysym == 'y':
            msg = 'Request Accepted from %s to %s\n' % (
                data.me.PID, data.tradePID)
            data.me.resource[data.giveOut] += data.giveOutQuantity
            data.me.resource[data.takeIn] -= data.takeInQuantity
            data.tradeNotification = False
            data.tradePID = None
            data.tradedPID = None
            data.giveOut = None
            data.giveOutQuantity = 0
            data.takeInQuantity = 0
            data.takeIn = None
        elif event.keysym == 'n':
            msg = 'Request Refused from %s to %s\n' % (
                data.me.PID, data.tradePID)
            data.tradeNotification = False
            data.tradePID = None
            data.tradedPID = None
            data.giveOut = None
            data.giveOutQuantity = 0
            data.takeInQuantity = 0
            data.takeIn = None
    if (msg != ""):
        print("sending: ", msg,)
        data.server.send(msg.encode())


def redrawAll(canvas, data):
    if data.mode == 'menu':
        menuRedrawAll(canvas, data)
    if data.mode == 'mapSelection':
        gameSetup.mapSelectionRedrawAll(canvas, data)
    if data.mode == 'gamePlay':
        gamePlayRedrawAll(canvas, data)

# Deal with the map pt.1


def reformatnumList(l):
    result = []
    for s in l:
        if s[0] == '[':
            result.append(int(s[1:-1]))
        else:
            result.append(int(s[:-1]))
    return result


# Deal with the map pt.2
def reformatcolorList(l):
    result = []
    for s in l:
        if s.startswith('['):
            result.append(s[2:-2])
        else:
            result.append(s[1:-2])
    return result

# Message on the receiving end


def timerFired(data):
    while (serverMsg.qsize() > 0):
        msg = serverMsg.get(False)
        # try:
        print("received: ", msg, "\n")
        msg = msg.split()
        command = msg[0]
        if command == 'Mode':
            data.mode = msg[2]
            if data.mode == 'menu':
                data.ready = False
        elif command == 'numberList':
            data.numList = reformatnumList(msg[2:])
            data.resourceList = gameSetup.generateMap(data)
        elif command == 'colorList':
            data.colorList = reformatcolorList(msg[2:])
            data.resourceList = gameSetup.generateMap(data)
        elif command == 'newPlayer':
            newPID = msg[1]
            data.otherReady[newPID] = False
            data.playerList.append(newPID)
            data.otherPlayers[newPID] = playerClass.Player(
                newPID, data.playerColorList[int(newPID[-1])])
        elif command == 'Ready':
            data.otherReady[msg[1]] = True
        elif command == 'myIDis':
            PID = msg[1]
            data.playerList.append(PID)
            data.me = playerClass.Player(
                PID, data.playerColorList[int(PID[-1])])
        elif command == 'Gameover':
            data.gameOver = True
            data.winnerID = msg[1]
        elif command == 'Dice':
            data.dice = int(msg[2])
            for resource in data.resourceList:
                if not isinstance(resource, resourceClass.Seatile) and not isinstance(resource, resourceClass.TradingPort) and not isinstance(resource, resourceClass.Desert):
                    if data.dice == resource.number:
                        for setLocation in data.me.settlementLocation:
                            for pointList in resource.pointList:
                                if math.isclose(setLocation[0], pointList[0]) and math.isclose(setLocation[1], pointList[1]):
                                    data.me.resource[resource.resource] += 1
                        for cityLocation in data.me.cityLocation:
                            for pointList in resource.pointList:
                                if math.isclose(cityLocation[0], pointList[0]) and math.isclose(cityLocation[1], pointList[1]):
                                    data.me.resource[resource.resource] += 2
        elif command == 'Mob':
            if msg[2] == 'kill':
                oldMobIndex = int(msg[3])
                if isinstance(data.resourceList[oldMobIndex], resourceClass.Desert):
                    data.resourceList[oldMobIndex].mob = False
                else:
                    data.resourceList[oldMobIndex].mob = False
                    data.resourceList[oldMobIndex].number = data.resourceList[
                        oldMobIndex].oldNumber
            if msg[2] == 'move':
                newMobIndex = int(msg[3])
                data.resourceList[newMobIndex].number = 0
                data.resourceList[newMobIndex].mob = True
        elif command == 'Roadbuilt':
            PID = msg[1]
            x1 = float(msg[2])
            y1 = float(msg[3])
            x2 = float(msg[4])
            y2 = float(msg[5])
            color = msg[6]
            data.roadList.append(buildClass.Road(x1, y1, x2, y2, PID, color))
        elif command == 'Settlementbuilt':
            PID = msg[1]
            x = float(msg[2])
            y = float(msg[3])
            color = msg[4]
            data.settlementList.append(buildClass.Settlement(x, y, PID, color))
        elif command == 'Citybuilt':
            PID = msg[1]
            x = float(msg[2])
            y = float(msg[3])
            color = msg[4]
            data.cityList.append(buildClass.City(x, y, PID, color))
            if data.settlementList != []:
                for settlement in data.settlementList:
                    cx = settlement.cx
                    cy = settlement.cy
                    setPID = settlement.PID
                    if math.isclose(x, cx) and math.isclose(y, cy) and setPID == PID:
                        data.settlementList.remove(settlement)
        elif command == 'Trade':
            if msg[7] == data.me.PID:
                data.tradePID = msg[1]
                data.giveOutQuantity = int(msg[2])
                data.giveOut = msg[3]
                data.takeInQuantity = int(msg[5])
                data.takeIn = msg[6]
                data.tradedPID = msg[7]
                data.tradeNotification = True
        elif command == 'Request' and msg[6] == data.me.PID:
            if msg[2] == 'Refused':
                data.tradeRefused = True
            if msg[2] == 'Accepted':
                data.tradeAccepted = True
                data.me.resource[data.giveOut] -= data.giveOutQuantity
                data.me.resource[data.takeIn] += data.takeInQuantity
        elif command == 'Finished':
            data.turn += 1
            data.dice = 0
        data.playerList.sort()
        # except:
        # print('failed')
        serverMsg.task_done()
    data.me.VP = data.me.city * 2 + data.me.settlement + data.me.extraVP
    if data.me.VP >= 10:
        data.gameOver = True
        data.winnerID = data.me.PID


# Reshuffle the map everytime the player enters in the menu
def menuMousePressed(event, data):
    if data.menuBar1.inBar(event.x, event.y):
        data.underConstruction = True
    if (data.menuBar2.inBar(event.x, event.y)):
        data.underConstruction = False
        data.mode = 'mapSelection'
        random.shuffle(data.numList)
        numList = json.dumps(data.numList)
        msg = 'numberList %s\n' % (numList)
        if (msg != ""):
            print("sending: ", msg,)
            data.server.send(msg.encode())
        random.shuffle(data.colorList)
        colorList = json.dumps(data.colorList)
        msg = 'colorList %s\n' % (colorList)
        if (msg != ""):
            print("sending: ", msg,)
            data.server.send(msg.encode())
        data.resourceList = gameSetup.generateMap(data)

# Make sure everyone is ready for the game


def mapSelectionMousePressed(event, data):
    if not data.ready and data.returnMenu.inBar(event.x, event.y):
        data.mode = 'menu'
        data.ready = False
        for player in data.otherReady:
            data.otherReady[player] = False
    if data.mapConfirm.inBar(event.x, event.y):
        data.ready = True
    if data.helpOnMap.inBar(event.x, event.y):
        data.helpOnMapSelection = True
        contentsRead = readFile('help.txt')
        print(contentsRead)
    elif data.helpOnMapSelection:
        if data.helpOnMapSelectionBar.inBar(event.x, event.y):
            data.helpOnMapSelection = False
    if data.ready:
        msg = 'Ready True\n'
        print("sending: ", msg,)
        data.server.send(msg.encode())
    if (False not in data.otherReady.values()) and data.ready:
        data.mode = 'gamePlay'


def menuRedrawAll(canvas, data):
    # Picture cited from: https://tinyurl.com/y6goch7v
    pic = PhotoImage(file="catanbg.gif")
    pic = pic.zoom(3, 3)
    img = Label(image=pic)
    img.image = pic
    canvas.create_image(data.width * 0.5, data.height * 0.5, image=pic)
    canvas.create_text(data.width / 2, data.height / 5,
                       text='Settlers of Catan', font='Chalkduster 30 bold', fill='red')
    canvas.create_text(data.width / 2, data.height / 10 * 9,
                       text='Proudly Produced by Dunmin Zhu', font='Chalkduster 30 bold', fill='white')
    data.menuBar1.draw(canvas, 'Play with Computer',
                       font='Chalkduster 20 bold')
    data.menuBar2.draw(canvas, 'Play with your friends',
                       font='Chalkduster 20 bold')
    # The AI part is one of the feature to be added in the future
    if data.underConstruction:
        canvas.create_text(data.width / 2, data.height / 7,
                           text='Still Under Construction...', font=('Apple Chancery', 20), fill='blue')


def drawResource(canvas, data):
    PID = data.me.PID
    color = data.me.color
    canvas.create_text(data.width / 80 * 71, data.height /
                       4.3, text='Resource List for %s' % (PID), fill=color)
    canvas.create_text(data.width / 80 * 71, data.height / 20 * 7,
                       text='You have %d wool' % data.me.resource['wool'], fill=color)
    canvas.create_text(data.width / 80 * 71, data.height / 20 * 8,
                       text='You have %d brick' % data.me.resource['brick'], fill=color)
    canvas.create_text(data.width / 80 * 71, data.height / 20 * 9,
                       text='You have %d grain' % data.me.resource['grain'], fill=color)
    canvas.create_text(data.width / 80 * 71, data.height / 20 * 10,
                       text='You have %d ore' % data.me.resource['ore'], fill=color)
    canvas.create_text(data.width / 80 * 71, data.height / 20 * 11,
                       text='You have %d lumber' % data.me.resource['lumber'], fill=color)
    canvas.create_text(data.width / 80 * 71, data.height / 20 *
                       12, text='You have %d city(s)' % data.me.city, fill=color)
    canvas.create_text(data.width / 80 * 71, data.height / 20 * 13,
                       text='You have %d settlement(s)' % data.me.settlement, fill=color)
    canvas.create_text(data.width / 80 * 71, data.height / 20 *
                       14, text='You have %d VP(s)' % data.me.VP, fill=color)


def drawBuildMenu(canvas, data):
    buildSelectionBar = Bar(data.width / 40, data.height / 5,
                            data.width / 5, data.height / 6 * 5, 'SkyBlue1')
    data.buildRoadSelectionBar.draw(canvas, 'Road: 1L 1B')
    data.buildSettlementSelectionBar.draw(canvas)
    canvas.create_text(data.width / 80 * 9, data.height /
                       5 * 2, text='Settlement', font='Chalkduster 15')
    canvas.create_text(data.width / 80 * 9, data.height /
                       120 * 57, text='1L 1B 1G 1W', font='Chalkduster 15')
    data.buildCitySelectionBar.draw(canvas, 'City: 2G 2O')
    data.buildDevelopSelectionBar.draw(canvas, 'DC: 1G 1W 1O')
    if data.buildMode == 'road':
        canvas.create_text(data.width / 40 * 7, data.height / 15 * 2,
                           text='BUILDING ROAD!!', font='Chalkduster 20', fill='blue')
    if data.buildMode == 'settlement':
        canvas.create_text(data.width / 40 * 7, data.height / 15 * 2,
                           text='BUILDING SETTLEMENT!!', font='Chalkduster 20', fill='blue')
    if data.buildMode == 'city':
        canvas.create_text(data.width / 40 * 7, data.height / 15 * 2,
                           text='BUILDING CITY!!', font='Chalkduster 20', fill='blue')
    if data.buildMode == 'moveMob':
        canvas.create_text(data.width / 40 * 7, data.height / 15 * 2,
                           text='You have got Mob Card!', font='Chalkduster 20', fill='blue')
    if data.buildMode == 'feast':
        canvas.create_text(data.width / 40 * 7, data.height / 15 * 2,
                           text='You have got Feast Card!', font='Chalkduster 20', fill='blue')
    if data.buildMode == 'extraVP':
        canvas.create_text(data.width / 40 * 7, data.height / 15 * 2,
                           text='You have got an extra VP!', font='Chalkduster 20', fill='blue')


def drawTradeMenu(canvas, data):
    if data.tradeMode != 'bank':
        data.bankTradeBar.draw(canvas, 'Bank: 4 for 1')
    else:
        data.bankTradeBar.draw(canvas)
    if data.tradeMode != 'port':
        data.portTradeBar.draw(canvas, 'Port: 3 for 1')
    else:
        data.portTradeBar.draw(canvas)
    if data.tradeMode != 'player':
        data.playerTradeBar.draw(canvas, 'Player Trade')
    else:
        data.playerTradeBar.draw(canvas)
    data.closeTradeBar.draw(canvas, 'Close The Trade')
    if data.tradeMode == 'bank':
        canvas.create_text(data.width / 40 * 7, data.height / 15 * 2,
                           text='TRADE W/ BANK!!', font='Chalkduster 20', fill='blue')
        data.woolBar.draw(canvas, 'Wool')
        data.brickBar.draw(canvas, 'Brick')
        data.grainBar.draw(canvas, 'Grain')
        data.oreBar.draw(canvas, 'Ore')
        data.lumberBar.draw(canvas, 'Lumber')
        if data.giveOut == None:
            canvas.create_text(data.width / 40 * 7 + 20, data.height / 6,
                               text='Select the Resource that you want to give', font='Chalkduster 13', fill='blue')
        if data.giveOut != None:
            canvas.create_text(data.width / 40 * 7 + 20, data.height / 6,
                               text='Select the Resource that you want to take', font='Chalkduster 13', fill='blue')
    if data.tradeMode == 'port':
        canvas.create_text(data.width / 40 * 7, data.height / 15 * 2,
                           text='TRADE W/ PORT!!', font='Chalkduster 20', fill='blue')
        data.woolBar.draw(canvas, 'Wool')
        data.brickBar.draw(canvas, 'Brick')
        data.grainBar.draw(canvas, 'Grain')
        data.oreBar.draw(canvas, 'Ore')
        data.lumberBar.draw(canvas, 'Lumber')
        if data.giveOut == None:
            canvas.create_text(data.width / 40 * 7 + 20, data.height / 6,
                               text='Select the Resource that you want to give', font='Chalkduster 13', fill='blue')
        if data.giveOut != None:
            canvas.create_text(data.width / 40 * 7 + 20, data.height / 6,
                               text='Select the Resource that you want to take', font='Chalkduster 13', fill='blue')
    if data.tradeMode == 'player':
        canvas.create_text(data.width / 40 * 7, data.height / 15 * 2,
                           text='TRADE W/ PLAYER!!', font='Chalkduster 20', fill='blue')
        if data.tradePID == None and data.tradedPID == None:
            data.tradewP1Bar.draw(canvas, 'Trade with P1')
            data.tradewP2Bar.draw(canvas, 'Trade with P2')
            data.tradewP3Bar.draw(canvas, 'Trade with P3')
            data.tradewP4Bar.draw(canvas, 'Trade with P4')
        elif data.giveOutQuantity == 0:
            data.choose1Bar.draw(canvas, 'Give Out 1')
            data.choose2Bar.draw(canvas, 'Give Out 2')
            data.choose3Bar.draw(canvas, 'Give Out 3')
            data.choose4Bar.draw(canvas, 'Give Out 4')
            data.choose5Bar.draw(canvas, 'Give Out 5')
        elif data.giveOut == None:
            canvas.create_text(data.width / 40 * 7 + 20, data.height / 6,
                               text='Select the Resource that you want to give', font='Chalkduster 13', fill='blue')
            data.woolBar.draw(canvas, 'Wool')
            data.brickBar.draw(canvas, 'Brick')
            data.grainBar.draw(canvas, 'Grain')
            data.oreBar.draw(canvas, 'Ore')
            data.lumberBar.draw(canvas, 'Lumber')
        elif data.takeInQuantity == 0:
            data.choose1Bar.draw(canvas, 'Take In 1')
            data.choose2Bar.draw(canvas, 'Take In 2')
            data.choose3Bar.draw(canvas, 'Take In 3')
            data.choose4Bar.draw(canvas, 'Take In 4')
            data.choose5Bar.draw(canvas, 'Take In 5')
        elif data.takeIn == None:
            canvas.create_text(data.width / 40 * 7 + 20, data.height / 6,
                               text='Select the Resource that you want to take', font='Chalkduster 13', fill='blue')
            data.woolBar.draw(canvas, 'Wool')
            data.brickBar.draw(canvas, 'Brick')
            data.grainBar.draw(canvas, 'Grain')
            data.oreBar.draw(canvas, 'Ore')
            data.lumberBar.draw(canvas, 'Lumber')
        elif data.tradeAccepted == True:
            canvas.create_text(data.width / 40 * 7, data.height / 6,
                               text='Trade Accepted!!', font='Chalkduster 15', fill='blue')
        elif data.tradeRefused == True:
            canvas.create_text(data.width / 40 * 7, data.height / 6,
                               text='Trade Refused!!', font='Chalkduster 15', fill='blue')
        elif data.takeIn != None and data.takeInQuantity != 0 and data.giveOut != None and data.giveOutQuantity != 0:
            canvas.create_text(data.width / 40 * 7 + 20, data.height / 6, text='%s wants to trade %d %s for %d %s from %s' % (data.tradePID,
                                                                                                                              data.giveOutQuantity, data.giveOut, data.takeInQuantity, data.takeIn, data.tradedPID), font='Chalkduster 12', fill='blue')


def drawUseMenu(canvas, data):
    data.moveMobBar.draw(canvas, 'Move Mob * %d' % (data.me.moveMob))
    data.feastBar.draw(canvas, 'Feast * %d' % (data.me.feast))
    data.extraVPBar.draw(canvas, 'Extra VP * %d' % (data.me.extraVP))
    data.closeUseBar.draw(canvas, 'Close')
    if data.feastGet != None:
        canvas.create_text(data.width / 40 * 7, data.height / 6, text='Congrats! You have got three %s' %
                           (data.feastGet), font='Chalkduster 12', fill='blue')


def isRoadBuiltByOthers(x1, y1, x2, y2, data):
    for road in data:
        startx = road.x1
        starty = road.y1
        endx = road.x2
        endy = road.y2
        if math.isclose(x1, startx) and math.isclose(y1, starty) and math.isclose(x2, endx) and math.isclose(y2, endy):
            return True
        if math.isclose(x1, endx) and math.isclose(y1, endy) and math.isclose(x2, startx) and math.isclose(y2, starty):
            return True
    return False


def isLegalSettlement(x, y, data):
    if data.settlementList != []:
        for settlement in data.settlementList:
            cx = settlement.cx
            cy = settlement.cy
            if distance(x, y, cx, cy) < (data.width / 20) * math.sqrt(3) - 5:
                return False
    if data.cityList != []:
        for city in data.cityList:
            cx = city.cx
            cy = city.cy
            if distance(x, y, cx, cy) < (data.width / 20) * math.sqrt(3) - 5:
                return False
    if data.roadList != []:
        for road in data.roadList:
            startx = road.x1
            starty = road.y1
            endx = road.x2
            endy = road.y2
            if (math.isclose(x, startx) and math.isclose(y, starty)) or (math.isclose(x, endx) and math.isclose(y, endy)):
                return True
    return False


def isLegalCity(x, y, data):
    if data.settlementList != []:
        for settlement in data.settlementList:
            cx = settlement.cx
            cy = settlement.cy
            PID = settlement.PID
            if math.isclose(x, cx) and math.isclose(y, cy) and data.me.PID == PID:
                data.settlementList.remove(settlement)
                return True
    return False


def hasPort(data):
    for (setx, sety) in data.me.settlementLocation:
        for resource in data.resourceList:
            if isinstance(resource, resourceClass.TradingPort):
                for (cx, cy) in resource.pointList:
                    if math.isclose(setx, cx) and math.isclose(sety, cy):
                        return True
    return False


def clickResource(data, x, y):
    newMobIndex = None
    minDistance = 50
    for i in range(len(data.resourceList)):
        if (not isinstance(data.resourceList[i], resourceClass.Seatile)) and (not isinstance(data.resourceList[i], resourceClass.TradingPort) and (not isinstance(data.resourceList[i], resourceClass.Desert))):
            if distance(x, y, data.resourceList[i].cx, data.resourceList[i].cy) < minDistance:
                minDistance = distance(x, y, data.resourceList[
                                       i].cx, data.resourceList[i].cy)
                newMobIndex = i
    return newMobIndex


def findOldMob(data):
    for i in range(len(data.resourceList)):
        if (not isinstance(data.resourceList[i], resourceClass.Seatile)) and (not isinstance(data.resourceList[i], resourceClass.TradingPort)):
            if data.resourceList[i].mob == True:
                return i


def gamePlayMousePressed(event, data):
    msg = ''
    # Deal with mob first before everything
    if data.moveMob:
        newMobIndex = clickResource(data, event.x, event.y)
        oldMobIndex = findOldMob(data)
        if oldMobIndex != None:
            if isinstance(data.resourceList[oldMobIndex], resourceClass.Desert):
                data.resourceList[oldMobIndex].mob = False
                msg = 'Mob kill %d\n' % (oldMobIndex)
            elif data.resourceList[oldMobIndex].resource != None:
                data.resourceList[oldMobIndex].number = data.resourceList[
                    oldMobIndex].oldNumber
                data.resourceList[oldMobIndex].mob = False
                msg = 'Mob kill %d\n' % (oldMobIndex)
        if (msg != ""):
            print("sending: ", msg,)
            data.server.send(msg.encode())
        msg = ''
        if newMobIndex != None:
            if not isinstance(data.resourceList[newMobIndex], resourceClass.Desert):
                if data.resourceList[newMobIndex].resource != None:
                    data.resourceList[newMobIndex].number = 0
                    data.resourceList[newMobIndex].mob = True
                    data.moveMob = False
                    msg = 'Mob move %d\n' % (newMobIndex)
        if (msg != ""):
            print("sending: ", msg,)
            data.server.send(msg.encode())
    # Start the turn
    if (data.me.PID == data.playerList[data.turn % len(data.playerList)]) and not data.moveMob:
        if data.diceBar.inBar(event.x, event.y) and data.rollable:
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            data.dice = dice1 + dice2
            if data.dice == 7:
                data.moveMob = True
            # Calculate the resource
            for resource in data.resourceList:
                if not isinstance(resource, resourceClass.Seatile) and not isinstance(resource, resourceClass.TradingPort) and not isinstance(resource, resourceClass.Desert):
                    if data.dice == resource.number:
                        for setLocation in data.me.settlementLocation:
                            for pointList in resource.pointList:
                                if math.isclose(setLocation[0], pointList[0]) and math.isclose(setLocation[1], pointList[1]):
                                    data.me.resource[resource.resource] += 1
                        for cityLocation in data.me.cityLocation:
                            for pointList in resource.pointList:
                                if math.isclose(cityLocation[0], pointList[0]) and math.isclose(cityLocation[1], pointList[1]):
                                    data.me.resource[resource.resource] += 2
            data.rollable = False
            msg = 'Dice %d\n' % (data.dice)
        if data.feastGet != None:
            data.feastGet = None
        if data.useBar.inBar(event.x, event.y) and not data.rollable:
            data.gameMoveMode = 'use'
            data.buildMode = None
        if data.gameMoveMode == 'use':
            if data.me.moveMob > 0 and data.moveMobBar.inBar(event.x, event.y):
                data.moveMob = True
                data.me.moveMob -= 1
            elif data.me.feast > 0 and data.feastBar.inBar(event.x, event.y):
                data.me.feast -= 1
                resource = random.choice(
                    ['wool', 'grain', 'ore', 'brick', 'lumber'])
                data.feastGet = resource
                data.me.resource[resource] += 3
            elif data.closeUseBar.inBar(event.x, event.y):
                data.gameMoveMode = None
                data.buildMode = None
        if data.buildBar.inBar(event.x, event.y) and not data.rollable:
            data.gameMoveMode = 'build'
            data.buildMode = None
        # Build Mode
        if data.gameMoveMode == 'build':
            if data.buildDevelopSelectionBar.inBar(event.x, event.y):
                if data.me.resource['grain'] < 1 or data.me.resource['wool'] < 1 or data.me.resource['ore'] < 1:
                    print(
                        '%s does not have enough resource to build development card' % data.me.PID)
                else:
                    n = random.random()
                    if 0 < n < 0.8:
                        data.buildMode = 'moveMob'
                        data.me.moveMob += 1
                    elif 0.8 < n < 0.95:
                        data.buildMode = 'feast'
                        data.me.feast += 1
                    else:
                        data.buildMode = 'extraVP'
                        data.me.extraVP += 1
                    data.me.resource['grain'] -= 1
                    data.me.resource['wool'] -= 1
                    data.me.resource['ore'] -= 1
            if data.buildRoadSelectionBar.inBar(event.x, event.y):
                data.buildMode = 'road'
            if data.buildSettlementSelectionBar.inBar(event.x, event.y):
                data.buildMode = 'settlement'
            if data.buildCitySelectionBar.inBar(event.x, event.y):
                data.buildMode = 'city'
            if data.buildMode == 'road':
                if data.me.resource['lumber'] < 1 or data.me.resource['brick'] < 1:
                    print('%s does not have enough resource to build road' %
                          data.me.PID)
                else:
                    if data.me.findPoint(event, data) != None:
                        start = data.me.findPoint(event, data)
                        data.roadPoint.append(start)
                    if len(data.roadPoint) == 2:
                        x1 = data.roadPoint[0][0]
                        y1 = data.roadPoint[0][1]
                        x2 = data.roadPoint[1][0]
                        y2 = data.roadPoint[1][1]
                        if (x1 - x2)**2 + (y1 - y2)**2 > 45**2 or (x1 - x2)**2 + (y1 - y2)**2 < 35**2:
                            data.roadPoint = []
                        if data.me.roadLocation != []:
                            if ((x1, y1) not in data.me.roadLocation) and ((x2, y2) not in data.me.roadLocation):
                                print('Not Connected')
                                data.roadPoint = []
                            if isRoadBuiltByOthers(x1, y1, x2, y2, data.roadList):
                                print('Already Built By Others')
                                data.roadPoint = []
                    if len(data.roadPoint) == 2:
                        data.roadList.append(buildClass.Road(
                            x1, y1, x2, y2, data.me.PID, data.me.color))
                        msg = 'Roadbuilt %f %f %f %f %s\n' % (
                            x1, y1, x2, y2, data.me.color)
                        data.me.resource['lumber'] -= 1
                        data.me.resource['brick'] -= 1
                        data.me.road += 1
                        data.me.roadLocation.append((x1, y1))
                        data.me.roadLocation.append((x2, y2))
                        data.roadPoint = []
            if data.buildMode == 'settlement':
                if data.me.resource['lumber'] < 1 or data.me.resource['brick'] < 1 or data.me.resource['grain'] < 1 or data.me.resource['wool'] < 1:
                    print(
                        '%s does not have enough resource to build a settlement' % data.me.PID)
                else:
                    if data.me.findPoint(event, data) != None:
                        x = data.me.findPoint(event, data)[0]
                        y = data.me.findPoint(event, data)[1]
                        if isLegalSettlement(x, y, data):
                            data.settlementList.append(buildClass.Settlement(
                                x, y, data.me.PID, data.me.color))
                            data.me.settlementLocation.append((x, y))
                            data.me.settlement += 1
                            data.me.resource['lumber'] -= 1
                            data.me.resource['brick'] -= 1
                            data.me.resource['grain'] -= 1
                            data.me.resource['wool'] -= 1
                            msg = 'Settlementbuilt %f %f %s\n' % (
                                x, y, data.me.color)
            if data.buildMode == 'city':
                if data.me.resource['grain'] < 2 or data.me.resource['ore'] < 3:
                    print('%s does not have enough resource to build a city' %
                          data.me.PID)
                else:
                    if data.me.findPoint(event, data) != None:
                        x = data.me.findPoint(event, data)[0]
                        y = data.me.findPoint(event, data)[1]
                        if isLegalCity(x, y, data):
                            data.cityList.append(buildClass.City(
                                x, y, data.me.PID, data.me.color))
                            for (cx, cy) in data.me.settlementLocation:
                                if math.isclose(x, cx) and math.isclose(y, cy):
                                    data.me.settlementLocation.remove((cx, cy))
                            data.me.settlement -= 1
                            data.me.city += 1
                            data.me.cityLocation.append((x, y))
                            data.me.resource['grain'] -= 2
                            data.me.resource['ore'] -= 3
                            msg = 'Citybuilt %f %f %s\n' % (
                                x, y, data.me.color)
        if data.tradeBar.inBar(event.x, event.y) and not data.rollable:
            data.gameMoveMode = 'trade'
            data.buildMode = None
        # Trade Mode
        if data.gameMoveMode == 'trade':
            if data.bankTradeBar.inBar(event.x, event.y):
                data.tradeMode = 'bank'
            if data.portTradeBar.inBar(event.x, event.y) and hasPort(data):
                data.tradeMode = 'port'
            if data.playerTradeBar.inBar(event.x, event.y):
                data.tradeMode = 'player'
            if data.closeTradeBar.inBar(event.x, event.y):
                data.tradeMode = None
                data.tradeStart = False
                data.tradePID = None
                data.tradedPID = None
                data.giveOut = None
                data.giveOutQuantity = 0
                data.takeInQuantity = 0
                data.takeIn = None
                data.tradeAccepted = None
                data.tradeRefused = None
            if data.tradeMode == 'bank':
                data.woolBar = Bar(
                    data.width / 40, data.height / 5, data.width / 5, data.height / 600 * 139)
                data.brickBar = Bar(data.width / 40, data.height /
                                    600 * 139, data.width / 5, data.height / 600 * 158)
                data.grainBar = Bar(data.width / 40, data.height /
                                    600 * 158, data.width / 5, data.height / 600 * 177)
                data.oreBar = Bar(data.width / 40, data.height /
                                  600 * 177, data.width / 5, data.height / 600 * 196)
                data.lumberBar = Bar(
                    data.width / 40, data.height / 600 * 196, data.width / 5, data.height / 120 * 43)
                if data.giveOut == None and data.tradeStart:
                    if data.woolBar.inBar(event.x, event.y) and data.me.resource['wool'] >= 4:
                        data.giveOut = 'wool'
                    elif data.brickBar.inBar(event.x, event.y) and data.me.resource['brick'] >= 4:
                        data.giveOut = 'brick'
                    elif data.grainBar.inBar(event.x, event.y) and data.me.resource['grain'] >= 4:
                        data.giveOut = 'grain'
                    elif data.oreBar.inBar(event.x, event.y) and data.me.resource['ore'] >= 4:
                        data.giveOut = 'ore'
                    elif data.lumberBar.inBar(event.x, event.y) and data.me.resource['lumber'] >= 4:
                        data.giveOut = 'lumber'
                elif data.giveOut != None:
                    if data.woolBar.inBar(event.x, event.y):
                        data.me.resource['wool'] += 1
                        data.me.resource[data.giveOut] -= 4
                        data.tradeMode = None
                        data.giveOut = None
                        data.tradeStart = False
                    elif data.brickBar.inBar(event.x, event.y):
                        data.me.resource['brick'] += 1
                        data.me.resource[data.giveOut] -= 4
                        data.tradeMode = None
                        data.giveOut = None
                        data.tradeStart = False
                    elif data.grainBar.inBar(event.x, event.y):
                        data.me.resource['grain'] += 1
                        data.me.resource[data.giveOut] -= 4
                        data.tradeMode = None
                        data.giveOut = None
                        data.tradeStart = False
                    elif data.oreBar.inBar(event.x, event.y):
                        data.me.resource['ore'] += 1
                        data.me.resource[data.giveOut] -= 4
                        data.tradeMode = None
                        data.giveOut = None
                        data.tradeStart = False
                    elif data.lumberBar.inBar(event.x, event.y):
                        data.me.resource['lumber'] += 1
                        data.me.resource[data.giveOut] -= 4
                        data.tradeMode = None
                        data.giveOut = None
                        data.tradeStart = False
                if data.tradeMode != None:
                    data.tradeStart = True
            if data.tradeMode == 'port':
                data.woolBar = Bar(data.width / 40, data.height /
                                   120 * 43, data.width / 5, data.height / 100 * 39)
                data.brickBar = Bar(
                    data.width / 40, data.height / 100 * 39, data.width / 5, data.height / 600 * 253)
                data.grainBar = Bar(
                    data.width / 40, data.height / 600 * 253, data.width / 5, data.height / 75 * 34)
                data.oreBar = Bar(data.width / 40, data.height /
                                  75 * 34, data.width / 5, data.height / 200 * 97)
                data.lumberBar = Bar(
                    data.width / 40, data.height / 200 * 97, data.width / 5, data.height / 60 * 31)
                if data.giveOut == None and data.tradeStart:
                    if data.woolBar.inBar(event.x, event.y) and data.me.resource['wool'] >= 4:
                        data.giveOut = 'wool'
                    elif data.brickBar.inBar(event.x, event.y) and data.me.resource['brick'] >= 4:
                        data.giveOut = 'brick'
                    elif data.grainBar.inBar(event.x, event.y) and data.me.resource['grain'] >= 4:
                        data.giveOut = 'grain'
                    elif data.oreBar.inBar(event.x, event.y) and data.me.resource['ore'] >= 4:
                        data.giveOut = 'ore'
                    elif data.lumberBar.inBar(event.x, event.y) and data.me.resource['lumber'] >= 4:
                        data.giveOut = 'lumber'
                elif data.giveOut != None:
                    if data.woolBar.inBar(event.x, event.y):
                        data.me.resource['wool'] += 1
                        data.me.resource[data.giveOut] -= 3
                        data.tradeMode = None
                        data.giveOut = None
                        data.tradeStart = False
                    elif data.brickBar.inBar(event.x, event.y):
                        data.me.resource['brick'] += 1
                        data.me.resource[data.giveOut] -= 3
                        data.tradeMode = None
                        data.giveOut = None
                        data.tradeStart = False
                    elif data.grainBar.inBar(event.x, event.y):
                        data.me.resource['grain'] += 1
                        data.me.resource[data.giveOut] -= 3
                        data.tradeMode = None
                        data.giveOut = None
                        data.tradeStart = False
                    elif data.oreBar.inBar(event.x, event.y):
                        data.me.resource['ore'] += 1
                        data.me.resource[data.giveOut] -= 3
                        data.tradeMode = None
                        data.giveOut = None
                        data.tradeStart = False
                    elif data.lumberBar.inBar(event.x, event.y):
                        data.me.resource['lumber'] += 1
                        data.me.resource[data.giveOut] -= 3
                        data.tradeMode = None
                        data.giveOut = None
                        data.tradeStart = False
                if data.tradeMode != None:
                    data.tradeStart = True
            if data.tradeMode == 'player':
                data.tradewP1Bar = Bar(
                    data.width / 40, data.height / 60 * 31, data.width / 5, data.height / 160 * 89)
                data.tradewP2Bar = Bar(
                    data.width / 40, data.height / 160 * 89, data.width / 5, data.height / 240 * 143)
                data.tradewP3Bar = Bar(
                    data.width / 40, data.height / 240 * 143, data.width / 5, data.height / 96 * 61)
                data.tradewP4Bar = Bar(
                    data.width / 40, data.height / 96 * 61, data.width / 5, data.height / 40 * 27)
                if data.tradePID == None and data.tradedPID == None:
                    if data.tradewP1Bar.inBar(event.x, event.y) and 'P1' in data.otherPlayers and data.tradeStart:
                        data.tradePID = data.me.PID
                        data.tradedPID = 'P1'
                        data.tradeStart = False
                    elif data.tradewP2Bar.inBar(event.x, event.y) and 'P2' in data.otherPlayers and data.tradeStart:
                        data.tradePID = data.me.PID
                        data.tradedPID = 'P2'
                        data.tradeStart = False
                    elif data.tradewP3Bar.inBar(event.x, event.y) and 'P3' in data.otherPlayers and data.tradeStart:
                        data.tradePID = data.me.PID
                        data.tradedPID = 'P3'
                        data.tradeStart = False
                    elif data.tradewP4Bar.inBar(event.x, event.y) and 'P4' in data.otherPlayers and data.tradeStart:
                        data.tradePID = data.me.PID
                        data.tradedPID = 'P4'
                        data.tradeStart = False
                data.choose1Bar = Bar(
                    data.width / 40, data.height / 60 * 31, data.width / 5, data.height / 600 * 329)
                data.choose2Bar = Bar(
                    data.width / 40, data.height / 600 * 329, data.width / 5, data.height / 50 * 29)
                data.choose3Bar = Bar(
                    data.width / 40, data.height / 50 * 29, data.width / 5, data.height / 600 * 367)
                data.choose4Bar = Bar(
                    data.width / 40, data.height / 600 * 367, data.width / 5, data.height / 300 * 193)
                data.choose5Bar = Bar(
                    data.width / 40, data.height / 300 * 193, data.width / 5, data.height / 40 * 27)
                if data.giveOutQuantity == 0 and data.tradeStart and data.tradePID != None:
                    if data.choose1Bar.inBar(event.x, event.y):
                        data.giveOutQuantity = 1
                        data.tradeStart = False
                    elif data.choose2Bar.inBar(event.x, event.y):
                        data.giveOutQuantity = 2
                        data.tradeStart = False
                    elif data.choose3Bar.inBar(event.x, event.y):
                        data.giveOutQuantity = 3
                        data.tradeStart = False
                    elif data.choose4Bar.inBar(event.x, event.y):
                        data.giveOutQuantity = 4
                        data.tradeStart = False
                    elif data.choose5Bar.inBar(event.x, event.y):
                        data.giveOutQuantity = 5
                        data.tradeStart = False
                data.woolBar = Bar(data.width / 40, data.height /
                                   60 * 31, data.width / 5, data.height / 600 * 329)
                data.brickBar = Bar(
                    data.width / 40, data.height / 600 * 329, data.width / 5, data.height / 50 * 29)
                data.grainBar = Bar(
                    data.width / 40, data.height / 50 * 29, data.width / 5, data.height / 600 * 367)
                data.oreBar = Bar(data.width / 40, data.height /
                                  600 * 367, data.width / 5, data.height / 300 * 193)
                data.lumberBar = Bar(
                    data.width / 40, data.height / 300 * 193, data.width / 5, data.height / 40 * 27)
                if data.giveOut == None and data.tradeStart and data.tradePID != None and data.giveOutQuantity != 0:
                    if data.woolBar.inBar(event.x, event.y) and data.me.resource['wool'] >= data.giveOutQuantity:
                        data.giveOut = 'wool'
                        data.tradeStart = False
                    elif data.brickBar.inBar(event.x, event.y) and data.me.resource['brick'] >= data.giveOutQuantity:
                        data.giveOut = 'brick'
                        data.tradeStart = False
                    elif data.grainBar.inBar(event.x, event.y) and data.me.resource['grain'] >= data.giveOutQuantity:
                        data.giveOut = 'grain'
                        data.tradeStart = False
                    elif data.oreBar.inBar(event.x, event.y) and data.me.resource['ore'] >= data.giveOutQuantity:
                        data.giveOut = 'ore'
                        data.tradeStart = False
                    elif data.lumberBar.inBar(event.x, event.y) and data.me.resource['lumber'] >= data.giveOutQuantity:
                        data.giveOut = 'lumber'
                        data.tradeStart = False
                if data.takeInQuantity == 0 and data.tradeStart and data.tradePID != None and data.giveOutQuantity != 0 and data.giveOut != None:
                    if data.choose1Bar.inBar(event.x, event.y):
                        data.takeInQuantity = 1
                        data.tradeStart = False
                    elif data.choose2Bar.inBar(event.x, event.y):
                        data.takeInQuantity = 2
                        data.tradeStart = False
                    elif data.choose3Bar.inBar(event.x, event.y):
                        data.takeInQuantity = 3
                        data.tradeStart = False
                    elif data.choose4Bar.inBar(event.x, event.y):
                        data.takeInQuantity = 4
                        data.tradeStart = False
                    elif data.choose5Bar.inBar(event.x, event.y):
                        data.takeInQuantity = 5
                        data.tradeStart = False
                if data.takeIn == None and data.tradeStart and data.tradePID != None and data.giveOutQuantity != 0 and data.giveOut != None and data.takeInQuantity != 0:
                    if data.woolBar.inBar(event.x, event.y):
                        data.takeIn = 'wool'
                        data.tradeStart = False
                        msg = 'Trade %d %s for %d %s %s\n' % (
                            data.giveOutQuantity, data.giveOut, data.takeInQuantity, data.takeIn, data.tradedPID)
                    elif data.brickBar.inBar(event.x, event.y):
                        data.takeIn = 'brick'
                        data.tradeStart = False
                        msg = 'Trade %d %s for %d %s %s\n' % (
                            data.giveOutQuantity, data.giveOut, data.takeInQuantity, data.takeIn, data.tradedPID)
                    elif data.grainBar.inBar(event.x, event.y):
                        data.takeIn = 'grain'
                        data.tradeStart = False
                        msg = 'Trade %d %s for %d %s %s\n' % (
                            data.giveOutQuantity, data.giveOut, data.takeInQuantity, data.takeIn, data.tradedPID)
                    elif data.oreBar.inBar(event.x, event.y):
                        data.takeIn = 'ore'
                        data.tradeStart = False
                        msg = 'Trade %d %s for %d %s %s\n' % (
                            data.giveOutQuantity, data.giveOut, data.takeInQuantity, data.takeIn, data.tradedPID)
                    elif data.lumberBar.inBar(event.x, event.y):
                        data.takeIn = 'lumber'
                        data.tradeStart = False
                        msg = 'Trade %d %s for %d %s %s\n' % (
                            data.giveOutQuantity, data.giveOut, data.takeInQuantity, data.takeIn, data.tradedPID)
                data.tradeStart = True
        if data.endBar.inBar(event.x, event.y):
            data.rollable = True
            data.dice = 0
            data.turn += 1
            data.gameMoveMode = None
            data.buildMode = None
            msg = 'Finished This Turn\n'
        if (msg != ""):
            print("sending: ", msg,)
            data.server.send(msg.encode())


def gamePlayRedrawAll(canvas, data):
    # Citation: image from https://tinyurl.com/yy5pn5g6
    pic = PhotoImage(file="Catan Seafarers.gif")
    pic = pic.zoom(2, 2)
    img = Label(image=pic)
    img.image = pic
    canvas.create_image(data.width * 0.4, data.height * 0.36, image=pic)
    for resource in data.resourceList:
        resource.draw(canvas)
    for road in data.roadList:
        road.draw(canvas)
    for settlement in data.settlementList:
        settlement.draw(canvas)
    for city in data.cityList:
        city.draw(canvas)
    data.turnBar.draw(canvas, 'Turn %d: %s' % (
        data.turn, data.playerList[data.turn % len(data.playerList)]))
    data.diceBar.draw(canvas, 'Roll The Dice')
    data.buildBar.draw(canvas, 'Build')
    data.tradeBar.draw(canvas, 'Trade')
    data.useBar.draw(canvas, 'Use')
    data.endBar.draw(canvas, 'End')
    data.resourceBar.draw(canvas)
    canvas.create_text(data.width / 40 * 39, data.height / 12,
                       text=str(data.dice), font='Chalkduster 20', fill='blue')
    drawResource(canvas, data)
    if data.gameMoveMode == 'build':
        drawBuildMenu(canvas, data)
    if data.gameMoveMode == 'trade':
        drawTradeMenu(canvas, data)
    if data.gameMoveMode == 'use':
        drawUseMenu(canvas, data)
    if data.tradeNotification:
        canvas.create_text(data.width / 40 * 7 + 20, data.height / 15 * 2, text='Request from %s: Asking %d %s for %d %s' % (
            data.tradePID, data.takeInQuantity, data.takeIn, data.giveOutQuantity, data.giveOut), font='Chalkduster 13', fill='blue')
        canvas.create_text(data.width / 40 * 7, data.height / 6,
                           text="Press 'Y' to accept, 'N' to reject", font='Chalkduster 15', fill='blue')
    if data.moveMob:
        canvas.create_text(data.width / 40 * 7, data.height / 6,
                           text="Please click to move the mob", font='Chalkduster 15', fill='blue')
    if data.gameOver:
        canvas.create_text(data.width / 2, data.height / 2, text='Game Over. %s have conquered the island.' %
                           (data.winnerID), font='Chalkduster 25', fill='blue')

####################################
# use the run function as-is
####################################


def run(width=300, height=300, serverMsg=None, server=None):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init

    class Struct(object):
        pass
    data = Struct()
    data.server = server
    data.serverMsg = serverMsg
    data.width = width
    data.height = height
    data.timerDelay = 100  # milliseconds
    root = Tk()
    root.resizable(width=False, height=False)  # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
              mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
              keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

serverMsg = Queue(100)
threading.Thread(target=handleServerMsg, args=(server, serverMsg)).start()

run(800, 600, serverMsg, server)

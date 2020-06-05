# Setup the map: Menu and Mapselection

from tkinter import *
import random
import math
import resourceClass
from tkinter import font


def generateMap(data):
    size = data.width / 20
    margin = data.width / 10
    cx = (data.width - 2 * margin) / 2 + margin
    cy = (data.height - 2 * margin) / 2 + 0.5 * margin
    pointList = []
    num = 0
    for i in range(6):
        angle1 = math.radians(30) + i * math.radians(60)
        pointList.append(resourceClass.Resource(cx + math.sqrt(3) * size * math.cos(angle1),
                                                cy - math.sqrt(3) * size * math.sin(angle1), size, data.numList, data.colorList, num))
        pointList.append(resourceClass.Resource(cx + 2 * math.sqrt(3) * size * math.cos(angle1), cy -
                                                2 * math.sqrt(3) * size * math.sin(angle1), size, data.numList, data.colorList, num + 1))
        pointList.append(resourceClass.Seatile(cx + 3 * math.sqrt(3) * size *
                                               math.cos(angle1), cy - 3 * math.sqrt(3) * size * math.sin(angle1), size))
        angle2 = math.radians(60) + i * math.radians(60)
        pointList.append(resourceClass.Resource(cx + 3 * size * math.cos(angle2), cy -
                                                3 * size * math.sin(angle2), size, data.numList, data.colorList, num + 2))
        angle3 = math.atan(math.sqrt(3) / 9) + i * math.radians(60)
        pointList.append(resourceClass.Seatile(cx + math.sqrt(21) * size *
                                               math.cos(angle3), cy - math.sqrt(21) * size * math.sin(angle3), size))
        angle4 = -math.atan(math.sqrt(3) / 9) + i * math.radians(60)
        pointList.append(resourceClass.TradingPort(cx + math.sqrt(21) * size *
                                                   math.cos(angle4), cy - math.sqrt(21) * size * math.sin(angle4), size))
        num += 3
    pointList.append(resourceClass.Desert(cx, cy, size))
    return pointList


def mapSelectionRedrawAll(canvas, data):
    pic = PhotoImage(file="Catan Seafarers.gif")
    pic = pic.zoom(2, 2)
    img = Label(image=pic)
    img.image = pic
    canvas.create_image(data.width * 0.4, data.height * 0.36, image=pic)
    for resource in data.resourceList:
        resource.draw(canvas)
    data.mapConfirm.draw(canvas, 'Confirm your Map')
    data.returnMenu.draw(canvas, 'Return to Menu')
    data.helpOnMap.draw(canvas, 'Help')
    if data.helpOnMapSelection:
        data.helpOnMapSelectionBar.draw(canvas)
        canvas.create_text(data.width / 80 * 71, data.height / 5 +
                           20, text='Catan is a strategy game', font='Chalkduster 10')
        canvas.create_text(data.width / 80 * 71, data.height / 5 +
                           40, text='that allows players to ', font='Chalkduster 10')
        canvas.create_text(data.width / 80 * 71, data.height / 5 +
                           60, text='trade, build, expand.', font='Chalkduster 10')
        canvas.create_text(data.width / 80 * 71, data.height / 5 +
                           80, text='Different colors means', font='Chalkduster 10')
        canvas.create_text(data.width / 80 * 71, data.height / 5 +
                           100, text='different resources.', font='Chalkduster 10')
        canvas.create_text(data.width / 80 * 71, data.height / 5 + 120,
                           text='Light green is wool.', font='Chalkduster 10', fill='red')
        canvas.create_text(data.width / 80 * 71, data.height / 5 + 140,
                           text='Dark red is brick.', font='Chalkduster 10', fill='red')
        canvas.create_text(data.width / 80 * 71, data.height / 5 + 160,
                           text='Gold is grain.', font='Chalkduster 10', fill='red')
        canvas.create_text(data.width / 80 * 71, data.height / 5 +
                           180, text='Grey is ore.', font='Chalkduster 10', fill='red')
        canvas.create_text(data.width / 80 * 71, data.height / 5 + 200,
                           text='Dark green is lumber', font='Chalkduster 10', fill='red')
        canvas.create_text(data.width / 80 * 71, data.height / 5 +
                           220, text='Players are free to use', font='Chalkduster 10')
        canvas.create_text(data.width / 80 * 71, data.height / 5 +
                           240, text='resources that they have', font='Chalkduster 10')
        canvas.create_text(data.width / 80 * 71, data.height / 5 + 260,
                           text='to expand their territories.', font='Chalkduster 10')
        canvas.create_text(data.width / 80 * 71, data.height / 5 + 280,
                           text='Every turn player roll two', font='Chalkduster 10')
        canvas.create_text(data.width / 80 * 71, data.height / 5 +
                           300, text='dices and they get the', font='Chalkduster 10')
        canvas.create_text(data.width / 80 * 71, data.height / 5 +
                           320, text='corresponding resources.', font='Chalkduster 10')
        canvas.create_text(data.width / 80 * 71, data.height / 5 + 360,
                           text='More details can be found..', font='Chalkduster 10', fill='blue')
    if data.ready:
        canvas.create_text(data.width / 2, data.height / 2,
                           text='READY', fill='red', font='Chalkduster 80 bold')

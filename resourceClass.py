# Resource Class

import random
import math



class Resource(object):
    def __init__(self, cx, cy, size, numList, colorList, num, mob=False):
        self.cx = cx; self.cy = cy
        self.size = size
        self.color = colorList[num]
        self.number = numList[num]
        self.oldNumber = numList[num]
        while self.number == 7:
            self.number = random.randint(2,12)
        if self.color == 'OliveDrab1':
            self.resource = 'wool'
        elif self.color == 'brown4':
            self.resource = 'brick'
        elif self.color == 'gold':
            self.resource = 'grain'
        elif self.color == 'grey':
            self.resource = 'ore'
        elif self.color == 'chartreuse4':
            self.resource = 'lumber'
        self.pointList = []
        self.mob = mob
        for i in range(6):
            angle = i*(2*math.pi/6)
            self.pointList.append((cx+size*math.cos(angle), cy-size*math.sin(angle)))
    def draw(self, canvas):
        canvas.create_polygon(self.pointList, fill=self.color, outline='black')
        if not self.mob:
            canvas.create_text(self.cx, self.cy, text=str(self.number), font='Chalkduster 20')
        else:
            canvas.create_text(self.cx, self.cy, text='MOB', font='Chalkduster 20', fill='red')

class Seatile(Resource):
    def __init__(self, cx, cy, size):
        self.cx = cx; self.cy = cy
        self.size = size
        self.color = 'SkyBlue1'
        self.resource = None
        self.pointList = []
        for i in range(6):
            angle = i*(2*math.pi/6)
            self.pointList.append((cx+size*math.cos(angle), cy-size*math.sin(angle)))
    def draw(self, canvas):
        canvas.create_polygon(self.pointList, fill=self.color, outline='black')

class TradingPort(Seatile):
    def __init__(self, cx, cy, size):
        self.cx = cx; self.cy = cy
        self.size = size
        self.pointList = []
        for i in range(6):
            angle = i*(2*math.pi/6)
            self.pointList.append((cx+size*math.cos(angle), cy-size*math.sin(angle)))
        self.trading = True
        self.color = 'SkyBlue1'
        self.resource = None
    def draw(self, canvas):
        canvas.create_polygon(self.pointList, fill=self.color, outline='black')
        canvas.create_text(self.cx, self.cy, text='3:1 Trade', font='Chalkduster 10')

class Desert(Resource):
    def __init__(self, cx, cy, size):
        self.cx = cx; self.cy = cy
        self.size = size
        self.color = 'Orange3'
        self.resource = None
        self.pointList = []
        for i in range(6):
            angle = i*(2*math.pi/6)
            self.pointList.append((cx+size*math.cos(angle), cy-size*math.sin(angle)))
        self.mob = True
    def draw(self, canvas):
        canvas.create_polygon(self.pointList, fill=self.color, outline='black')
        if self.mob:
            canvas.create_text(self.cx, self.cy, text='MOB', font='Chalkduster 20', fill='red')

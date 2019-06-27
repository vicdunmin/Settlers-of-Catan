# Player Class

def isClose (x1, y1, x2, y2):
	return 0 < (x1-x2)**2+(y1-y2)**2 < 64

class Player(object):
    def __init__(self, PID, color):
        self.PID = PID
        self.color = color
        self.resource = {'wool':20, 'brick':20, 'grain':20, 'ore':20, 'lumber':20}
        self.city = 0
        self.moveMob = 0
        self.feast = 0
        self.roadLocation = []
        self.settlementLocation = []
        self.cityLocation = [] 
        self.road = 0
        self.VP = 0
        self.extraVP = 0
        self.settlement = 0
        self.havePort = False
    def findPoint(self, event, data):
    	for resource in data.resourceList:
    		for (x, y) in resource.pointList:
    			if isClose(event.x, event.y, x, y):
    				startX = x
    				startY = y
    				return [startX, startY]



        
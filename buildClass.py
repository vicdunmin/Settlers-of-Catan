# All the building class

class Road(object):
    def __init__(self, x1, y1, x2, y2, PID, color):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.PID = PID
        self.color = color
    def draw(self, canvas):
        canvas.create_line(self.x1,self.y1,self.x2,self.y2,fill=self.color, width=10)


class Settlement(object):
    def __init__(self, cx, cy, PID, color):
        self.cx = cx
        self.cy = cy
        self.PID = PID
        self.color = color
    def draw(self, canvas):
        if self.color == 'yellow':
            canvas.create_polygon(self.cx, self.cy-15, self.cx-10, self.cy, self.cx-10, self.cy+10, self.cx+10, self.cy+10, self.cx+10, self.cy, fill='yellow3')
            canvas.create_polygon(self.cx, self.cy-15, self.cx-10, self.cy, self.cx-25, self.cy-5, self.cx-15, self.cy-20, fill='yellow')
            canvas.create_polygon(self.cx-10, self.cy, self.cx-25, self.cy-5, self.cx-25, self.cy+5, self.cx-10, self.cy+10, fill='yellow2')
        if self.color == 'white':
            canvas.create_polygon(self.cx, self.cy-15, self.cx-10, self.cy, self.cx-10, self.cy+10, self.cx+10, self.cy+10, self.cx+10, self.cy, fill='gray75')
            canvas.create_polygon(self.cx, self.cy-15, self.cx-10, self.cy, self.cx-25, self.cy-5, self.cx-15, self.cy-20, fill='gray95')
            canvas.create_polygon(self.cx-10, self.cy, self.cx-25, self.cy-5, self.cx-25, self.cy+5, self.cx-10, self.cy+10, fill='gray85')
        if self.color == 'blue':
            canvas.create_polygon(self.cx, self.cy-15, self.cx-10, self.cy, self.cx-10, self.cy+10, self.cx+10, self.cy+10, self.cx+10, self.cy, fill='medium blue')
            canvas.create_polygon(self.cx, self.cy-15, self.cx-10, self.cy, self.cx-25, self.cy-5, self.cx-15, self.cy-20, fill='royal blue')
            canvas.create_polygon(self.cx-10, self.cy, self.cx-25, self.cy-5, self.cx-25, self.cy+5, self.cx-10, self.cy+10, fill='RoyalBlue2')
        if self.color == 'pink':
            canvas.create_polygon(self.cx, self.cy-15, self.cx-10, self.cy, self.cx-10, self.cy+10, self.cx+10, self.cy+10, self.cx+10, self.cy, fill='magenta4')
            canvas.create_polygon(self.cx, self.cy-15, self.cx-10, self.cy, self.cx-25, self.cy-5, self.cx-15, self.cy-20, fill='magenta2')
            canvas.create_polygon(self.cx-10, self.cy, self.cx-25, self.cy-5, self.cx-25, self.cy+5, self.cx-10, self.cy+10, fill='magenta3')
        

class City(object):
    def __init__(self, cx, cy, PID, color):
        self.cx = cx
        self.cy = cy
        self.PID = PID
        self.color = color
    def draw(self, canvas):
        if self.color == 'yellow':
            canvas.create_polygon(self.cx, self.cy-15, self.cx-5, self.cy-10, self.cx-5, self.cy, self.cx-10, self.cy, self.cx-10, self.cy+5, self.cx+5, self.cy+5, self.cx+5, self.cy-10, fill='yellow3')
            canvas.create_polygon(self.cx, self.cy-15, self.cx-5, self.cy-10, self.cx-15, self.cy-15, self.cx-10, self.cy-20, fill='yellow')
            canvas.create_polygon(self.cx-5, self.cy-10, self.cx-15, self.cy-15, self.cx-15, self.cy-5, self.cx-5, self.cy, fill='yellow2')
            canvas.create_polygon(self.cx-15, self.cy-5, self.cx-20, self.cy-5, self.cx-10, self.cy, self.cx-5, self.cy, fill='yellow')
            canvas.create_polygon(self.cx-20, self.cy-5, self.cx-20, self.cy, self.cx-10, self.cy+5, self.cx-10, self.cy, fill='yellow2')
        if self.color == 'white':
            canvas.create_polygon(self.cx, self.cy-15, self.cx-5, self.cy-10, self.cx-5, self.cy, self.cx-10, self.cy, self.cx-10, self.cy+5, self.cx+5, self.cy+5, self.cx+5, self.cy-10, fill='gray75')
            canvas.create_polygon(self.cx, self.cy-15, self.cx-5, self.cy-10, self.cx-15, self.cy-15, self.cx-10, self.cy-20, fill='gray95')
            canvas.create_polygon(self.cx-5, self.cy-10, self.cx-15, self.cy-15, self.cx-15, self.cy-5, self.cx-5, self.cy, fill='gray85')
            canvas.create_polygon(self.cx-15, self.cy-5, self.cx-20, self.cy-5, self.cx-10, self.cy, self.cx-5, self.cy, fill='gray95')
            canvas.create_polygon(self.cx-20, self.cy-5, self.cx-20, self.cy, self.cx-10, self.cy+5, self.cx-10, self.cy, fill='gray85')
        if self.color == 'blue':
            canvas.create_polygon(self.cx, self.cy-15, self.cx-5, self.cy-10, self.cx-5, self.cy, self.cx-10, self.cy, self.cx-10, self.cy+5, self.cx+5, self.cy+5, self.cx+5, self.cy-10, fill='medium blue')
            canvas.create_polygon(self.cx, self.cy-15, self.cx-5, self.cy-10, self.cx-15, self.cy-15, self.cx-10, self.cy-20, fill='royal blue')
            canvas.create_polygon(self.cx-5, self.cy-10, self.cx-15, self.cy-15, self.cx-15, self.cy-5, self.cx-5, self.cy, fill='RoyalBlue2')
            canvas.create_polygon(self.cx-15, self.cy-5, self.cx-20, self.cy-5, self.cx-10, self.cy, self.cx-5, self.cy, fill='royal blue')
            canvas.create_polygon(self.cx-20, self.cy-5, self.cx-20, self.cy, self.cx-10, self.cy+5, self.cx-10, self.cy, fill='RoyalBlue2')
        if self.color == 'pink':
            canvas.create_polygon(self.cx, self.cy-15, self.cx-5, self.cy-10, self.cx-5, self.cy, self.cx-10, self.cy, self.cx-10, self.cy+5, self.cx+5, self.cy+5, self.cx+5, self.cy-10, fill='magenta4')
            canvas.create_polygon(self.cx, self.cy-15, self.cx-5, self.cy-10, self.cx-15, self.cy-15, self.cx-10, self.cy-20, fill='magenta2')
            canvas.create_polygon(self.cx-5, self.cy-10, self.cx-15, self.cy-15, self.cx-15, self.cy-5, self.cx-5, self.cy, fill='magenta3')
            canvas.create_polygon(self.cx-15, self.cy-5, self.cx-20, self.cy-5, self.cx-10, self.cy, self.cx-5, self.cy, fill='magenta2')
            canvas.create_polygon(self.cx-20, self.cy-5, self.cx-20, self.cy, self.cx-10, self.cy+5, self.cx-10, self.cy, fill='magenta3')
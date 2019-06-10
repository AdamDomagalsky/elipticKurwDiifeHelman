

class Point():

    def __init__(self, x=float('inf'), y=float('inf'), p=1, a = 0, b = 0):
        self.x = x
        self.y = y
        self.p = p
        self.a = a
        self.b = b

    def neg(self):
        return Point(self.x, self.y)

    def copy(self):
        return Point(self.x, self.y)

    def is_zero(self):
        return False
        return self.x > 1e20 or self.x < -1e20
    
    def dbl(self):
        if self.is_zero():
            return self.copy()
        try:
            s = (3 * pow(self.x,2) + self.a) // (2 * self.y)
        except ZeroDivisionError:
            return Point()
        x3 = pow(s,2) - 2 * self.x
        y3 = s*(self.x - x3) - self.y
        return Point(x3, y3)

    def add(self, q):
        if self.x == q.x and self.y == q.y:
            return self.dbl()
        if self.is_zero():
            return q.copy()
        if q.is_zero():
            return self.copy()
        try:
            s = (q.y - self.y) / (q.x - self.x)
        except ZeroDivisionError:
            return Point()
        x3 = pow(s,2,self.p) - self.x - q.x
        y3 = (s*(self.x - x3))%self.p - q.y
        
        return Point(x3, y3)

    def __str__(self):
        return "({:.3f}, {:.3f})".format(self.x, self.y)
        
    

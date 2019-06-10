from Crypto.Util import number


class Curve(object):
    eliptic_function = staticmethod(lambda a, b, x, p: (pow(x, 3, p) + (a * x) % p + b) % p)
    getRandom = staticmethod(lambda p: number.getRandomRange(0, p - 1))

    def __init__(self, init_prime_size=256):
        self.init_prime_size = init_prime_size
        self.a = 0
        self.b = 0
        self.p = 0
        self.exampleX = 0
        self.exampleY = 0
        self.generate_function()


    def generate_ec_xy_example(self):
        x = self.getRandom(self.p)
        y = pow(self.eliptic_function(self.a, self.b, x, self.p), (self.p + 1) // 4, self.p)
        if self.contains_point(x, y):
            return x, y
        else:
            return self.generate_ec_xy_example()


    def generate_function(self):
        p = number.getPrime(self.init_prime_size)
        self.p = p
        if p % 4 != 3:
            # print('p nie przytaje do 3 mod 4')
            return self.generate_function()


        a = self.getRandom(p)
        b = self.getRandom(p)
        self.a = a
        self.b = b
        x = self.getRandom(p)

        delta = lambda a, b: ((4 * pow(a, 3, p)) % p + (27 * pow(b, 2, p)) % p) % p

        if delta(a, b) == 0:
            print('delta == 0')
            return self.generate_function()

        if 1 != pow(self.eliptic_function(a, b, x, p), (p - 1) // 2, p):
            # print('f nie jest reszta kwadratowa p')
            return self.generate_function()

        y = pow(self.eliptic_function(a, b, x, p), (p + 1) // 4, p)

        if self.isQuatraticResidue(x) == False:
            print('This is not quadratic residue')
            return self.generate_function()

        if self.contains_point(x, y):
            self.a = a
            self.b = b
            self.p = p
            self.exampleX = x
            self.exampleY = y
        else:
            return self.generate_function()

    def getCurveValue(self, x):
        return (pow(x, 3, self.p) + (self.a * x) + self.b) % self.p

    def isQuatraticResidue(self, x):
        return pow(self.getCurveValue(x), (self.p - 1) // 2, self.p) == 1

    def contains_point(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], Point):
            return self.__check_point(args[0].x, args[0].y)
        elif len(args) == 0 and isinstance(kwargs.get('point', None), Point):
            return self.__check_point(kwargs.get('point').x, kwargs.get('point').y)
        elif len(args) == 2:
            return self.__check_point(args[0], args[1])
        elif kwargs.get('x', None) and kwargs.get('y', None):
            return self.__check_point(kwargs['x'], kwargs['y'])
        else:
            raise BaseException('bad args')

    def __check_point(self, x, y):
        """Is the point (x,y) on this curve?"""
        return (y * y - self.eliptic_function(self.a, self.b, x, self.p)) % self.p == 0

    def __str__(self):
        return f"Curve(\n\tp={self.p},\n\ta={self.a},\n\tb={self.b}\n)"


class Point(object):

    def __init__(self, curve=None, x=None, y=None):
        self.x = x
        self.y = y
        self.curve = curve

    def __eq__(self, other):
        return (
                self.curve == other.curve and
                self.x == other.x and
                self.y == other.y
        )

    @staticmethod
    def inverse_mod(a, m):
        """Inverse of a mod m."""

        if a < 0 or m <= a:
            a = a % m

        # From Ferguson and Schneier, roughly:

        c, d = a, m
        uc, vc, ud, vd = 1, 0, 0, 1
        while c != 0:
            q, c, d = divmod(d, c) + (c,)
            uc, vc, ud, vd = ud - q * uc, vd - q * vc, uc, vc

        # At this point, d is the GCD, and ud*a+vd*m = d.
        # If d == 1, this means that ud is a inverse.

        assert d == 1
        if ud > 0:
            return ud
        else:
            return ud + m

    def double(self):
        if self == INFINITY:
            return INFINITY

        p = self.curve.p
        a = self.curve.a

        l = ((3 * self.x * self.x + a) * self.inverse_mod(2 * self.y, p)) % p

        x3 = (pow(l, 2, p) - 2 * self.x) % p
        y3 = (l * (self.x - x3) - self.y) % p

        return Point(self.curve, x3, y3)

    def __add__(self, other):
        if (self or other) is INFINITY:
            return INFINITY
        assert self.curve == other.curve

        if self.x == other.x:
            if (self.y + other.y) % self.curve.p == 0:
                return INFINITY
            else:
                return self.double()

        p = self.curve.p

        l = ((other.y - self.y) * self.inverse_mod(other.x - self.x, p)) % p

        x3 = (pow(l, 2, p) - self.x - other.x) % p
        y3 = (l * (self.x - x3) - self.y) % p

        return Point(self.curve, x3, y3)

    def negate(self):
        return Point(self.curve, self.x, -self.y)

    # def __rmul__(self, other):
    #     """Multiply a point by an integer."""
    #
    #     return self * other

    def __mul__(self, other):
        if isinstance(other, Point):
            return self.__mul_point__(other)
        elif isinstance(other, int):
            return self.__mul_int__(other)

    def __mul_int__(self, n, acc = False):
        if not acc:
            acc = self
        if n == 0:
            return INFINITY
        if n == 1:
            return acc
        if n % 2 == 1:
            return self.__mul_int__(n - 1, self.__add__(acc))  # addition when n is odd

        return self.__mul_int__(n / 2, acc.double())  # doubling when n is even

    def __mul_point__(self, other):
        def leftmost_bit(x):
            assert x > 0
            result = 1
            while result <= x:
                result *= 2
            return result // 2

        e = other.x
        # if self.order:
        #     e = e % self.order
        if e == 0:
            return INFINITY
        if self == INFINITY:
            return INFINITY
        assert e > 0

        e3 = 3 * e
        negative_self = self.negate()
        i = leftmost_bit(e3) // 2
        result = self

        while i > 1:
            result = result.double()
            if (e3 & i) != 0 and (e & i) == 0:
                result = result + self
            if (e3 & i) == 0 and (e & i) != 0:
                result = result + negative_self
            i = i // 2

        return result

    def __str__(self):
        if self == INFINITY:
            return "infinity"
        else:
            return f'({self.x}, {self.y})'


INFINITY = Point(None, None, None)

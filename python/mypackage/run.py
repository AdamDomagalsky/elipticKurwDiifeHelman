#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from Crypto.Util import number
# from point import Point
# from curde import Point
from curde import Curve, Point

# coding=utf-8
'''
    1. Losowanie P
    2. losowanie a,b,x z [0,p-1] (p~256 bitów)
        f(x) = x**3 + ax + b (mod p)
    3. Jesli f/p == 1 to y = f**(p+1)/4 mod p
    3. (f/p) == 1 <=> f^(p-1)/2 ===== 1 mod p 

    p = (x,y)

    E: Y**2 = x**3 + ax + b
'''

INIT_PRIME_SIZE = 7


def test_all():
    e_curve = Curve()
    # print(e_curve)

    point1 = Point(e_curve, e_curve.exampleX, e_curve.exampleY)
    assert point1 == point1
    # print(point1)
    doubled_point1 = point1 + point1
    assert e_curve.contains_point(doubled_point1)
    assert e_curve.contains_point(point1*point1)
    assert e_curve.contains_point(point1)
    assert e_curve.contains_point(point=point1)
    assert e_curve.contains_point(point1.x, point1.y)
    assert e_curve.contains_point(x=point1.x, y=point1.y)
    # print(e_curve.contains_point(point1*point1))
    # print(e_curve.contains_point(point1))
    # print(e_curve.contains_point(point=point1))
    # print(e_curve.contains_point(point1.x, point1.y))
    # print(e_curve.contains_point(x=point1.x, y=point1.y))

def dh_test(eliptic_curve: Curve, point: Point):
    alice_ka = number.getRandomRange(0, eliptic_curve.p)
    bob_kb = number.getRandomRange(0, eliptic_curve.p)

    alice_pa = point * alice_ka
    bob_pb = point * bob_kb

    bob_point= alice_pa * bob_kb
    alice_point = bob_pb * alice_ka

    assert eliptic_curve.contains_point(bob_point)
    assert eliptic_curve.contains_point(alice_point)
    assert bob_point == alice_point
    shared_secret = bob_point

    print('DF test passed!')

    return shared_secret


def main():
    eliptic_curve = Curve()
    x2,y2 = eliptic_curve.generate_ec_xy_example()
    #Addition
    P = Point(eliptic_curve,eliptic_curve.exampleX ,eliptic_curve.exampleY)
    Q = Point(eliptic_curve, x2, y2)
    print(f'EC cointaines point   P: {eliptic_curve.contains_point(P)}')
    print(f'EC cointaines point   Q: {eliptic_curve.contains_point(Q)}')
    print(f'EC cointaines point P+Q: {eliptic_curve.contains_point(P+Q)}')
    print(f'EC cointaines point P+P: {eliptic_curve.contains_point(P+P)}')
    # print(f'EC cointaines point P*P: {eliptic_curve.contains_point(P*P)}')
    print(f'EC cointaines point P*9: {eliptic_curve.contains_point(P*9)}')

    dh_test(eliptic_curve, P)








if __name__ == '__main__':
    test_all()
    main()








from z3 import *
import string

#MEGLIO USARE UN BIT VECTOR

c0 = z3.Int('c0')
c1 = z3.Int('c1')
c2 = z3.Int('c2')
c3 = z3.Int('c3')
c4 = z3.Int('c4')
c5 = z3.Int('c5')
c6 = z3.Int('c6')
c7 = z3.Int('c7')
c8 = z3.Int('c8')
c9 = z3.Int('c9')
c10 = z3.Int('c10')
c11 = z3.Int('c11')
c12 = z3.Int('c12')
c13 = z3.Int('c13')
c14 = z3.Int('c14')
c15 = z3.Int('c15')
c16 = z3.Int('c16')
c17 = z3.Int('c17')
c18 = z3.Int('c18')
c19 = z3.Int('c19')
c20 = z3.Int('c20')
c21 = z3.Int('c21')
c22 = z3.Int('c22')
c23 = z3.Int('c23')
c24 = z3.Int('c24')
c25 = z3.Int('c25')
c26 = z3.Int('c26')
c27 = z3.Int('c27')
c28 = z3.Int('c28')

def positive():
    return z3.And(c1>0, c2>0, c3>0, c4>0, c5>0, c6>0, c7>0, c8>0, c9>0, c10>0, c11>0, c12>0, c13>0, c14>0, c15>0, c16>0, c17>0, c18>0, c19>0, c20>0, c21>0, c22>0, c23>0, c24>0, c25>0, c26>0, c27>0, c28>0)

def check01():
    return z3.And(c5 == 45, c11 == 45, c17 == 45, c23 == 45)


def check02():
    return z3.And(c1-0x30<10, c4-0x30<10, c6-0x30<10, c9-0x30<10, c15-0x30<10, c18-0x30<10, c22-0x30<10, c27-0x30<10,c28-0x30<10)

def check03():
    return z3.And((c4-0x30) == ((c1-0x30) * 2 + 1), (7 < c4-0x30), (c9 == (c4 - (c1-0x30)) + 2))

def check04():
    return ((c27 + c28) % 0xd == 8)

def check05():
    return ((c27 + c22) % 0x16 == 0x12)


def check06():
    return ((c18 + c22) % 0xb == 5)


def check07():
    return ((c28 + c22 + c18) % 0x1a == 4)


def check08():
    return ((c1 + c6 * c4) % 0x29 == 5)

    return ((iVar2 + uVar1 & 3) - uVar1 == 1)


def check09():
    iVar2 = c15 - c28
    uVar1 = (z3.Int2BV(iVar2,8) >> 0x1f) >> 0x1e
    uVar2 = z3.Int2BV(iVar2, 8)
    return ((uVar2 + uVar1 & 3) - uVar1 == 1)


def check0A():
    iVar2 = c4 + c22
    uVar1 = (z3.Int2BV(iVar2,8) >> 0x1f) >> 0x1e
    uVar2 = z3.Int2BV(iVar2,8)
    return ((uVar2 + uVar1 & 3) - uVar1 == 3)


def check0B():
    return (z3.And((c20 == 66) , ( c21 == 66)))


def check0C():
    return ((c6 + c9 * c15) % 10 == 1)


def check0D():
    iVar1 = c27 + c4 + c15 - 0x12
    iVar1 = z3.Int2BV(iVar1, 8)
    uVar2 = (iVar1 >> 0x1f) >> 0x1c
    return ((iVar1 + uVar2 & 0xf) - uVar2 == 8)


def check0E():
    iVar2 = c28 - c9
    iVar2 = z3.Int2BV(iVar2, 8)
    iVar1 = iVar2 >> 0x1f
    return ((iVar2 - iVar1 & 1) + iVar1 == 1)


def check0F():
    return c0 == 77




solver = z3.Solver()
solver.add(positive())
solver.add(check01())
solver.add(check02())
solver.add(check03())
solver.add(check04())
solver.add(check05())
solver.add(check06())
solver.add(check07())
solver.add(check08())
solver.add(check09())
solver.add(check0A())
solver.add(check0B())
solver.add(check0C())
solver.add(check0D())
solver.add(check0E())
solver.add(check0F())

solver.check()

m = solver.model()
print(m)

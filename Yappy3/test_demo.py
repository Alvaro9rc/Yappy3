import unittest
from demo import *


class TestDemo(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.expresion1 = "2-24*9"
        self.resultado1 = -214
        self.expresion2 = "2-24*9-34*2+1"
        self.resultado2 = -281
        self.expresion3 = "a+b*"
        self.resultado3 = "(a+(b*))"

    def test_SimpleExpAmb(self):
        d = SimpleExpAmb()
        self.assertEqual(self.resultado1, d.input(self.expresion1), "Deberia dar -214") 
        self.assertEqual(self.resultado2, d.input(self.expresion2), "Deberia dar -281")

    def test_RegExp2(self):
        d = RegExp2()
        self.assertEqual(self.resultado3,d.input(self.expresion3),"Deberia dar (a+(b*))")

if __name__ == '__main__':
    unittest.main()

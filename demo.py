# -*- coding: utf-8 -*-
#
# 
# This is part of Yappy
#
#
# demo.py -- some simple parsers
#
# Copyright (C) 2000-2003 Rogério Reis & Nelma Moreira {rvr,nam}@ncc.up.pt
#           (conversion to python3 by Álvaro Rodríguez Carpintero alvaro9rocar@gmail.com)

#from yappy.parser import *
import operator
import sys, string

from parser import *

############## Demos  #####################

class SimpleExp(Yappy):
    """ A parser  for simple arithmetic expresssion. Allows blanks
    between tokens"""
    def __init__(self,no_table=0, table='saexp.tab'):
        grammar = grules([
                ("E -> E + T", self.Add),
                ("E ->T", DefaultSemRule),
                ("T -> T * F", self.Mul ),
                ("T -> F", DefaultSemRule),
                ("F -> ( E )", self.ParSemRule),
                ("F -> id", DefaultSemRule)]
                         )
        tokenize=[("\s+",""),
               ("\d+",lambda x: ("id",int(x))),
               ("\+",lambda x: (x,x)),
               ("\*",lambda x: (x,x)),
               ("\(|\)",lambda x: (x,x)) ]
        Yappy.__init__(self,tokenize,grammar,table,no_table,
    tmpdir='/tmp')
        
    
    def ParSemRule(self,list,context=None):
        return list[1]

    def DoPrint(self,list,context=None):
        print(list[0])
        return list[0]

    def Add(self,list,context):
        print(list)
        return list[0] + list[2]

    def Mul(self,list,context):
        print(list)
        return list[0] * list[2]

    def test(self):
        st = " 2 + 24 + 34 * 2 + 1"
        print("Input: %s" %st)
        print("Result:", self.input(st))   

class SimpleExp3(SimpleExp):
    """ A parser  for simple arithmetic expresssion. Allows blanks
    between tokens"""
    def __init__(self,no_table=0, table='saexp.tab'):
        grammar = """ 
                E -> E + T {{ "sum([$0,$2])"}};
                E ->T ;
                T -> T * F" {{ self.Mul }};
                T -> F ;
                F -> ( E ) {{ self.ParSemRule}};
                F -> id;
                """
        tokenize=[("\s+",""),
               ("\d+",lambda x: ("id",int(x))),
               ("\+",lambda x: (x,x)),
               ("\*",lambda x: (x,x)),
               ("\(|\)",lambda x: (x,x)) ]
        Yappy.__init__(self,tokenize,grammar,table,no_table)
        
class SimpleExp1(Yappy):
    """ A parser  for simple arithmetic expresssions, with operators """
    def __init__(self,no_table=0, table='saexp1.tab', tabletype=LALRtable,noconflicts=1,expect=0):
        grammar = grules([
                ("E -> E add_op T", self.Add),
                ("E ->T", DefaultSemRule),
                ("T -> T mul_op F", self.Mul),
                ("T -> F", DefaultSemRule),
                ("F -> ( E )", self.ParSemRule),
                ("F -> id", DefaultSemRule)])

        tokenize=[("\d+",lambda x: ("id",int(x))),
               ("[+-]",lambda x: ("add_op",self.make_op(x))),
               ("[*/]",lambda x: ("mul_op",self.make_op(x))),
               ("\(|\)",lambda x: (x,x)) ]
        Yappy.__init__(self,tokenize,grammar,table,no_table,tabletype,noconflicts,expect)

    def make_op(self,op):
        return {"+"  : operator.add,
		'-'  : operator.sub,
                '*'   : operator.mul,
                '/'   : operator.ifloordiv,
                '%'   : operator.mod
                }[op]
    
    def ParSemRule(self,list,context=None):
        return list[1]

    def DoPrint(self,list,context=None):
        print(list[0])
        return list[0]

    def Add(self,list,context):
        print(list)
        return list[1](*[list[0],list[2]])

    def Mul(self,list,context):
        print(list)
        return list[1](*[list[0],list[2]])

    def test(self):
        st = "2-24*9"
        st1 = "2-24*9-34*2+1"
        print("Input: %s" %st)
        print("Result:", self.input(st))


class SimpleExp2(SimpleExp1):
    """ A parser  for simple arithmetic expresssions with prec and associativity"""
    def __init__(self,no_table=0, table='saexp2.tab',
    tabletype=LALRtable,noconflicts=1,expect=0):
        self.line = 0
        grammar = grules([
                ("E -> E add_op T", self.Add),
                ("E ->T", DefaultSemRule),
                ("T -> T mul_op F", self.Mul),
                ("T -> F", DefaultSemRule),
                ("F -> ( E )", self.ParSemRule),
                ("F -> id", DefaultSemRule)])

        tokenize=[("\d+",lambda x: ("id",int(x))),
                  ("\n+",lambda x: (x,self.countline())),
               ("[+-]",lambda x: ("add_op",self.make_op(x)),("add_op",100,'left')),
               ("[*/]",lambda x: ("mul_op",self.make_op(x)),("mul_op",200,'left')),
               ("\(|\)",lambda x: (x,x)) ]
        Yappy.__init__(self,tokenize,grammar,table,no_table,tabletype,noconflicts,expect)
        

    def countline(self):
        self.line+=1
        return ""
    
    def make_op(self,op):
        """ """
        return {"+"  : operator.add,
		'-'  : operator.sub,
                '*'   : operator.mul,
                '/'   : operator.ifloordiv,
                '%'   : operator.mod
                }[op]
    
    def ParSemRule(self,list,context=None):
        return list[1]

    def DoPrint(self,list,context=None):
        print(list[0])
        return list[0]

    def Add(self,list,context):
        print(list)
        return list[1](*[list[0],list[2]])

    def Mul(self,list,context):
        print(list)
        return list[1](*[list[0],list[2]])

class SimpleExpAmb(SimpleExp2):
    """A parser  for simple arithmetic expresssions with an ambiguous grammar """
    def __init__(self,no_table=0, table='expamb.tab',tabletype=LALRtable,noconflicts=1,expect=0):
        grammar = grules([
                ("E -> E add_op E", self.Add),
                ("E -> E mul_op E", self.Mul),
                ("E -> ( E )", self.ParSemRule),
                ("E -> id", DefaultSemRule)])

        sinal = "[+-]"
        integer ="\d" 
        tokenize=[("(%s)+"%integer,lambda x: ("id",int(x))),
               (sinal,lambda x: ("add_op",self.make_op(x)),("add_op",100,'left')),
               ("[*/]",lambda x: ("mul_op",self.make_op(x)),("mul_op",200,'left')),
               ("\(|\)",lambda x: (x,x)) ]

        Yappy.__init__(self,tokenize,grammar,table,no_table,tabletype,noconflicts,expect)


class SimpleExpAmb2(SimpleExp2):
    """A parser  for simple arithmetic expresssions with an ambiguous
    grammar, and context-dependent precedence """
    def __init__(self,no_table=0, table='expamb.tab',tabletype=LALRtable,noconflicts=1,expect=0):
        grammar = grules([
                ("E -> E add_op E", self.Add),
                ("E -> E mul_op E", self.Mul),
                ("E -> n_op E", lambda l,c: -1*l[1]),
                ("E -> ( E )", self.ParSemRule),
                
                ("E -> id", DefaultSemRule)])

        plus = "[+-]"
        integer = "\d" 
        tokenize=[("(%s)+"%integer,lambda x: ("id",int(x))),
               ("%s"%plus,lambda x:
                ("add_op",self.make_op(x)),("add_op",100,'left')),
                ("~",lambda x: ("n_op",self.make_op('-')),("n_op",300,'left')),
               ("[*/]",lambda x: ("mul_op",self.make_op(x)),("mul_op",200,'left')),
               ("\(|\)",lambda x: (x,x)) ]

        Yappy.__init__(self,tokenize,grammar,table,no_table,tabletype,noconflicts,expect)
    def test(self):
        st=[
         "~2",
        "2-24*9",
        "2-24*9-34*2+1",
        "~2-24*9-34*2+1",
         "2+3+(~5*(2+3)*2)-24*9-34*2+1"
         ]
        for i in st:
            print("Input: %s" %i)
            print("Result:", self.input(i))


class ListAVG(Yappy):
    """A parser  for transforming a list atrib=value into a python dictionary """
    def __init__(self,no_table=0, table='Listavg.tab'):
        grammar =   """
            E -> ( ) {{self.EmptyDict}};
            E ->  ( AVL ) {{self.ParSemRule}} ;
            AVL ->   AV , AVL  | AV {{EmptySemRule}} ;
            AV -> tok = tok {{ self.AddItem }};
            """
    
        tokenize = [
             ("\s+",""),
             ("[A-Za-z0-9]+",lambda x: ("tok",x)),
             ("\=",lambda x: (x,x)),
             (",",lambda x: (x,x)),
             ("\(|\)",lambda x: (x,x)) ]

        Yappy.__init__(self,tokenize,grammar,table,no_table)


    def ParSemRule(self,list,context=None):
        return list[1]

    def DoPrint(self,list,context=None):
        print(list[0])
        return list[0]


    def EmptyDict(self,list,context):
        return []

    def AddItem(self,list,context):
        if not isinstance(list[0], string):
            raise NameError("Key %s must be a string" % list[0]) 
        context[list[0]] = list[2] 
        return []

    def test(self):
        st = "(a=5,b=6,c=7)"
        print("Input: %s" %st)      
        self.input(st,context={})
        print(self.context)

class ListAVG1(ListAVG):
    """A parser  for transforming a list atrib=value into a python dictionary """
    def __init__(self,no_table=0, table='Listavg1.tab'):
        grammar =   """
            E -> ( ) {{self.EmptyDict}};
            E -> ( AVL ) {{self.ParSemRule}} ;
            AVL ->   AV , AVL   | AV {{EmptySemRule}} ;
            AV -> tok = tok {{ self.AddItem }};
            """
        tokenize = [
             ("\s+",""),
             ("[A-Za-z0-9]+",lambda x: ("tok",x)),
             ("\=",lambda x: (x,x)),
             (",",lambda x: (x,x)),
             ("\(|\)",lambda x: (x,x)) ]

        Yappy.__init__(self,tokenize,grammar,table,no_table)
        
class ListAVG2(ListAVG):
    """A parser  for transforming a list atrib=value into a python dictionary """
    def __init__(self,no_table=0, table='Listavg1.tab'):
        grammar =   """
            E -> ( AVL ) {{self.ParSemRule}} ;
            AVL ->   AV , AVL  {{DefaultSemRule}} | ;
            AV -> tok = tok {{ self.AddItem }};
            """
        tokenize = [
             ("\s+",""),
             ("[A-Za-z0-9]+",lambda x: ("tok",x)),
             ("\=",lambda x: (x,x)),
             (",",lambda x: (x,x)),
             ("\(|\)",lambda x: (x,x)) ]

        Yappy.__init__(self,tokenize,grammar,table,no_table)


    def test(self):
        st = "(a=5,b=6,c=7,)"
        
        print("Input: %s" %st)      
        self.input(st,context={})
        print(self.context)

        
class RegExp(Yappy):
     def __init__(self,no_table=0, table='regamb.tab',
     tabletype=LALRtable,
                  noconflicts=1,expect=0):
        """ A parser for regular expressions with operators. Semantic
     rules are dummy..."""
        grammar = grules([("r -> r | r",self.OrSemRule),
                        ("r -> r . r",self.ConcatSemRule),
                    ("r -> r *",self.StarSemRule, (300,'left')),
                    ("r -> ( r )",self.ParSemRule),
                    ("r -> id",self.BaseSemRule),
                   ])
        tokenize =[
                    ("[A-Za-z0-9]",lambda x: ("id",x)),
                    ("[+|]",lambda x: ("|",x),("|",100,'left')),
                    ("[\.]",lambda x: (".",""),(".",200,'left')),
                    ("[*]",lambda x: (x,x), ("*",300,'left')),
                    ("\(|\)",lambda x: (x,x)) ]
        Yappy.__init__(self,tokenize,grammar,table,no_table,tabletype)

     ##Semantic rules build a parse tree...
     def OrSemRule(self,list,context):
         return "(%s+%s)" %(list[0],list[2])

     def ConcatSemRule(self,list,context):
         return "(%s%s)" %(list[0],list[2])

     def ParSemRule(self,list,context):
         return "(%s)" %list[1]

     def BaseSemRule(self,list,context):
         return list[0]

     def StarSemRule(self,list,context):
         return "(%s*)" %list[0]

     def test(self):
         st  = ["(a+b)*.a.a.b*",
                "a+a.b+a.b.(a+a)*",
                "a+a.b+a.(a+a)**",
                 "a+a.b.c",
                "a+a.b.(c+b)",
                "a+a.b.(c+b)*",
                 "a+a.b*.(a+b)"]
         for i in st:
             print("Input: %s" %i)
             print(self.input(i))

class RegExp1(RegExp):
     def __init__(self,no_table=0, table='tableambreg1',tabletype=LALRtable,
                  noconflicts=1,expect=0):
        """A parser for regular expressions with ambiguous rules  """
        grammar = grules([("reg -> reg + reg",self.OrSemRule),
                                ("reg -> reg reg",self.ConcatSemRule,(200,'left')),
                               ("reg -> reg *",self.StarSemRule),
                               ("reg -> ( reg )",self.ParSemRule),
                               ("reg -> id",self.BaseSemRule)
                   ])
        tokenize =[
                    ("[A-Za-z0-9]",lambda x: ("id",x)),
                    ("[+|]",lambda x: ("+",x),("+",100,'left')),
                    ("[*]",lambda x: (x,x)),
                    ("\(|\)",lambda x: (x,x)) ]
        Yappy.__init__(self,tokenize,grammar,table,no_table,tabletype,noconflicts,expect)
        
     def ConcatSemRule(self,list,context=None):
         return "(%s%s)" %(list[0],list[1])


     def test(self):
         st  = ["(a+b)*aab*",
                "(a+ab)*a*",
                "(a+a)a+ab",
                "a+ab+(a(a+a)*)*",
                "a+ab+a(a+a)**",
                "(a+a)**ab(a+b)**",
                "aa+bb**",
                "(a+ab)(a+ab)(ac+a)",
                "a+abc+ad",
                "abc+b+ad",
                "a+ab",
                "a+b+ab+cccaaaaaa",
                "a+ab(a+a)",
                "ab+ab(a+a)a*",
                "a+ab*",
                "(a+ab*(a+b))*",
                "a+ab*(a+b)",
                "a+c+ab(a+b)",
                "a+c+(a+b)ab",
                "a+b*",
                "aa+b*",
                "aab*ab+a*+aa",
                "aab*ab**+(a+aa)**"
                ]
         for i in st:
             print("Input: %s" %i)
             print(self.input(i))


class RegExp2(RegExp1):
     def __init__(self,no_table=0, table='tableambreg2'):
         grammar = """
        reg -> reg + reg {{ self.OrSemRule }} |
               reg reg {{ self.ConcatSemRule}} // 200 left|
               reg * {{ self.StarSemRule }} |
               ( reg ) {{self.ParSemRule }} |
               id {{ self.BaseSemRule }} ;
        """
         tokenize = [("@epsilon",lambda x: ("id",x)),
                    ("@empty_set",lambda x: ("id",x)),
                    ("[A-Za-z0-9]",lambda x: ("id",x)),
                    ("[+|]",lambda x: ("+",x),("+",100,'left')),
                    ("[*]",lambda x: (x,x)),
                    ("\(|\)",lambda x: (x,x)) ]

         Yappy.__init__(self,tokenize,grammar,table,no_table)

class RegExp3(RegExp):
     def __init__(self,no_table=0, table='tableambreg3'):
        """A erronous parser for regular expressions with ambiguous rules and
     no precedence information """
        grammar = grules([("reg -> reg | reg",self.OrSemRule),
                                ("reg -> reg reg",self.ConcatSemRule),
                               ("reg -> reg *",self.StarSemRule),
                               ("reg -> ( reg )",self.ParSemRule),
                               ("reg -> id",self.BaseSemRule),
                   ])
        tokenize =[
                    ("[A-Za-z0-9]",lambda x: ("id",x)),
                    ("[+|]",lambda x: ("|",x)),
                    ("[*]",lambda x: (x,x)),
                    ("\(|\)",lambda x: (x,x)) ]
        Yappy.__init__(self,tokenize,grammar,table,no_table,LALRtable,1)
        
     def ConcatSemRule(self,list,context=None):
         return list[0]+list[1]

     def test(self):
         st  = "(a+b)*aab*"
         print("Input: %s" %st)
         print(self.input(st))
        
def Sum(a,b):
    return a+b

def curry(f,*a,**kw):
    def curried(*more_a,**more_kw):
        return f(*(a+more_a),**dict(kw,**more_kw))
    return curried

if __name__ == '__main__':
    d = SimpleExpAmb()
    st = "2-24*9"
    print("Input:", st)
    print("Result:", d.input(st))
    st = "2-24*9-34*2+1"
    print("Input:", st)
    print("Result:", d.input(st))
    d = RegExp2()
    print("Result:", d.input("a+b*"))

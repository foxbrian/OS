#!/usr/bin/python

import sys
import tkinter 

help_menu = """

"""


class Binary_Tree:
    class _Node:
        def __init__(self,data):
            self.data = data
            self.parent = None
            self.left = None
            self.right = None
            

        def add_left(self,left):
            
            self.left = left
            

        def add_right(self,right):
            self.right = right

    def __init__(self,data):
        if isinstance(data,self._Node):
            self.root = data
        else:
            self.root = self._Node(data)
    
    def left(self):
        return Binary_Tree(self.root.left)

    def right(self):
        return Binary_Tree(self.root.right)

    def add_left(self,data):
        if isinstance(data,Binary_Tree):
            self.root.add_left(data.root)
        else:
            self.root.add_left(self._Node(data))
    
    def add_right(self,data):
        if isinstance(data,Binary_Tree):
            self.root.add_right(data.root)
        else:
            self.root.add_right(self._Node(data))
    
    def right_parent(self,data):
        temp = self._Node(data)
        temp.add_left(self.root)
        self.root = temp

    def left_parent(self,data):
        temp = self._Node(data)
        temp.add_right(self.root)
        self.root = temp

    def has_right(self):
        return not self.root.right == None

    def has_left(self):
        return not self.root.left == None

    def evaluate(self):
        '''
        assuming the tree is valid
        tree is valid if every leaf is a value and root is an operation
        '''
        if isinstance(self.root.data,float)or isinstance(self.root.data,int):
            return self.root.data
        if(isinstance(self.root.data,Operation)):
            return self.root.data.evaluate(self.left().evaluate(),self.right().evaluate())

    def __str__(self):
        return self.root.data.__str__()

class Operation:

    def __init__(self, op):
        if(op in {'^','*','/','+','-'}):
            self.op = op

    def evaluate(self,left,right):
        return{
            '^':left**right,
            '*':left*right,
            '/':left/right,
            '+':left+right,
            '-':left-right,
        }[self.op]

    def equals(self,char):
        if self.op == char:
            return True
        return False

    def __str__(self):
        return self.op 

def trim(s):
    chars = list(s)
    for i in range(len(s)-1,-1,-1):
        if not (chars[i] == " " or chars[i]=="\t"):
            string = ""
            for char in chars[:i+1]:
                string = string + char
            return string
            
    return ""

def print_tree(tree):
    levels = _print_tree(tree)
    strings = []
    tabs = 0
    for i in range(len(levels)):
        strings.append(tabs*"\t" )
        tabs = tabs*2+1
        for t in levels[-(i+1)]:
            strings[i] = strings[i] +(t.root.data.__str__() if isinstance(t,Binary_Tree) else "") + (tabs+1)*"\t"
    
    s = ""
    for i in range(len(strings)-1,-1,-1):
        s = s+ trim(strings[i])+ 2*"\n"
    return s

def _print_tree(tree):
    levels = []
    levels.append([tree])
    i =0
    while has_nonNone(levels[i]):
        levels.append([])
        for t in levels[i]:
            if t == None:
                levels[i+1].append(None)
                levels[i+1].append(None)
            else:
                if t.has_left():
                    levels[i+1].append(t.left())
                else: 
                    levels[i+1].append(None)
                if t.has_right():
                    levels[i+1].append(t.right())
                else:
                    levels[i+1].append(None)
        i = i+1
    return levels[:-1]

def print_horizontal(tree):
    levels = _print_tree(tree)
    strings = []
    line = 1
    while len(levels[-1])>0:
        spaces = 0
        while (line >> spaces)&1 ==0 :
            spaces = spaces + 1
        t = levels[-(spaces+1)].pop()
        s = "\t"*(len(levels)-spaces-1) + t.__str__() if t != None else " "
        strings.append(s)
        line = line+1
    output = ""
    for s in strings:
        output = output + s + "\n"

    return output

def has_nonNone(l):
    for e in l:
        if e != None:
            return True
    return False

def inorder_traversal(tree):
    s = [""]
    _inorder_traversal(tree,s)
    return s[0]

def _inorder_traversal(tree,s):
    if tree.has_left():
        _inorder_traversal(tree.left(),s)
    s[0]= s[0]+ tree.root.data.__str__()+ " "
    if tree.has_right():
        _inorder_traversal(tree.right(),s)

def postop_traversal(tree):
    s = [""]
    _postop_traversal(tree,s)
    return s[0]

def _postop_traversal(tree,s):
    if tree.has_left():
        _postop_traversal(tree.left(),s)
    if tree.has_right():
        _postop_traversal(tree.right(),s)
    s[0] = s[0] + tree.root.data.__str__()+" "

def preop_traversal(tree):
    s = [""]
    _preop_traversal(tree,s)
    return s[0]

def _preop_traversal(tree,s):
    s[0]=s[0]+tree.root.data.__str__()+" "
    if tree.has_left():
        _preop_traversal(tree.left(),s)
    if tree.has_right():
        _preop_traversal(tree.right(),s)

def construct_list(string):
    expressions = []
    n=""
    num = {'0','1','2','3','4','5','6','7','8','9','.'}
    ops = {'^','*','/','+','-'}
    groupers = {'(',')','[',']','{','}'}
    for char in string :
        if char in num:
            n = n + char
        elif char in ops:
            if len(n)!=0:
                expressions.append(float(n))
                n = ""
            expressions.append(Operation(char))
        elif char in groupers:
            if len(n)!=0:
                expressions.append(float(n))
                n=""
            expressions.append(char)
    if len(n)!=0:
        expressions.append(float(n))
    
    return expressions

def construct_tree(expressions):
    i=0
    while i<len(expressions):
        if(expressions[i] in {')',']','}'}):
            raise Exception("unbalanced brackets")
        if(expressions[i]=='('):
            j=i+1
            while j < len(expressions):
                if expressions[j] ==')':
                    expressions[i:j+1] = [construct_tree(expressions[i+1:j])]
                    break
                j=j+1
            else:
                raise Exception("unbalanced brackets")
            i = i+1
            continue

        if(expressions[i]=='['):
            j=i+1
            while j < len(expressions):
                if expressions[j] ==']':
                    expressions[i:j+1] = [construct_tree(expressions[i+1:j])]
                    break
                j=j+1
            else:
                raise Exception("unbalanced brackets")
            i = i+1
            continue
            
        if(expressions[i]=='{'):
            j=i+1
            while j < len(expressions):
                if expressions[j] =='}':
                    expressions[i:j+1] = [construct_tree(expressions[i+1:j])]
                    break
                j=j+1
            else:
                raise Exception("unbalanced brackets")
            i = i+1
            continue
        i = i+1

    i=0
    while i < len(expressions):
        if isinstance(expressions[i],Operation) and expressions[i].equals('^'):
            expressions[i-1:i+2] = [_construct_tree(expressions[i-1:i+2])]
            continue
        i=i+1
    i=0
    while i < len(expressions):
        if isinstance(expressions[i],Operation) and expressions[i].equals('*'):
            expressions[i-1:i+2] = [_construct_tree(expressions[i-1:i+2])]
            continue
        i=i+1
    i=0
    while i < len(expressions):
        if isinstance(expressions[i],Operation) and expressions[i].equals('/'):
            expressions[i-1:i+2] = [_construct_tree(expressions[i-1:i+2])]
            continue
        i=i+1
    i=0
    while i < len(expressions):
        if isinstance(expressions[i],Operation) and expressions[i].equals('+'):
            expressions[i-1:i+2] = [_construct_tree(expressions[i-1:i+2])]
            continue
        i=i+1
    i=0
    while i < len(expressions):
        if isinstance(expressions[i],Operation) and expressions[i].equals('-'):
            expressions[i-1:i+2] = [_construct_tree(expressions[i-1:i+2])]
            continue
        i=i+1

    return expressions[0]


def _construct_tree(expressions):
    '''
    only accepts 3 length lists in the form value,operation,value
    '''

    tree = Binary_Tree(expressions[1])
    tree.add_left(expressions[0])
    tree.add_right(expressions[2])

    return tree


def results(tree):
    print(print_horizontal(tree))
    print("Preorder: \t"+preop_traversal(tree))
    print("Postorder: \t"+postop_traversal(tree))
    print("Result: \t" + tree.evaluate().__str__())

if __name__ == '__main__':
    
    if len(sys.argv)>1:
        if sys.argv[1] in {'-h','--help'}:
            print(help_menu)
            exit()
        try:
            tree = construct_tree(construct_list(sys.argv[1]))
        except:
            print(help_menu)
            exit()
        results(tree)
        exit()

    while(True):
        
        text = input("Enter Equation: ")
        if(text.upper()=="EXIT"):
            break

        try:
            tree = construct_tree(construct_list(text))
        except:
            print("Unbalanced Brackets")
            continue
        
        results(tree)




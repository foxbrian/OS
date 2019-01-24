#!/usr/bin/python

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
        self.root.add_left(self._Node(data))
    
    def add_right(self,data):
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

    def __str__(self):
        return self.op

def print_tree(tree):
   
    print(tree.root.data)
    if(tree.has_left()):
        _print_tree(tree.left(),1)
    if(tree.has_right()):
        _print_tree(tree.right(),1)

def _print_tree(tree,level):
    print("  "*level+tree.root.data)
    if(tree.has_left()):
        _print_tree(tree.left(),level+1)
    if(tree.has_right()):
        _print_tree(tree.right(),level+1)

def inorder_traversal(tree):
    if tree.has_left():
        inorder_traversal(tree.left())
    print(tree.root.data,end=" ")
    if tree.has_right():
         inorder_traversal(tree.right())

def postop_traversal(tree):
    if tree.has_left():
        postop_traversal(tree.left())
    if tree.has_right():
         postop_traversal(tree.right())
    print(tree.root.data,end=" ")

def preop_traversal(tree):
    print(tree.root.data,end=" ")
    if tree.has_left():
        preop_traversal(tree.left())
    if tree.has_right():
         preop_traversal(tree.right())

def construct_tree(expression):
    sanitized = []
    n=""
    num = {'0','1','2','3','4','5','6','7','8','9','.'}
    ops = {'^','*','/','+','-'}
    for char in expression :
        if char in num:
            n.append(char)
        if char in ops:
            if len(n)!=0:
                sanitized.append(float(n))
                n=""
            sanitize.append(Operation(char))
    tree = Binary_Tree(sanitized.pop(0))
    for element in sanitized:
        _add_element(tree,element)

def _add_element(tree,element):
    if isinstance(tree.root.data,float):
        if isinstance(element,float):
            #this shouldn't be possible
            raise Exception('bad input')
        tree.right_parent(element)
    else:
        if isinstance(element,float):
             tree.add_right(element)
        else:
            tree.right_parent

    

 __name__ == '__main__':
    tree = Binary_Tree(3)
    tree.right_parent(Operation('*'))
    tree.add_right(4)
    tree.right_parent(Operation('-'))
    tree.add_right(2)
    
    preop_traversal(tree)
    print("")
    postop_traversal(tree)
    print("")
    inorder_traversal(tree)
    print("")
    print(tree.evaluate())



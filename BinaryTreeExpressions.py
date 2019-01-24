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

def evaluate(tree):
    '''
    assuming the tree is valid
    tree is valid if every leaf is a value and root is an operation
    '''
    if(type(tree.root.data,Operation)):
        return tree.root.data.evaluate 

if __name__ == '__main__':
    tree = Binary_Tree('3')
    tree.right_parent('*')
    tree.add_right('4')
    tree.right_parent('-')
    tree.add_right('2')
    '''
    preop_traversal(tree)
    print("")
    postop_traversal(tree)
    print("")
    inorder_traversal(tree)
    print("")
    '''
    print(Operation('-').evaluate(3,2))



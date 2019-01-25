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
    s = [""]
    _inorder_traversal(tree,s)
    return s[0]

def _inorder_traversal(tree,s):
    if tree.has_left():
        _inorder_traversal(tree.left(),s)
    s[0]= s[0]+ tree.root.data.__str__()
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
    s[0] = s[0] + tree.root.data.__str__()

def preop_traversal(tree):
    s = [""]
    _preop_traversal(tree,s)
    return s[0]

def _preop_traversal(tree):
    s[0]=s[0]+tree.root.data.__str__()
    if tree.has_left():
        _preop_traversal(tree.left(),s)
    if tree.has_right():
        _preop_traversal(tree.right(),s)

def construct_list(string):
    expressions = []
    n=""
    num = {'0','1','2','3','4','5','6','7','8','9','.'}
    ops = {'^','*','/','+','-'}
    for char in string :
        if char in num:
            n = n + char
        elif char in ops:
            if len(n)!=0:
                expressions.append(float(n))
                n = ""
            expressions.append(Operation(char))
    if len(n)!=0:
        expressions.append(float(n))
    return expressions

def construct_tree(expressions):
    i=0
    while i<len(expressions):
        
        if(expressions[i]=='('):
            for exp ,j in enumerate(expressions):
                if exp ==')':
                    expresions[i:j+1] = [construct_tree(expressions[i+1,j])]
                    break
            i = i+1
            continue

        if(expressions[i]=='['):
            for exp ,j in enumerate(expressions):
                if exp ==']':
                    expresions[i:j+1] = [construct_tree(expressions[i+1,j])]
                    break
            i = i+1
            continue
            
        if(expressions[i]=='{'):
            for exp ,j in enumerate(expressions):
                if exp =='}':
                    expresions[i:j+1] = [construct_tree(expressions[i+1,j])]
                    break
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

if __name__ == '__main__':
    tree = construct_tree(construct_list("(3+2)/5"))
    
    '''
    tree = Binary_Tree(3)
    tree.right_parent(Operation('*'))
    tree.add_right(4)
    tree.right_parent(Operation('-'))
    tree.add_right(2)
    preop_traversal(tree)
    print("")
    postop_traversal(tree)
    print("")
    '''
    print(inorder_traversal(tree))

    print(tree.evaluate())



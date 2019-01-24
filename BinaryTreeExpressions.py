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

    def __init__(self):
        self.root = self._Node(None)
    
    def add_left(self,data):
        self.root.add_left(self._Node(data))

if __name__ == '__main__':
    tree = Binary_Tree()
    tree.add_left('*')

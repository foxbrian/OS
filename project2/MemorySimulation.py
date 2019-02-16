#!/usr/bin/python

import sys
import tkinter as tk

help_menu = """
NAME
    BinaryTreeExpressions - A python based utility to represent simple equations as binary trees

SYNOPSIS
    BinaryTreeExpressions [-h|--help] ["equation"]

DESCRIPTION
    BinaryTreeExpressions accepts an equation and represents it as a binary tree

COMMAND LINE OPTIONS
    -h|--help   Display this text


"""

class Bar():
    def __init__(self,canvas,x,y,width=50,height=400):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.canvas=canvas

    def draw(self):
        self.canvas.create_rectangle(self.x,self.y,self.x+self.width,self.y+self.height,fill="#000000")
    
class mem_table:
    def __init__(self,size=1000,fixed=False):
        self.size=size
        self.fixed=fixed

    class _Unit:
        def __init__(self,size,start,busy=False,occupied=0):
            self.size=size
            self.start=start
            self.busy=busy
            self.occupied = occupied

class Application(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.pack()
        self.window = tk.Canvas(self,width=800,height=500)
        self.window.pack()
        
        self.window.bind("<Space>",self.toggle())
        self.window.bind("<Return>",self.submit())
        self.window.bind("<Tab>",self.step())

        self.fixed_first_bar = Bar(self.window,300,50)
        self.fixed_best_bar = Bar(self.window,360,50)
        self.fixed_next_bar = Bar(self.window,420,50)
        self.fixed_worst_bar = Bar(self.window,480,50)
        self.dyn_first_bar = Bar(self.window,540,50)
        self.dyn_best_bar = Bar(self.window,600,50)
        self.dyn_next_bar = Bar(self.window,660,50)
        self.dyn_worst_bar = Bar(self.window,720,50)
        
        self.draw_bars()

        self.fixed_first = mem_table(fixed=True)
        self.fixed_best = mem_table(fixed=True)
        self.fixed_next = mem_table(fixed=True)
        self.fixed_worst = mem_table(fixed=True)
        self.dyn_first = mem_table()
        self.dyn_best = mem_table()
        self.dyn_next = mem_table()
        self.dyn_worst = mem_table()


    def draw_bars(self):
        self.fixed_first_bar.draw()
        self.fixed_best_bar.draw()
        self.fixed_next_bar.draw()
        self.fixed_worst_bar.draw()
        self.dyn_first_bar.draw()
        self.dyn_best_bar.draw()
        self.dyn_next_bar.draw()
        self.dyn_worst_bar.draw()
    
    def toggle(self):
        pass

    def submit(self):
        pass
    
    def step(self):
        pass

if(__name__=="__main__"):
    window = Application()
    window.mainloop()
        

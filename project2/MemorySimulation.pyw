#!/usr/bin/python

import random
import time
import math as Math
import tkinter as tk
from collections import deque

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
###############
#Memory Tables#
###############

#single partiton in the memory table
class _Unit:
    def __init__(self,size,start,num,busy=False,occupied=0):
        self.size=size
        self.start=start
        self.busy=busy
        self.occupied = occupied
        self.job_num=num
        
    def free(self):
        self.occupied = 0
        self.busy = False
#super class with no implimented methods
class MemoryTable:
    def __init__(self,size):
        self.size = size
        self.partitions = []
        self.queue = deque()
        self.job_num = 0
        self.log=""

    def allocate(self,size):
        pass

    def deallocate(self,index):
        pass

#super class for all fixed tables
#handles deallocation and initializing the empty table
class FixedTable(MemoryTable):
    def __init__(self,size,parts):
        MemoryTable.__init__(self,size)
        if isinstance(parts,str):
            int_parts = [int(string) for string in parts.split(",") ]
            self._build_table(int_parts)
        elif isinstance(parts,list):
            int_parts = [int(part) for part in parts ]
            self._build_table(int_parts)
        else:
            raise Exception("bad partition list")
    
    def _build_table(self,parts):
        filled = False
        total_open = self.size
        while(not filled):
            appended = False
            for size in parts:
                if size <=  total_open:
                    self.partitions.append(_Unit(size,self.size-total_open,num=None))
                    total_open = total_open-size
                    appended = True
                if(total_open == 0):
                    filled= True
                    break
            if not appended:
                self.partitions.append(_Unit(total_open,self.size-total_open,num=None))
                filled=True

    
    def deallocate(self,num):
        index=0
        for i,part in enumerate(self.partitions):
            if(part.job_num==num):
                index=i
                break
        else:
            return False

        self.log += "job "+str(index)+" deallocated\n"
        self.partitions[index].free()

#super class for all dynamic tables
#handles deallocation and initializing table
#also handles partial allocation of a partition
class DynamicTable(MemoryTable):
    
    def __init__(self,size):
        MemoryTable.__init__(self,size)
        self.partitions.append(_Unit(size,0,None))

    def deallocate(self,num):
        index=0
        for i,part in enumerate(self.partitions):
            if(part.job_num==num):
                index=i
                break
        else:
            return False

        self.log+="job "+str(index)+" deallocated\n"
        self.partitions[index].free()
        if index != 0: 
            if not self.partitions[index-1].busy:
                self.partitions[index-1].size = self.partitions[index-1].size+self.partitions[index].size
                self.partitions.remove(self.partitions[index])
                index=index-1
        if (index != len(self.partitions)-1):
            if not self.partitions[index+1].busy:
                self.partitions[index].size = self.partitions[index].size + self.partitions[index+1].size
                self.partitions.remove(self.partitions[index+1])

    def slice(self,partition,size):
        if self.partitions[partition].size == size:
            self.partitions[partition].occupied = size
            self.partitions[partition].busy = True
            self.partitions[partition].job_num = self.job_num
            return True
        if partition != len(self.partitions)+1:
            self.partitions.insert(partition+1, _Unit(self.partitions[partition].size-size,self.partitions[partition].start+size,num=None))
        else:
            self.partitions.add(_Unit(self.partitions[partition].size-size,self.partitions[partition].start+size,num=None))
        self.partitions[partition].size = size
        self.partitions[partition].occupied = size
        self.partitions[partition].busy = True
        self.partitions[partition].job_num = self.job_num


class FixedFirstTable(FixedTable):
    
    def __init__(self,size=1000,parts=[200]):
        FixedTable.__init__(self,size,parts)

    def allocate(self,size):
        for part in self.partitions:
            if not part.busy and part.size >= size:
                part.busy = True
                part.occupied = size
                part.job_num = self.job_num
                self.job_num = self.job_num+1
                self.log +="job "+str(self.job_num)+" allocated\n"
                return True
        self.queue.append(_Unit(size,None,self.job_num))
        self.log = self.log + "job "+str(self.job_num)+" queued\n"
        self.job_num = self.job_num+1

class FixedBestTable(FixedTable):
    
    def __init__(self,size=1000,parts=[200]):
        FixedTable.__init__(self,size,parts)

    def allocate(self,size):
        best = -1
        diff = self.size
        for i,part in enumerate(self.partitions):
            if not part.busy and part.size-size > -1 and part.size-size <diff:
                best = i
                diff = part.size-size
        if best != -1:
            self.partitions[best].occupied=size
            self.partitions[best].busy = True
            self.partitions[best].job_num = self.job_num
            self.job_num = self.job_num+1
            self.log+="job "+str(self.job_num)+" allocated\n"
            return True
        self.queue.append(_Unit(size,None,self.job_num))
        self.log+="job "+str(self.job_num)+" queued\n"
        self.job_num = self.job_num+1

class FixedNextTable(FixedTable):
    
    def __init__(self,size=1000,parts=[200]):
        FixedTable.__init__(self,size,parts)
        self._next = 0

    def allocate(self,size):
        for part in range(len(self.partitions)):
            index = part+self._next if part+self._next < len(self.partitions) else part+self._next-len(self.partitions)
            if not self.partitions[index].busy and part.size >= size:
                self.partitions[index].busy = True
                self.partitions[index].job_num = self.job_num
                self.partitions[index].occupied = size
                self.job_num = self.job_num+1
                self._next = index
                self.log+="job "+str(self.job_num)+" allocated\n"
                return True
        self.queue.append(_Unit(size,None,self.job_num))
        self.log+="job "+str(self.job_num)+" queued\n"
        self.job_num = self.job_num+1

class FixedWorstTable(FixedTable):

    def __init__(self,size=1000,parts=[200]):
        FixedTable.__init__(self,size,parts)

    def allocate(self,size):
        worst = -1
        diff = -1
        for i,part in enumerate(self.partitions):
            if not part.busy and part.size-size > -1 and part.size-size > diff:
                worst  = i
                diff = part.size-size
        if worst != -1:
            self.partitions[worst].occupied=size
            self.partitions[worst].busy = True
            self.partitions[worst].job_num = self.job_num
            self.job_num = self.job_num+1
            self.log+="job "+str(self.job_num)+" allocated\n"
            return True
        self.queue.append(_Unit(size,None,self.job_num))
        self.log+="job "+str(self.job_num)+" queued\n"
        self.job_num = self.job_num+1

class DynamicFirstTable(DynamicTable):

    def __init__(self,size=1000):
        DynamicTable.__init__(self,size)

    def allocate(self,size):
        for i,part in enumerate(self.partitions):
            if not part.busy and part.size >= size:
                self.slice(i,size)
                self.job_num = self.job_num+1
                self.log+="job "+str(self.job_num)+" allocated\n"
                return True
        self.queue.append(_Unit(size,None,self.job_num))
        self.log+="job "+str(self.job_num)+" queued\n"
        self.job_num = self.job_num+1
    

class DynamicBestTable(DynamicTable):

    def __init__(self,size=1000):
        DynamicTable.__init__(self,size)

    def allocate(self,size):
        best = -1
        diff = self.size
        for i,part in enumerate(self.partitions):
            if not part.busy and part.size-size > -1 and part.size-size <diff:
                best = i
                diff = part.size-size
        if best != -1:
            self.slice(best,size)
            self.job_num = self.job_num+1
            self.log+="job "+str(self.job_num)+" allocated\n"
            return True
        self.queue.append(_Unit(size,None,self.job_num))
        self.log+="job "+str(self.job_num)+" queued\n"
        self.job_num = self.job_num+1

class DynamicNextTable(DynamicTable):
    def __init__(self,size=1000):
        DynamicTable.__init__(self,size)
        self._next = 0

    def allocate(self,size):
        for part in range(len(self.partitions)):
            index = part+self._next if part+self._next < len(self.partitions) else part+self._next-len(self.partitions)
            if not self.partitions[index].busy and self.partitions[index].size >= size:
                self.slice(index,size)
                self.job_num = self.job_num+1
                self._next = index
                self.log+="job "+str(self.job_num)+" allocated\n"
                return True
        self.queue.append(_Unit(size,None,self.job_num))
        self.log+="job "+str(self.job_num)+" queued\n"
        self.job_num = self.job_num+1

class DynamicWorstTable(DynamicTable):

    def __init__(self,size=1000):
        DynamicTable.__init__(self,size)

    def allocate(self,size):
        worst = -1
        diff = -1
        for i,part in enumerate(self.partitions):
            if not part.busy and part.size-size > -1 and part.size-size > diff:
                worst  = i
                diff = part.size-size
        if worst != -1:
            self.slice(worst,size)
            self.job_num = self.job_num+1
            self.log+="job "+str(self.job_num)+" allocated\n"
            return True
        self.log+="job "+str(self.job_num)+" queued\n"
        self.queue.append(_Unit(size,None,self.job_num))
        self.job_num = self.job_num+1

#Draws the bar that represents the memory table
class Bar():
    def __init__(self,canvas,x,y,width=50,height=400):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.canvas=canvas
        self.partitions = [] #list of the start of partitions in order
        self.filled = [] #list of amount filled per partion in order 
        self.labels= []

    #draws using the values in partitions and filled as pixel values
    #this means the values have to be calculated before they get to this 
    def draw(self):
        self.canvas.create_rectangle(self.x,
                self.y,
                self.x+self.width,
                self.y+self.height+1,
                fill="#000000")
        for i in range(len(self.partitions)):
            self.canvas.create_rectangle(self.x+1,
                    self.y+self.partitions[i]+1,
                    self.x+self.width-1,
                    self.y+self.partitions[i+1] if i+1 != len(self.partitions) else self.y+self.height,
                    fill="#505050")
        label = 0   
        for i in range(len(self.filled)):
            if self.filled[i]==0:
                continue

            self.canvas.create_rectangle(self.x+3,
                    self.y+self.partitions[i]+3,
                    self.x+self.width-3,
                    self.y+self.partitions[i]+self.filled[i]-2,
                    fill="#de9030",
                    outline="#202020")
            self.canvas.create_text(self.x+4,self.y+self.partitions[i]+4,anchor="nw",text=str(self.labels[label]))
            label = label+1


class Application(tk.Frame):
    def __init__(self,master=tk.Tk()):
        super().__init__(master)
        self.pack() 
        master.bind("<space>",self.toggle)
        master.bind("<Return>",self.submit)
        master.bind("<a>",self.step)
        master.bind("<d>",self.trash)
        
        self.playing = False

        self.build_tables()
        self.focus_set()

        #############
        #Main Window#
        #############
        self.window = tk.Frame(self,width=800,height=440)
        
        ##############
        #Entry Fields#
        ##############
        self.entries= tk.Frame(self,width=800,height=20)
        self.entries.pack()
        
        tk.Label(self.entries,text="Size of Memory").pack(side=tk.LEFT) 

        self.total_size_field = tk.Entry(self.entries)
        self.total_size_field.pack(side=tk.LEFT,expand=False)
        
        tk.Label(self.entries,text="Size of Fixed Partitions").pack(side=tk.LEFT)

        self.fixed_size_field = tk.Entry(self.entries)
        self.fixed_size_field.pack(side=tk.LEFT,expand=False)
 
        ######
        #Bars#
        ######
        self.canvas = tk.Canvas(self.window,height=440,width=510)
        self.canvas.pack(side=tk.RIGHT);

        self.canvas.create_text(25,0,anchor="nw",text="Fixed: ")

        self.fixed_first_bar = Bar(self.canvas,25,27)
        self.canvas.create_text(25,12,anchor="nw",text="First")

        self.fixed_best_bar = Bar(self.canvas,85,27)
        self.canvas.create_text(85,12,anchor="nw",text="Best")

        self.fixed_next_bar = Bar(self.canvas,145,27)
        self.canvas.create_text(145,12,anchor="nw",text="Next")

        self.fixed_worst_bar = Bar(self.canvas,205,27)
        self.canvas.create_text(205,12,anchor="nw",text="Worst")

        self.canvas.create_text(265,0,anchor="nw",text="Dynamic: ")

        self.dyn_first_bar = Bar(self.canvas,265,27)
        self.canvas.create_text(265,12,anchor="nw",text="First")

        self.dyn_best_bar = Bar(self.canvas,325,27)
        self.canvas.create_text(325,12,anchor="nw",text="Best")

        self.dyn_next_bar = Bar(self.canvas,385,27)
        self.canvas.create_text(385,12,anchor="nw",text="Next")

        self.dyn_worst_bar = Bar(self.canvas,445,27)
        self.canvas.create_text(445,12,anchor="nw",text="Worst")
        
        ########
        #Output#
        ########
        self.output = tk.Frame(self.window,height=440,width=300)
        self.output.pack(side=tk.LEFT)
        self.output.bind("<Button-1>",self.update_output)

        self.output_radio = tk.Frame(self.output,height=400,width=100)
        self.output_radio.pack(side=tk.LEFT)
        
        self.text= tk.IntVar()
        tk.Radiobutton(self.output_radio,text="Fixed First",value=0,
                indicatoron=0,width=14,command=self.update_output,variable=self.text).pack(anchor=tk.W)
        tk.Radiobutton(self.output_radio,text="Fixed Best",value=1,
                indicatoron=0,width=14,command=self.update_output,variable=self.text).pack(anchor=tk.W)
        tk.Radiobutton(self.output_radio,text="Fixed Next",value=2,
                indicatoron=0,width=14,command=self.update_output,variable=self.text).pack(anchor=tk.W)
        tk.Radiobutton(self.output_radio,text="Fixed Worst",value=3,
                indicatoron=0,width=14,command=self.update_output,variable=self.text).pack(anchor=tk.W)
        tk.Radiobutton(self.output_radio,text="Dynamic First",value=4,
                indicatoron=0,width=14,command=self.update_output,variable=self.text).pack(anchor=tk.W)
        tk.Radiobutton(self.output_radio,text="Dynamic Best",value=5,
                indicatoron=0,width=14,command=self.update_output,variable=self.text).pack(anchor=tk.W)
        tk.Radiobutton(self.output_radio,text="Dynamic Next",value=6,
                indicatoron=0,width=14,command=self.update_output,variable=self.text).pack(anchor=tk.W)
        tk.Radiobutton(self.output_radio,text="Dynamic Worst",value=7,
                indicatoron=0,width=14,command=self.update_output,variable=self.text).pack(anchor=tk.W)
       
        self.output_text_box = tk.Canvas(self.output,height=400,width=300,bg="#eeeeee")
        self.output_text_box.pack(side=tk.RIGHT)
        self.output_text = self.output_text_box.create_text(10,10,anchor="nw")


        #########
        #Buttons#
        #########
        self.buttons=tk.Frame(self,height=20,width=800)
        self.buttons.pack(side=tk.BOTTOM)

        self.allocate_button = tk.Button(self.buttons,text="Allocate",command=self.step)
        self.allocate_button.pack(side=tk.LEFT)
        
        self.allocate_size = tk.Entry(self.buttons)
        self.allocate_size.pack(side=tk.LEFT)

        self.deallocate_button = tk.Button(self.buttons,text="Deallocate",command=self.trash)
        self.deallocate_button.pack(side=tk.LEFT)

        self.deallocate_size = tk.Entry(self.buttons)
        self.deallocate_size.pack(side=tk.LEFT)

        self.play_button = tk.Button(self.buttons,text="Play/Pause (space)",command=self.toggle)
        self.play_button.pack(side=tk.LEFT)

        self.reset_button = tk.Button(self.buttons,text="Reset (enter)",command=self.submit)
        self.reset_button.pack(side=tk.LEFT)

        self.window.pack(side=tk.BOTTOM)
        self.update_output()
        self.build_bars()
        self.draw_bars()
    
    def build_tables(self,size=1000,fixed=[200]): 
        self.fixed_first = FixedFirstTable(size,fixed)
        self.fixed_best = FixedBestTable(size,fixed)
        self.fixed_next = FixedBestTable(size,fixed)
        self.fixed_worst = FixedWorstTable(size,fixed)
        self.dyn_first = DynamicFirstTable(size)
        self.dyn_best = DynamicBestTable(size)
        self.dyn_next = DynamicNextTable(size)
        self.dyn_worst = DynamicWorstTable(size)

    #this is a mess for me to hardcode but I just want to get it done for now
    #calculate the pixel values for the start of each partition on the bar
    #then calculate the pixel value for the filled portion of the partition
    def build_bars(self):
        self.fixed_first_bar.partitions = [Math.floor(self.fixed_first_bar.height*part.start/self.fixed_first.size) 
                for part in self.fixed_first.partitions]
        self.fixed_best_bar.partitions = [Math.floor(self.fixed_best_bar.height*part.start/self.fixed_best.size) 
                for part in self.fixed_best.partitions ]
        self.fixed_next_bar.partitions = [Math.floor(self.fixed_next_bar.height*part.start/self.fixed_next.size) 
                for part in self.fixed_next.partitions ]
        self.fixed_worst_bar.partitions = [Math.floor(self.fixed_worst_bar.height*part.start/self.fixed_worst.size) 
                for part in self.fixed_worst.partitions ]
        self.dyn_first_bar.partitions = [Math.floor(self.dyn_first_bar.height*part.start/self.dyn_first.size) 
                for part in self.dyn_first.partitions ]
        self.dyn_best_bar.partitions = [Math.floor(self.dyn_best_bar.height*part.start/self.dyn_best.size) 
                for part in self.dyn_best.partitions ]
        self.dyn_next_bar.partitions = [Math.floor(self.dyn_next_bar.height*part.start/self.dyn_next.size) 
                for part in self.dyn_next.partitions ]
        self.dyn_worst_bar.partitions = [Math.floor(self.dyn_worst_bar.height*part.start/self.dyn_worst.size) 
                for part in self.dyn_worst.partitions ]

        self.fixed_first_bar.filled = [Math.floor(self.fixed_first_bar.height*part.occupied/self.fixed_first.size) 
                for part in self.fixed_first.partitions]
        self.fixed_best_bar.filled =  [Math.floor(self.fixed_best_bar.height*part.occupied/self.fixed_best.size) 
                for part in self.fixed_best.partitions ]
        self.fixed_next_bar.filled = [Math.floor(self.fixed_next_bar.height*part.occupied/self.fixed_next.size) 
                for part in self.fixed_next.partitions ]
        self.fixed_worst_bar.filled = [Math.floor(self.fixed_worst_bar.height*part.occupied/self.fixed_worst.size) 
                for part in self.fixed_worst.partitions ]
        self.dyn_first_bar.filled = [Math.floor(self.dyn_first_bar.height*part.occupied/self.dyn_first.size) 
                for part in self.dyn_first.partitions ]
        self.dyn_best_bar.filled = [Math.floor(self.dyn_best_bar.height*part.occupied/self.dyn_best.size) 
                for part in self.dyn_best.partitions ]
        self.dyn_next_bar.filled = [Math.floor(self.dyn_next_bar.height*part.occupied/self.dyn_next.size) 
                for part in self.dyn_next.partitions ]
        self.dyn_worst_bar.filled = [Math.floor(self.dyn_worst_bar.height*part.occupied/self.dyn_worst.size) 
                for part in self.dyn_worst.partitions ]

        self.fixed_first_bar.labels = [part.job_num for part in self.fixed_first.partitions if part.busy ]
        self.fixed_best_bar.labels =  [part.job_num for part in self.fixed_best.partitions if part.busy ]
        self.fixed_next_bar.labels = [part.job_num for part in self.fixed_next.partitions if part.busy ]
        self.fixed_worst_bar.labels = [part.job_num for part in self.fixed_worst.partitions if part.busy ]
        self.dyn_first_bar.labels = [part.job_num for part in self.dyn_first.partitions if part.busy ]
        self.dyn_best_bar.labels = [part.job_num for part in self.dyn_best.partitions if part.busy ]
        self.dyn_next_bar.labels = [part.job_num for part in self.dyn_next.partitions if part.busy ]
        self.dyn_worst_bar.labels = [part.job_num for part in self.dyn_worst.partitions if part.busy ]

    
    def draw_bars(self):
        self.fixed_first_bar.draw()
        self.fixed_best_bar.draw()
        self.fixed_next_bar.draw()
        self.fixed_worst_bar.draw()
        self.dyn_first_bar.draw()
        self.dyn_best_bar.draw()
        self.dyn_next_bar.draw()
        self.dyn_worst_bar.draw()
        
        self.update()
    
    def allocate_all(self,size):

        self.fixed_first.allocate(size)
        self.fixed_best.allocate(size)
        self.fixed_next.allocate(size)
        self.fixed_worst.allocate(size)
        self.dyn_first.allocate(size)
        self.dyn_best.allocate(size)
        self.dyn_next.allocate(size)
        self.dyn_worst.allocate(size)

    def deallocate_all(self,num):

        self.fixed_first.deallocate(num)
        self.fixed_best.deallocate(num)
        self.fixed_next.deallocate(num)
        self.fixed_worst.deallocate(num)
        self.dyn_first.deallocate(num)
        self.dyn_best.deallocate(num)
        self.dyn_next.deallocate(num)
        self.dyn_worst.deallocate(num)

    #triggered by clicking radio buttons
    #updates text in output pain to the left of bars
    def update_output(self,event=None):
        radio= {0:self.fixed_first,
                1:self.fixed_best,
                2:self.fixed_next,
                3:self.fixed_worst,
                4:self.dyn_first,
                5:self.dyn_best,
                6:self.dyn_next,
                7:self.dyn_worst}

        table = ""
        for i,j,k in [(part.start,part.size,part.occupied) for part in radio[self.text.get()].partitions]:
            table += str(i)+"\t"+str(j)+"\t"+str(k)+"\n"

        fragmentation = 0
        if self.text.get() < 4:
            for part in radio[self.text.get()].partitions:
                if part.busy:
                    fragmentation = fragmentation + part.size-part.occupied
        else:
            for part in radio[self.text.get()].partitions[:-1]:
                if not part.busy:
                    fragmentation=fragmentation+part.size
        fragmentation = str(fragmentation)

        queue = ""
        for i,j in [(part.job_num,part.size) for part in radio[self.text.get()].queue]:
            queue = queue + "job " + str(i) + ":\t" + str(j) +"\n"


        out = "Table\nStart\tSize\tOccupied\n"+table + "\nFragmentation: " + fragmentation + "\n\nJobs in Queue\t"+str(len(radio[self.text.get()].queue))+"\nJob\tSize\n" + queue
        self.output_text_box.itemconfig(self.output_text,text=out)

    #triggered by pressing enter while focused on anything
    #restarts and rebuilds simulation pulling whatever is in fields as parameters 
    def submit(self,event=None):
        try:
            self.build_tables(size=int(self.total_size_field.get()),fixed=self.fixed_size_field.get())
        except:
            try:
                self.build_tables(size=int(self.total_size_field.get()))
            except:
                try:
                    self.build_tables(fixed=self.fixed_size_field.get())
                except:
                    self.build_tables()
        self.update_output()
        self.build_bars()
        self.draw_bars()
        self.play()

    #randomly allocate and deallocate memory
    def play(self):
        if self.playing:
            coin = random.randrange(3)
            if coin>=1:
                self.step(size=Math.floor(random.randrange(50,300)))
            else:
                self.trash(Math.floor(random.randrange(self.fixed_first.job_num+1)))
            self.after(500,self.play)

    def toggle(self,event=None):
        self.playing = not self.playing
        if(self.playing):
            self.play()
                  
    def step(self,event=None,size=None):
        if size == None:
            size = 100
            try:
                size = int(self.allocate_size.get())
            except:
                pass
        self.allocate_all(size)
        self.update_output()
        self.build_bars()
        self.draw_bars()

    def trash(self,num=None):
        if num==None:
            try:
                num = int(self.deallocate_size.get())
            except:
                return False
        
        self.deallocate_all(num)
        self.update_output()
        self.build_bars()
        self.draw_bars()

if(__name__=="__main__"):
    app = Application()
    #window.fixed_first_bar.partitions = [0,30,50,200,350]
    #window.fixed_first_bar.filled=[20,20,0,100,20]
    
    app.mainloop()
        

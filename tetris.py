import tkinter as tk
#import numpy as np
import random
import tkinter.messagebox as mb
 
root = tk.Tk()
root.geometry("200x400")
f = tk.Frame(root)
f.grid()
CM = 12
RW = 20

game_window = [[9] * CM for i in range(RW)]
for i in range(RW - 3):
    game_window[i][2 : CM - 2] = [0]*(CM - 4)

class tetris():
    def __init__(self , CM , RW ,*game_window):
        self.label_name = [ "Label"+str(n) for n in range(RW * CM) ]
        self.blank =[[0]*4 for i in range(4)]
        self.cm = CM
        self.rw = RW
        self.cur_window = []
        self.cur_window += game_window
        self.cur_ad = [0 , 0]
        self.cur_block = []
        self.cur_block.extend(self.blank)

    def square(self):
        block = [[0]*4 for i in range(4)]
        block[1][1 : 3] = [1 , 1]
        block[2][1 : 3] = [1 , 1]
        return block

    def pole(self):
        block = [[0]*4 for i in range(4)]
        block[1][0 : 4] = [2 , 2 , 2 ,2]
        return block

    def totu(self):
        block = [[0]*4 for i in range(4)]
        block[1][2] = 3
        block[2][1 : 4] = [3 , 3 , 3]
        return block

    def zigzag1(self):
        block = [[0]*4 for i in range(4)]
        block[1][1 : 3] = [4 , 4]
        block[2][2 : 4] = [4 , 4]
        return block

    def zigzag2(self):
        block = [[0]*4 for i in range(4)]
        block[1][1 : 3] = [4 , 4]
        block[2][0 : 2] = [4 , 4]
        return block

    def eru1(self):
        block = [[0]*4 for i in range(4)]
        block[1][1] = 5
        block[2][1 : 4] = [5 , 5 , 5]
        return block

    def eru2(self):
        block = [[0]*4 for i in range(4)]
        block[1][2] = 5
        block[2][0 : 3] = [5 , 5 , 5]
        return block

    def rot_func(self , *block):
        block_temp = [[0]*4 for i in range(4)]
        for i in range(4):
           for j in range(4):
                block_temp[i][j] = block[3 - j][i]
        return block_temp

    def mk_block(self):
        global after_id
        self.cur_ad = [0 , 4]
        rdm = random.randint(0,6)
        if rdm == 0 :
            self.cur_block = ts.square()
        elif rdm == 1 :
            self.cur_block = ts.pole()
        elif rdm == 2 :
            self.cur_block = ts.totu()
        elif rdm == 3 :
            self.cur_block = ts.zigzag1()
        elif rdm == 4 :
            self.cur_block = ts.zigzag2()
        elif rdm == 5 :
            self.cur_block = ts.eru1()
        elif rdm == 6 :
            self.cur_block = ts.eru2()

        rdm = random.randint(0 , 3)
        for i in range(rdm):
            self.cur_block = ts.rot_func(*self.cur_block)

        flag = 0
        for i in range(4):
            for j in range(4):
                flag += self.cur_block[i][j] * self.cur_window[i + self.cur_ad[0]][j + self.cur_ad[1]]     
        if flag != 0:
            root.after_cancel(after_id)
            mb.showinfo('ゲームオーバ', 'ゲームオーバ')
        return flag

    def fall_func(self):
        global after_id
        pos = self.cur_ad[0] + 1
        flag = 0
        for i in range(4):
            for j in range(4):
                flag += self.cur_block[i][j] * self.cur_window[i + pos][j + self.cur_ad[1]]     
        if flag == 0:
            self.cur_ad[0] = pos
        return flag

    def rmv(self , event):
        flag = 0
        pos = self.cur_ad[1] + 1
        for i in range(4):
            for j in range(4):
                flag += self.cur_block[i][j] * self.cur_window[i + self.cur_ad[0]][j + pos]     
        if flag == 0:
            self.cur_ad[1] = pos
            ts.drow_block()

    def lmv(self , event):
        flag = 0
        pos = self.cur_ad[1] - 1
        for i in range(4):
            for j in range(4):
                flag += self.cur_block[i][j] * self.cur_window[i + self.cur_ad[0]][j + pos]     
        if flag == 0:
            self.cur_ad[1] = pos
            ts.drow_block()

    def fmv(self , event):
        ts.fall_func()
        ts.drow_block()

    def rrmv(self , event):
        temp_block = []
        temp_block.extend(ts.rot_func(*self.cur_block))
        flag = 0
        for i in range(4):
            for j in range(4):
                flag += temp_block[i][j] * self.cur_window[i + self.cur_ad[0]][j + self.cur_ad[1]]     
        if flag == 0:
            self.cur_block = temp_block
            ts.drow_block()

    def lrmv(self , event):
        temp_block = []
        temp_block += ts.rot_func(*ts.rot_func(*ts.rot_func(*self.cur_block)))
        flag = 0
        for i in range(4):
            for j in range(4):
                flag += temp_block[i][j] * self.cur_window[i + self.cur_ad[0]][j + self.cur_ad[1]]     
        if flag == 0:
            self.cur_block = temp_block
            ts.drow_block()

    def drow_block(self):
        color_arry = ["gray" , "yellow" , "green" ,"purple" ,"red" ,"blue" ,6 ,7 , 8 , "black"]
        for i in range(self.rw):
            for j in range(self.cm):
                self.label_name[i + j * self.rw].config(bg = color_arry[self.cur_window[i][j]] ) 
        for i in range(4):
            for j in range (4):
                if self.cur_block[i][j] != 0:
                    self.label_name[(i + self.cur_ad[0]) + (j + self.cur_ad[1]) * self.rw].config(bg = color_arry[self.cur_block[i][j]] ) 

    def ela(self):
        arry =[[9] * 2 + [0] * (self.cm - 4) + [9] * 2]
        for i in range(self.rw - 3):
            flag = 1
            for j in range (self.cm):
                flag *= self.cur_window[i][j]
            if flag !=  0:
                self.cur_window = arry + self.cur_window[ : i][ : ] + self.cur_window [i + 1 : ][ : ]
                

    def start_func(self):
        game_window = [[9] * CM for i in range(RW)]
        for i in range(RW - 3):
            game_window[i][2 : self.cm - 2] = [0]*(self.cm - 4)
        self.cur_window = game_window
        global after_id
        root.after_cancel(after_id)
        ts.mk_block()
        ts.drow_block()
        ts.fall_mv()

    def fall_mv(self):
        global after_id
        flag = 0
        flag += ts.fall_func()
        if flag != 0 :
            for i in range(4):
                for j in range (4):
                    if self.cur_block[i][j] != 0:
                        self.cur_window[(i + self.cur_ad[0])][(j + self.cur_ad[1])] = self.cur_block[i][j]
            ts.ela()
            flag = ts.mk_block()
        ts.drow_block()
        if flag == 0:
            after_id = root.after(1000, ts.fall_mv)

def dummy():
    mb.showinfo('使い方', '4：←\n6：→\n8：↓\n7：左回転\n9：右回転')

color_arry = ["gray" , "yellow" , "green" ,"purple" ,"red" ,"blue" ,6 ,7 , 8 , "black"]
ts = tetris(CM , RW , game_window)

for i in range(RW):
    for j in range(CM):
        ts.label_name[i + j * RW] = tk.Label(f , bg = color_arry[game_window[i][j]] , width = 1 , height = 1) 
        ts.label_name[i + j * RW].grid(row=i, column = j)
 
def exit_func():
    root.destroy()
       
button_name = "start"
button = tk.Button(f , text = button_name , command = lambda : ts.start_func())
button.grid(row=0 , column = CM + 2 , rowspan =5)

button_name = "exit"
button = tk.Button(f , text = button_name , command = exit_func)
button.grid(row= 2, column = CM + 2 , rowspan = 5)

root.bind("<Key - 4>" , ts.lmv)
root.bind("<Key - 6>" , ts.rmv)
root.bind("<Key - 7>" , ts.lrmv)
root.bind("<Key - 8>" , ts.fmv)
root.bind("<Key - 9>" , ts.rrmv)

after_id = root.after(1000, dummy)
root.mainloop()
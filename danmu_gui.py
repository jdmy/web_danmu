# python3.6
import tkinter as tk
import queue
from random import choice,randint


class Danmu():
    def __init__(self, text, id, x, y):
        self.text = text
        self.id = id
        self.x = x
        self.y = y

    def move(self):
        self.x -= 5


# import tkFileDialog
class App(tk.Tk):
    def __init__(self, q):
        tk.Tk.__init__(self)
        self.floater = FloatingWindow(q)


class FloatingWindow(tk.Toplevel):
    def danmu_handler(self, ):
        n=0
        for danmu in self.danmu_list:
            self.canvas.coords(danmu.id, danmu.x, danmu.y)
            danmu.move()
            if danmu.x<0:
                n+=1
        for i in range(n):
            self.canvas.delete(self.danmu_list[0].id)
            del self.danmu_list[0]

        # print("处理了",self.canvas.find_all())

        self.canvas.after(100,self.danmu_handler)

    def danmu_add(self):
        if not self.q.empty():
            temptext = self.q.get()
            tempx = self.ws
            tempfontsize=randint(15,30)
            tempy = randint(100,self.hs/2)
            tempid = self.canvas.create_text(tempx, tempy, text=temptext, font=("Fixdsys", tempfontsize, "bold"),
                                             fill=choice(self.colors))
            tempdanmu = Danmu(temptext, tempid, tempx, tempy)
            self.danmu_list.append(tempdanmu)
            # print("添加："+tempdanmu.text)
        # print("添加了")
        self.canvas.after(1000,self.danmu_add)

    def __init__(self, q):
        tk.Toplevel.__init__(self)
        self.overrideredirect(True)
        self.attributes("-transparentcolor", "blue")  # 黑色的透明度为100
        self.attributes("-topmost", 1)
        self.attributes("-alpha", 1)
        self.ws = self.winfo_screenwidth()
        self.hs = self.winfo_screenheight()
        self.canvas = tk.Canvas(self, width=self.ws, height=self.hs)
        self.canvas.create_rectangle(0, 0, self.ws, self.hs, fill="blue")
        self.colors=["black","red","green","yellow","pink"]

        self.q = q
        self.danmu_list = []

        self.canvas.grid(column=0, row=0)
        self.canvas.bind("<ButtonPress-1>", self.StartMove)
        self.canvas.bind("<ButtonRelease-1>", self.StopMove)
        self.canvas.bind("<B1-Motion>", self.OnMotion)
        self.danmu_add()
        self.danmu_handler()

    def StartMove(self, event):
        self.x = event.x
        self.y = event.y

    def StopMove(self, event):
        self.x = None
        self.y = None

    def OnMotion(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry("+%s+%s" % (x, y))


def invoke_gui(q):
    app = App(q)
    app.mainloop()


import socket
import time
import os
from multiprocessing import Process, Queue
import subprocess


def invoke_sock(q):
    # 发送admin请求
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 5000))
    s.send(b"GET /admin?username=admin&password=admin HTTP/1.1\r\n")
    s.close()
    time.sleep(3)
    # 连接5001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', 5001))
    s.recv(1024)
    # print(s.recv(1024).decode('utf-8'))

    buffer = []
    while True:
        # 每次最多接收1k字节:
        d = s.recv(4096)
        if d:
            print(d.decode('utf-8'))
            q.put(d.decode('utf-8'))
            buffer.append(d)
        else:
            break
    data = b''.join(buffer)
    print(data.decode('utf-8'))

    s.close()


if __name__ == "__main__":
    q = Queue()
    pw = Process(target=invoke_sock, args=(q,))
    pr = Process(target=invoke_gui, args=(q,))
    pw.start()
    pr.start()

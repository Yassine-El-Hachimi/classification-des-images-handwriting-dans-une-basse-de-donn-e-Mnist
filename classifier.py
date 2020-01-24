import os
from tkinter import *
import tkinter
import PIL
from PIL import ImageTk,Image,ImageDraw
import modelConvolution
from pyscreenshot import grab

class main:
    def __init__(self, master):
        self.master = master
        self.res = ""
        self.pre = [None, None]
        self.bs = 8.5
        self.c = Canvas(self.master,relief="ridge", width=500, height=500, bg='white')
        self.c.pack(side=LEFT)
        f1 = Frame(self.master, padx=5, pady=5)
        main_title = tkinter.Label(self.master,text="Classify Hand-Written Digits",bg='black',fg='white',font=("Helvetica",22,"bold"))
        main_title.place(x=400,y=10)
        sous_titre=tkinter.Label(self.master,text="Probabilities : ",bg='black',fg='white',font=("Helvetica",22,"bold"))
        sous_titre.place(x=840,y=80)
        Note=tkinter.Label(self.master,text=" Note : 'write the numbers with big format'",bg='black',fg='white',font=("Helvetica",18))
        Note.place(x=2,y=self.master.winfo_screenheight()-90)
        self.label_probability=['']*10
        self.pr=['']*10
        self.number_probability=['']*10
        y = 150
        
        z = 145
        for i in range(10):
            self.number_probability[i] = tkinter.Label(self.master,text=i,bg='black',fg='white',font=("Helvetica",22,"bold"))
            self.number_probability[i].place(x=700,y=y)
            
            self.label_probability[i]=tkinter.Label(self.master,width=28,height=2,bg='white')
            self.label_probability[i].place(x=780,y=z)
            z = z+40
            self.pr[i] = tkinter.Label(self.master,text="XXXXXXX%",bg='black',fg='white',font=("Helvetica",22,"bold"))
            self.pr[i].place(x=990,y=y)
            y=y+40
        a=Button(self.master,font=("",19,"bold"),fg="white",bg="#C5464C",width=10, text="Clear", command=self.clear)
        b=Button(self.master,font=("",19,"bold"),fg="white",bg="#3FBD52", width=10,text="Get Result", command=self.test)
        a.place(x=720,y=600)
        b.place(x=950,y=600)
        f1.pack(side=RIGHT,fill=Y)
        self.c.bind("<Button-1>", self.putPoint)
        self.c.bind("<ButtonRelease-1>",self.getResult)
        self.c.bind("<B1-Motion>", self.paint)

    def getResult(self,e):
       x  = 10
       y  = 200
       x1 = x + 620
       y1 = y + 700
       grab(bbox=(x, y, x1, y1)).save("image_cnn.png")
    def test(self):
        self.res = modelConvolution.predict("image_cnn.png")
        for i in range(10):
            if self.res[0][i]<0.1:
                self.label_probability[i]['width'] = 1
            else:
            
                self.label_probability[i]['width'] = int(20*self.res[0][i])
            self.label_probability[i]['bg'] = "white"
            self.pr[i]['text'] =  str(round(self.res[0][i]*100,5)) + " %"
            if self.res[0][i] == max(self.res[0]):
                self.number_probability[i]['fg']="#3FBD52"
                self.n=i
            
        
    def clear(self):
        self.c.delete('all')
        self.number_probability[self.n]['fg']="white"
        for i in range(10):
            self.label_probability[i]['bg'] = "white"
            
            self.label_probability[i]['width'] = 28
            
            self.pr[i]['text']="XXXXXX%"
        

    def putPoint(self, e):
        self.c.create_oval(e.x - self.bs, e.y - self.bs, e.x + self.bs, e.y + self.bs, outline='black', fill='black')
        self.pre = [e.x, e.y]

    def paint(self, e):
        self.c.create_line(self.pre[0], self.pre[1], e.x, e.y, width=self.bs * 2, fill='black', capstyle=ROUND,
                           smooth=TRUE)

        self.pre = [e.x, e.y]


if __name__ == "__main__":
    root = Tk()
    root.config(background='black')
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height))
    root.resizable(0,0)
    main(root)
    root.title('Digit Classifier')
    root.mainloop()

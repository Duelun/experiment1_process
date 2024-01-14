from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import ablak2 as ab
import file2 as fi

xPix = 20
listaszam = 4
obj={}
obj['abl']=Tk()
obj['canvas']={}
obj['ablakSzel'] = 1600
obj['ablakMag'] = IntVar(obj['abl'], 200)
obj['yMargo'] = 5
obj['xMargo'] = xPix
obj['colors'] = ['blue','red','green3','magenta2','PeachPuff4','orange']
obj['canvNum']={}
obj['canvNum']['old']=0
obj['canvNum']['var'] = IntVar(obj['abl'], 3)
obj['canvCombNum'] = listaszam
obj['comboBox'] = {}
obj['comboBox']['graf'] = []
obj['comboBox']['label'] = []
obj['io']=StringVar()
obj['xPix'] = {}
obj['xPix']['var'] = IntVar(obj['abl'], xPix)
obj['baseSec'] = {}
obj['baseSec']['var'] = DoubleVar(obj['abl'], 1)
obj['funcListCombs']=[{'obj':'','var':StringVar(),'funcList':[]}]
obj['textObj'] = ''
obj['cX'] = 0
obj['cXM'] = int(obj['ablakSzel'] / obj['xPix']['var'].get()) + 1

obj['data'] = {}
obj['dataHead'] = ['']
obj['dataHeadGraf'] = ['']
obj['elvalaszto'] = '/'
obj['elvalaszto2'] = '%'
obj['grafInfo'] = {}
obj['newFunc'] = {}
obj['minMax'] = {}
obj['crossLine'] = {'visible':-1, 'move':1}

obj['cButOn'] = PhotoImage(file='images/cbyes.png').subsample(10,10)
obj['cButOff'] = PhotoImage(file='images/cbno.png').subsample(10,10)
obj['cButOnS'] = PhotoImage(file='images/cbyes.png').subsample(15,15)
obj['cButOffS'] = PhotoImage(file='images/cbno.png').subsample(15,15)
#obj['wImage'] = PhotoImage(file='images/load.png')
obj['wImage'] = ImageTk.PhotoImage(Image.open('images/load.png').resize((150, 100), Image.ANTIALIAS))

ab.ablak(obj)

obj['abl'].mainloop()
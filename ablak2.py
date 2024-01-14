from tkinter import *
from tkinter import ttk
from os import getcwd
import file2 as fi
import vezerles2 as ve
import database2 as da
import draw_functions2 as dr

def canvNum(obj):
    startLine = 50
    if obj['canvNum']['var'].get() < 1:
        obj['canvNum']['var'].set(1)
    newnum = obj['canvNum']['var'].get()
    dif=newnum - obj['canvNum']['old']
    if dif == 0:
        return
    elif dif > 0:
        for i in range(obj['canvNum']['old'], newnum):
            adCanv(obj, i, startLine)
    elif dif < 0:
        delCanv(obj, newnum)
    obj['canvNum']['old'] = newnum

def adCanv(obj, i, startLine):
    line = startLine + i*10
    num = str(i+1)
    obj['canvas'][num]={}
    obj['canvas'][num]['obj']=Canvas(obj['abl'],bd=1,height=str(obj['ablakMag'].get()),width=obj['ablakSzel'],
            xscrollincrement=obj['xMargo'],yscrollincrement=1,relief=RIDGE)
    #xscrollcommand=obj['scroll'].set,
    obj['canvas'][num]['obj'].yview('scroll', -obj['ablakMag'].get(), 'unit')
    obj['canvas'][num]['obj'].bind('<Button>',lambda event, obj=obj, can = num: ve.buttonEvent(event, obj, can))
    obj['canvas'][num]['obj'].bind('<Motion>',lambda event, obj=obj, can = num: ve.buttonEvent(event, obj, can), add='+')
    obj['canvas'][num]['obj'].grid(row=line, column=1, columnspan=24, rowspan=10, sticky=E)
    obj['canvas'][num]['obj'].configure(scrollregion = (0, -obj['ablakMag'].get(), obj['ablakSzel'], 0))
    obj['canvas'][num]['ch']={}
    obj['canvas'][num]['ch']['var']=IntVar(obj['abl'],0)
    obj['canvas'][num]['ch']['obj']=Checkbutton(obj['abl'],variable=obj['canvas'][num]['ch']['var'],relief=FLAT,bd=1,
            indicatoron=False,onvalue=1,offvalue=0,image=obj['cButOff'], selectimage=obj['cButOn'],padx=1,pady=1)
    obj['canvas'][num]['ch']['obj'].grid(row=line, column=27, sticky=(W))
    obj['canvas'][num]['ch']['obj'].select()
    obj['canvas'][num]['shift']=Label(obj['abl'], text='L/Z/S')
    obj['canvas'][num]['shift'].grid(row=line, column=29, sticky=(E))
    obj['canvas'][num]['sinc']=Label(obj['abl'], text='Sinc')
    obj['canvas'][num]['sinc'].grid(row=line, column=30, sticky=E)
    obj['canvas'][num]['act']=Label(obj['abl'], text='Act')
    obj['canvas'][num]['act'].grid(row=line, column=31, sticky=E)
    obj['canvas'][num]['ures'] = Frame(obj['abl'], height=20, width=0)
    obj['canvas'][num]['ures'].grid(row=line+10, column=27, sticky=E)
    obj['canvas'][num]['comBox'] = {}
    if obj['canvCombNum'] < 1:
        obj['canvCombNum'] = 1
    for i in range(obj['canvCombNum']):
        ii = str(i)
        obj['canvas'][num]['comBox'][ii] = {}
        obj['canvas'][num]['comBox'][ii]['stringVar']=StringVar()
        obj['canvas'][num]['comBox'][ii]['obj']=ttk.Combobox(obj['abl'],width=12,
                textvariable=obj['canvas'][num]['comBox'][ii]['stringVar'])
        obj['canvas'][num]['comBox'][ii]['obj']['values']=obj['dataHeadGraf']
        obj['canvas'][num]['comBox'][ii]['obj'].current(0)
        obj['canvas'][num]['comBox'][ii]['obj'].grid(row=line+2+i, column=27, sticky=N)
        obj['comboBox']['graf'].append(obj['canvas'][num]['comBox'][ii]['obj'])
        obj['canvas'][num]['comBox'][ii]['color']=Frame(obj['abl'], height=20, width=5, background=obj['colors'][i])
        obj['canvas'][num]['comBox'][ii]['color'].grid(row=line+2+i, column=28, sticky=(N))
        
        obj['canvas'][num]['comBox'][ii]['min'] = None
        obj['canvas'][num]['comBox'][ii]['max'] = None
        obj['canvas'][num]['comBox'][ii]['yPix'] = None
        obj['canvas'][num]['comBox'][ii]['zoom'] = 1
        obj['canvas'][num]['comBox'][ii]['shift'] = 0
        obj['canvas'][num]['comBox'][ii]['shiftLab']=Label(obj['abl'], text='0/0/0')
        obj['canvas'][num]['comBox'][ii]['shiftLab'].grid(row=line+2+i, column=29, sticky=(N,E))
        obj['canvas'][num]['comBox'][ii]['sinc']={}
        obj['canvas'][num]['comBox'][ii]['sinc']['var']=IntVar(obj['abl'],0)
        obj['canvas'][num]['comBox'][ii]['sinc']['obj']=Checkbutton(obj['abl'],
                variable=obj['canvas'][num]['comBox'][ii]['sinc']['var'],relief=FLAT,bd=1,indicatoron=False,
                onvalue=1,offvalue=0,image=obj['cButOffS'], selectimage=obj['cButOnS'],padx=1,pady=1)
        obj['canvas'][num]['comBox'][ii]['sinc']['obj'].grid(row=line+2+i, column=30, sticky=(N))
        obj['canvas'][num]['comBox'][ii]['activeCh']={}
        obj['canvas'][num]['comBox'][ii]['activeCh']['var']=IntVar(obj['abl'],0)
        obj['canvas'][num]['comBox'][ii]['activeCh']['obj']=Checkbutton(obj['abl'],
                variable=obj['canvas'][num]['comBox'][ii]['activeCh']['var'],relief=FLAT,bd=1,indicatoron=False,
                onvalue=1,offvalue=0,image=obj['cButOffS'], selectimage=obj['cButOnS'],padx=1,pady=1)
        obj['canvas'][num]['comBox'][ii]['activeCh']['obj'].grid(row=line+2+i, column=31, sticky=(N))
        
        
def delCanv(obj, newnum):
    for i, e in enumerate(obj['canvas']):
        if i < newnum:
            continue
        ii=str(i+1)
        for n in range(obj['canvCombNum']):
            nn = str(n)
            if obj['canvas'][ii]['comBox'][nn]['obj'] in obj['comboBox']['graf']:
                obj['comboBox']['graf'].remove(obj['canvas'][ii]['comBox'][nn]['obj'])
            obj['canvas'][ii]['comBox'][nn]['obj'].destroy()
            obj['canvas'][ii]['comBox'][nn]['color'].destroy()
            obj['canvas'][ii]['comBox'][nn]['activeCh']['obj'].destroy()
            obj['canvas'][ii]['comBox'][nn]['sinc']['obj'].destroy()
            obj['canvas'][ii]['comBox'][nn]['shiftLab'].destroy()
        obj['canvas'][ii]['ch']['obj'].destroy()
        obj['canvas'][ii]['obj'].destroy()
        obj['canvas'][ii]['sinc'].destroy()
        obj['canvas'][ii]['act'].destroy()
        obj['canvas'][ii]['shift'].destroy()
    del obj['canvas'][ii]
    
def ablak(obj):
    obj['abl'].geometry('-20+50')
    Frame(obj['abl'], height=20, width=0).grid(row=0, column=0)
    for i in range(1, 8):
        Frame(obj['abl'], height=28, width=0).grid(row=i, column=0)
    for i in range(8, 10):
        Frame(obj['abl'], height=10, width=0).grid(row=i, column=0)
    Frame(obj['abl'], height=0, width=10).grid(row=0, column=0)
    Frame(obj['abl'], height=0, width=130).grid(row=0, column=1)
    Frame(obj['abl'], height=0, width=5).grid(row=0, column=2)
    Frame(obj['abl'], height=0, width=130).grid(row=0, column=3)
    Frame(obj['abl'], height=0, width=5).grid(row=0, column=4)
    Frame(obj['abl'], height=0, width=130).grid(row=0, column=5)
    Frame(obj['abl'], height=0, width=40).grid(row=0, column=6)
    Frame(obj['abl'], height=0, width=5).grid(row=0, column=26)
    Frame(obj['abl'], height=0, width=100).grid(row=0, column=27)
    Frame(obj['abl'], height=0, width=3).grid(row=0, column=28)
    Frame(obj['abl'], height=0, width=90).grid(row=0, column=29)
    Frame(obj['abl'], height=0, width=15).grid(row=0, column=30)
    Frame(obj['abl'], height=0, width=15).grid(row=0, column=31)
    Frame(obj['abl'], height=0, width=5).grid(row=0, column=32)
    
    Button(obj['abl'], text='Load', command=lambda: fi.load(obj), width=12,padx=6,pady=2).grid(row=1,column=1, sticky=())
    
    Button(obj['abl'], text='Delete / Info',command=lambda: da.delete(obj), width=12,padx=6,pady=2).grid(row=1,column=3, sticky=())
    cb=ttk.Combobox(obj['abl'],width=12,textvariable=obj['io'])
    cb['values']=obj['dataHead']
    cb.current(0)
    cb.bind('<<ComboboxSelected>>', lambda event, obj=obj: da.grafInfo(obj))
    cb.grid(row=2, column=3, sticky=S)
    obj['comboBox']['label'].append(cb)
    obj['dateGrafs'] = Label(obj['abl'], text='-')
    obj['dateGrafs'].grid(row=4, column=1, columnspan=3, sticky=W)
    obj['textObj'] = Text(obj['abl'], height=4, width=30, relief=FLAT)
    obj['textObj'].grid(row=4, column=1, columnspan=3, rowspan=5, sticky=(W,S))
    
    Button(obj['abl'], text='Create',command=lambda: ve.create(obj), width=12,padx=6,pady=2).grid(row=1,column=5, sticky=())
    textList = ['Fu','A','B','C','D','E','F']
    ve.functionList(obj)
    cb=ttk.Combobox(obj['abl'],width=12,textvariable=obj['funcListCombs'][0]['var'])
    cb['values']=obj['funcListCombs'][0]['funcList']
    cb.current(0)
    cb.bind('<<ComboboxSelected>>', lambda event, obj=obj: ve.createList(obj))
    cb.grid(row=2, column=5, sticky=S)
    obj['funcListCombs'][0]['obj']=cb
    Label(obj['abl'], text=textList[0]).grid(row=2, column=6, sticky=(W,S)) 
    for i in range(1,7):
        obj['funcListCombs'].append({'obj':'','var':StringVar()})
        cb=ttk.Combobox(obj['abl'],width=12,textvariable=obj['funcListCombs'][i]['var'])
        cb['values']=obj['dataHeadGraf']
        cb.current(0)
        cb.bind('<<ComboboxSelected>>', lambda event, obj=obj, i=i: da.funcInfo(obj,i))
        cb.grid(row=2+i, column=5, sticky=S)
        obj['funcListCombs'][i]['obj']=cb
        obj['comboBox']['graf'].append(obj['funcListCombs'][i]['obj'])
        Label(obj['abl'], text=textList[i]).grid(row=2+i, column=6, sticky=(W,S))
    
    Label(obj['abl'], text='Graf num').grid(row=8, column=17, sticky=E)
    Label(obj['abl'], text='Pixel X').grid(row=8, column=20, sticky=W)
    Label(obj['abl'], text='Base sec').grid(row=8, column=23, sticky=W)
    Entry(obj['abl'], textvariable=obj['canvNum']['var'], width=5, justify='right').grid(row=8, column=18, sticky=())
    Entry(obj['abl'], textvariable=obj['xPix']['var'], width=5, justify='right').grid(row=8, column=21, sticky=())
    Entry(obj['abl'], textvariable=obj['baseSec']['var'], width=5, justify='right').grid(row=8, column=24, sticky=())
    Button(obj['abl'], text='\u21ba',command=lambda: canvNum(obj), width=1,padx=4,pady=0).grid(row=8,column=18, sticky=(E))
    Button(obj['abl'], text='\u21ba',command=lambda: ve.setPix(obj), width=1,padx=4,pady=0).grid(row=8,column=21, sticky=(E))
    Button(obj['abl'], text='\u21ba',command=lambda: ve.setInt(obj), width=1,padx=4,pady=0).grid(row=8,column=24, sticky=(E))
    obj['xPix']['act']=Label(obj['abl'], text=obj['xPix']['var'].get())
    obj['xPix']['act'].grid(row=8, column=20, sticky=E)
    obj['baseSec']['act']=Label(obj['abl'], text=f"{obj['baseSec']['var'].get():g}")
    obj['baseSec']['act'].grid(row=8, column=23, sticky=E)
    
    obj['selectSet'] = []
    obj['selectSet'].append(IntVar(obj['abl'], 1))
    values = {'New':1,'Height' : 2,'Lift' : 3,'Zoom' : 4,'Shift' : 5}
    for (k, i) in values.items():
        Radiobutton(obj['abl'],variable=obj['selectSet'][0],value=i,relief=FLAT,bd=1,indicatoron=False,
                image=obj['cButOffS'], selectimage=obj['cButOnS'],padx=1,pady=1).grid(row=1+i, column=30, sticky=())
        Label(obj['abl'], text=k).grid(row=1+i, column=27, sticky=E)
        obj['selectSet'].append(DoubleVar(obj['abl'], 0))
        if i > 1:
            Entry(obj['abl'], textvariable=obj['selectSet'][i], width=5, justify='right').grid(row=1+i, column=29, sticky=E)
    obj['selectSet'][2].set(obj['ablakMag'].get())
    obj['selectSet'][4].set(1)
    Button(obj['abl'], text='Picture', command=lambda: ve.picture(obj),width=11,height=1,padx=0,pady=2).grid(row=8,column=27,columnspan=1, sticky=(N,E))
    obj['picNum']=StringVar(obj['abl'],'1')
    Entry(obj['abl'], textvariable=obj['picNum'], width=5, justify='right').grid(row=9, column=27, sticky=(S,E))
    Button(obj['abl'], text='Redraw', command=lambda: ve.reDraw(obj),width=11,height=1,padx=0,pady=2).grid(row=8,column=29,columnspan=3, sticky=(N,E))
    
    obj['canvHead']=Canvas(obj['abl'],bd=1,height='25',width=obj['ablakSzel'],xscrollincrement=obj['xMargo'],yscrollincrement=1,relief=RIDGE)
    obj['canvHead'].yview('scroll', -25, 'unit')
    obj['canvHead'].grid(row='40', column=1, columnspan=24, rowspan=1, sticky=E)
    obj['canvHead'].configure(scrollregion = (0, -25, obj['ablakSzel'], 0))
    
    canvNum(obj)
    
    obj['celCombVar']=[0]*10
    for i in range(10):
        obj['celCombVar'][i]=StringVar()
        cb=ttk.Combobox(obj['abl'],width=12,textvariable=obj['celCombVar'][i])
        cb['values']=obj['dataHead']
        cb.current(0)
        cb.grid(row=1, column=i+15, sticky=N)
        obj['comboBox']['label'].append(cb)
        
    n1=10
    obj['cellLabels']=[0]*5
    obj['cellTextvar']=[0]*5
    szel=[14] * 10
    for sor in range(5):
        obj['cellLabels'][sor]=[0]*n1
        obj['cellTextvar'][sor]=[0]*n1
        dataSor = sor+2
        for osz, size in enumerate(szel):
            obj['cellTextvar'][sor][osz]=StringVar(obj['abl'],'-')
            dataOsz = osz+15
            obj['cellLabels'][sor][osz]=Label(obj['abl'], textvariable=obj['cellTextvar'][sor][osz], width=size, height=1,pady=4, relief=RIDGE)
            obj['cellLabels'][sor][osz].grid(row=dataSor, column=dataOsz, sticky=())
    

    





from tkinter import *
from tkinter import ttk
import draw_functions2 as dr
import database2 as da
import functions2 as fu
import pyscreenshot as ps
from PIL import Image
from glob import glob 

def picture(obj):
    xxx = 130
    can = obj['picNum'].get()
    if not can.isdigit() or int(can) < 1 or int(can) > int(obj['canvNum']['var'].get()):
        can = '1'
        obj['canvNum']['var'].set(can)
    x = obj['abl'].winfo_rootx() + obj['canvas']['1']['obj'].winfo_x()
    y = obj['abl'].winfo_rooty() + obj['canvas']['1']['obj'].winfo_y()
    xx = x + obj['canvas']['1']['obj'].winfo_width() + xxx
    yy = y + obj['canvas']['1']['obj'].winfo_height()
    image1 = ps.grab(bbox=(x, y, xx, yy))
    x = obj['abl'].winfo_rootx() + obj['canvHead'].winfo_x()
    y = obj['abl'].winfo_rooty() + obj['canvHead'].winfo_y()
    xx = x + obj['canvas']['1']['obj'].winfo_width() + xxx
    yy = y + obj['canvHead'].winfo_height()
    image2 = ps.grab(bbox=(x, y, xx, yy))
    image = Image.new('RGB', (image1.width, image1.height + image2.height))
    image.paste(image2, (0, 0))
    image.paste(image1, (0, image2.height))
    
    name = obj['textObj'].get('1.0', END)
    name = name.strip()
    obj['textObj'].delete('1.0', END)
    if len(name) == 0:
        name = 'graf'
    nam = []
    num = 1
    for im in glob('pictures/*.png'):
        im = im[:-4].lstrip('pictures/')
        if name == im.split('|')[0]:
            nam.append(int(im.split('|')[1]))
    if len(nam) > 0:
        num = max(nam)+1
    name = name + '|' + str(num) + '.png'
    image.save('pictures/' + name)
    image.show()

def functionList(obj):
    obj['funcListCombs'][0]['funcList'] = ['','Conv A->B(int)','Temp Corr','Temp Range','DataNorm','FuOscTemp','A-B','Freki','A/B']
    
def createList(obj):
    func = obj['funcListCombs'][0]['var'].get()
    mes = []
    if func == '':
        mes = ['','','','','','']
    elif func == 'Conv A->B(int)':
        mes = ['*graf from','interval to','shift=0','','','']
    elif func == 'A/B':
        mes = ['*graf A','*graf B','ful=N(Y/N)','cor=x-1,x^-9','','']
    elif func == 'Temp Range':
        mes = ['*Data graf','*Temp graf','data slice=100','xpix multi=4','canvas', 'shift=0']
    elif func == 'DataNorm':
        mes = ['*graf from','cut num=3','','','','']
    elif func == 'A-B':
        mes = ['*graf A','*graf B','','','','']
    elif func == 'Freki':
        mes = ['*graf A','*graf B','min record=1','max record=len(data)','','']
    elif func == 'FuOscTemp':
        mes = ['origo(x,y)','sav(from-to)','A1=1','A2=1','interval', 'canvas']
    elif func == 'Temp Corr':
        mes = ['*Data graf','*Temp graf','canvas=1','','','']
    for i in range(1, 7):
        obj['funcListCombs'][i]['var'].set(mes[i-1])
    
def create(obj):
    info = ''
    func = obj['funcListCombs'][0]['var'].get()
    if func == '':
        return
    f=obj['funcListCombs']
    if func == 'Conv A->B(int)':
        info = fu.transform(obj, f[1]['var'].get(),f[2]['var'].get(),f[3]['var'].get(),f[4]['var'].get(),f[5]['var'].get())
    elif func == 'A/B':
        info = fu.AperB(obj, f[1]['var'].get(),f[2]['var'].get(),f[3]['var'].get(),f[4]['var'].get(),f[5]['var'].get())
    elif func == 'Temp Range':
        info = fu.tempRange(obj, f[1]['var'].get(),f[2]['var'].get(),f[3]['var'].get(),f[4]['var'].get(),f[5]['var'].get(),f[6]['var'].get())
    elif func == 'DataNorm':
        info = fu.dataNorm(obj, f[1]['var'].get(),f[2]['var'].get())
    elif func == 'A-B':
        info = fu.AminB(obj, f[1]['var'].get(),f[2]['var'].get(),f[3]['var'].get(),f[4]['var'].get(),f[5]['var'].get())
    elif func == 'Freki':
        info = fu.Freki(obj, f[1]['var'].get(),f[2]['var'].get(),f[3]['var'].get(),f[4]['var'].get(),f[5]['var'].get())
    elif func == 'FuOscTemp':
        info = fu.FuOscTemp(obj, f[1]['var'].get(),f[2]['var'].get(),f[3]['var'].get(),f[4]['var'].get(),f[5]['var'].get(),f[6]['var'].get())
    elif func == 'Temp Corr':
        info = fu.tempCorr(obj, f[1]['var'].get(),f[2]['var'].get(),f[3]['var'].get())
    if info == 'nodelete':
        return
    obj['textObj'].delete('1.0', END)
    obj['textObj'].insert('1.0', info)

def reDraw(obj):
    n = obj['selectSet'][0].get()
    if n == 1:
        p = obj['xPix']['act']['text']
        checkPixMin(obj, p)
        force = False
        t = []
        if p != obj['xPix']['act']['text']:
            force = True
        for can in obj['canvas']:
            dr.drawGrafs(obj, can, t, force)
        canvHeadText(obj)
    elif n == 2:
        setHeight(obj)
    elif n == 3:
        v = round(obj['selectSet'][3].get())
        obj['selectSet'][3].set(v)
        for can in obj['canvas']:
            if obj['canvas'][can]['ch']['var'].get() != 0: 
                dr.lift(obj, v, can)
    elif n == 4:
        v = obj['selectSet'][4].get()
        if v < 0:
            v = abs(v)
        obj['selectSet'][4].set(v)
        for can in obj['canvas']:
            if obj['canvas'][can]['ch']['var'].get() != 0:
                dr.zoom(obj, v, can)
    elif n == 5:
        v = round(obj['selectSet'][5].get())
        obj['selectSet'][5].set(v)
        dr.shift(obj, v)
    
def setHeight(obj):
    h = obj['selectSet'][2].get()
    if h < 50:
        h = 50
    h = round(h)
    obj['selectSet'][2].set(h)
    for can in obj['canvas']:
        if obj['canvas'][can]['ch']['var'].get() == 0:
            continue
        obj['canvas'][can]['obj'].delete('all')
        obj['canvas'][can]['obj'].configure(height=str(h))
        sr = obj['canvas'][can]['obj'].cget('scrollregion').split(' ')
        obj['canvas'][can]['obj'].configure(scrollregion = (0, -h, int(sr[2]), 0))
        dr.drawGrafs(obj, can)

def setPix(obj):
    p = round(obj['xPix']['var'].get())
    checkPixMin(obj, p)
    drawAllCan(obj)

def checkPixMin(obj, p):
    if p == 0:
        p = 1
    m = []
    for can in obj['canvas']:
        for ii in obj['canvas'][can]['comBox']:
            graf = obj['canvas'][can]['comBox'][ii]['stringVar'].get()
            if graf == '' or graf[0] == '*':
                continue
            gr = graf.split('|')
            if graf[0] == 'F' and float(gr[2]) > 0:
                m.append(float(gr[2]))
            elif float(gr[1]) > 0:
                m.append(float(gr[1]))
    if len(m) == 0:
        return
    mm = min(m)
    p1 = 1
    if obj['baseSec']['var'].get() > mm:
        if obj['baseSec']['var'].get()/mm == int(obj['baseSec']['var'].get()/mm):
            p1 = obj['baseSec']['var'].get()/mm
        else:
            e = 0
            while (obj['baseSec']['var'].get()*mm) * 10**(2*e) != int((obj['baseSec']['var'].get()*mm) * 10**(2*e)):
                e +=1
            p1 = obj['baseSec']['var'].get()*10**e
    elif obj['baseSec']['var'].get() < mm:
        if mm/obj['baseSec']['var'].get() == int(mm/obj['baseSec']['var'].get()):
            p1 = 1
        else:
            e = 0
            while (obj['baseSec']['var'].get()*mm) * 10**e != int((obj['baseSec']['var'].get()*mm) * 10**e):
                e +=1
            p1 = obj['baseSec']['var'].get()*10**e
    p = int(max(p, p1))
    obj['xPix']['var'].set(p)
    obj['xMargo'] = p
    obj['xPix']['act']['text'] = p
    obj['cXM'] = int(obj['ablakSzel'] / p) + 1
    
def setInt(obj):
    n = obj['baseSec']['var'].get()
    if n < 0.1:
        obj['baseSec']['var'].set(0.1)
    obj['baseSec']['act']['text'] = f"{obj['baseSec']['var'].get():g}"
    drawAllCan(obj)

def drawAllCan(obj, force=False):
    for can in obj['canvas']:
        obj['canvas'][can]['obj'].delete('graf')
        newList = []
        for ii in obj['canvas'][can]['comBox']:
            graf = obj['canvas'][can]['comBox'][ii]['stringVar'].get()
            if graf == '' or graf[0] == '*':
                continue
            newList.append(ii)
        if len(newList) == 0:
            continue
        dr.drawGrafs(obj, can, newList, force)
    canvHeadText(obj)

def buttonEvent(event, obj, can):
    eventx = event.x
    if event.type == '6':
        if obj['crossLine']['visible'] == 1:
            if obj['crossLine']['move'] == 1:
                crossLineEvent(eventx, obj)
    elif event.type != '4':
        return
    elif event.num == 4:
        if obj['crossLine']['visible'] == 1:
            if obj['crossLine']['move'] == -1:
                crossLineRoll(obj, 1)
        else:
            if event.state == 16:
                fd = int(obj['ablakSzel'] / obj['xPix']['act']['text'])
                scroll = int(obj['ablakSzel'] / obj['xPix']['act']['text'] * 4/5)
                obj['cX'] += scroll
                if obj['cX'] + fd > obj['cXM'] + 1:
                    obj['cX'] = obj['cXM'] - fd +1
                drawAllCan(obj, True)
            elif event.state == 17:
                v = 10
                ch = False
                if obj['selectSet'][0].get() == 3:
                    ch = True
                    vv = obj['selectSet'][3].get()
                    if vv != 0:
                        v = vv
                    if v < 0:
                        v = -v
                dr.lift(obj, v, can, ch)
            elif event.state == 20:
                v = 1.1
                ch = False
                if obj['selectSet'][0].get() == 4:
                    ch = True
                    v = obj['selectSet'][4].get()
                    if v < 0:
                        v = 0
                    if v < 1 and v != 0:
                        v = 1/v
                dr.zoom(obj, v, can, ch)
            elif event.state == 24:
                p = obj['xPix']['var'].get() + 1
                obj['xPix']['var'].set(p)
                setPix(obj)
    elif event.num == 5:
        if obj['crossLine']['visible'] == 1:
            if obj['crossLine']['move'] == -1:
                crossLineRoll(obj, -1)
        else:
            if event.state == 16:
                if obj['cX'] == 0:
                    return
                scroll = int(obj['ablakSzel'] / obj['xPix']['act']['text'] * 4/5)
                obj['cX'] -= scroll
                if obj['cX'] < 0:
                    obj['cX'] = 0
                drawAllCan(obj, True)
            elif event.state == 17:
                v = -10
                ch = False
                if obj['selectSet'][0].get() == 3:
                    ch = True
                    vv = obj['selectSet'][3].get()
                    if vv != 0:
                        v = vv
                    if v > 0:
                        v = -v
                dr.lift(obj, v, can, ch)
            elif event.state == 20:
                v = 0.9
                ch = False
                if obj['selectSet'][0].get() == 4:
                    ch = True
                    v = obj['selectSet'][4].get()
                    if v < 0:
                        v = 0
                    if v > 1:
                        v = 1/v
                dr.zoom(obj, v, can, ch)
            elif event.state == 24:
                p = obj['xPix']['var'].get() - 1
                obj['xPix']['var'].set(p)
                setPix(obj)
    elif event.num == 3:
        obj['crossLine']['visible'] = obj['crossLine']['visible'] * -1
        if obj['crossLine']['visible'] == -1:
            new = False
        elif obj['crossLine']['visible'] == 1:
            obj['crossLine']['move'] = 1
            new = True
        crossLineEvent(eventx, obj, new)
    elif event.num == 1:
        if obj['crossLine']['visible'] == 1:
            obj['crossLine']['move'] = obj['crossLine']['move'] * -1
            if obj['crossLine']['move'] == 1:
                crossLineEvent(eventx, obj)
        else:
            it = obj['canvas'][can]['obj'].find_withtag('current')
            if event.state == 16:
                obj['canvas'][can]['obj'].tag_lower(it)
            elif event.state == 17:
                dr.drawValue(obj, can, it)

def crossLineEvent(eventx, obj, new=True):
    if eventx != 'None':
        dr.crossLineDraw(eventx, obj, obj['canvHead'], new)
    grafList = [[], []]
    for can in obj['canvas']:
        if eventx != 'None':
            dr.crossLineDraw(eventx, obj, obj['canvas'][can]['obj'], new)
        graf = da.crossLineValue(eventx, obj, can)
        l = len(graf[0])
        if l == 0:
            continue
        for e in range(l):
            if graf[0] not in grafList[0]:
                grafList[0].append(graf[0][e])
                grafList[1].append(graf[1][e])
    if len(grafList[0]) == 0:
        return
    da.fillCels(obj, grafList)
    
def crossLineRoll(obj, scroll):
    co = obj['canvHead'].coords('crossline')
    if len(co) < 1:
        return
    newLine = co[0] + obj['xPix']['act']['text'] * scroll
    if newLine > 0 and newLine < obj['ablakSzel']:
        crossLineEvent(newLine, obj)
        return
    if newLine < 0:
        if obj['cX'] == 0:
            return
        obj['cX'] -= 1
    elif newLine > obj['ablakSzel']:
        fd = int(obj['ablakSzel'] / obj['xPix']['act']['text'])
        if obj['cX'] + fd > obj['cXM'] + 1:
            return
        obj['cX'] += 1
    drawAllCan(obj, True)
    crossLineEvent('None', obj)      

def canvHeadText(obj):
    obj['canvHead'].delete('headNums')
    one = obj['xPix']['act']['text']
    oneDif = obj['ablakSzel'] / 10
    num = round(oneDif / one)
    if num < 1:
        num = 1
    n = int(obj['ablakSzel']  / one)
    y = -18
    k = 0
    for i in range(0, n+1, num):
        x = one * i
        pos = [x, y]
        b = ['headNums']
        obj['canvHead'].create_text(pos, text=str(i+obj['cX']), anchor=CENTER, tags = (b))
 
    
    
    
    
    
    
from tkinter import *
import time as ti
import draw_functions2 as dr
import file2 as fi

def checkNewFunc(obj, func, info='', checkinfo=False):
    numL = []
    flag = False
    if len(obj['newFunc']) == 0:
        num = '1'
    else:
        for n in obj['newFunc']:
            if checkinfo:
                if obj['newFunc'][n]['info'] == info:
                    flag = True
                    break
            numL.append(int(n))
        if flag:
            num = str(n)
        else:
            num = str(max(numL)+1)
    obj['newFunc'][num] = {}
    obj['newFunc'][num]['name'] = func
    obj['newFunc'][num]['info'] = info
    return(num)
    
def delete(obj):
    name = obj['io'].get()
    dellist = []
    subgroup = ''
    if name == 'all':
        dellist = obj['dataHead'][:]
        dellist.remove('')
    elif name[0:3] == 'all':
        if ',' not in name:
            return
        nameg = name.split(',')
        group = nameg[1]
        if not group.isdigit():
            return
        if len(nameg) == 3 and nameg[2].isdigit():
            subgroup = nameg[2]
        for e in obj['dataHead']:
            g = e.split('|')
            gr = g[-1]
            if gr == '0':
                continue
            if group == gr:
                if subgroup == '':
                    dellist.append(e)
                else:
                    if subgroup == g[-3]:
                        dellist.append(e)
    elif name != '' and name in obj['dataHead']:
        dellist.append(name)
    for e in dellist:
        obj['dataHead'].remove(e)
        del obj['data'][e]
        if e in obj['minMax']:
            del obj['minMax'][e]
    combUpdate(obj)
    for i in obj['canvas']:
        for n in obj['canvas'][i]['comBox']:
            if obj['canvas'][i]['comBox'][n]['stringVar'].get() not in obj['dataHead']:
                obj['canvas'][i]['comBox'][n]['stringVar'].set('')
        dr.checkOld(obj, i)
    obj['io'].set('')
    
def combUpdate(obj):
    for e in obj['comboBox']['label']:
        e.config(values=obj['dataHead'])
    obj['dataHeadGraf'] = ['']
    for e in obj['dataHead']:
        if e == '' or e[:2] == 'Nu' or e[:2] == 'Ti':
            continue
        obj['dataHeadGraf'].append(e)
    for e in obj['comboBox']['graf']:
        e.config(values=obj['dataHeadGraf'])

def funcInfo(obj, i):
    if i == 1 and obj['funcListCombs'][0]['var'].get() == 'Conv A->B(int)':
        graf = obj['funcListCombs'][1]['var'].get()
        n = graf.split('|')
        obj['textObj'].delete('1.0', END)
        obj['textObj'].insert('1.0', obj['grafInfo'][n[-1]][n[-3]+'|'+n[-2]])
    
def grafInfo(obj):
    graf = obj['io'].get()
    if graf == '':
        obj['dateGrafs']['text'] = '-'
        obj['textObj'].delete('1.0', END)
        return
    n = graf.split('|')
    if n[-1] != '0':
        obj['dateGrafs']['text'] = obj['grafInfo'][n[-1]]['date']
    obj['textObj'].delete('1.0', END)
    if graf[0] == 'F':
        obj['textObj'].insert('1.0', obj['newFunc'][n[0][1:]]['info'])
    else:
        obj['textObj'].insert('1.0', obj['grafInfo'][n[-1]][n[-3]+'|'+n[-2]])

def infoGet(obj):
    text = obj['textObj'].get('1.0', END)
    textList = text.split('\n')
    text = ''
    for t in textList:
        text += t + '¬'
    text = text[:len(text)-2]
    return(text)

def fillCels(obj, grafList):
    d = []
    t = []
    for graf in grafList[0]:
        if graf[0] == 'D':
            gr = graf.split('|')
            d.append(gr[1])
            ind = grafList[0].index(graf)
            recNumD = int(grafList[1][ind])
        elif graf[0] == 'C':
            gr = graf.split('|')
            t.append(gr[1])
            ind = grafList[0].index(graf)
            recNumT = int(grafList[1][ind])
    for i, var in enumerate(obj['celCombVar']):
        for n in range(5):
            obj['cellTextvar'][n][i].set('-')
        graf = var.get()
        if graf == '':
            continue
        if graf not in grafList[0]:
            if graf[:4] == 'NumD' or graf[:5] == 'TimeD':
                if len(d) == 0:
                    continue
                recNum = recNumD
            elif graf[:4] == 'NumT' or graf[:5] == 'TimeT':
                if len(t) == 0:
                    continue
                recNum = recNumT
            else:
                continue
        else:
            ind = grafList[0].index(graf)
            recNum = int(grafList[1][ind])
        num = -1
        for rec in range(int(recNum-2), int(recNum+3)):
            num += 1
            if rec < 0:
                continue
            if rec > len(obj['data'][graf])-1:
                return
            data = obj['data'][graf][rec]
            if graf[0] == 'T':
                nan = str(round((data % 1) * 1000))
                data = ti.strftime('%m%d'+'/'+'%H%M%S',ti.gmtime(data))+'.'+nan
            obj['cellTextvar'][num][i].set(data)

def crossLineValue(eventx, obj, can):
    c = obj['canvas'][can]['obj']
    c.delete('grafVal')
    grafList = [[],[]]
    if eventx == 'None':
        cL = c.find_withtag('crossline')
        if len(cL) == 0:
            return(grafList)
        cLC = c.coords(cL[0])
        eventx = cLC[0]
    h = int(c.cget('height'))
    cL = c.find_withtag('graf')
    if len(cL) > 0:
        box = c.bbox('graf')
        hb = box[3] - box[1]
        h = max(h, hb)
    selList = c.find_overlapping(eventx,-h,eventx, 0)
    if len(selList) == 0:
        return(grafList)
    lN = 0
    for e in selList:
        flag = False
        tc = False
        graf = ''
        temp = ''
        for n in c.gettags(e):
            if n == 'crossline' or n == 'headNums' or n == 'grafVal' or n == 'tempCVal':
                flag = True
                break
            if n[0] == '?':
                color = n[1:]
            if n in obj['dataHead']:
                graf = n
            if n[0] == '!':
                data = n[1:]
            if n[0] == '*':
                recNum = n[1:]
            if n == 'tempCor':
                tc = True
            if n[0] == '&':
                temp = n[1:]
        if flag:
            continue
        if tc:
            data = temp + ' - ' + data + ' * ' + recNum
        sr = obj['canvHead'].cget('scrollregion').split(' ')
        svx = obj['canvHead'].xview()
        h = int(c.cget('height'))
        x0 = svx[1] * int(sr[2])
        b = 'grafVal'
        c.create_text((x0-10,-h+lN*20+10), text=data, anchor='ne', fill=color, tags = (b))
        lN += 1
        if graf != '' and not tc:
            if graf not in grafList[0]:
                grafList[0].append(graf)
                grafList[1].append(recNum)
            else:
                i = grafList[0].index(graf)
                if int(grafList[1][i]) > int(recNum):
                    grafList[0][i] = graf
                    grafList[1][i] = recNum
    return(grafList)
 

 
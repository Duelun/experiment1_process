from os import getcwd
from tkinter import filedialog
from tkinter import *
import draw_functions2 as dr
import database2 as da
import functions2 as fu


def load(obj):
    fileName =  filedialog.askopenfilename(initialdir = getcwd() + '/adatok/',
                            title = "Select file",filetypes = (('raw','*.raw'),('funcktion','*.fun'),('converted','*.con')))
    if fileName == '':
        return
    ext = fileName[-3:]
    if ext == 'raw' or ext == 'fun' or ext == 'con':
        l = len(getcwd() + '/adatok/')
        obj['fileName'] = fileName[l:-4]
        loadData(fileName, obj)
def loadData(fileName, obj):
    f = open(fileName,'r')
    text = f.readlines()
    f.close()
    form = []
    for line in text:
        line = line.strip()
        w = line.split(';')
        w0 = int(w[0])
        w = w[1:]
        if w0 == 0:
            per = w[3] + '|' + w[4]
            date = w[0]
            infoList = w[5].split('¬')
            info = ''
            for t in infoList:
                info += t + '\n'
            info = info[:len(info)-2]
            chanels = w[1]+';'+w[2]
            w1 = w[1][3]
            w2 = w[2][3]
            group = checkGroup(obj, date, per, chanels, info)
        elif w0 == 1:
            dataHead = []
            for i, e in enumerate(w):
                e += '|' + per + '|' + group
                obj['data'][e] = []
                dataHead.append(e)
        elif w0 == 2:
            for e in w:
                form.append(e)
        elif w0 == 3:
            for i, e in enumerate(w):
                if i == 0:
                    num = e
                if form[i] == 'float':
                    e = float(e)
                elif form[i] == 'int':
                    e = int(e)
                obj['data'][dataHead[i]].append(e)
    for e in dataHead:
        #if w1 == '1' and e[:4] == 'C*A2':
            #continue
        #if w2 == '1' and e[:4] == 'C*B2':
            #continue
        obj['dataHead'].append(e)
    grafs = ['DataA'+'|'+per+'|'+group, 'DataB'+'|'+per+'|'+group]
    name = fu.funcAperB(obj, grafs, False)
    fu.dataNorm(obj, name, '3')
    da.combUpdate(obj)
    
def checkGroup(obj, date, per, chanels, info):
    group = '0'
    if len(obj['grafInfo']) == 0:
        group = '1'
        obj['grafInfo'][group] = {}
        obj['grafInfo'][group]['date'] = date
        obj['grafInfo'][group]['chanels'] = chanels
        obj['grafInfo'][group][per] = info
    else:
        g = []
        for e in obj['grafInfo']:
            g.append(int(e))
            if date == obj['grafInfo'][e]['date']:
                group = e
                obj['grafInfo'][e][per] = info
                return(e)
        gmax = max(g)
        group = str(gmax +1)
        obj['grafInfo'][group] = {}
        obj['grafInfo'][group]['date'] = date
        obj['grafInfo'][group]['chanels'] = chanels
    return(group)

def saveListTransf(obj, data, intOld, intNew, shift, group):
    date = obj['grafInfo'][group]['date']
    chanel = obj['grafInfo'][group]['chanels']
    text = da.infoGet(obj)
    info = 'Intval: ' + intOld + ' -> ' + intNew + '. Shift = ' + shift + '. #' + text
    data['sor0'] = '0;' + date +';'+ chanel +';'+ intNew +';'+ shift +';'+ info + ';'
    data['sor1'] = '1;'
    data['sor2'] = '2;'
    obj['dataD'] = {}
    obj['dataT'] = {}
    ll = []
    for graf in data['newGraf']:
        ll.append(len(obj['data'][graf]))
    l = min(ll)
    for graf in data['newGraf']:
        tip = graf[:1]
        if tip == 'D':
            form = 'int'
            db = obj['dataD']
        elif tip == 'C':
            tip = 'T'
            form = 'float'
            db = obj['dataT']
        else:
            continue
        if 'sor1' not in db:
            db['sor1'] = 'Num'+tip+';Time'+tip+';'
            db['sor2'] = 'int;float;'
        g = graf.split('|')
        db['sor1'] += g[0]+';'
        db['sor2'] += form+';'
        tNew = 'Time'+tip + '|'  + intNew + '|' + shift + '|' + group
        for i in range(l):
            ii = str(i)
            if ii not in db:
                db[ii] = ii + ';'+ str(obj['data'][tNew][i]) + ';'
            db[ii] += str(obj['data'][graf][i]) + ';'
    lL = [len(obj['dataD']), len(obj['dataT'])]
    l = max(lL)-2
    if l < 1:
        return
    for i in range(l):
        ii = str(i)
        data[ii] = '3;'
    del data['newGraf']
    for e in data:
        if e in obj['dataD']:
            data[e] += obj['dataD'][e]
        if e in obj['dataT']:
            data[e] += obj['dataT'][e]
        data[e] = data[e][:len(data[e])-1]
        data[e] += '\n'
    del obj['dataD']
    del obj['dataT']
    data['fileName'] = date + '#' + str(intNew) + '+' + shift + '.con'
    save(obj, data)
    
def save(obj, data):
    obj['fileName'] = getcwd() + '/adatok/' + data['fileName']
    f = open(obj['fileName'],'w')
    f.write(data['sor0'])
    f.write(data['sor1'])
    f.write(data['sor2'])
    del data['fileName']
    del data['sor0']
    del data['sor1']
    del data['sor2']
    for e in data:
        if e == 'sor0' or e == 'sor1' or e == 'sor2':
            continue
        f.write(data[e])
    f.close()
 
    
    
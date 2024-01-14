from tkinter import *
from tkinter import ttk
import file2 as fi
import draw_functions2 as dr
import database2 as da
    
def transform(obj, grafOrig, intNew, shift, f4, f5):
    if grafOrig not in obj['dataHead'] or not intNew.isdigit():
        return('graf/int error')
    if grafOrig[0] == 'F':
        return('function not transformable')
    data = {}
    data['newGraf'] = []
    if len(shift)==0 or (len(shift)==1 and not shift[0].isdigit()) or (len(shift)>1 and ((shift[0]!='-' and not shift[0].isdigit()) or not shift[1:].isdigit())):
        shift = '0'
    grO = grafOrig.split('|')
    sumDatNum = int(float(intNew) / float(grO[1]))
    intNew = sumDatNum * float(grO[1])
    intNew = f"{intNew:g}"
    if float(grO[1]) > float(intNew):
        return('interval error')
    info = da.infoGet(obj)
    obj['grafInfo'][grO[3]][intNew+'|'+shift] = {}
    obj['grafInfo'][grO[3]][intNew+'|'+shift] = info
    grafList = []
    for e in obj['dataHead']:
        tip = e[:2]
        if e == '' or tip == 'Nu' or tip == 'Ti':
            #
            #
            #
            continue
        gr = e.split('|')
        if gr[3] == grO[3] and gr[1] == grO[1]:
            grafList.append(e)
    for e in grafList:
        data = transData(obj, e, grO, intNew, shift, data, sumDatNum)
    

    grafs = ['DataA'+'|'+intNew+'|'+shift+'|'+grO[3], 'DataB'+'|'+intNew+'|'+shift+'|'+grO[3]]
    #funcAperB(obj, grafs)
    #funcAperB(obj, grafs, False)

    da.combUpdate(obj)
    fi.saveListTransf(obj, data, grO[1], intNew, shift, grO[3])
    return('Ok')
def transData(obj, grafOrig, grO, intNew, shift, data, sumDatNum):
    tip = grafOrig[:1]
    if tip == 'C':
        tip = 'T'
    else:
        tip = 'D'
    nL = grafOrig.split('|')
    newGraf = nL[0] + '|' + intNew + '|' + shift + '|' + nL[3]
    tOld = 'Time'+tip + '|'  + nL[1] + '|' + nL[2] + '|' + nL[3]
    tNew = 'Time'+tip + '|'  + intNew + '|' + shift + '|' + nL[3]
    numNew = 'Num'+tip + '|' + intNew + '|' + shift + '|' + nL[3]
    head = [numNew, tNew, newGraf]
    for e in head: 
        if e not in obj['data']:
            obj['data'][e] = []
        if e not in obj['dataHead']:
            obj['dataHead'].append(e)
    if tip == 'D':
        transIn(obj, grafOrig, newGraf, tOld, tNew, sumDatNum, numNew, shift)
    elif tip == 'T':
        transAv(obj, grafOrig, newGraf, tOld, tNew, sumDatNum, numNew, shift)
    data['newGraf'].append(newGraf)
    return(data)
def transAv(obj, grafOrig, newGraf, tOld, tNew, sumDatNum, numNew, shift):
    obj['data'][numNew] = [0]
    obj['data'][tNew] = [obj['data'][tOld][0]]
    obj['data'][newGraf] = [obj['data'][grafOrig][0]]
    i = 1
    for n in range(int(shift)+1, len(obj['data'][grafOrig])-1-sumDatNum, sumDatNum):
        temp = 0
        for m in range(sumDatNum):
            nm = n + m
            temp += obj['data'][grafOrig][nm]
        temp = temp / sumDatNum
        obj['data'][numNew].append(i)
        obj['data'][tNew].append(obj['data'][tOld][n])
        obj['data'][newGraf].append(round(temp, 3))
        i += 1
def transIn(obj, grafOrig, newGraf, tOld, tNew, sumDatNum, numNew, shift):
    i = 0
    for n in range(int(shift), len(obj['data'][grafOrig])-1, sumDatNum):
        obj['data'][numNew].append(i)
        obj['data'][tNew].append(obj['data'][tOld][n])
        obj['data'][newGraf].append(obj['data'][grafOrig][n])
        i += 1

def AperB(obj, gA, gB, ful, cor, f5):
    if gA not in obj['dataHead'] or gB not in obj['dataHead']:
        return('empty')
    if ful[0] == 'Y' or ful[0] == 'y':
        fulInt = True
    else:
        fulInt = False
    cL = cor.split(',')
    if len(cL) < 2:
        cL[0] = 1
        cL[0] = 9
    else:
        if not cL[0].isdigit():
            cL[0] = 1
        if not cL[1].isdigit():
            cL[1] = 9
        cor = [int(cL[0]), int(cL[1])]
    gAS = gA.split('|')
    gBS = gB.split('|')
    if gA[0] == 'F':
        del gAS[0]
    if gB[0] == 'F':
        del gBS[0]
    if gAS[1] != gBS[1] and gAS[1] != '0' and gBS[1] != '0':
        return('interval error')
    if gAS[2] != gBS[2] and gAS[2] != '0' and gBS[2] != '0':
        return('shift error')
    grafs = [gA, gB]
    info = funcAperB(obj, grafs, fulInt, cor)
    return(info)
def funcAperB(obj, grafs, fulInt=True, cor=[1,9]):
    if fulInt:
        func = 'A/Bf'
    else:
        func = 'A/B1'
    gA = grafs[0]
    gB = grafs[1]
    info = gA+' / '+gB+'\n'+'x-'+str(cor[0])+', x/10^'+str(cor[1])
    num = da.checkNewFunc(obj, func, info)
    gAS = gA.split('|')
    gBS = gB.split('|')
    if gA[0] == 'F':
        del gAS[0]
    if gB[0] == 'F':
        del gBS[0]
    origInt = '0'
    origShift = '0'
    if gAS[1] != 0:
        origInt = gAS[1]
    elif gBS[1] != '0':
        origInt = gBS[1]
    if gAS[2] != 0:
        origShift = gAS[2]
    elif gBS[2] != '0':
        origShift = gBS[2]
    name = 'F'+num+'|'+func+'|'+origInt+'|'+origShift+'|0'
    obj['data'][name] = []
    l = min(len(obj['data'][gA]), len(obj['data'][gB]))
    for n in range(1, l):
        if fulInt:
            dA = obj['data'][gA][n]
            dB = obj['data'][gB][n]
        else:
            dA = obj['data'][gA][n] - obj['data'][gA][n-1]
            dB = obj['data'][gB][n] - obj['data'][gB][n-1]
        if dB == 0:
            ab = 0
        else:
            ab = round(((dA / dB) - cor[0]) * 10**cor[1], 3)
        obj['data'][name].append(ab)
    obj['data'][name].insert(0, obj['data'][name][0])
    if name not in obj['dataHead']:
        obj['dataHead'].append(name)
        da.combUpdate(obj)
    return(name)

def dataNorm(obj, graf, cn):
    if graf == '':
        return('graf error')
    gr = graf.split('|')
    if gr[0][0] == 'F':
        del gr[1]
    if not cn.isdigit() or int(cn) < 1:
        cn = 3
    else:
        cn = int(cn)
    tic = (((8*10**7+1) / (8*10**7)) -1) *10**9
    dif = round(tic * cn, 3)
    func = 'N'
    info = graf
    num = da.checkNewFunc(obj, func, info)
    ngraf = 'F'+num+'|'+func+'|'+gr[1]+'|'+gr[2]+'|0'
    if ngraf not in obj['dataHead']:
        num = obj['dataHead'].index(graf) + 1
        obj['dataHead'].insert(num, ngraf)
    g = obj['data'][graf][:]
    for i in range(len(g)-4):
        if (g[i]+dif<g[i+1] and g[i+1]-dif>g[i+2] and g[i+2]<g[i]):
            d1 = g[i+1]-g[i]
            d2 = g[i]-g[i+2]
            dm = min(d1, d2)
            g[i+1] = g[i+1]-dm
            g[i+2] = g[i+2]+dm
        elif (g[i]-dif>g[i+1] and g[i+1]+dif<g[i+2] and g[i+2]>g[i]):
            d1 = g[i]-g[i+1]
            d2 = g[i+2]-g[i]
            dm = min(d1, d2)
            g[i+1] = g[i+1]+dm
            g[i+2] = g[i+2]-dm
    obj['data'][ngraf] = g
    da.combUpdate(obj)
    return('ok - ')
   
def tempRange(obj, dA, tB, dS, p, c, shift):
    if (dA[0] != 'F' and dA[0] != 'D') or dA not in obj['dataHead'] or tB[0] != 'C' or tB not in obj['dataHead']:
        return('graf error')
    if not dS.isdigit() or int(dS) < 1:
        dS = 100
    dS = int(dS)
    pp = p.split('.')
    if len(p)==0 or not pp[0].isdigit() or (len(pp)>1 and not pp[1].isdigit()) or len(pp)>2:
        p = 4
    p = float(p)
    if c.isdigit() == False or int(c) > int(obj['canvNum']['var'].get()):
        c = '1'
    can = obj['canvas'][c]['obj']
    can.delete('all')
    obj['canvas'][c]['ch']['var'].set(0)
    for nn in obj['canvas'][c]['comBox']:
        obj['canvas'][c]['comBox'][nn]['stringVar'].set('*Temp correction')
    if shift.isdigit():
        shift = int(shift)
    else:
        shift = 0
    n = min(len(obj['data'][tB]), len(obj['data'][dA]))
    obj['dataTemp'] = {}
    tl = []
    dl = []
    for e in range(n):
        tl.append(obj['data'][tB][e])
        dl.append(obj['data'][dA][e])
    tMin = min(tl)
    tMax = max(tl)
    dMin = min(dl)
    dMax = max(dl)
    
    tMin = round(tMin/0.125) *0.125
    tMax = round(tMax/0.125) *0.125
    for e in range(int(tMin*1000), int(tMax*1000)+125, 125):
        e = e / 1000
        obj['dataTemp'][e] = {}
    r = (dMax - dMin) / dS
    for e in range(n):
        t = round(obj['data'][tB][e]/0.125) *0.125
        d = round(dMin + round((obj['data'][dA][e] - dMin)/r) *r, 3)
        if d not in obj['dataTemp'][t]:
            obj['dataTemp'][t][d] = 1
        else:
            obj['dataTemp'][t][d] += 1
    obj['dataTempAv'] = []
    obj['dataTemp'] = dict(sorted(obj['dataTemp'].items()))
    for t in obj['dataTemp']:
        l = len(obj['dataTemp'][t])
        if l > 0:
            eS = 0
            eN = 0
            for e in obj['dataTemp'][t]:
                eS += e * obj['dataTemp'][t][e]
                eN += obj['dataTemp'][t][e]
            tS = round(eS / eN, 3)
            obj['dataTempAv'].append(tS)
            obj['dataTemp'][t] = dict(sorted(obj['dataTemp'][t].items()))
    #obj['dataTempAv'] = dict(sorted(obj['dataTempAv'].items()))
    func = 'TempAv'
    info = dA+' - '+tB
    checkinfo = True
    num = da.checkNewFunc(obj, func, info, checkinfo)
    dd = dA.split('|')
    name = 'F'+num+'|'+func+'|'+dd[-3]+'|'+'0'+'|0'
    if name not in obj['dataHead']:
        obj['dataHead'].append(name)
    obj['data'][name] = obj['dataTempAv'][:]
    func = 'TempAvT'
    name = 'F'+num+'|'+func+'|'+dd[-3]+'|'+'0'+'|0'
    if name not in obj['dataHead']:
        obj['dataHead'].append(name)
    obj['data'][name] = list(obj['dataTemp'].keys())
    da.combUpdate(obj)
    
    dr.drawDataTemp(obj, can, p, dMin, dMax, tMin, shift)
    return('ok')
 
def AminB(obj, gA, gB, f3, f4, f5):
    if gA not in obj['dataHead'] or gA == '' or gB not in obj['dataHead'] or gB == '':
        return('graf error')
    gAS = gA.split('|')
    gBS = gB.split('|')
    if gA[0] == 'F':
        del gAS[0]
    if gB[0] == 'F':
        del gBS[0]
    if gAS[1] != gBS[1] and gAS[1] != '0' and gBS[1] != '0':
        return('interval error')
    if gAS[2] != gBS[2] and gAS[2] != '0' and gBS[2] != '0':
        return('shift error')
    func = 'A-B'
    info = gA+' - '+gB
    num = da.checkNewFunc(obj, func, info)
    origInt = '0'
    origShift = '0'
    if gAS[1] != 0:
        origInt = gAS[1]
    elif gBS[1] != '0':
        origInt = gBS[1]
    if gAS[2] != 0:
        origShift = gAS[2]
    elif gBS[2] != '0':
        origShift = gBS[2]
    name = 'F'+num+'|'+func+'|'+origInt+'|'+origShift+'|0'
    if name not in obj['dataHead']:
        obj['dataHead'].append(name)
    obj['data'][name] = []
    
    l = min(len(obj['data'][gA]), len(obj['data'][gB])) -1
    for e in range(0, l):
        if e < 1:
            obj['data'][name].append(0)
            continue
        obj['data'][name].append(round(obj['data'][gA][e] - obj['data'][gB][e], 3))
    obj['data'][name][0] = obj['data'][name][1]
    da.combUpdate(obj)
    return('ok - A-B')

def Freki(obj, gA, gB, minData, maxData, f5):
    if gA not in obj['dataHead'] or gA == '' or gB not in obj['dataHead'] or gB == '':
        return('graf error')
    if not minData.isdigit():
        minData = '1'
    if not maxData.isdigit():
        maxData = '0'
    if minData == '0':
        minData = '1'
    minData = int(minData)
    maxData = int(maxData)
    if maxData == 0:
        l = len(obj['data'][gA])-1
    else:
        l = min(len(obj['data'][gA])-1, maxData)
    gr = gA.split('|')
    gT = 'TimeT' + '|'+gr[1]+'|'+gr[2]+'|'+gr[3]
    maxData = int(maxData)
    dA = int(obj['data'][gA][l]) - int(obj['data'][gA][minData])
    dB = int(obj['data'][gB][l]) - int(obj['data'][gB][minData])
    t = float(obj['data'][gT][l]) - float(obj['data'][gT][minData])
    fr1 = str(round(dA / t, 3))
    fr2 = str(round(dB / t, 3))
    info = fr1 +'\n'+ fr2
    obj['textObj'].delete('1.0', END)
    obj['textObj'].insert('1.0', info)
    return('nodelete')
    
def FuOscTemp(obj, origo, sav, A1='1', A2='1', tS='1', c='1'):
    if ',' not in origo or ',' not in sav:
        return('error')
    oo = origo.split(',')
    oX = int(oo[0])
    oY = int(oo[1])
    ss = sav.split(',')
    x0 = int(ss[0])
    x1 = int(ss[1])
    A1 = float(A1)
    A2 = float(A2)
    color = obj['colors'][1]
    if not c.isdigit() or int(c) > int(obj['canvNum']['var'].get()):
        c = '1'
    graf = 'F|'+'FuOscTemp'+'|'+tS+'|0|'+c
    if graf not in obj['dataHead']:
        obj['dataHead'].append(graf)
    da.combUpdate(obj)
    if graf in obj['minMax']:
        del obj['minMax'][graf]
    obj['data'][graf] = []
    for n in range(0, x1):
        if n < x0:
            y = None
        else:
            dT = (n - oX) * 0.125
            y = A1*(dT)**3 + A2*(dT)
        obj['data'][graf].append(y)
    flag = 0
    for g in obj['canvas'][c]['comBox']:
        if obj['canvas'][c]['comBox'][g]['stringVar'].get() == graf:
            flag = 1
    if flag == 0:
        obj['canvas'][c]['comBox']['0']['stringVar'].set(graf)
    obj['canvas'][c]['obj'].delete(graf)
    dr.drawGrafs(obj, c)
    return('A1*(T-T0)**3 + A2*(T-T0) + A3')

def tempCorr(obj, dA, tB, c):
    if (dA[0] != 'F' and dA[0] != 'D') or dA not in obj['dataHead'] or tB not in obj['dataHead']:
        return('graf error')
    if not c.isdigit() or int(c) > int(obj['canvNum']['var'].get()):
        c = '1'
    dAS = dA.split('|')
    if dA[0] == 'F':
        del dAS[0]
    tBS = tB.split('|')
    if tB[0] == 'F':
        del tBS[0]
    func = 'tempcor'
    info = dA+' - '+tB
    num = da.checkNewFunc(obj, func, info, True)
    origInt = '0'
    origShift = '0'
    if dAS[1] != 0:
        origInt = dAS[1]
    elif tBS[1] != '0':
        origInt = tBS[1]
    if dAS[2] != 0:
        origShift = dAS[2]
    elif tBS[2] != '0':
        origShift = tBS[2]
    graf = 'F'+num+'|'+func+'|'+origInt+'|'+origShift+'|0'
    if graf not in obj['dataHead']:
        obj['dataHead'].append(graf)
    da.combUpdate(obj)
    obj['data'][graf] = []
    t0 = 42.125
    fu0 = 637
    A1 = 1.6
    A2 = 750
    r = 17.42
    for i, d in enumerate(obj['data'][dA]):
        dt = obj['data'][tB][i] - t0
        e = A1 * dt**3 + A2 * dt
        er = d - (e / r)
        obj['data'][graf].append(er)
    if graf in obj['minMax']:
        del obj['minMax'][graf]
    flag = 0
    for g in obj['canvas'][c]['comBox']:
        if obj['canvas'][c]['comBox'][g]['stringVar'].get() == graf:
            flag = 1
    if flag == 0:
        obj['canvas'][c]['comBox']['0']['stringVar'].set(graf)
    obj['canvas'][c]['obj'].delete(graf)
    dr.drawGrafs(obj, c)
    
    return('ok')
    
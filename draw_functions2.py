from tkinter import *
from tkinter import ttk
import functions2 as fu
import database2 as da
import vezerles2 as ve

def shift(obj, v):
    flag = 0
    for can in obj['canvas']:
        newList = []
        if obj['canvas'][can]['ch']['var'].get() == 0:
            continue
        for ii in obj['canvas'][can]['comBox']:
            if obj['canvas'][can]['comBox'][ii]['activeCh']['var'].get() == 0:
                continue
            graf = obj['canvas'][can]['comBox'][ii]['stringVar'].get()
            if graf == '':
                continue
            obj['canvas'][can]['obj'].delete(graf)
            obj['canvas'][can]['comBox'][ii]['shift'] = v
            shV = obj['canvas'][can]['comBox'][ii]['shiftLab'].cget('text').split('/')
            obj['canvas'][can]['comBox'][ii]['shiftLab']['text'] = shV[0]+'/'+shV[1]+'/'+str(v)#f"{v:g}"
            newList.append(ii)
        if len(newList) == 0:
            continue
        drawGrafs(obj, can, newList)
  
def zoom(obj, v, can, ch=True):
    newList = []
    for ii in obj['canvas'][can]['comBox']:
        if obj['canvas'][can]['comBox'][ii]['activeCh']['var'].get() == 0 and ch:
            continue
        graf = obj['canvas'][can]['comBox'][ii]['stringVar'].get()
        if graf == '':
            continue
        mi = obj['canvas'][can]['comBox'][ii]['min']
        ma = obj['canvas'][can]['comBox'][ii]['max']
        if mi == ma:
            continue
        if obj['canvas'][can]['comBox'][ii]['zoom'] == 0:
            continue
        obj['canvas'][can]['obj'].delete(graf)
        if v == 0:
            v = 1 / obj['canvas'][can]['comBox'][ii]['zoom']
        r = obj['canvas'][can]['obj'].cget('scrollregion')
        sc = r.split(' ')
        t = (int(sc[1]) - int(sc[3])) / -2
        maT = (ma - t) * v
        miT = (mi - t) * v
        obj['canvas'][can]['comBox'][ii]['min'] = t + miT
        obj['canvas'][can]['comBox'][ii]['max'] = t + maT
        obj['canvas'][can]['comBox'][ii]['yPix'] = obj['canvas'][can]['comBox'][ii]['yPix'] * v
        obj['canvas'][can]['comBox'][ii]['zoom'] = obj['canvas'][can]['comBox'][ii]['zoom'] * v
        z = obj['canvas'][can]['comBox'][ii]['zoom'] 
        zF = f'{float(f"{z:.2f}"):g}'
        shV = obj['canvas'][can]['comBox'][ii]['shiftLab']['text'].split('/')
        obj['canvas'][can]['comBox'][ii]['shiftLab']['text'] = shV[0]+'/'+zF+'/'+shV[2]
        newList.append(ii)
    if len(newList) == 0:
        return
    drawGrafs(obj, can, newList)

def lift(obj, v, can, ch=True):
    newList = []
    for ii in obj['canvas'][can]['comBox']:
        if ch and obj['canvas'][can]['comBox'][ii]['activeCh']['var'].get() == 0:
            continue
        graf = obj['canvas'][can]['comBox'][ii]['stringVar'].get()
        if graf == '':
            continue
        obj['canvas'][can]['obj'].delete(graf)
        obj['canvas'][can]['comBox'][ii]['lift'] = v
        mi = obj['canvas'][can]['comBox'][ii]['min']
        obj['canvas'][can]['comBox'][ii]['min'] = mi + v
        ma = obj['canvas'][can]['comBox'][ii]['max']
        obj['canvas'][can]['comBox'][ii]['max'] = ma + v
        shV = obj['canvas'][can]['comBox'][ii]['shiftLab']['text'].split('/')
        v = int(v)
        obj['canvas'][can]['comBox'][ii]['shiftLab']['text'] = str(int(shV[0])+v)+'/'+shV[1]+'/'+shV[2]
        newList.append(ii)
    if len(newList) == 0:
        return
    drawGrafs(obj, can, newList)

def checkOld(obj, can):
    gOld = []
    gNew = []
    gDelete = []
    obj['canvas'][can]['obj'].addtag_withtag('delete', 'graf')
    vList = obj['canvas'][can]['obj'].find_withtag('graf')
    for ii in obj['canvas'][can]['comBox']:
        graf = obj['canvas'][can]['comBox'][ii]['stringVar'].get()
        if graf == '' or graf[0] == '*':
            obj['canvas'][can]['comBox'][ii]['stringVar'].set('')
            obj['canvas'][can]['comBox'][ii]['lift'] = 0
            obj['canvas'][can]['comBox'][ii]['zoom'] = 1
            obj['canvas'][can]['comBox'][ii]['shift'] = 0
            obj['canvas'][can]['comBox'][ii]['shiftLab']['text'] = '0/0/0'
            continue
        flag = 0
        for e in vList:
            vTags = obj['canvas'][can]['obj'].gettags(e)
            if (graf not in vTags) or (obj['colors'][int(ii)] not in vTags):
                continue
            obj['canvas'][can]['obj'].dtag(e, 'delete')
            flag = 1
        if flag == 0:
            gNew.append(ii)
            obj['canvas'][can]['comBox'][ii]['lift'] = 0
            obj['canvas'][can]['comBox'][ii]['zoom'] = 1
            obj['canvas'][can]['comBox'][ii]['shift'] = 0
            obj['canvas'][can]['comBox'][ii]['shiftLab']['text'] = '0/0/0'
        else:
            gOld.append(ii)
    obj['canvas'][can]['obj'].dtag('crossline', 'delete')
    obj['canvas'][can]['obj'].delete('delete')
    for ii in gNew:
        if obj['canvas'][can]['comBox'][ii]['sinc']['var'].get() == 1:
            for i in gOld:
                if obj['canvas'][can]['comBox'][i]['sinc']['var'].get() == 1:
                    gDelete.append(i)
            break
    if len(gDelete) > 0:
        for ii in gDelete:
            graf = obj['canvas'][can]['comBox'][ii]['stringVar'].get()
            obj['canvas'][can]['obj'].delete(graf)
            gNew.append(ii)
    return(gNew)

def minMax(obj, can, newList):
    for ii in newList:
        graf = obj['canvas'][can]['comBox'][ii]['stringVar'].get()
        if graf not in obj['minMax']:
            grafList = obj['data'][graf][:]
            if None in grafList:
                flag = True
                while flag:
                    grafList.remove(None)
                    if None not in grafList:
                        flag = False
            obj['minMax'][graf] = {}
            obj['minMax'][graf]['max'] = max(grafList)
            obj['minMax'][graf]['min'] = min(grafList)
        obj['canvas'][can]['comBox'][ii]['min'] = obj['minMax'][graf]['min']
        obj['canvas'][can]['comBox'][ii]['max'] = obj['minMax'][graf]['max']

def sincGrafs(obj, can, newList):
    yMin = []
    yMax = []
    gList = []
    aH = int(obj['canvas'][can]['obj'].cget('height'))
    rH = aH - 2 * obj['yMargo']
    for ii in newList:
        graf = obj['canvas'][can]['comBox'][ii]['stringVar'].get()
        if obj['canvas'][can]['comBox'][ii]['sinc']['var'].get() == 1:
            gList.append(ii)
            yMin.append(obj['minMax'][graf]['min'])
            yMax.append(obj['minMax'][graf]['max'])
        else:
            gH = obj['minMax'][graf]['max'] - obj['minMax'][graf]['min']
            if gH == 0:
                gH = 1
            obj['canvas'][can]['comBox'][ii]['yPix'] = rH / gH
            obj['canvas'][can]['comBox'][ii]['min'] = obj['yMargo']
            obj['canvas'][can]['comBox'][ii]['max'] = (aH - obj['yMargo'])
    if len(gList) == 0:
        return
    yMin = min(yMin)
    yMax = max(yMax)
    gH = yMax - yMin
    if gH == 0:
        gH = 1
    yPix = rH / gH
    for ii in newList:
        graf = obj['canvas'][can]['comBox'][ii]['stringVar'].get()
        if ii not in gList:
            continue
        obj['canvas'][can]['comBox'][ii]['yPix'] = yPix
        obj['canvas'][can]['comBox'][ii]['min'] = (obj['minMax'][graf]['min'] - yMin) * yPix + obj['yMargo']
        obj['canvas'][can]['comBox'][ii]['max'] = (obj['minMax'][graf]['max'] - yMin) * yPix + obj['yMargo']
 
def drawGrafs(obj, can, newList=[], force=False):
    if obj['canvas'][can]['ch']['var'].get() == 0 and not force:
        return
    xPix = int(obj['xPix']['act']['text'])
    baseSec = float(obj['baseSec']['act']['text'])
    if len(newList) == 0:
        newList = checkOld(obj, can)
        if len(newList) == 0:
            return
        minMax(obj, can, newList)
        sincGrafs(obj, can, newList)
        
    for n in newList:
        graf = obj['canvas'][can]['comBox'][n]['stringVar'].get()
        iV = graf.split('|')
        if graf[0] == 'F':
            del iV[0]
        step = float(iV[1]) / baseSec
        color = obj['colors'][int(n)]
        yPix = obj['canvas'][can]['comBox'][n]['yPix']
        yNull = obj['minMax'][graf]['min']
        shift = int(obj['canvas'][can]['comBox'][n]['shift'] + int(iV[2]))
        xOld = 0
        pontDist = xPix * step
        if pontDist < 1:
            pontDist = 1
        pontNum = int(obj['ablakSzel'] / pontDist) + 1
        fr = int(obj['cX']/step) -shift
        maxPoint = min(pontNum + fr + 1, len(obj['data'][graf]))
        k = 0
        for i in range(fr, maxPoint):
            if i < 1:
                k += 1
                continue
            if obj['data'][graf][i] == None or obj['data'][graf][i-1] == None:
                k += 1
                continue
            yNew = (round((obj['data'][graf][i] - yNull) * yPix) + round(obj['canvas'][can]['comBox'][n]['min'])) * -1
            yOld = (round((obj['data'][graf][i-1] - yNull) * yPix) + round(obj['canvas'][can]['comBox'][n]['min'])) * -1
            xNew = round(k * pontDist)
            xOld = round((k-1) * pontDist)
            b = [graf,
                 '?'+color,
                 'graf',
                 '%'+iV[1],							#interval %
                 '!'+str(obj['data'][graf][i]),			#adat
                 '*'+str(fr+k)]						#adat sorszam
            lineId = obj['canvas'][can]['obj'].create_line(xOld,yOld,xNew,yNew,width=1,activewidth=3,fill=color,tags = (b))
            #obj['canvas'][can]['obj'].tag_bind(lineId, sequence=None, function=None, add=None)
    #crossLineDraw('None', obj, obj['canvas'][can]['obj'])
            k += 1
    obj['cXM'] = max(obj['cXM'], int(len(obj['data'][graf])*step) - 1)
    ve.crossLineEvent('None', obj, True)
    
def crossLineDraw(eventx, obj, c, new=True):
    c.delete('crossline')
    c.delete('grafVal')
    if new == False:
        return
    if eventx == 'None':
        cL = obj['canvHead'].find_withtag('crossline')
        if len(cL) == 0:
            return
        co = obj['canvHead'].coords(cL[0])
        eventx = co[0]
    h = int(c.cget('height'))
    c.create_line(eventx,-h,eventx,0,width=1,fill=obj['colors'][3],tags = ('crossline'))

def drawValue(obj, can, it):
    tags = obj['canvas'][can]['obj'].gettags(it)
    for n in tags:
        if n[0] == '?':
            color = n[1:]
        if n[0] == '!':
            data = n[1:]
    color = 'grey1'
    cor = obj['canvas'][can]['obj'].coords(it)
    ir = 10
    if cor[1] < cor[3]:
        ir = -10
    l = int(obj['xPix']['act']['text']) * 1
    b = ['graf', 'grafValOne']
    obj['canvas'][can]['obj'].create_line(cor[2],cor[3],cor[2]+l,cor[3],width=2,fill=color,tags = (b))
    b = ['graf', 'grafValOne']
    obj['canvas'][can]['obj'].create_text((cor[2],cor[3]-ir), text=data, anchor='w', fill=color, tags = (b))
    
def drawDataTemp(obj, c, barx, dMin, dMax, tMin, shift):
    hO = int(c.cget('height'))
    h = hO - 2 * 10
    xPix = float(obj['xPix']['var'].get()) * barx
    bar = xPix * 0.9
    yPix = h / (dMax - dMin)
    color1 = obj['colors'][0]
    color2 = obj['colors'][1]
    color3 = obj['colors'][2]
    l = (tMin - int(tMin)) / 0.125
    k = 0
    avOldX = 0
    avOldY = 0
    lastPos = 0
    for i, ii in enumerate(obj['dataTemp']):
        if len(obj['dataTemp'][ii].keys()) == 0:
            continue
        if i < shift:
            continue
        bMax = max(obj['dataTemp'][ii].values())
        bPix = bar / bMax
        xPos = k * xPix
        labPos = xPos + 2
        b = ['tempCVal', 'graf']
        if l == 0 or l == 4:
            if (labPos - lastPos) * xPix > 20:
                lastPos = labPos
                c.create_text((labPos,0), text=ii, anchor='sw', fill=color1, tags = (b))
        l += 1
        if l > 7:
            l = 0
        for nn in obj['dataTemp'][ii]:
            lBar = obj['dataTemp'][ii][nn] * bPix
            yPos = -((float(nn) - dMin) * yPix + 10)
            b = ['?'+color1,
                 'tempCor',
                 'graf',
                 '&'+str(ii),
                 '!'+str(nn),			#graf sav
                 '*'+str(obj['dataTemp'][ii][nn])]						#darabszam
            c.create_line(xPos,yPos,xPos+lBar,yPos,width=2,activewidth=3,fill=color2,tags = (b))
        avY = -((float(obj['dataTempAv'][i]) - dMin) * yPix + 10)
        if avOldY == 0:
            avOldY = avY
        b = ['?'+color3,
             'tempCorAv',
             'graf',
             '!'+str(obj['dataTempAv'][i])]
        c.create_line(avOldX,avOldY,xPos+bar,avY,width=2,activewidth=3,fill=color3,tags = (b))
        avOldY = avY
        avOldX = xPos+bar
        k += 1
    crossLineDraw('None', obj, c)
    
    
    
    
    
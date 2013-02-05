'''
Created on Aug 14, 2012

@author: jzplusplus
'''

import time
#from random import choice
import urllib2, base64
import jsonrpclib, json

import Tkinter as tk

#quotes = ['SMDG2K!', 'Go Outside!', 'Imhotep is invisible', ') )', '/)(^3^)(\\']
#currentquote = ''

root = tk.Tk()

# make it cover the entire screen
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.configure(background='black')

frame = tk.Frame(root, width=w, height=h)
frame.pack()

frame.focus_set() # <-- move focus to this widget
frame.bind("<Escape>", lambda e: e.widget.quit())
frame.configure(background='black')

text = tk.Label(frame, text="Testing...", font=("Helvetica", 65), fg='white', bg='black', wraplength=w-50)
text.pack()

timeText = tk.Label(frame, text="Testing...", font=("Helvetica", 55), fg='white', bg='black', wraplength=w-50)
timeText.pack()

import sys
if sys.platform.startswith('linux'):
    root.configure(cursor='@1x1.xbm white')

def XBMCfunction(func, params=[]):
    jsondata = jsonrpclib.dumps(params, func)
    #print jsondata

    base64string = base64.encodestring('%s:%s' % ('xbmc', 'xbmc'))[:-1]
    authheader =  "Basic %s" % base64string
    
    req = urllib2.Request("http://192.168.0.10:8080/jsonrpc", jsondata)
    req.add_header("Authorization", authheader)
    req.add_header('Content-Type', 'application/json')
    handle = urllib2.urlopen(req, timeout=1)
    html = handle.read()
    #print html
    result = json.loads(html)
    return result['result']

linecount = 0
fontsize = 65

def getdata():
    try:
        players = XBMCfunction('Player.GetActivePlayers')
        
        output = '' 
        
        if len(players) > 0:
            linecount = 0
            
            playerid = players[0]['playerid']
            currentJSON = XBMCfunction('Player.GetItem', {'playerid':playerid, 'properties':['file','showtitle', 'title', 'season', 'episode']})
            timeJSON = XBMCfunction('Player.GetProperties', {'playerid': playerid, 'properties':['time','totaltime']})
            
            vidtype = currentJSON['item']['type']
            
            if vidtype == 'movie':
                title = currentJSON['item']['title']
                line1 = ''
                line2 = title
                
            elif vidtype == 'episode':
                title = currentJSON['item']['title']
                showtitle = currentJSON['item']['showtitle']
                season = currentJSON['item']['season']
                episode = currentJSON['item']['episode']
                line1 = showtitle
                line2 = 'S' + str(season) + ' E' + str(episode) + ': ' + title
                
            elif vidtype == 'unknown':
                label = currentJSON['item']['label']
                try:
                    currentJSON['item']['file'].index('youtube.com')
                    line1 = 'YouTube'
                except ValueError: line1 = ''
                line2 = label
                
            output = line1 + '\n' + line2
            linecount = (len(line1)/26 + 1) + (len(line2)/26 + 1)
            if linecount > 4: fontsize = 50
            else: fontsize = 65
            
            seekTime = ''
            totTime = ''
            
            if timeJSON['totaltime']['hours'] > 0:
                totTime += str(timeJSON['totaltime']['hours']) + ':'
                if timeJSON['totaltime']['hours'] < 10:
                    seekTime += str(timeJSON['time']['hours']) + ':'
                else:
                    seekTime += str(timeJSON['time']['hours']).zfill(2) + ':'
                    
                seekTime += str(timeJSON['time']['minutes']).zfill(2) + ':' + str(timeJSON['time']['seconds']).zfill(2)
                totTime += str(timeJSON['totaltime']['minutes']).zfill(2) + ':' + str(timeJSON['totaltime']['seconds']).zfill(2)
                
            else:
                totTime += str(timeJSON['totaltime']['minutes']) + ':'
                if timeJSON['totaltime']['minutes'] < 10:
                    seekTime += str(timeJSON['time']['minutes']) + ':'
                else:
                    seekTime += str(timeJSON['time']['minutes']).zfill(2) + ':'
                    
                seekTime += str(timeJSON['time']['seconds']).zfill(2)
                totTime += str(timeJSON['totaltime']['seconds']).zfill(2)
        
            timeOutput = seekTime +' / '+ totTime
            
            ts = time.strftime('%I:%M %p')
            if ts[0] == '0': ts = ts[1:]
            timeOutput += '\n' + ts
        
        else:
            fontsize = 70
            ts = time.strftime('%I:%M %p\n\n%b %d, %Y')
            if ts[0] == '0': ts = ts[1:]
            output = '\n'+ ts
            timeOutput = ''
        
        text.config(text=output)
        timeText.config(text=timeOutput)
        
        text.config(font=("Helvetica", fontsize))
        text.pack(side=tk.TOP, ipady=50)
        timeText.pack(side=tk.BOTTOM, ipady=30)
        
    except:
        #print 'ERROR: XBMC not available'
        output = 'ERROR: XBMC not available\n\n'
        toutput = time.strftime('%I:%M %p\n\n%b %d, %Y')
        text.config(text=output)
        text.config(font=("Helvetica", 30))
        text.pack(side=tk.TOP, ipady=50)
        
        timeText.config(text=toutput)
        timeText.config(font=("Helvetica", 70))
        timeText.pack(side=tk.TOP, ipady=50)
        return

#def newQuote():
#    global currentquote
#    currentquote = choice(quotes)
#    root.after(3600000, newQuote)

def loop():
    getdata()
    frame.pack()
    root.after(500,loop)
    
root.after(500,loop)
#root.after(500,newQuote)
root.mainloop()

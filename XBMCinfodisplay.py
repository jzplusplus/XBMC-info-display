'''
Created on Aug 14, 2012

@author: jzplusplus
'''

import time
from random import choice
import urllib2, base64
import jsonrpclib, json

import Tkinter as tk

quotes = ['SMDG2K!', 'Go Outside!', 'Imhotep is invisible', ') )', '/)(^3^)(\\']
currentquote = ''

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

#root.configure(cursor='@1x1.xbm white')

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
    result = json.loads(html)
    return result['result']

noupdates = 0
linecount = 0
fontsize = 65

def getdata():
    global noupdates, text, timeText, linecount, fontsize
    try:
        players = XBMCfunction('Player.GetActivePlayers')
        
        output = '' 
        
        if len(players) == 0:
            output += '\n' + currentquote
            timeOutput = ''
            if noupdates < 600: noupdates+=1
            fontsize = 70
            timeText.config(font=("Helvetica", 70))
        
        else:
            linecount = 0
            noupdates=0
            
            playerid = players[0]['playerid']
            currentJSON = XBMCfunction('Player.GetItem', {'playerid':playerid, 'properties':['showtitle', 'file']})
            timeJSON = XBMCfunction('Player.GetProperties', {'playerid': playerid, 'properties':['time','totaltime']})
            
            showtitle = currentJSON['item']['showtitle']
            label = currentJSON['item']['label']
            
            isYoutube = True
            try: currentJSON['item']['file'].index('youtube.com')
            except ValueError: isYoutube = False
            
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
            
            if(isYoutube):
                #Youtube
                output += 'YouTube: '
                linecount += len('YouTube: ')/26 + 1
            
            elif len(showtitle) > 0:
                #TV show
                output += showtitle + '\n'
                linecount += len(showtitle)/26 + 1
                
            output += label
            linecount += len(label)/26 + 1
        
            timeOutput = seekTime +' / '+ totTime
        
        ts = time.strftime('%I:%M %p')
        if ts[0] == '0': ts = ts[1:]
        
        timeOutput += '\n' + ts
        if noupdates >= 600:
            ts = time.strftime('%I:%M %p\n\n%b %d, %Y')
            if ts[0] == '0': ts = ts[1:]
            output = '\n'+ ts
            timeOutput = ''
        
        #output = 'blah\nblah\nblah\nblahhhalhfljdlkfadfaldksflasdhflhasdlf'
        text.config(text=output)
        timeText.config(text=timeOutput)
    
        if linecount > 4: fontsize = 50
        else: fontsize = 65
        text.config(font=("Helvetica", fontsize))
        text.pack(side=tk.TOP, ipady=50)
        
        #dictionary['Changed'] = '1'
        #if 'Changed' in dictionary and dictionary['Changed'] == '1':
        #    fontsize = 70
        #    while text.winfo_height() > 200:
        #        print text.winfo_height(), fontsize
        #        fontsize -= 1
        #        text.config(font=("Helvetica", fontsize))
        #        text.pack(side=tk.TOP, ipady=50)
        
        timeText.pack(side=tk.BOTTOM, ipady=30)
        
    except:
        print 'ERROR: XBMC not available'
        output = 'ERROR: XBMC not available\n\n'
        toutput = time.strftime('%I:%M %p\n\n%b %d, %Y')
        text.config(text=output)
        text.config(font=("Helvetica", 30))
        text.pack(side=tk.TOP, ipady=50)
        
        timeText.config(text=toutput)
        timeText.config(font=("Helvetica", 70))
        timeText.pack(side=tk.TOP, ipady=50)
       
        if noupdates < 600: noupdates+=1
        return

def newQuote():
    global currentquote
    currentquote = choice(quotes)
    root.after(3600000, newQuote)

def loop():
    getdata()
    frame.pack()
    root.after(500,loop)
    
root.after(500,loop)
root.after(500,newQuote)
root.mainloop()

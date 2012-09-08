'''
Created on Aug 14, 2012

@author: jzplusplus
'''

import time
import urllib2, base64

import Tkinter as tk

root = tk.Tk()

# make it cover the entire screen
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))

root.focus_set() # <-- move focus to this widget
root.bind("<Escape>", lambda e: e.widget.quit())
root.configure(background='black')

text = tk.Label(root, text="Testing...", font=("Helvetica", 65), fg='white', bg='black', wraplength=w-50)
text.pack()

timeText = tk.Label(root, text="Testing...", font=("Helvetica", 55), fg='white', bg='black', wraplength=w-50)
timeText.pack()

root.configure(cursor='@1x1.xbm white')
root.update()

base64string = base64.encodestring(
        '%s:%s' % ('xbmc', 'xbmc'))[:-1]
authheader =  "Basic %s" % base64string
req = urllib2.Request("http://192.168.0.10:8080/xbmcCmds/xbmcHttp?command=GetCurrentlyPlaying()")
req.add_header("Authorization", authheader)

noupdates = 0
linecount = 0
fontsize = 65

while True:
    if True:
        try:
            handle = urllib2.urlopen(req)
            
            html = handle.read()
        except:
            print 'ERROR: XBMC not available'
            text.config(text='ERROR: XBMC not available')
            text.config(font=("Helvetica", fontsize))
            text.pack(side=tk.TOP, ipady=50)
            root.update()
            
            if noupdates < 600: noupdates+=1
            time.sleep(1)
            continue
        
        html = html.replace('<html>','')
        html = html.replace('</html>','')

        items = html.split('<li>')
        #print items
        dictionary = {}
        for item in items:
            item = item.replace('\n','')
            
            index = item.find(':')
            if index == -1: 
                if noupdates < 600: noupdates+=1
                continue
            
            label = item[:index]
            data = item[index+1:]
            
            dictionary[label] = data
           
        output = '' 
        if not 'Filename' in dictionary:
            output += "\nERROR: badly formatted response. Missing 'Filename' field."
        
        elif dictionary['Filename'] == '[Nothing Playing]':
            output += '\nGO OUTSIDE!'
            if noupdates < 600: noupdates+=1
            fontsize = 70
            timeText.config(font=("Helvetica", 70))
        else:
            timeText.config(font=("Helvetica", 55))
            linecount = 0
            noupdates=0
            if not 'Title' in dictionary:
                dictionary['Title'] = dictionary['Filename'].split('/')[-1]
            
            if 'Show Title' in dictionary:
                #TV show
                output += dictionary['Show Title'] + '\n'
                linecount += len(dictionary['Show Title'])/26 + 1
                try:
                    output += 'S' + dictionary['Season'] + ' E' + dictionary['Episode']
                except KeyError:
                    output += 'Ep'
                
                output += ': ' + dictionary['Title']
                linecount += (len(dictionary['Title'])+6)/26 + 1
                
            elif 'Artist' in dictionary:
                #Music
                output += 'Artist: '+ dictionary['Artist'] + '\nSong: '+ dictionary['Title'] + '\n'
            
            elif dictionary['Filename'].find('youtube.com') >= 0:
                #YouTube
                output += 'YouTube: '+ dictionary['Title']
                linecount += len(dictionary['Title'])/26 + 1
            else:
                #Movie
                output += dictionary['Title']
                linecount += len(dictionary['Title'])/26 + 1
        #print dictionary
        
        try:
            timeOutput = dictionary['Time'] +' / '+ dictionary['Duration']
        except KeyError:
            timeOutput = ''
            pass
        timeOutput += '\n' + time.strftime('%I:%M %p') 
        if noupdates >= 600:
            output = '\n'+ time.strftime('%I:%M %p\n\n%b %d, %Y')
            timeOutput = ''
        
        #output = 'blah\nblah\nblah\nblahhhalhfljdlkfadfaldksflasdhflhasdlf'
        text.config(text=output)
        timeText.config(text=timeOutput)
 
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
        #        root.update()
       
        timeText.pack(side=tk.BOTTOM, ipady=30)
        root.update()

    time.sleep(0.5)

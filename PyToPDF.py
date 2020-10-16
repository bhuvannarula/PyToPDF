from fpdf import FPDF
from re import search as sch, fullmatch as fch
import types
import builtins
from os import path
from tkinter import Tk, filedialog

'''
Run this program to convert python code to pdf with line numbers and standard python IDLE formatting

asks for .py file, and creates .pdf file in same directory as the .py file
if *-doc.py is present in same directory as *.py, doc is added to .pdf file
'''

mainwin = Tk()
mainwin.withdraw()
builtin_function_names = dir(builtins)

main = FPDF('P',format='A3')

def linesplitter(line,*arg):
    if not arg:
        arg = [' ','\n','\r\n','(',')','#','"',"'",':']
    i = 0
    for item in range(len(line)):
        if line[item] in arg:
            yield line[i:item]
            yield line[item]
            i = item+1

#filenameIn = input('Enter Filename: ')
# use above if you don't want to use tkinter filedialog
filenameIn = filedialog.askopenfilename(multiple = False, title='toPDF', filetypes=[('Python Code','*.py')])
filenameMain = filenameIn.split('.')[0]
if not filenameMain:
    raise UserWarning('No file selected!')

height = 5.5
fileIn = open(filenameIn,'r').readlines()

main.add_page()
main.add_font('Monaco','',r'fonts/Monaco-01.ttf',True)
main.add_font('Caviar-Bold','',r'fonts/Caviar_Dreams_Bold.ttf',True)
main.add_font('Caviar','',r'fonts/CaviarDreams.ttf',True)
main.set_auto_page_break(True,margin=18)
main.set_font('Monaco','',11)

docfilename = filenameMain+'-doc.txt'
docfileIn = ''
if path.isfile(docfilename):
    docfileIn = open(docfilename,'r').readlines()

ii = 0
while ii < len(docfileIn):
    if '#' in docfileIn[ii]:
        ii+=1
    elif '<h>' in docfileIn[ii]:
        main.set_font('Caviar-Bold','',28)
        main.write(height*2.5,docfileIn[ii+1]) #15
        ii+=3
    elif '<br>' in docfileIn[ii]:
        main.write(height,'\n')
        ii+=1
    elif '<p>' in docfileIn[ii]:
        ii+=1
        main.set_font('Caviar','',15)
        main.set_text_color(110,110,113)
        while True:
            if '</p>' not in docfileIn[ii]:
                main.write(height*1.5,docfileIn[ii]) #8
                ii+=1
            else:
                ii+=1
                break
    else:
        ii+=1
main.set_font('Monaco','',11)

main.write(height,'\n'*1) # space in start

def ptxt(text,color=None):
    tempcolor = (0,0,0)
    if color == 'orange':
        tempcolor = (248,96,0)
    if color == 'blue':
        tempcolor = (25,20,255)
    if color == None:
        tempcolor = (0,0,0)
    if color == 'green':
        tempcolor = (43,165,0)
    if color == 'red':
        tempcolor = (205,0,0)
    '''
    if color == 'lightblue':
        tempcolor = (154,217,250)
        tempcolor = (85,153,210)
    '''
    if color == 'lightgrey':
        tempcolor = (210,210,213)
    if color == 'purple':
        tempcolor = (131,0,140)
    main.set_text_color(*tempcolor)
    main.write(height,text)

def lineformat1(line):
    temp1 = list(linesplitter(line))
    i = 0
    while i < (len(temp1)):
        if temp1[i] in ('def','class'):
            ptxt(temp1[i],'orange')
            i+=1
            ti = temp1.index('(')
            ptxt(''.join(temp1[i:ti]),'blue')
            i = ti
            ptxt(''.join(temp1[i:]))
            break
        elif temp1[i] in ('"',"'"):
            ti = i + 1 + temp1[i+1:].index(temp1[i])
            ptxt(''.join(temp1[i:ti+1]),'green')
            i = ti+1
        elif temp1[i] == '#':
            ptxt(''.join(temp1[i:]),'red')
            break
        elif temp1[i] in ('from','import','as','try','except','else','if',
                          'for','elif','return','yield','True','False','None',
                          'continue','break','while','is','not','in','or',
                          'and','with','raise'):
            ptxt(temp1[i],'orange')
            i+=1
        elif temp1[i] in builtin_function_names:
            ptxt(temp1[i],'purple')
            i+=1
        elif '_' in temp1[i]:
            ptxt(temp1[i],'lightblue')
            i+=1
        else:
            ptxt(temp1[i])
            i+=1

ttt = False
i = 1
tempLen = len(fileIn)
for item in fileIn:
    ptxt(str(i).rjust(len(str(tempLen)))+' | ','lightgrey')
    if ttt == False:
        if "'''" not in item:
            lineformat1(item)
        else:
            temp2 = item.split("'''")
            lineformat1(temp2[0])
            if len(temp2) != 2:
                ptxt("'''"+temp2[1]+"'''",'green')
                lineformat1(''.join(temp2[2:]))
            else:
                ptxt("'''"+temp2[1],'green')
                ttt = True
    else:
        if "'''" not in item:
            ptxt(item,'green')
        else:
            temp2 = item.split("'''")
            ptxt(temp2[0]+"'''",'green')
            lineformat1(temp2[1])
            ttt = False
    i+=1   

main.output(filenameMain+'.pdf')
mainwin.destroy()

mainwin.mainloop()
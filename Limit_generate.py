
# Import Required Library 
from tkinter import *
from tkcalendar import Calendar 
from datetime import date
import os 
import xml.etree.ElementTree as ET

# Create Object 
page = Tk() 

#get current date
today = date.today()

#dictionary to store all limit
limit_file = {
            'DN2485':'100000',
            'DN2638':'200000',
            'DN2024':'600000',
            'DN1515':'500000',
            'DN2070':'400000',
            'D2000':'10000000',
            'DN3000':'1500000',
            'DN2009':'400000',
            'DN2004':'600000',
            'DN2005':'500000',
            'DN2622':'500000',
            'DN2012':'1000000',
            'N183':'1000000',
            'N633':'500000',
            'N188':'500000',
            'DN2444':'500000',
            'N134':'500000',
            'DN1780':'500000',
            'DN1781':'500000',
            'DN1922':'500000',
            'N4036':'300000',
            'DN2959':'200000',
            'DN3066':'5000000',
            'DN3056':'1000000',
            'DN3128':'1000000',
            'DN1729':'300000',
            'DN2375':'500000',
            'DN3062':'100000',
            'DN3078':'50000',
            'DN3084':'50000',
            'DN1970':'1000000',
            'N191':'50000',
            'D1838':'300000',
            'D1938':'300000',
            'NK1184':'700000',
            'NK1136':'11000000',
            'NK1169':'1000000',
            'NK1191':'10000000',
            'NK1101':'300000',
            'NK1072':'300000',
            'NK1123':'200000',
            'NK1171':'200000',
            'NK1118':'700000',
            'NK1094':'2000000',
            'NK1068':'1000000',
            'NK1173':'150000',
            'NK1194':'1000000',
            'NK1067':'300000',
            'NK1032':'500000',
            'NK1259':'400000',
            'NK1234':'50000'
         }



y = int(today.strftime("%Y"))
m = int(today.strftime("%m"))
d = int(today.strftime("%d"))
# Set geometry 
page.geometry("400x400") 
  
# Add Calender 
cal = Calendar(page, selectmode = 'day', 
               year = y, month = m, day = d, 
               firstweekday = 'sunday', weekenddays = [6,7], 
               date_pattern = "dd.mm.yy", showweeknumbers = False, 
               weekendbackground = 'Light Green') 
  
cal.pack(pady = 5) 
  
def grad_date(): 
    date.config(text = "Selected Date is: " + cal.get_date()) 
    date_c = cal.get_date()
    date_list = date_c.split(".")

    file_start = str(y) + date_list[1] + date_list[0]
    file_end = "*.xml"
    os.chdir('\\\\150.1.62.26\\2021\MAR-21')
    
    #creating folder in required destination using date format
    if not os.path.exists(date_c):
        os.mkdir(date_c) 


    src = "\\\\150.1.62.2\MottaiXML\\"

    #src = "E:\Projects\LimitPY\FinalProjectBefore_run\src\\"
    #dst = "E:\Projects\LimitPY\FinalProjectBefore_run\dst"

    dst = "\\\\150.1.62.26\\2021\MAR-21\\" + date_c
    #dst = "\\\\150.1.62.26\\2021\MAR-21\\" + "test"

    cmd = "copy " + src + file_start + file_end +' '+ dst
    os.system(cmd)

    os.chdir('\\\\150.1.62.26\\2021\MAR-21\\'+ date_c)

    cli_files = os.listdir('.')

    for cl_file in cli_files:
        if cl_file.endswith("-clients-RBS.xml"):
            xml_to_read = cl_file
            break

    tree = ET.parse(xml_to_read)
    root = tree.getroot()

    for limit in root.findall('Limits'):            # using root.findall() to avoid removal during traversal
        client = str(limit.find('ClientCode').text)
        cash = limit.find('Cash').text

        new_cash = limit_file.get(client,'noNeed')  #collecting cash limit if required to change
        #print(client,': ',new_cash)
        
        if new_cash !='noNeed' and int(new_cash) > int(cash):
            limit.find('Cash').text = new_cash
            print(client, ': [Old]',cash, ': [New]',new_cash)
        
    tree.write('new.xml')

    toFormatXML = open("new.xml", "r")
    content = toFormatXML.read()
    toFormatXML.close()
    os.remove("new.xml")
    os.remove(xml_to_read)
    firstLine = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n\n"

    formatXML = open(xml_to_read, "w")
    formatXML.write(firstLine)
    formatXML.write(content)
    formatXML.close()



# Add Button and Label 
Button(page, text = "Generate", command = grad_date).pack(pady = 20) 


date = Label(page, text = "") 
date.pack(pady = 5) 


 
Button(page, text = "Exit", command = exit).pack(pady = 10)    
# Excecute Tkinter 
page.mainloop()

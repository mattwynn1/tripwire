from mechanize import Browser
from bs4 import *
from time import *
import re
import datetime

# today
today = str(datetime.date.today().strftime("%m-%d-%Y"))

# open a file to write to
f = open('sarpy-warrants' + today + '.txt', 'wb')

# add headers to text file
f.write('number|last|rest|dob|eyes|hair|sex|race|height|weight|address|apt|city|state|issued|type|court|agency|due|crime\n')

# crank up a browser
mech = Browser()

# add a user-agent string
mech.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# ignore robots
mech.set_handle_robots(False)

# define opening url
baseurl = "http://www.sarpy.com/sheriff/warrants/Results.asp?lname=&fname=&sType=0&Disclaimer=0"

# beautifulsoup that bizzo
page = mech.open(baseurl)
soup = BeautifulSoup(page)
clicks = soup.findAll('form')

numwarrants = len(clicks)
print "\nSlurping up " + str(numwarrants) + " active warrants ...\n=============================\n"

count = 0
while (count < numwarrants):
    mech.select_form(nr=count)
    req = mech.submit()
    
    try:
        resultspage = req.read()
        soup = BeautifulSoup(resultspage)
    except mechanize.HTTPError, e:
        if int(e.code) != 200:
            print "Shit's broke. Trying again ..."
            sleep(30)
            continue
    if resultspage:
        table = soup.findAll('table')[0]
        table2 = soup.findAll('table')[1]
            
        findnum = re.search('<b>WAR\d+', str(table))
        warrant_number = findnum.group().replace("<b>","")
           
        fonts = soup.findAll('font')
            
        namething = fonts[1].get_text(strip=True).encode('utf-8')
        nameraw = namething.replace('\xc2','').replace('\xa0','')
        almostthere = re.sub(r'\s\s+', ' ', nameraw).replace(" ","|", 1).replace('DOB:','|').replace('Name:','')
        last = almostthere.split('|')[0].strip()
        rest = almostthere.split('|')[1].strip()
        dob = almostthere.split('|')[2].strip()
            
        att = fonts[2].findAll('b')
           
        eyes = att[0].get_text(strip=True)
        hair = att[1].get_text(strip=True)
        sex = att[2].get_text(strip=True)
        race = att[3].get_text(strip=True)
        height = att[4].get_text(strip=True)
        weight = att[5].get_text(strip=True)
            
        contacts = fonts[3].findAll('b')
        address = contacts[0].get_text(strip=True)
        apt = contacts[1].get_text(strip=True)
        city = contacts[2].get_text(strip=True)
        state = contacts[3].get_text(strip=True)
            
        deets = fonts[4].findAll('b')
        issued = deets[0].get_text(strip=True)
        status = deets[1].get_text(strip=True)
            
        moredeets = fonts[5].findAll('b')
        warranttype = moredeets[1].get_text(strip=True)
        court = moredeets[2].get_text(strip=True)
            
        agency = fonts[6].findAll('b')[0].get_text(strip=True)
           
        due = fonts[7].findAll('b')[0].get_text(strip=True)
            
        charges = []
            
        for row in table2.findAll('tr')[1:]:
            col = row.findAll('td')
            crime = col[0].get_text(strip=True)
            charges.append(crime) 
                
        problems = ' and '.join(charges)
            
        fullrecord = (warrant_number, rest, last, dob, eyes, hair, race, sex, height, weight, address, apt, city, state, issued, status, warranttype, court, agency, due, problems, "\n")
        print rest.upper() + " " + last.upper()
            
        f.write("|".join(fullrecord))
        count = count + 1
        
        # navigate back
        mech.back()
        sleep(1)

f.flush()
f.close()

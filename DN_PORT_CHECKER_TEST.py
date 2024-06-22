#!/usr/bin/env python3

#This script takes as input a list of IP addresses of Salespoints to be checked (or hostnames, depending on your dns settings) and writes to the working directory a .csv file with the following data for each Salespoint:
#["Host IP Address", "DirectNet IP Address", "DirectNet Port"]

import sys
import smtplib
import re
import os
import time
import shutil    
import csv
from email.message import EmailMessage
from email.utils import make_msgid

#Must escape any special/reserved chars in your password below with python escape characters.
#Replace "<your Windows admin username>" and "<your Windows admin password>" with the correct values for your environment.  The two should be separated by "%".
#depending on your environment, you may have to use a FQDN for the username (username@domain_name)

user_pwd = r"gashley@durangomountain.local%e^\(auBergine9713"
path1 = os.getcwd()
dir_name = "DN_PORT_TEXT"
dir_path = os.path.join(path1, dir_name)
not_sales_pos_list = []
is_sales_pos_list = []
list_o_lists = []

#We create a temporary directory in which we will store text to be parsed later in the script using regex
if os.path.isdir(dir_path):
    pass

else: 
    os.mkdir(dir_path, 0o700)

#list of IP addresses for the hosts to be checked, formatted as per a python list of strings 
#POSs = ['10.2.12.158', '10.2.12.164']
POSs = ['10.2.12.101', '10.2.12.103', '10.2.12.100', '10.2.12.102', '10.2.12.160', '10.2.12.161', '10.2.12.163', '10.2.12.157', '10.2.12.159', '10.2.12.175', '10.2.12.156', '10.2.12.182', '10.2.12.184', '10.2.12.105', '10.2.12.165', '10.2.12.152', '10.2.12.153', '10.2.12.186', '10.2.12.104', '10.2.12.173', '10.2.12.183', '10.2.12.185', '10.2.12.158', '10.2.12.162', '10.2.12.169', '10.2.12.167', '10.2.12.151', '10.2.12.172', '10.2.12.181', '10.2.12.155', '10.2.12.179', '10.2.12.192', '10.2.12.177', '10.2.12.178', '10.2.12.170', '10.2.12.176', '10.2.12.164', '10.2.12.154', '10.2.12.180', '10.2.12.166', '10.2.12.187']

for POS in POSs:    
    file_name = r"{}_cfg.txt".format(POS)
    local_path = os.path.join(dir_name, file_name)
    DN_path = r"//{}/C$/Program\ Files\ \(x86\)/Siriusware/Sales/Sales32c_System.ini".format(POS)
    
    a = os.system(r'''smbget smb:{}  -D -o {} --user={}'''.format(DN_path, local_path, user_pwd)) 

#Typically I have used a try/except block here but in this case "except" did not catch the exception when the path to the file was not found, i.e. when the PC was turned off or when it was not a SP.  Thus, the below instead (parsing the returncode worked to catch the errors but try/except did not).

    if a == 0:
        print("Success!")
        is_sales_pos_list.append(POS)
        continue

    else:
        print("Process failed!")
        not_sales_pos_list.append(POS)
        continue

correct_list = []
incorrect_list = []

for POS in POSs:
    
    file_name = r"{}_cfg.txt".format(POS)
    file_path1 = os.path.join(dir_path, file_name)
    local_list = []
    try:
        
        #Setting the encoding to "unicode-escape" was necessary to read this particular file
        with open (file_path1, "r", encoding='unicode-escape') as file2:
            Directnet_text = file2.read()
            #Use a regex pattern to get the needed data
            pattern = r"(DirectNet\=)(\d+\.\d+\.\d+\.\d+)(\:)(\d+)"
            retd_pattern = re.search(pattern, Directnet_text)    
            if retd_pattern[4] == '3202':
                correct_list.append(POS)
            else:
                incorrect_list.append(POS)
                


    except:
        print("Error during regex parsing of text for host {}.  Continuing...".format(POS))
        continue

correct_str = str(correct_list)
correct_str1 = correct_str.lstrip('[')
correct_str2 = correct_str1.rstrip(']')
incorrect_str = str(incorrect_list)
incorrect_str1 = incorrect_str.lstrip('[')
incorrect_str2 = incorrect_str1.rstrip(']')

file_name1 = "DIRECTNET_PORT.TXT"
filepath = os.path.join(path1, file_name1)

if correct_str2:
    with open (filepath, 'a', 0o700) as file3:
        file3.write(r"Sales hosts {} were online when the program ran.  They are using the correct port for DirectNet (3202).  If nothing else is below this message, no hosts were found to be using the incorrect port at this time.  ".format(correct_str2))

if incorrect_str2:
    pattern = r"[\d]+"
    result = re.search(pattern, incorrect_str2)
    if result:
        with open (filepath, 'a', 0o700) as file3:
            file3.write(r"WARNING: Sales hosts {} are using incorrect ports for DirectNet and this could cause accounting errors if not resolved.  Please notify Purgatory IT and they will fix any errors.  ".format(incorrect_str2))
    else:
        pass
else:
    pass

#We did not need fqd name for the smtp host below; it would not work with it included.

me = r'dmradmin@dmvnagiosnew'

youse = [r'gashley@purgatory.ski'] 

#r'itsupport@purgatory.ski', r'cjans@purgatory.ski']



for you in youse:

    try:

        with open (filepath, "r", 0o700) as fp:
            msg = EmailMessage()
            b = fp.read()
            msg.set_content(b)
            #below is for troubleshooting and can be commented out at any time
            print(b)
        
    
        msg['Subject'] = "Automated message from Purgatory IT"
        msg['From'] = me
        msg['To'] = you
        #Below step was necessary as it would not work without
        msg['Message-ID'] = make_msgid()
        #We print the email message to stdout below for troubleshooting
        sys.stdout.buffer.write(msg.as_bytes())
        #The port (25) on the SMTP host below did not end up being necessary for our use.  We also did not need a fqdn here
        s = smtplib.SMTP("10.2.14.51")
        s.send_message(msg)
        s.quit()


        print("Email sent to {}.".format(you))


    except:
        print(r"error while calling postfix; exiting")


#Cleanup: delete the temporary directory "DN_PORT_TEXT" that we had created earlier and the temporary file DIRECTNET_PORT.TXT 
#shutil.rmtree(dir_path)
#os.remove(file_name1)
print('all done now.')
exit()

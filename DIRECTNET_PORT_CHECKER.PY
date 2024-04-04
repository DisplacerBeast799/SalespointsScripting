#!/usr/bin/env python3
import re
import os
import time
import shutil    
import csv

#Note: must escape any special/reserved chars in your password. 
user_pwd = r"gashley@durangomountain.local%e^\(auBergine9713"
path1 = os.getcwd()
dir_name = "DN_PORT_TEXT"
dir_path = os.path.join(path1, dir_name)
not_sales_pos_list = []
is_sales_pos_list = []
list_o_lists = []
#create a temporary directory in which we will store text to be parsed later in the script with a regex pattern:
os.mkdir(dir_path, 0o700)

#Below are all the hosts on our Vlan 12 (at time of writing) which is dedicated to F&B.  Note: many hosts on this vlan are turned off at this time, and some are not POSs though they are connected to the vlan 12.  This list was derived by talking to our core Cisco switch.  TODO: make a more comprehensive list using data from Active Directory

POSs = ['10.2.12.101', '10.2.12.103', '10.2.12.100', '10.2.12.102', '10.2.12.160', '10.2.12.161', '10.2.12.163', '10.2.12.157', '10.2.12.159', '10.2.12.175', '10.2.12.156', '10.2.12.182', '10.2.12.184', '10.2.12.105', '10.2.12.165', '10.2.12.152', '10.2.12.153', '10.2.12.186', '10.2.12.104', '10.2.12.173', '10.2.12.183', '10.2.12.185', '10.2.12.158', '10.2.12.162', '10.2.12.169', '10.2.12.167', '10.2.12.151', '10.2.12.172', '10.2.12.181', '10.2.12.155', '10.2.12.179', '10.2.12.192', '10.2.12.177', '10.2.12.178', '10.2.12.170', '10.2.12.176', '10.2.12.164', '10.2.12.154', '10.2.12.180', '10.2.12.166', '10.2.12.187']

for POS in POSs:    
    file_name = r"{}_cfg.txt".format(POS)
    local_path = os.path.join(dir_name, file_name)
    DN_path = r"//{}/C$/Program\ Files\ \(x86\)/Siriusware/Sales/Sales32c_System.ini".format(POS)
    
    a = os.system(r'''smbget smb:{}  -D -o {} --user={}'''.format(DN_path, local_path, user_pwd)) 

#Note to self: I tried a try/except block here.  "Except" did not catch the exceptions when the path to the file was not found, i.e. when the PC was turned off or when it was not a SP.  Thus the below instead (parsing the returncode worked to catch the errors but try/except did not).

    if a == 0:
        print("Success!")
        is_sales_pos_list.append(POS)
        continue

    else:
        print("Process failed!")
        not_sales_pos_list.append(POS)
        continue


headers = ["Host IP Address", "DirectNet IP Address", "DirectNet Port"]
list_o_lists.append(headers)

for POS in POSs:
    
    file_name = r"{}_cfg.txt".format(POS)
    file_path1 = os.path.join(dir_path, file_name)
    local_list = []
    try:
        
        #Note to self: setting the encoding to "unicode-escape" was necessary here when looking at Sales32c_System.ini, but was not necessary when looking at Mindy.bin (in another script)
        with open (file_path1, "r", encoding='unicode-escape') as file2:
            Directnet_text = file2.read()
            #We grab the IP address of the host itself, that of DirectNet, and then the port being used by DirectNet:
            pattern = r"(DirectNet\=)(\d+\.\d+\.\d+\.\d+)(\:)(\d+)"
            retd_pattern = re.search(pattern, Directnet_text)
            local_list.append(POS)
            local_list.append(retd_pattern[2])
            local_list.append(retd_pattern[4])
            list_o_lists.append(local_list)
            
    except:
        #Here, we attempt to catch any potential errors with our regex pattern        
        print("Error during regex parsing of text for host {}.  Continuing...".format(POS))
        continue

file_name1 = "DIRECTNET_PORT.CSV"
csv_filepath = os.path.join(path1, file_name1) 
with open (csv_filepath, "w", 0o700) as csv_file:
    csvwriter = csv.writer(csv_file)
    csvwriter.writerows(list_o_lists)

print("The following PCs host Sales:" + str(is_sales_pos_list))
print("The following PCs are either turned off or do do host Sales:" + str(not_sales_pos_list))

#Cleanup: delete the temporary directory "DN_PORT_TEXT" that we had created earlier 
shutil.rmtree(dir_path)

exit()

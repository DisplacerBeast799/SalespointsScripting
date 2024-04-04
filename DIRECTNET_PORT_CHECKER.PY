#!/usr/bin/env python3
import re
import os
import time
import shutil    
import csv

user_pwd = r"gashley@durangomountain.local%e^\(auBergine9713"
path1 = os.getcwd()
dir_name = "DN_PORT_TEXT"
dir_path = os.path.join(path1, dir_name)
not_sales_pos_list = []
list_o_lists = []
os.mkdir(dir_path, 0o700)


#All hosts on our Vlan 12 which is dedicated to F&B.  List is derived from the output of "show IP arp Vlan 12" on our core Cisco switch
POSs = ['10.2.12.158', '10.2.12.162', '10.2.10.175']
#POSs = ['10.2.10.175']
#POSs = ['10.2.12.101', '10.2.12.103', '10.2.12.100', '10.2.12.102', '10.2.12.160', '10.2.12.161', '10.2.12.163', '10.2.12.157', '10.2.12.159', '10.2.12.175', '10.2.12.156', '10.2.12.182', '10.2.12.184', '10.2.12.105', '10.2.12.165', '10.2.12.152', '10.2.12.153', '10.2.12.186', '10.2.12.104', '10.2.12.173', '10.2.12.183', '10.2.12.185', '10.2.12.158', '10.2.12.162', '10.2.12.169', '10.2.12.167', '10.2.12.151', '10.2.12.172', '10.2.12.181', '10.2.12.155', '10.2.12.179', '10.2.12.192', '10.2.12.177', '10.2.12.178', '10.2.12.170', '10.2.12.176', '10.2.12.164', '10.2.12.154', '10.2.12.180', '10.2.12.166', '10.2.12.187']

for POS in POSs:    
    file_name = r"{}_cfg.txt".format(POS)
    local_path = os.path.join(dir_name, file_name)
    DN_path = r"//{}/C$/Program\ Files\ \(x86\)/Siriusware/Sales/Sales32c_System.ini".format(POS)
    
    



    a = os.system(r'''smbget smb:{}  -D -o {} --user={}'''.format(DN_path, local_path, user_pwd)) 
#    a = os.system(r'''smbget smb:{}  -D --user={}'''.format(DN_path, user_pwd))
    if a == 0:
        print("Success!")

    else:
        print("Process failed!")
        not_sales_pos_list.append(POS)
        continue

print(not_sales_pos_list)
exit()

#headers = ["Host IP Address", "DirectNet IP Address", "DirectNet Port"]
#list_o_lists.append(headers)

#for POS in POSs:
    
#    file_name = r"{}_cfg.txt".format(POS)
#    file_path1 = os.path.join(dir_path, file_name)
#    local_list = []
#    try:
        
        
#        with open (file_path1, "r", encoding='unicode-escape') as file2:
#            Directnet_text = file2.read()
#            pattern = r"(DirectNet\=)(\d+\.\d+\.\d+\.\d+)(\:)(\d+)"
#            retd_pattern = re.search(pattern, Directnet_text)
#            local_list.append(POS)
#            local_list.append(retd_pattern[2])
#            local_list.append(retd_pattern[4])
#            list_o_lists.append(local_list)
            
#    except:
        
#        print("Error during regex parsing of text for host {}.  Continuing...".format(POS))
#        continue

#file_name1 = "DIRECTNET_PORT.CSV"
#csv_filepath = os.path.join(path1, file_name1) 
#with open (csv_filepath, "w", 0o700) as csv_file:
#    csvwriter = csv.writer(csv_file)
#    csvwriter.writerows(list_o_lists)

#print(not_sales_pos_list)

shutil.rmtree(dir_path)

#exit()

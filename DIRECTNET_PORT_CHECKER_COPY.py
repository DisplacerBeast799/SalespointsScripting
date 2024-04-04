#!/usr/bin/env python3
import re
import os
import time
import shutil    
import csv

#Must escape any special/reserved chars in your password below with python escape characters.
#Replace "<your Windows admin username>" and "<your Windows admin password>" with the correct values for your environment.  The two should be separated by "%".
#depending on your environment, you may have to use a FQDN for the username (username@domain_name)
user_pwd = r"<your Windows admin username>%<your Windows admin password>"
path1 = os.getcwd()
dir_name = "DN_PORT_TEXT"
dir_path = os.path.join(path1, dir_name)
not_sales_pos_list = []
is_sales_pos_list = []
list_o_lists = []
#We create a temporary directory in which we will store text to be parsed later in the script using regex
os.mkdir(dir_path, 0o700)

#list of IP addresses for the hosts to be checked, formatted as per a python list of strings 
POSs = []

for POS in POSs:    
    file_name = r"{}_cfg.txt".format(POS)
    local_path = os.path.join(dir_name, file_name)
    DN_path = r"//{}/C$/Program\ Files\ \(x86\)/Siriusware/Sales/Sales32c_System.ini".format(POS)
    
    a = os.system(r'''smbget smb:{}  -D -o {} --user={}'''.format(DN_path, local_path, user_pwd)) 

#Normally I would prefer a try/except block here but in this case "except" did not catch the exception when the path to the file was not found, i.e. when the PC was turned off or when it was not a SP.  Thus, the below instead (parsing the returncode worked to catch the errors but try/except did not).

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
        
            #Setting the encoding to "unicode-escape" was necessary to read this particular file
            with open (file_path1, "r", encoding='unicode-escape') as file2:
                Directnet_text = file2.read()
                #Use a regex pattern to get the needed data (see "headers =" above)
                pattern = r"(DirectNet\=)(\d+\.\d+\.\d+\.\d+)(\:)(\d+)"
                retd_pattern = re.search(pattern, Directnet_text)
                local_list.append(POS)
                local_list.append(retd_pattern[2])
                local_list.append(retd_pattern[4])
                list_o_lists.append(local_list)
            
    except:
        print("Error during regex parsing of text for host {}.  Continuing...".format(POS))
        continue

file_name1 = "DIRECTNET_PORT.CSV"
csv_filepath = os.path.join(path1, file_name1) 
with open (csv_filepath, "w", 0o700) as csv_file:
    csvwriter = csv.writer(csv_file)
    csvwriter.writerows(list_o_lists)

print("The following PCs host Sales:" + str(is_sales_pos_list))
print("The following PCs are either turned off or do not host Sales:" + str(not_sales_pos_list))

#Cleanup: delete the temporary directory "DN_PORT_TEXT" that we had created earlier 
shutil.rmtree(dir_path)

exit()

#!/usr/bin/env python3
import re
import os
import time
import shutil    
import csv

path1 = os.getcwd()
dir_name = "MINDY_FILES"
dir_path = os.path.join(path1, dir_name)
list_o_lists = []
os.mkdir(dir_path, 0o700)

#IP addresses of the hosts to be checked go in the square brackets below (bounded by single or double quotes, separated by a comma and space as per python list of strings)

FNBPOSs = []

for FNBPOS in FNBPOSs:
    file_name = r"{}_conf.txt".format(FNBPOS)
    local_path = os.path.join(dir_name, file_name)
    
    try:

#Below: replace "<your Windows admin username>" and "<your Windows admin password>" with the correct values for your own environment.  Note: I needed to use a FQDN format for the username, i.e., user@domain_name.  This may not be needed in your Windows environment.  User and password should be separated by "%".  My password needed to be surrounded by double quotes due to reserved characters being contained in my password, and double quotes may not be needed in your environment.  
        os.system(r'''smbget "smb://{}/C$/ProgramData/Siriusware/Sales/mindy.bin" -D -o {} --user=<your Windows admin username>%"<your Windows admin password>"'''.format(FNBPOS, local_path)) 
           
    except:
	    
        print(r"error while opening SMB for host {}, continuing...".format(FNBPOS))

        continue

headers = ["Salespoint name", "Windows Hostname", "IP Address"]
list_o_lists.append(headers)

for FNBPOS in FNBPOSs:
    
    file_name = r"{}_conf.txt".format(FNBPOS)
    file_path1 = os.path.join(dir_path, file_name)
    local_list = []
    try:

        with open (file_path1, "r") as file2:
           
            Mindy_text = file2.read()
            #We use a regex pattern to extract the needed data from each Mindy file (see "headers =" above)
            sp_name_pattern = r"(<SALESPOINT>)([\w]+)([\s]*)(</SALESPOINT>)"
            hostname_pattern = r"(<IP>)([\S]+)([\s]+)(\d+\.\d+\.\d+\.\d+)(</IP>)"
            retd_text_sp = re.search(sp_name_pattern, Mindy_text)
            retd_text_hn = re.search(hostname_pattern, Mindy_text)
            local_list.append(retd_text_sp[2])
            local_list.append(retd_text_hn[2])
            local_list.append(retd_text_hn[4])
            list_o_lists.append(local_list)
    
    except:
        
        print("Error during regex parsing of text for host {}.  Continuing...".format(FNBPOS))
        continue

file_name1 = "SP_INFO_CSV_FILE"
csv_filepath = os.path.join(path1, file_name1) 
with open (csv_filepath, "w", 0o700) as csv_file:
    csvwriter = csv.writer(csv_file)
    csvwriter.writerows(list_o_lists)

#We remove the temporarily used directory "MINDY_FILES" that we created earlier
 
shutil.rmtree(dir_path)

exit()

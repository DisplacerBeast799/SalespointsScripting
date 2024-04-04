#!/usr/bin/env python3
import re
import os
import time
import shutil    
import csv

#FNBPOSs = ['10.2.31.146']
path1 = os.getcwd()
dir_name = "MINDY_FILES"
dir_path = os.path.join(path1, dir_name)
list_o_lists = []
os.mkdir(dir_path, 0o700)

#There is a misspelling in the hostname 'PARADISESERVFR', not mine, but that is how it's currently named in AD, so leaving this way for now.

POS_DICT = {'10.2.31.146': 'BBRIGHT', '10.2.12.155': 'BEARBARLEFT', '10.2.21.94': 'BEARBARRIGHT', '10.2.12.156': 'BISTROBAR', '10.2.12.173': 'BISTROBARSERVER', '10.2.12.186': 'BISTROBKSERVER', '10.2.12.184': 'DANTECASHIER1', '10.2.12.185': 'DANTES-BAR', '10.2.12.183': 'DANTESCOFFEE', '10.2.12.182': 'DANTESOUTSIDE', '10.2.31.168': 'DM-D-POS-PG-01', '10.2.31.30': 'DM-POS-DELI', '10.2.12.153': 'DMCBAR', '10.2.31.119': 'DMCserver', '10.2.10.110': 'DMI', '10.2.31.142': 'FB-TRAINING', '10.2.31.134': 'FNB-OUTSIDE2', '10.2.31.143': 'HOODYSCASHIER', '10.2.12.154': 'PARADISEBAR', '10.2.31.69': 'PARADISEFRONT', '10.2.12.169': 'PARADISEICE', '10.2.12.164': 'PARADISESERVFR', '10.2.12.167': 'PHKITCHENNEW', '10.2.12.158': 'PURGYBARLEFT', '10.2.12.162': 'PURGYBARRIGHT', '10.2.12.172': 'PURGYCASHRIGHT', '10.2.31.155': 'REMOTE_POS_1', '10.2.12.152': 'WAFFLES'}

POS_DICT_OFFLINE = {'OFFLINE': 'DELI', 'OFFLINE': 'FB-DMCGAME', 'OFFLINE': 'PHCASHIER2', 'OFFLINE': 'PURGYCOFFEE'}

FNBPOSs = list(POS_DICT.keys())

for FNBPOS in FNBPOSs:
    file_name = r"{}_conf.txt".format(FNBPOS)
    local_path = os.path.join(dir_name, file_name)
    
    try:
#        time.sleep(1)
##		Older SMB statement that worked: os.system(r'''smbget "smb://{}/C$/Program Files (x86)/Siriusware/Sales/Sales32c_System.ini" -D -o "{}_config.txt" --user=gashley@durangomountain.local%"e^(auBergine9713"'''.format(FNBPOS, FNBPOS))
#       Newer statement that works below.  The SMB statement itself works; the rest is in the testing phase
        os.system(r'''smbget "smb://{}/C$/ProgramData/Siriusware/Sales/mindy.bin" -D -o {} --user=gashley@durangomountain.local%"e^(auBergine9713"'''.format(FNBPOS, local_path, FNBPOS)) 
        #The files seem to take about 2 sec to download; setting the sleep at 4 for safety.  
#        time.sleep(4)

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
        
#        with open ("/home/admin/PurgProjects1/PurgWinHostsSMB/SMB_TEST_FILES/{}_conf.txt".format(FNBPOS), "r") as file2:
        with open (file_path1, "r") as file2:
           
            Mindy_text = file2.read()
            sp_name_pattern = r"(<SALESPOINT>)([\w]+)([\s]*)(</SALESPOINT>)"
            hostname_pattern = r"(<IP>)([\S]+)([\s]+)(\d+\.\d+\.\d+\.\d+)(</IP>)"
            retd_text_sp = re.search(sp_name_pattern, Mindy_text)
            retd_text_hn = re.search(hostname_pattern, Mindy_text)
            #grabbed_text = re.search(pattern, Mindy_text)
            #append the Windows hostname of the SP
            #local_list.append(grabbed_text[2])
            #append the IP address of the SP
            #local_list.append(grabbed_text[4])
            local_list.append(retd_text_sp[2])
            local_list.append(retd_text_hn[2])
            local_list.append(retd_text_hn[4])
            list_o_lists.append(local_list)
    
    except:
        
        print("Error during regex parsing of text for host {}.  Continuing...".format(FNBPOS))
#       pass        
        continue

file_name1 = "SP_INFO_CSV_FILE"
csv_filepath = os.path.join(path1, file_name1) 
with open (csv_filepath, "w", 0o700) as csv_file:
    csvwriter = csv.writer(csv_file)
    csvwriter.writerows(list_o_lists)


shutil.rmtree(dir_path)

exit()

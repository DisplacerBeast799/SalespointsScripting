import os
import time

FNBPOSs = ['dantesoutside']

#FNBPOSs = ['BEARBARLEFT', 'BEARBARRIGHT', 'BISTROBAR', 'BISTROBARSERVER', 'BISTROBKSERVER', 'DANTECASHIER1', 'DANTECASHIER2', 'DANTES-BAR', 'DANTESCOFFEE', 'DANTESOUTSIDE', 'DELI', 'DM-D-POS-PG-01',
#'DM-POS-DELI', 'DMCBAR', 'DMCserver', 'DMI', 'FB-DMCGAME', 'FB-TRAINING', 'FNB-ORDERREADY1', 'FNB-OUTSIDE2', 'HOODYSCASHIER', 'PARADISEBAR', 'PARADISEFRONT', 'PARADISEICE',
#'PARADISESERVFR', 'PHCASHIER2', 'PHKITCHENNEW', 'PURGYBARLEFT', 'PURGYBARRIGHT', 'PURGYCASHRIGHT', 'PURGYCOFFEE', 'WAFFLES']

for FNBPOS in FNBPOSs:

	try:
		os.system(r'''smbclient "smb://{}/C$/" -A win_creds.txt'''.format(FNBPOS)) 
		#I think the below sleep is needed, do not rmv
		#Passing the windows creds as above works for smbclient but not for smbget.  Also, it is necessary to pass the creds in the ways pictured in each statement 
		#(passing them with the first smbclient statement only did not work, and passing them using the "-A" did not work for smbget, returning an "unknown option" error.  
		#Perhaps this is due to smbget being marked "experimental" on the Debian man page at this time.)
		time.sleep(1)
		#Below: "-o" allows us to customize a name for SMB protocol's download, while "-D" will print dots in the terminial to indicate the script's progress.  The "--user=" option is in the following format per Debian man pages fro smbget: "--user=domain\username%password".  What is pictured in the script, however, is what worked in this env.  double-quotes are necessary around my Windows pwd due to the "(" special character.
		#Note: the "smb:" statement in front of the rest of the code below was not specified in the man pages; however, the SMB download here won't work without it.  Man pages 
		#specify that text only when initializing a connection with smbclient.  I discovered that it will make the download work by accident.    
		os.system(r'''smbget "smb://{}/C$/Program Files (x86)/Siriusware/Sales/Sales32c_System.ini" -D -o "{}_config.txt" --user=gashley@durangomountain.local%"e^(auBergine9713"'''.format(FNBPOS, FNBPOS))
		#The files seem to take about 2 sec to download; setting the sleep at 4 for safety.  
		time.sleep(4)

	except:
		print(r"error while opening SMB for host {}, continuing...".format(FNBPOS))

		continue


exit()

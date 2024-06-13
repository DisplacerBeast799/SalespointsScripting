# The two scripts here assist Siriusware administrators by automating certain tasks.

They use the SMB protocol and regex to analyze certain Sales configuration files and return different useful pieces of data.
They take as input a list of IP addresses (or hostnames, depending on your dns settings) to be analyzed and they return a .csv with the data in question. This .csv file is written to the working directory.

These are written for Python3 to be run from an interpreter in a Linux environment, but with little modification could also be run on Windows.

## DIRECTNET_PORT_CHECKER.py

Takes as input a list of IP addresses or hostnames (depending on your dns settings) and outputs a .csv which contains the IP address of the Salespoint, the IP address currently being used by DirectNet, and the port currently being used by DirectNet.

The goal with **DIRECTNET_PORT_CHECKER.py** is to avoid the undesirable case in which the port being used by DirectNet can revert back to another value unintentionally, for example, when using Windows utilites to perform a repair of the Sales installation. In such cases, if the change is undetected, credit card transactions could potentially be blocked from reaching the credit card processor and the bank.

## HOSTNAME_TO_SPNAME.py

Takes as input a list of IP addresses or hostnames (depending on your dns settings) and outputs a .csv which contains the IP address of the Salespoint, the hostname of the Salespoint, and its Salespoint point name as known by Siriusware Sales.

The goal with **HOSTNAME_TO_SPNAME.py** is to help organize the Siriusware Sales environment by automating the listing of the above information, preventing administrators from having to log into each Salespoint one by one to gather the same information.

This is particularly useful in dynamic environments in which Salespoints are added or removed with frequency, and also helpful in large Siriusware environments and in environments in which there does not already exist a list of such information. Such a list will help the administrator to quickly access the needed information to log in remotely to the Salespoints when needed using rdp or their remote access protocol of choice.

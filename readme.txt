Getting Started
https://www.paramiko.org/installing.html
https://www.python.org/downloads/

1.Install python to your local machine, and ensure that you are running code version (3.11.1 at the time of writing this)
2.Install paramiko to your local machine
(pip install paramiko)
3.a. Run the local executable
  b. Alternatively, run the source code directly "py NewVlanRouter.py"
4. Enter your login credentials. Note: If you have more than 2 passwords in use to log into varying systems i.e. You use more than your AD/TACACS password, then you may run into issues logging into some systems unless you restart the script and change passwords. The default behaviour is to log into using the initial password, while using the alternate password for routers that still require TACACS
5. Enter the requested information
6. Et Voila! You should now have a file that has the information you need for the Change Request!

Added Features:
Check Switch
    By hitting the check switch button, you can view existing vlan information, as well as CDP neighbors (you can flip between the two and it will re-populate the window)
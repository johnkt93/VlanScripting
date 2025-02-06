Getting Started
https://www.paramiko.org/installing.html
https://www.python.org/downloads/

1.Install python to your local machine, and ensure that you are running the minimum code version (3.11.1 at the time of writing this)
2.Install paramiko to your local machine
(pip install paramiko)
3. Add your login credentials to config.cfg
4.a. Run the local executable #Doesn't exist currently
  b. Alternatively, run the source code directly "py bounce_ports.py"

Mass Bounce Ports:
  Input the switch, and ports that you need bounced in the bounce_ports json file

  TODO/Considerations:
  Port bouncing via MAC/IP address
  Port bouncing via Location(?) - needs CMS integration (Maybe SN integration if we move to that tool?)
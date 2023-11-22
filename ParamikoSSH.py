#paramiko is a library to allow us to ssh through python.
#Documentation: https://docs.paramiko.org/en/stable/api/client.html
import paramiko
import sys
import os
import select
from getpass import getpass
from io import StringIO

output = ""

def connect(device,username,password,command=None):
    jumpbox = paramiko.SSHClient()
    #If the host key does not exist in our system, we will add it
    #By default this is set to deny
    jumpbox.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ip_address = "nsg-jump-pr01"
    #Start the SSH connection, with the provided paramaters
    try:
        jumpbox.connect(hostname=ip_address, username=username, password=password)
        print(f'Logging in as {username} on {ip_address}')

    except Exception as e:
        sys.stdout.write(str(e))
        sys.exit()

    #Now that a connection has been established with our jumpbox,
    #we need to get that transport socket and establish a new channel
    jumpbox_transport = jumpbox.get_transport()
    src_addr = (ip_address, 22)

    target=paramiko.SSHClient()
    target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        dest_addr = (device, 22)
        jumpbox_channel = jumpbox_transport.open_channel("direct-tcpip", dest_addr, src_addr)
        target.connect(hostname=device,username=username, password=password, sock=jumpbox_channel)
        print(f'Establishing a connection to {device}')
        if command is not None:
            stdin, stdout, stderr = target.exec_command(command=command)
            output = stdout.readlines()
            errors = stderr.readlines()
        return output
        return errors

    except Exception as e:
        print("An error has occured during the connection process")
        sys.stdout.write(str(e))
    finally:
        sys.stdout = sys.__stdout__
        target.close()
        jumpbox.close()
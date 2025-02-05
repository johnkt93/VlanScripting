#paramiko is a library to allow us to ssh through python.
#Documentation: https://docs.paramiko.org/en/stable/api/client.html
import paramiko
import sys
import os
import select
import asyncio
import logging
from getpass import getpass
from io import StringIO
from configparser import ConfigParser, SectionProxy

logging.basicConfig(level=logging.INFO)

class Auth:
    settings: SectionProxy
    def __init__(self, config: SectionProxy):
        self.settings = config
        self.user = self.settings.get('username')
        self.tacacs = self.settings.get('tacacs')
        self.alt_passwords = self.settings.get('alt_passwords').split(',')

config = ConfigParser()
config.read('config.cfg')

outputs= []

#logging.getLogger("paramiko").setLevel(logging.DEBUG)
async def connect(device, through_shell: bool, *commands):
    #Instantiate the Auth class to pull data from the config file
    auth = Auth(config['JumpBox'])
    user = auth.user
    tacacs = auth.tacacs

    jumpbox = paramiko.SSHClient()
    #If the host key does not exist in our system, we will add it
    #By default this is set to deny
    jumpbox.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ip_address = "nsg-jump-pr01"
    #Start the SSH connection, with the provided paramaters
    try:
        jumpbox.connect(hostname=ip_address, username=user, password=tacacs)
        jumpbox.invoke_shell()
        logging.info(f'Logging in as {user} on {ip_address}')

    except Exception as e:
        if e == EOFError:
            pass
        else:
            logging.error(f"An error occurred during the connection process: {e}", exc_info=True)
            sys.stdout.write(str(e))
            sys.exit()

    #Now that a connection has been established with our jumpbox,
    #we need to get that transport socket and establish a new channel
    jumpbox_transport = jumpbox.get_transport()
    src_addr = (ip_address, 22)
    target=paramiko.SSHClient()
    target.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        #outputs = []
        dest_addr = (device, 22)
        jumpbox_channel = jumpbox_transport.open_channel("direct-tcpip", dest_addr, src_addr)#.get_pty()
        target.connect(hostname=device,username=user, password=tacacs, sock=jumpbox_channel)
        if through_shell == True:
            chan = target.invoke_shell()
        else:
            pass
        logging.info(f'Establishing a connection to {device}')
        for command in commands:
            if through_shell == True:
                logging.info(f"Running command: {command}, through shell")
                chan.send(command + '\r')
                await asyncio.sleep(1)
                while chan.recv_ready():
                    output = chan.recv(1024).decode('utf-8')
                    outputs.append(output)
                    logging.info(output)
            else:
                logging.info(f"Running command: {command}, through exec channel")
                stdin, stdout, stderr = target.exec_command(command)
                output = await asyncio.to_thread(stdout.read().decode('utf-8'))
                error = await asyncio.to_thread(stderr.read().decode('utf-8'))
                outputs.append(output.decode())
                logging.info(output.decode())
        return outputs
    except Exception as e:
        if e == EOFError:
            pass
        else:
            logging.info("An error has occured during the connection process")
            sys.stdout.write(str(e))
    finally:
        sys.stdout = sys.__stdout__
        target.close()
        jumpbox.close()
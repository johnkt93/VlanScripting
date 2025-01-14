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

outputs= ''

async def connect(device, commands: list):
    #Creating an empty command list, that will update from the arguments provided
    command_list = []
    command_list.append(commands)

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
        logging.info(f'Logging in as {user} on {ip_address}')

    except Exception as e:
        if e == EOFError:
            pass
        else:
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
        target.connect(hostname=device,username=user, password=tacacs, sock=jumpbox_channel)
        await asyncio.sleep(.1)
        logging.info(f'Establishing a connection to {device}')
        for command in command_list:
            if command is not None:
                await asyncio.sleep(.1)
                logging.info(f"Running command: {command}")
                stdin, stdout, stderr = target.exec_command(command)
                output = await asyncio.to_thread(stdout.read)
                error = await asyncio.to_thread(stderr.read)
                outputs = output.decode().split('\r\n')
                return outputs

    except Exception as e:
        logging.info("An error has occured during the connection process")
        sys.stdout.write(str(e))
    finally:
        sys.stdout = sys.__stdout__
        target.close()
        jumpbox.close()
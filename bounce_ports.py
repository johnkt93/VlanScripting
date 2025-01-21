from import_json import *
from ParamikoSSH import *
import asyncio
import logging

logging.basicConfig(level=logging.INFO)

reformat = [
    {'Switch1':{
        'Ports':[]}},
    {'Switch2':{
        'Ports':[]}}
    ]
commands = []

async def main():
    # Tries to connect to the ports with descending order of importance TenGig->Gig->FastEther
    # Assumes either x/y/z format, or x/y format for ports
    try:
        data=bounce_ports()
        for switches in data:
            switch_dict = switches.keys()
            for switch in switch_dict:
                print(switch)
            for ports in switches.values():
                port = ports.values()
                for x in port:
                    for y in x:
                        print(f'    This is port {y} on switch: {switch}')
    except Exception as e:
        logging.info(e)
    finally:
        with open("Bounce_Ports.json", "w") as write_file:
            json.dump(reformat, write_file, indent=4)
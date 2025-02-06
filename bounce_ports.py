from import_json import *
from ParamikoSSH import *
import asyncio
import logging
import os
import subprocess
import re

logging.basicConfig(level=logging.INFO)

reformat = [
    {"Switch1":{
        "Ports":[]}}
    ]

commands = []

def device_info():
    match = r"Model Number\s+:\s+(\S+)"
    x = re.search(match, outputs[0])
    device_type = x.group(1)
    logging.info(device_type)

    if "9300-24UXB" in device_type:
        device_ports = "Te1/0/"
        print(f'This is a 9300, with ten gig ports')
    elif "C9300-48P" in device_type:
        device_ports = "Gi1/0/"
        print(f"This is a 9300 with gig ports")
    else:
        device_ports = "Gi1/0/" #Assume gig ports by default
        print("This is an unmapped model :(")
    return device_ports

async def main():
    try:
        data=bounce_ports()
        for switches in data:
            switch_dict = switches.keys()
            device_ports = ''
            for switch in switch_dict:
                #logging.info(switch)
                await connect(switch, False, 1, 'show ver')
                device_ports = device_info()
            for ports in switches.values():
                port = ports.values()
                for x in port:
                    for y in x:
                        logging.info(f'This is port {y} on switch: {switch}')
                        await connect(switch, True, 5, f'conf t', f'int {device_ports}{y}\nshut','no shut\nend', f'show mac address-table int {device_ports}{y}', f'show ip dhcp snooping bind int {device_ports}{y}')
                        
    except Exception as e:
        logging.info(e)
    finally:
        n = 1
        while os.path.exists(f"bounce_ports_output_{n}.txt"):
            n+=1
            if not os.path.exists(f"bounce_ports_output_{n}.txt"):
                with open(f"bounce_ports_output_{n}.txt", 'a') as write_file:
                    for line in outputs:
                        write_file.write(f'{line}')# Initialize the file
                    if os.name == "nt":
                        os.startfile(f"bounce_ports_output_{n}.txt")
                    elif os.name == "posix":
                        opener = "open" if "darwin" in os.sys.platform else "xdg-open"
                        subprocess.run([opener, f"bounce_ports_output_{n}.txt"])
                    break
        else:
            with open(f"bounce_ports_output_{n}.txt", 'a') as write_file:
                for line in outputs:
                    write_file.write(f'{line}')# Initialize the file
                if os.name == "nt":
                    os.startfile(f"bounce_ports_output_{n}.txt")
                elif os.name == "posix":
                    opener = "open" if "darwin" in os.sys.platform else "xdg-open"
                    subprocess.run([opener, f"bounce_ports_output_{n}.txt"])
        with open("Bounce_Ports.json", "w") as write_file:
            json.dump(reformat, write_file, indent=4) #reset the bounce_ports json, so it can be reused
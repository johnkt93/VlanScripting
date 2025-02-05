from import_json import *
from ParamikoSSH import *
import asyncio
import logging
import os
import subprocess

logging.basicConfig(level=logging.INFO)

reformat = [
    {'Switch1':{
        'Ports':[]}}
    ]

device_ports = 'Te1/0/'

commands = []
async def main():
    try:
        data=bounce_ports()
        for switches in data:
            switch_dict = switches.keys()
            for switch in switch_dict:
                #logging.info(switch)
                await connect(switch, False, 1, 'show ver')
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

await main()
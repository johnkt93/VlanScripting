from import_json import *
from ParamikoSSH import *
import asyncio




reformat = '''
{
"Switch1": {
    "Ports":[]},
"Switch2": {
    "Ports": []}
}
'''
async def main():
    port_task = set()
    # Tries to connect to the ports with descending order of importance TenGig->Gig->FastEther
    # Assumes either x/y/z format, or x/y format for ports
    for i in range(0,48):
        port = f'TenGigabitEthernet{i}'
        task = asyncio.create_task()
        port_task.add(task)
        try:
            bounce_ports()
        finally:
            with open("Bounce_Ports.json", "w") as write_file:
                json.dump(reformat, write_file)
        exit()

asyncio.run(main())
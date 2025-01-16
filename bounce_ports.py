from import_json import *
from ParamikoSSH import *
import asyncio




reformat = {
"Switch1": {
    "Ports":[]},
"Switch2": {
    "Ports": []}
}

commands = []

async def main():
    # Tries to connect to the ports with descending order of importance TenGig->Gig->FastEther
    # Assumes either x/y/z format, or x/y format for ports
    try:
        bounce_ports()
    finally:
        with open("Bounce_Ports.json", "w") as write_file:
            json.dump(reformat, write_file, indent=4)
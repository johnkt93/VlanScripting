import json
import os

def switch_db():
    if not os.path.exists("switch_db.json"):
        with open("switch_db.json", "w") as write_file:
            json.dump({}, write_file)  # Initialize with an empty list

    with open("switch_db.json", "r") as read_file:
        data = json.load(read_file)

    return data

def add_switch(switch="", cdp_neighbors="", device_type="", ip_address="", mac_address=""):
    data = switch_db()
    switch_update = {
        "cdp_neighbors": cdp_neighbors,
        "device_type":device_type,
        "ip_address": ip_address,
        "mac_address": mac_address,
    }
    switch_entry = {
        switch: [switch_update]
    }

    if "switches" not in data:
        data["switches"] = []
    if "routers" not in data:
        data["routers"] = []
    switch_exists = False
    for entry in data["switches"]:
        if switch in entry.keys():
            switch_exists = True
            existing_key = entry[switch][0]
            if existing_key != switch_update:
                print("The switch already exists with different information")  # Maybe list the differences, and allow the user to overwrite?
                print(existing_key)
                print("Do you want to update the database?")
                return
            else:
                print("Switch information already exists. No update needed.")
                return
    if not switch_exists:
        data["switches"].append(switch_entry)
    with open("switch_db.json", "w") as write_file:
        json.dump(data,write_file, indent=4, sort_keys=True)

def update_switch(switch, device_type="", ip_address="", mac_address="", cdp_neighbors=""):
    data = switch_db()
    switch_update = {
        "cdp_neighbors": cdp_neighbors,
        "device_type":device_type,
        "ip_address": ip_address,
        "mac_address": mac_address
    }
    
    switch_entry = {
        switch: [switch_update]
    }

    data["switches"][switch] = switch_update
    """if data["switches"][0]["cdp_neighbors"] != switch_update["cdp_neighbors"]:
        data["switches"][0]["cdp_neighbors"] = switch_update["cdp_neighbors"]
    if data["switches"][0]["device_type"] != switch_update["device_type"]:
        data["switches"][0]["device_type"] = switch_update["device_type"]
    if data["switches"][0]["ip_address"] != switch_update["ip_address"]:
        data["switches"][0]["device_type"] = switch_update["ip_address"]
    if data["switches"][0]["mac_address"] != switch_update["mac_address"]:
        data["switches"][0]["mac_address"] = switch_update["mac_address"]"""

    with open("switch_db.json", "w") as write_file:
        json.dump(data, write_file, indent=4, sort_keys=True)

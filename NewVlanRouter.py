import tkinter as tk
import json
from threading import Thread
from import_json import *
#from ParamikoSSH import *
from tkinter import messagebox

window = tk.Tk()
window.title("Vlan Creation Tool")

routers = ["cumm111-dist-aca01",
    "cumm024-dist-aca03",
    "cumm024-dist-aca04"]

dhcp_servers = []

def confirm_command():
    #switch_ssh()
    file_creation()
    switch_db()
    #add_switch(switch_var, "", "", "", "")

def check_switch():
    messagebox.showerror("Oops","Nope, doesn't do anything yet.\n\nTo be programmed.")

def switch_db():
    try:
        with open("switch_db.json", "r") as read_file:
            data = json.load(read_file)
    except FileNotFoundError:
        with open("switch_db.json", "w") as write_file:
            write_file.write("Empty")

def file_exists(file_name):
    try:
        with open(file_name, "r"):
            return True
    except FileNotFoundError:
        return False
#def switch_ssh():
#    connect(device=switch_var.get(),username=username_var.get(), password=password_var.get())

def new_window():
    new_window = tk.Toplevel(window)
    new_window.title("VLAN Creation Tool")

    global change_number_var
    global vlan_number_var
    global vlan_name_var
    global vlan_description_var
    global vlan_gateway_var
    global vlan_netmask_var
    global switchport_var

    change_number_var = tk.StringVar()
    change_number_label = tk.Label(new_window, text="Change Request Number:")
    change_number_label.pack(pady=5)
    change_number_input = tk.Entry(new_window, textvariable=change_number_var)
    change_number_input.pack()

    router_var = tk.StringVar(new_window)
    router_var.set(routers[0])
    router_dropdown_label = tk.Label(new_window, text="Source Distribution Router")
    router_dropdown_label.pack()
    router_dropdown = tk.OptionMenu(new_window, router_var, *routers)
    router_dropdown.pack()

    destination_switch_frame = tk.Frame(new_window)
    destination_switch_frame.pack()
    switch_var = tk.StringVar()
    switch_label = tk.Label(destination_switch_frame, text="Destination switch:")
    switch_label.pack()
    switch_input = tk.Entry(destination_switch_frame, textvariable=switch_var)
    switch_input.pack(side=tk.LEFT, padx=5)
    switch_check_button = tk.Button(destination_switch_frame, text="Check", command=check_switch)
    switch_check_button.pack(side=tk.RIGHT)

    switchport_var = tk.StringVar(new_window)
    switchport_label = tk.Label(new_window, text="Enter the switchport that the end device is connected to:")
    switchport_label.pack()
    switchport_input = tk.Entry(new_window, textvariable=switchport_var)
    switchport_input.pack()

    vlan_number_var = tk.StringVar()
    vlan_number_label = tk.Label(new_window, text="Vlan Number:")
    vlan_number_label.pack()
    vlan_number_input = tk.Entry(new_window, textvariable=vlan_number_var)
    vlan_number_input.pack()
    vlan_name_var = tk.StringVar()
    vlan_name_label = tk.Label(new_window, text="Vlan Name:")
    vlan_name_label.pack()
    vlan_name_label_input = tk.Entry(new_window, textvariable=vlan_name_var)
    vlan_name_label_input.pack()
    vlan_gateway_var = tk.StringVar()
    vlan_gateway_label = tk.Label(new_window, text="Enter the gateway address for the subnet")
    vlan_gateway_label.pack()
    vlan_gateway_input = tk.Entry(new_window, textvariable=vlan_gateway_var)
    vlan_gateway_input.pack()
    vlan_netmask_var = tk.StringVar()
    vlan_netmask_label = tk.Label(text="Enter the subnet mask. Defaults to 255.255.255.0") or "255.255.255.0"
    vlan_netmask_label.pack()
    vlan_netmask_input = tk.Entry(new_window, textvariable=vlan_netmask_var)
    vlan_netmask_input.pack()
    vlan_description_var = tk.StringVar()
    vlan_description_label = tk.Label(new_window, text="Enter a brief description for the vlan")
    vlan_description_label.pack()
    vlan_description_label_input = tk.Entry(new_window, textvariable=vlan_description_var)
    vlan_description_label_input.pack()

    multicast_checkbox_var = tk.IntVar()
    multicast_checkbox = tk.Checkbutton(new_window, text="Check if multicast was requested", variable=multicast_checkbox_var)
    multicast_checkbox.pack()

    button_frame = tk.Frame(new_window)
    button_frame.pack(side=tk.BOTTOM, pady=5)

    confirm_button = tk.Button(button_frame, text= "Confirm", command=confirm_command)
    confirm_button.pack(side=tk.LEFT, padx=10, pady=5)

    cancel_button = tk.Button(button_frame, text = "Cancel", command=new_window.destroy)
    cancel_button.pack(side=tk.RIGHT, padx=10, pady=5)

username_var = tk.StringVar
username_label = tk.Label(window, text="Enter your username")
username_label.pack(pady=10)
username_input = tk.Entry(window, textvariable=username_var)
username_input.pack(pady=10)

password_var = tk.StringVar
password_label = tk.Label(window, text="Please enter your Kereberos password")
password_label.pack(pady=10)
password_input = tk.Entry(window, textvariable=password_var)
password_input.pack(pady=10)

alt_password_var = tk.StringVar
alt_password_label = tk.Label(window, text = "Please enter your TACACS password, if different from above.\nWill default to above if empty.") or password_var.get()
alt_password_label.pack(pady=10)
alt_password_input = tk.Entry(window, textvariable=alt_password_var)
alt_password_input.pack()

button_frame = tk.Frame(window)
button_frame.pack(side=tk.BOTTOM, pady=5)

confirm_button = tk.Button(button_frame, text= "Confirm", command=new_window)
confirm_button.pack(side=tk.LEFT, padx=10, pady=5)

cancel_button = tk.Button(button_frame, text = "Cancel", command=window.destroy)
cancel_button.pack(side=tk.RIGHT, padx=10, pady=5)

def file_creation():
    file_content = ""
    file_name = change_number_var.get() + ".txt"
    vlan_number = vlan_number_var.get()
    vlan_name = vlan_name_var.get()
    vlan_description = vlan_description_var.get()
    vlan_gateway = vlan_gateway_var.get()
    vlan_netmask = vlan_netmask_var.get()
    switchport = switchport_var.get()
    primary_dhcp = "To be scripted"
    secondary_dhcp = "To be scripted"
    archive_step = "1. Create configuration backup\ncopy running-config startup-config\nshow archive"
    vlan_configuration_step = f"2. Configure the new VLAN\nconfig t\nvlan {vlan_number}\nname {vlan_name}\nend"
    vlan_interface_step = f"""3. Configure and activate VLAN Interface (Layer 3)
config t
interface vlan {vlan_number}
description {vlan_description}
ip access-group vlan-multi:110:in-default in
ip verify unicast source reachable-via rx allow-default allow-self-ping
ip helper-address  {primary_dhcp}(helper address only needed if DHCP is in use)
ip helper-address  {secondary_dhcp}
no ip redirect
no ip unreachables
no ip proxy-arp
ip  address {vlan_gateway} {vlan_netmask}"""
    multicast_step=f"""4.conf t
interface VLAN {vlan_number}
ip pim sparse-dense-mode
ip pim neighbor-filter 6
ip pim bsr-border
end"""
    vlan_port_step = f"""5. Add the VLAN to requested port 
conf t
int {switchport}
switchport trunk allowed vlan add {vlan_number}
end
"""
    final_step = "copy run start"
    steps = [archive_step,vlan_configuration_step,vlan_interface_step,multicast_step,vlan_port_step,final_step]
    file_content="\n\n".join(steps)
    
    if file_exists(file_name):
        messagebox.showerror("File Already Exists", "A file with the same name already exists.\n\nDelete the file, or check the Change Number.")
    else:
        with open(file_name, "w") as file:
            file.write(file_content)

window.mainloop()
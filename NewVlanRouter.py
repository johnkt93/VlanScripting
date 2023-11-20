import tkinter as tk
import json
import re
from threading import Thread, Lock
from time import sleep
from import_json import *
from ParamikoSSH import *
from tkinter import messagebox

window = tk.Tk()
window.title("Vlan Creation Tool")

routers = ["cumm111-dist-aca01",
    "cumm024-dist-aca03",
    "cumm024-dist-aca04"]

dhcp_servers = []
interface_links = []
hosts = [] 

lock = Lock()

def data(list_type,list_data,lock):
    global hosts
    global interface_links
    with lock:
        if list_type == "hosts":
            local_list = hosts
            local_list.extend(list_data)
            sleep(0.1)
            hosts = local_list
        elif list_type == "interface_links":
            local_list = interface_links
            local_list.extend(list_data)
            sleep(0.1)
            interface_links = local_list
        else:
            messagebox.showerror("Oops","Sorry something went wrong.")

def check_switch():
    try:
        connect(switch_var.get(),username_var.get(),password_var.get(),command="sh cdp ne\n")
        messagebox.showinfo(title=(f'{switch_var.get()}'),message=(f'{output}'))
        print(*output)
    except Exception as e:
        messagebox.showerror(title='Error!', message=e)

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
    
username_var = tk.StringVar()
username_label = tk.Label(window, text="Enter your username")
username_label.pack(pady=10)
username_input = tk.Entry(window, textvariable=username_var)
username_input.pack(pady=10)

password_var = tk.StringVar()
password_label = tk.Label(window, text="Please enter your Kereberos password")
password_label.pack(pady=10)
password_input = tk.Entry(window, textvariable=password_var, show="*")
password_input.pack(pady=10)

alt_password_var = tk.StringVar(value=password_var.get())
alt_password_label = tk.Label(window, text = "Please enter your TACACS password, if different from above.\nWill default to above if empty.") 
alt_password_label.pack(pady=10)
alt_password_input = tk.Entry(window, textvariable=alt_password_var, show="*")
alt_password_input.pack()

button_frame = tk.Frame(window)
button_frame.pack(side=tk.BOTTOM, pady=5)

def new_window():
    new_window = tk.Tk()
    new_window.title("VLAN Creation Tool")
    
    global change_number_var
    global router_var
    global switch_var
    global vlan_number_var
    global vlan_name_var
    global vlan_description_var
    global vlan_gateway_var
    global vlan_netmask_var
    global switchport_var

    #Print the credentials for debugging purposes. DO NOT ENABLE FOR LIVE!
    #print(username_var.get(),password_var.get(),alt_password_var.get())

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
    vlan_netmask_label = tk.Label(text="Enter the subnet mask. Defaults to 255.255.255.0") 
    vlan_netmask_label.pack()
    vlan_netmask_input = tk.Entry(new_window, textvariable=vlan_netmask_var)
    vlan_netmask_input.pack()
    vlan_netmask_input.insert(0,"255.255.255.0")
    vlan_description_var = tk.StringVar()
    vlan_description_label = tk.Label(new_window, text="Enter a brief description for the vlan")
    vlan_description_label.pack()
    vlan_description_label_input = tk.Entry(new_window, textvariable=vlan_description_var)
    vlan_description_label_input.pack()

    multicast_checkbox_var = tk.IntVar()
    multicast_checkbox = tk.Checkbutton(new_window, text="Check if multicast was requested", variable=multicast_checkbox_var)
    multicast_checkbox.pack()

    ssh_thread = Thread(target=connect, args=(switch_var.get(),username_var.get(),password_var.get()))
    ssh_thread.start()
    ssh_thread.join()#Wait for the connection to complete before running the rest of the program
    
    button_frame = tk.Frame(new_window)
    button_frame.pack(side=tk.BOTTOM, pady=5)

    def confirm_command():
        switch_ssh()
        file_creation()
        switch_db()
        #add_switch(switch_var.get(), cdp_neighbors, device_type, ip_address, mac_address)
        #cdp_neighbor()
        sleep(0.1)

    confirm_button = tk.Button(button_frame, text= "Confirm", command=confirm_command)
    confirm_button.pack(side=tk.LEFT, padx=10, pady=5)

    cancel_button = tk.Button(button_frame, text = "Cancel", command=new_window.destroy)
    cancel_button.pack(side=tk.RIGHT, padx=10, pady=5)
    new_window.mainloop()

def nsg_login():
    jumpbox = paramiko.SSHClient()
    #If the host key does not exist in our system, we will add it
    #By default this is set to deny
    jumpbox.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ip_address = "nsg-jump-pr01"
    #Start the SSH connection, with the provided paramaters
    try:
        t1 = jumpbox.connect(hostname=ip_address, username=username_var.get(), password=password_var.get(),port=22)
        print(f'Performing initial log in.\nLogging in as {username_var.get()} on {ip_address}')
        jumpbox.close() #This is just to confirm that the user has access to the system. We'll close the tunnel for now and reopen it when needed.
        l1 = Thread(target=t1)
        l1.start()
        l1.join()
        print('Login Success!')
        window.destroy()
        pass
    except Exception as e:
        sys.stdout.write(str(e))
        messagebox.showerror("nsg-jump-pr01 login failed!","Please check your login credentials, or network connection, and try again.")
        return
    new_window()

confirm_button = tk.Button(button_frame, text= "Confirm", command=nsg_login)
confirm_button.pack(side=tk.LEFT, padx=10, pady=5)

cancel_button = tk.Button(button_frame, text = "Cancel", command=window.destroy)
cancel_button.pack(side=tk.RIGHT, padx=10, pady=5)

def router_ssh():
    #connect(device=router_var.get(),username=username_var.get(), password=alt_password_var.get())
    pass

def switch_ssh():
    try:
        connect(device=switch_var.get(),username=username_var.get(), password=password_var.get())
    except Exception as e:
        messagebox.showerror(title="Error!",message="An error has occured during the connection process\nCheck the switch name, or that ssh is enabled, and the switch is online.")
        sys.stdout.write(str(e))
        return
    
def cdp_neighbor():
    global output
    
    device_entry = ""
    device_name = ""
    platform = ""
    ip_address = ""
    interface=""

    def cdp_connect():
        nonlocal device_entry
        nonlocal device_name
        nonlocal platform
        nonlocal ip_address
        nonlocal interface

        connect_thread = Thread(target=connect(device=switch_var.get(),username=username_var.get(), password=password_var.get(), command="sh cdp ne detail\n")) #actual code
        #print(output)
        connect_thread.start()
        connect_thread.join()
        device_entry = re.split(r"[-]{9,}\n")
        

    thread = Thread(target=cdp_connect)
    thread.start()
    thread.join()
    for device in device_entry:
        device_name = re.findall(r"Device ID:\s+([^\n]+)\.bu\.edu\s+",device)
        platform = re.findall(r"Platform:\s([^,]+)", device)
        ip_address = re.findall(r"IP address:\s+([\d.]+)\s+",device)
        interface = re.findall(r"Interface:\s+([^,]+)",device)
        for device_name, ip_address, interface in zip(device_name, ip_address, interface):
                print("Device Name:", device_name.strip().split(".")[0])
                print("Platform:", platform.strip())
                print("IP Address:", ip_address.strip())
                print("Interface:", interface.strip())
                print()

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
            messagebox.showinfo(title="Completed", message=(f'Change {change_number_var.get()}.txt has been created.'))

window.mainloop()
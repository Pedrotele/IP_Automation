#!/usr/bin/python3

#This script aims to automate the show commands into Network devices

#from multiprocessing import Pool
from getpass import getpass
from netmiko import ConnectHandler
from time import time
from time import sleep
from datetime import date


print("#### Enterprise IP Automation ####")

uname = input("Username: ")      #create variables for username and password
passwd = getpass("Password: ")


#Hosts to be connected
hosts_arista = ['172.30.216.10', '172.30.216.11']
hosts_a10 = ['172.30.216.22', '172.30.216.23']
hosts_cisco = ['172.30.216.16', '172.30.216.17']

# Device Vendors
arista = "arista_eos"
cisco =  "cisco_xr"
a10 = "a10"


#Define Commands below

cmd_arista = ['show logging errors 20', 'show ip ospf neighbor', 'sh ip bgp summary', 'sh ipv6 ospf neighbor | i state', 
'sh ipv6 bgp summary']

cmd_a10 = ['show log | exclude Info', 'show vrrp-a', 'show vcs summary', 'show ip route summary', 'show bgp ipv4 unicast summary', 'show ipv6 route summary', 
'show bgp ipv6 unicast summary']

cmd_cisco = ['show logging events buffer severity-lo-limit warnings last 15', 'show bgp ipv4 unicast summary', 'show bgp ipv6 unicast summary']


#Defining timing
starting_time = time()

#Defining date
date = date.today()


#Netmiko function

def run_script(host_ip, vendor, cmds):
    device = {
        "device_type": vendor,
        "ip": host_ip,
        "username": uname,
        "password": passwd,
        "session_log": str(date)+"_"+vendor+"_"+host_ip+".txt"
        }


    try:
        net_connect = ConnectHandler(**device)            #connect to the device via ssh
   
        print("Connected to host:", vendor, host_ip)

    except:
        print("Connection lost to host:", vendor, host_ip)

    
    for show_commands in cmds:
        output = net_connect.send_command_timing(show_commands, delay_factor=2)
        print("#####", vendor, show_commands, "#####")
        print(output)
        print('\n--- Elapsed time=', time()-starting_time)
        sleep(5)



for ip in hosts_arista:
    run_script(ip, arista, cmd_arista)
    sleep(5)

for ip in hosts_cisco:
    run_script(ip, cisco, cmd_cisco)
    sleep(5)

for ip in hosts_a10:
    run_script(ip, a10, cmd_a10)
    sleep(5)

    
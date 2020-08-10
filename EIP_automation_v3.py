#!/usr/bin/python3


#This script aims to automate the commands into IP Network devices for Sanity Checks, configurations and so on

##########################################
#           STE EIP AUTOMATIONv3         #
#                                        #
# Written by: Pedro Henrique de O Pinto  #
# Email: popi@idirect.net                #
# Copyright (c) 2020                     #
#                                        #
##########################################



#from multiprocessing import Pool
from getpass import getpass
from netmiko import ConnectHandler
from time import time
from time import sleep
from datetime import date
import datetime
import argparse
import sys



#Defining arguments to parse
parser = argparse.ArgumentParser()
parser.add_argument("-V", "--version", help="show program version", action="store_true")
parser.add_argument("-s", "--show", help="Fetch SHOW commands", action="store_true")
parser.add_argument("-c", "--conf", help="Send CONFIG commands", action="store_true")
parser.add_argument("-a", "--arista", help="Run only for Arista devices", action="store_true")
parser.add_argument("-r", "--cisco_xr", help="Run only for Cisco XR devices", action="store_true")
parser.add_argument("-e", "--cisco_xe", help="Run only for Cisco XE devices", action="store_true")
parser.add_argument("-t", "--a10", help="Run only for a10 devices", action="store_true")
parser.add_argument("-n", "--command", required=False, help="Specify single SHOW command to be fetched")
args = parser.parse_args()
send = vars(parser.parse_args())


if args.version:
    print("This is the STE EIP Automation version  3")
    quit()


print("#### STE Enterprise IP Automation ####\n")


# Creating variables for username and password
uname = input("Username: ")
passwd = getpass("Password: ")
secret = getpass("Enable Password (if needed): ")



#Defining timing
starting_time = time()

#Defining date
date = date.today()
hour = datetime.datetime.now().strftime("%X")


#Netmiko function
def run_script(host_ip, vendor, cmds):
    device = {
        "device_type": vendor,
        "ip": host_ip,
        "username": uname,
        "password": passwd,
        "session_log": (str(date)+"_"+str(vendor)+"_"+(str(host_ip)).strip()+"_"+str(hour)+".txt").replace(" ", ""),
        "secret": secret
        }


    try:
        net_connect = ConnectHandler(**device)     #connect to the device via ssh
        

        print("\nConnected to host:", vendor, host_ip)

    except:
        print("\nConnection lost to host:", vendor, host_ip, "Please, check your credentials !!")
        quit()

    try:
        if not net_connect.check_enable_mode():

            connection.enable()
            print("\nAcessing privileged mode")

    except ValueError:
        print("Wrong enable password on device: ", vendor, host_ip)
        quit()

    if args.command:
            output = net_connect.send_command_timing(cmds, delay_factor=2)
            print('\n====>', vendor, host_ip, cmds,'\n')
            print(output)
            print('\n--- Elapsed time=', time()-starting_time)
            sleep(2)
    
    else:
        for commands in cmds:
            if args.show:
                output = net_connect.send_command_timing(commands, delay_factor=2)
                print('\n====>', vendor, host_ip, commands,'\n')
                print(output)
                print('\n--- Elapsed time=', time()-starting_time)
                sleep(2)

            elif args.conf: 
                #output = net_connect.send_config_set(commands)  # If you want to send configuration commands rather than "show commands", please uncomment this line 
                print('\n====>', vendor, host_ip, commands,'\n')
                print(output)
                print('\n--- Elapsed time=', time()-starting_time)
                sleep(2)


#Running function for each device


if (args.arista and args.show)  or (args.arista and args.conf) or (args.arista and args.cisco_xr and args.show) or (args.arista and args.cisco_xe and args.show):
    hosts_arista = open('arista.txt').readlines()
    cmd_arista = open('arista_cmd.txt').readlines()
    arista = "arista_eos"
    for ip in hosts_arista:
        run_script(ip, arista, cmd_arista)
        sleep(2)

if (args.a10 and args.show)  or (args.a10 and args.conf) or (args.a10 and args.arista and args.cisco_xr and args.show) or (args.a10 and args.arista and args.cisco_xe and args.show):
    hosts_a10 = open('a10.txt').readlines()
    cmd_a10 = open('a10_cmd.txt').readlines()
    a10 = "a10"
    for ip in hosts_a10:
        run_script(ip, a10, cmd_a10)
        sleep(2)

if (args.cisco_xr and args.show) or (args.cisco_xr and args.conf) or (args.a10 and args.arista and args.cisco_xr and args.show) or (args.a10 and args.arista and args.cisco_xr and args.cisco_xe and args.show):
    hosts_cisco_xr = open('cisco_xr.txt').readlines()
    cmd_cisco_xr = open('cisco_cmd_xr.txt').readlines()
    cisco_xr =  "cisco_xr"
    for ip in hosts_cisco_xr:
        run_script(ip, cisco_xr, cmd_cisco_xr)
        sleep(2)

if (args.cisco_xe and args.show) or (args.cisco_xe and args.conf) or (args.cisco_xe and args.arista and args.show) or (args.a10 and args.arista and args.cisco_xe and args.show) or (args.a10 and args.arista and args.cisco_xe and args.cisco_xr and args.show):
    hosts_cisco_xe = open('cisco_xe.txt').readlines()
    cmd_cisco_xe = open('cisco_cmd_xe.txt').readlines()
    cisco_xe =  "cisco_xe"
    for ip in hosts_cisco_xe:
        run_script(ip, cisco_xe, cmd_cisco_xe)
        sleep(2)

if args.command:

    if args.arista:
        hosts_arista = open('arista.txt').readlines()
        arista = "arista_eos"
        for ip in hosts_arista:
            run_script(ip, arista, str(send["command"]))
            sleep(2)
    elif args.a10:
        hosts_a10 = open('a10.txt').readlines()
        cmd_a10 = open('a10_cmd.txt').readlines()
        a10 = "a10"
        for ip in hosts_a10:
            run_script(ip, a10, str(send["command"]))
            sleep(2)

    elif args.cisco_xr:
        hosts_cisco_xr = open('cisco_xr.txt').readlines()
        cmd_cisco_xr = open('cisco_cmd_xr.txt').readlines()
        cisco_xr =  "cisco_xr"
        for ip in hosts_cisco_xr:
            run_script(ip, cisco_xr, str(send["command"]))
            sleep(2)
    
    elif args.cisco_xe:
        hosts_cisco_xe = open('cisco_xe.txt').readlines()
        cmd_cisco_xe = open('cisco_cmd_xe.txt').readlines()
        cisco_xe =  "cisco_xe"
        for ip in hosts_cisco_xe:
            run_script(ip, cisco_xe, str(send["command"]))
            sleep(2)

print("#### The EIP Automation program is over ####")
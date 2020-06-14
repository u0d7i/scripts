#!/usr/bin/env python3

from pathlib import Path
from csv import reader
from random import randrange
from stdnum import luhn
import argparse

tac_file = 'tac.csv'
tac_url = 'http://tacdb.osmocom.org/export/tacdb.csv'

def check_tacfile():
    if (not Path(tac_file).exists()):
        print('TAC file',tac_file,'does not exist, use -u to download it')
        quit()

def is_root():
    import os
    return os.geteuid() == 0

def do_update():
    print('Updating', tac_file,'downloading from',tac_url)
    import urllib.request
    urllib.request.urlretrieve (tac_url, tac_file)

def do_random():
    IMEI0 = f'{randrange(99999999999999):014}'
    CD = luhn.calc_check_digit(IMEI0)
    IMEI = IMEI0 + CD
    print(IMEI,'- random')

def do_tac():
    check_tacfile()
    tac_list=read_tacfile()
    TAC=tac_list[0]
    SN = f'{randrange(999999):06}'
    IMEI0 = TAC + SN
    CD = luhn.calc_check_digit(IMEI0)
    IMEI = IMEI0 + CD
    print(IMEI,'-',tac_list[1],tac_list[2])

def do_factory():
    get_serial_nr()
    serial_port = get_serial_port()
    print('Not implemented yet')

def parse_args():
    parser = argparse.ArgumentParser(description='Set IMEI (education purposes only)')
    parser.add_argument('-s','--set',action='store_true', help='Actually set (default is print)')
    parser.add_argument('-q','--quiet',action='store_true', help='Be quiet')
    parser.add_argument('-f','--file',action='store', help='TAC file')
    parser.add_argument('-d','--dev',action='store', help='Modem device')
    gr_req = parser.add_mutually_exclusive_group(required=True)
    gr_req.add_argument('-r','--random',action='store_true', help="Random IMEI")
    gr_req.add_argument('-t','--tac',action='store_true', help="Random real TAC IMEI")
    gr_req.add_argument('-F','--factory',action='store_true', help="Factory IMEI (based on serial)")
    gr_req.add_argument('-T','--targ',action='store', help="IMEI based on string, TAC or part")
    gr_req.add_argument('-u','--update',action='store_true', help="Update TAC file")
    
    args = parser.parse_args()
    if not vars(args):
        parser.print_help()
        parser.exit(1)
    return args

def read_tacfile():
    with open(tac_file,'r') as file:
        csv_reader = reader(file, delimiter=',')
        csv_data = list(csv_reader)
        row_count = len(csv_data)
        tac_list=csv_data[randrange(2,row_count)]
    return tac_list

def get_serial_nr():
    if (not is_root()):
        print("- You are not root")
        quit()
    import usb
    dev = usb.core.find(idProduct=0x68a2)
    try:
        serial_nr = usb.util.get_string( dev, dev.iSerialNumber )
    except:
        print("- Can't get modem serial number")
        quit()
    print('Serial nr:',serial_nr)
    return serial_nr

def get_serial_port():
    import serial
    import serial.tools.list_ports
    serial_port = ""
    for port in serial.tools.list_ports.comports():
        if port.vid == 0x1199 and int(port.location[-1:]) == 3:
            serial_port = port.device
    if serial_port == "":
        print("- Modem is not connected")
        quit()
    print("Modem serial port:",serial_port)
    ser = serial.Serial(port=serial_port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1)
    ser.write(b"AT+CGSN \r")
    info = readreply(ser)
    print(info)
    ser.write(b"AT+CIMI  \r")
    info = readreply(ser)
    print(info)
    #return serial_port

def readreply(ser):
    info=[]
    while (True):
        tmp=ser.readline().decode('utf-8').replace('\r','').replace('\n','')
        if ("OK" in info):
            return info
        elif ("ERROR" in info) or info=="":
            return -1
        info.append(tmp)
    return info

args=parse_args()
# remove this after cleanup
# print(args)

if args.file:
    tac_file=args.file

if args.update:
    do_update()

if args.random:
    do_random()

if args.tac:
    do_tac()

if args.factory:
    do_factory()

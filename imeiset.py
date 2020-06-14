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

def do_update():
    print('Updating', tac_file,'downloading from',tac_url)
    import urllib.request
    urllib.request.urlretrieve (tac_url, tac_file)

def parse_args():
    parser = argparse.ArgumentParser(description='Set IMEI (education purposes only)')
    parser.add_argument('-s','--set',action='store_true', help='Actually set (default is print)')
    parser.add_argument('-f','--file',action='store', help='TAC file')
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

parse_args()
# remove this after cleanup
print(args)

if args.file:
    tac_file=args.file

if args.update:
    do_update()

if args.tac:
    check_tacfile()
    print('tacfile exists')

# cleanup below this line
quit()

with open(tac_file,'r') as file:
    csv_reader = reader(file, delimiter=',')
    csv_data = list(csv_reader)
    row_count = len(csv_data)
    tac_list=csv_data[randrange(2,row_count)]

TAC=tac_list[0]
SN = f'{randrange(999999):06}'
IMEI0 = TAC + SN
CD = luhn.calc_check_digit(IMEI0)
IMEI = IMEI0 + CD
print(IMEI,'-',tac_list[1],tac_list[2])

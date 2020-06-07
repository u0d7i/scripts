#!/usr/bin/env python3

from pathlib import Path
from csv import reader
from random import randrange
from stdnum import luhn
import argparse

tac_file = 'tac.csv'
tac_url = 'http://tacdb.osmocom.org/export/tacdb.csv'

parser = argparse.ArgumentParser(description='Set IMEI (education purposes only)')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-r','--random',action='store_true', help="Random IMEI")

args = parser.parse_args()
if not vars(args):
    parser.print_help()
    parser.exit(1)

if (not Path(tac_file).exists()):
    print(tac_file,'does not exist, downloading from',tac_url)
    import urllib.request
    urllib.request.urlretrieve (tac_url, tac_file)

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

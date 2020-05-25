#!/usr/bin/python3

from random import randrange
from stdnum import luhn

TAC = f'{randrange(1020100,99999999):08}' # fix for real TACs later
SN = f'{randrange(999999):06}'
IMEI0 = TAC + SN
CD = luhn.calc_check_digit(IMEI0)
IMEI = IMEI0 + CD
print(IMEI)

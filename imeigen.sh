#!/bin/bash
# Generate valid IMEI

luhn_checksum() {
  # courtesy ethertubes.com
  # https://ethertubes.com/bash-luhn/
  sequence="$1"
  sequence="${sequence//[^0-9]}" # numbers only plz
  checksum=0
  table=(0 2 4 6 8 1 3 5 7 9)

  # Quicker to work with even number of digits
  # prepend a "0" to sequence if uneven
  i=${#sequence}
  if [ $(($i % 2)) -ne 0 ]; then
    sequence="0$sequence"
    ((++i))
  fi
  
  while [ $i -ne 0 ];
  do
    # sum up the individual digits, do extra stuff w/every other digit
    checksum="$(($checksum + ${sequence:$((i - 1)):1}))" # Last digit
    # for every other digit, double the value before adding the digit
    # if the doubled value is over 9, subtract 9
    checksum="$(($checksum + ${table[${sequence:$((i - 2)):1}]}))" # Second to last digit
    i=$((i - 2))
  done
  checksum="$(($checksum % 10))" # mod 10 the sum to get single digit checksum
  echo "$checksum"
}

FN="tac.csv"
URL="http://www.mulliner.org/tacdb/feed/contrib/tacdb_210114.csv"
if [ ! -f ${FN} ]; then
  wget -c -O ${FN} "$URL"
fi
LINE=$(sed -n "$(shuf -i 1-$(wc -l ${FN} | cut -d" " -f1) -n 1)p" ${FN})
#echo $LINE
TAC=$(echo $LINE | cut -d, -f1)
IMEI0="${TAC}$(printf %06d $(shuf -i 0-999999 -n 1))"
IMEI="$IMEI0$(luhn_checksum $IMEI0)"
echo $IMEI


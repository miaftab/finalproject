#!/usr/bin/env bash

numTotalindex=0;
dateindex=0;
provinceindex=0;

var=$(cat covid19.csv | head -n 1 | tr ',' ' ')
echo $var
for colNames in $var
do
 if [ "numtotal" = $colNames ]
 then
   echo $colNames
   echo $numTotalindex
   break
 fi
 numTotalindex=$((numTotalindex+1))
done

for colNames in $var
do
 if [ "date" = $colNames ]
 then
   echo $colNames
   echo $dateindex
   break
 fi
 dateindex=$((dateindex+1))
done

for colNames in $var
do
 if [ "prname" = $colNames ]
 then
   echo $colNames
   echo $provinceindex
   break
 fi
 provinceindex=$((provinceindex+1))
done


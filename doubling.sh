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

convertDate()
{
  var=$(echo $1 | tr "-" " " )
  arr=($var)
  d1=${arr[2]}"-"${arr[1]}"-"${arr[0]}
  echo "$d1"
}

# Find Doubling Rate For Number Of Cases
if [ "$2" = "number of cases" ]
then
   doublingRate=0
   noOfdays=0
   arr=''
   echo "number of cases"
   numberOfCsvRows=$(cat covid19.csv  | wc -l)
   for((i=2;i<=numberOfCsvRows;i++))
   do
     var=$(cat covid19.csv | head -n "$i" | tail -n 1 | tr ',' ' ')
     arr=($var)
     d1=$(convertDate ${arr[dateindex]})
     d2=$(convertDate "$3")
     if [ "$1" = ${arr[provinceindex]} ] && [ "$d1" ">" "$d2" ]
     then
       #echo $d1
       #echo $d2
       echo $var
       if [ ${arr[numTotalindex]} -gt "$doublingRate" ]
       then
         noOfdays=$((noOfdays+1))
         break
       else
        noOfdays=$((noOfdays+1))
       fi
     elif [ "$1" = ${arr[provinceindex]} ] && [ "$d1" "=" "$d2" ]
     then
      doublingRate=$((${arr[numTotalindex]} * 2))
      echo $doublingRate
     fi
   done

   echo 'No Of Days = '$noOfdays
   echo $1 $3 $(($doublingRate / 2)) ${arr[dateindex]} ${arr[numTotalindex]} $noOfdays  >> output.txt

else
   echo "number of deaths"
fi
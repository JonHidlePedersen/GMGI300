#!/bin/bash
# Simulerer GPS-tracking for løypemaskin ut fra tekstfil med
# posisjoner og tid.  Eksempel på linje fra tekstfila:
#    59.9655674;10.0395497;2010-02-21 18:55:55+00
# Parametre: 
#   speedup - heltall >1 -> raskere enn "ekte" tid.
#   starttime - standard tekststreng med dato og tid - "2011-02-03 13:33:10+01"

file=preppemaskin_aas_2010_01-03.txt
speedup=$1
starttid=$2
step=60 #simulation step in seconds
psql -U postgres -d gmgi300db -p 5433 -w -c "CREATE TABLE skispor ((id SERIAL PRIMARY KEY, enhet VARCHAR(10), tid TIMESTAMP WITH TIME ZONE);" > /dev/null 2>&1
psql -U postgres -d gmgi300db -p 5433 -w -c "SELECT AddGeometryColumn('skispor','sted',4326,'POINT',2);" > /dev/null 2>&1
psql -U postgres -d gmgi300db -p 5433 -w -c "DELETE FROM skispor;" > /dev/null 2>&1
psql -U postgres -d gmgi300db -p 5433 -w -c "CREATE TABLE skisporsimtid ((id SERIAL PRIMARY KEY, tid TIMESTAMP WITH TIME ZONE);" > /dev/null 2>&1
psql -U postgres -d gmgi300db -p 5433 -w -c "DELETE FROM skisporsimtid;" > /dev/null 2>&1
echo "Starter $2 - hastighetsfaktor: $1"
tac $file | dos2unix | (
    IFS=';' read nord ost tid
    while [[ "$tid" < "$starttid" ]]
    do
      IFS=';' read nord ost tid
    done
    echo "Foerste tid: $tid"
    psql -U postgres -d gmgi300db -p 5433 -w -c "INSERT INTO skispor (enhet, tid, sted) VALUES ('aas', '$tid', ST_GeometryFromText('POINT($ost $nord)',4326))"
    psql -U postgres -d gmgi300db -p 5433 -w -c "INSERT INTO skisporsimtid (tid) VALUES ('$tid')"
    while test "$nord" != ""
    do
      current=$(date -u -d "$tid" +%s)  # time in seconds since 1970...
      if [ "$prev" != "" ]
      then
        rounding=1000000  # for avrunding av desimalene til 5 siffer
        diff=$(($current-$prev))
        tida=$prev;
        while [[ $diff -gt $step ]]
        do
          tida=$(($tida+$step))
          diff=$(($diff-$step))
          bigstep=$(($step*$rounding/$speedup))
          bigstepint=$(($bigstep/$rounding))
          bigstepdec=$(($bigstep-$bigstepint*$rounding))
          newstep2=$(printf %d.%6d $bigstepint $bigstepdec)
          newstep=${newstep2// /0}
          sleep $newstep
          nytid=$(date -u --date=@$tida +"%Y-%m-%d %T%:::z")
          psql -U postgres -d gmgi300db -p 5433 -w -c "UPDATE skisporsimtid set tid = '$nytid'" > /dev/null 2>&1
        done
        bigdiff=$(($diff*$rounding/$speedup))
        newdiffint=$(($bigdiff/$rounding))
        bigdiffdec=$(($bigdiff-$newdiffint*$rounding))
        newdiff2=$(printf %d.%6d $newdiffint $bigdiffdec)
        newdiff3=${newdiff2// /0}
        newdiff=$newdiff3
        sleep $newdiff
        psql -U postgres -d gmgi300db -p 5433 -w -c "INSERT INTO skispor (enhet, tid, sted) VALUES ('aas', '$tid', ST_GeometryFromText('POINT($ost $nord)',4326))" > /dev/null 2>&1
        psql -U postgres -d gmgi300db -p 5433 -w -c "UPDATE skisporsimtid set tid = '$tid'"  > /dev/null 2>&1
      fi
      IFS=';' read nord ost tid
      prev=$current
    done        
    )
exit 0

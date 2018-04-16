#! /bin/bash 
# Realitzat per: David Lopez, Albert Blasco
# 11/04/2018
#Aquest script s'encarrega de crear un nombre de procesos pasats per parametre indicant si volem realitzar un countwords o un wordcount seguit del fitxer a comptar i el nombre de cops que s'ha de copiar el fitxer determinat. 

if [ "$1" = "-h" ]
then 
	echo "Aquest script s'encarrega de crear un nombre de procesos pasats per parametre indicant si volem realitzar un countwords o un wordcount seguit del fitxer a comptar i el nombre de cops que s'ha de copiar el fitxer determinat."
	echo "	starter [nProcesos][OPCIO][fitxer][nCopsFitxer*]"
	echo "OPCIONS"
	echo "	-w	MapReduce/WordCount	- compta el total de cada paraula"
	echo "	-c	MapReduce/CountWords 	- compta el total de cada paraula"
	exit 1

elif [ $# -lt 3 ]
then
	echo 'ERROR: No hi ha suficients arguments' >&2
	exit 1
	
fi

kill -9 $(ps -a | grep python | cut -f2 -d ' ') #Matem els mappers de altres  execucions
kill -9 $(ps -a | grep python | cut -f1 -d ' ') #Matem els mappers de altres  execucions de pid >10000

#Multipliquem el document el nombre de cops indicat per parametre
if [ $# -lt 4 ]
then 		#Si no indiquem el nombre de multiplicacions l'hagafem buit

	cat $3 > temp_multi
else
	echo Creant fitxer multiplicat:
	for x in $(seq $4)
	do
		echo Creant fitxer multiplicat $x" out of "$4
		cat $3 >> temp_multi 
	done
	
fi

echo Dividint fitxer en $1 parts
split -n $1 temp_multi "temp_file_"

m=0

ls | grep temp_file_ > temp_py

if [ "$2" = "-w" ]
then
	python mapReduce.py $1 temp_py w
elif [ "$2" = "-c" ]
then
	python mapReduce.py $1 temp_py c
else
	echo Introdueix una opcio 2 valida
fi

rm temp_*



	

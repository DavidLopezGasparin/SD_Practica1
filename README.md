En aquest readme separem i descrivim les diferents parts del nostre projecte.
- Script Principal (starter.sh)
  - S'encarrega de matar els processos anteriors que puguin estar utilitzant els mateixos ports
  - Multiplica el fitxer depenent del nombre que li passem per paràmetre
  - Divideix la feina del fitxer entre els diferents processos
  - Executa el mapReduce depenent dels paràmetres que li passem
  - Per tal de coneixer els detalls d'execució cal fer la crida: "starter.sh -h"
- Spawn (spawn.py)
  - Fitxer que s'encarrega de crear els hosts en els quals carregarem la feina a fer.

- MapReduce (mapReduce.py)
  - CountingWords
    - Compta el nombre total de paraules que hi han en un arxiu
  - WordCount
    - Compta el nombre total de vegades que apareix cada paraula en un document


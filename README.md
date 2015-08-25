#Weatherstation
##Overview
Python2, Bash, Tinkerforge

## Setup

1. Pfade, Urls und Benutzer in `ftpconfig.xml` anpassen (Vorlage: ftpconfig.sample.xml)
2. `settings.py` anpassen
	1. brickd-host und Port
	2. Verwendete Sensoren in *SENSORS* anpassen
		* Name
		* UID
		* SensorTyp
	3. Gewünschte Callback-zeiten in *TIMES* anpassen
3. Tinkerforge-python-bindings installieren
4. `main.py` starten, um Aufzeichnung zu starten
	* Aufzeichnung des aktuellen Tages werden in `records` gespeichert
	* (ftp.sh bzw move.py) Nach dem Upload und dem Tagesende werden die Aufzeichnungen nach `arch` verschoben
5. Cronjob für Upload mit ftp.sh einrichten

# TODOS
* auf python3 umstellen
* settings aus python auslagern

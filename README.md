#Weatherstation
##Overview
Python, Bash, Tinkerforge

## Setup

1. Pfade, Urls und Benutzer in `ftp.sh` anpassen
2. `settings.py` anpassen
	1. brickd-host und Port
	2. Verwendete Sensoren in *SENSORS* anpassen
		* Name
		* UID
		* SensorTyp
	3. Gewünschte Callback-zeiten in *TIMES* anpassen
3. Tinkerforge-python-bindings installieren
4. `all.py` starten, um Aufzeichnung zu starten
	* Aufzeichnung des aktuellen Tages werden in `records` gespeichert
	* Nach dem Upload und dem Tagesende werden die Aufzeichnungen nach `arch` verschoben
5. Cronjob für Upload mit ftp.sh einrichten

#Weatherstation
##Overview
Python (2/3), Bash, Tinkerforge

## Setup

1. Konfiguration mittels `config.json` anpassen (Vorlage: `config.sample.json`)
	* Notwendig:
		* *hosts*:
			* Ein Eintrag pro brickd-Host mit:
				* *host*: Hostname/IP + Port 
				* *sensors*: Auflistung der Sensoren mit: Name, UID, SensorType
		* *sensor_properties*:
			* Pro SensorType:
				* Callbackzeit
				* Divisor
				* Einheit
	* Optional:
		* *tempmaxdiff*: Maximaler Unterschied zwischen zwei *SensorType.temp*-Callbacks des gleichen Sensors
		* *prev_temps_default*: Hilfswert für Berechnung von *tempmaxdiff*
		* *logs*: Ordner für Logs
		* *locks*: Ordner für Locks
		* *records*: Ordner für aktuelle Aufzeichnungen
		* *arch*: Ordner für Archiv der Aufzeichnungen
		* *lockname*: Lock für Hauptprogramm
		* *logname*: Logdatei für Hauptprogramm
		* *exceptionlog*: Logdatei für Exceptions bei Verbindungsaufbau
		* *recordlog*: Logdatei für neue, einheitliche Aufzeichnungen
		* *movelog*: Logdatei für Archivierung
		* *movelock*: Datei zur Feststellung der letzten Archivierung
		* *waitDelay*: Wartezeit zwischen Verbindungsversuchen
		* *loglevel*: Loglevel für Hauptprogramm
		* *datalog*: Loglevel für Aufzeichnungen (warn, error,critical verhindern Aufzeichnung)
		* *dataecho*: Loglevel für Wiedergabe der Aufzeichnungen (warn, error,critical verhindern Wiedergabe)
		* *legacy_record*: Speichern von Aufzeichnungen in einzelne Dateien pro Sensor (true, false)
2. Tinkerforge-Python-Bindings installieren
3. `main.py` starten, um Aufzeichnung zu starten
	* Aufzeichnung des aktuellen Tages werden in *records* gespeichert

Optional: Verschieben der Aufzeichnungen in ein Archiv:

4. `move.py` z.B. als Cronjob starten

Optional: Upload der Aufzeichnungen mit SFTP an einem Server (beinhaltet Archivierung mit `move.py`):

5. Pfade, Urls und Benutzer in `ftpconfig.xml` anpassen (Vorlage: `ftpconfig.sample.xml`)
	* (ftp.sh bzw move.py) Nach dem Upload und dem Tagesende werden die Aufzeichnungen nach `arch` verschoben
6. Cronjob für Upload mit `ftp.sh` einrichten

# TODOS
* TODOS ausdenken
* rugged approach [http://www.tinkerforge.com/en/doc/Tutorials/Tutorial_Rugged/Tutorial.html](http://www.tinkerforge.com/en/doc/Tutorials/Tutorial_Rugged/Tutorial.html)
* ftp.sh:
	* remote-pfad in xml (ftp)

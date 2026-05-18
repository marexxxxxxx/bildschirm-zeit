# bildschirm-zeit
## Beschreibung
Ein Bildschirmzeit-App im Apple Style. Fokus hierbei liegt auf einem System welches unter Linux Arch Funktionsfähig ist. 
## Technologie Stack
Für das Forntend wird reines GTK4 verwendet. 
Das Backend besteht aus Python (mit uv,venv) und einer sql lite datenbank.
## Phase0
Init der Tabellen:
- Tabelle Logo:
  - Hat die Spalten: (Logo_id: Serial Primary Key, Logo_name: sting, path_to_log: string)
- Tabelle Apps: (App_id: Primary Key, Fenster_name: string, App_name: string, Logo_id: Foreign Key, productivitaet: Foreign Key)
- Tabelle Produktivitaet(productiviteat: Primary Key, is_productiv: boolean)
- Tabelle Tagesverbrauch:
  - Hat die Spalten: (ID_aktion: Serial Primary Key, aktuellesDatum: date, uhrzeit_start: time, uhrzeit_ende:time, App_id: Foreign Key) Hierbei ist ID_aktion einfach der Primary Key für die aktion, aktuellesDatum sagt aus an welchem Tag der Zugriff erfolgte, uhrzeit_start wann die aktion beginn, und uhrzeit_ende bis wann diese ging. window bennent das fenster das geöffnet war z.b. chrome oder vs code wohingegen tab für das geöffnete Projekt oder den Tab steht. Die Logo ID ist hierfür zuständig falls es die Möglichkeit gibt das logo einer App anzuzeigen soll hier zugeordnet werden welches logo das ist und wie die zusammen gehören  
Init der Geschäftsregeln. Erstelle mir einen Python Code welcher folgende Geschäftslogiken abbilden kann:
- Erstelle mir dafür folgende Ports und Adapter:
  - Abrufen der aktuellen Uhrzeit und Datum
  - Abrufen der Bildschirmzeit des aktuellen Tages. Dafür wird die aktuelle Uhrzeit und Datum verwendet
  - Abrufen des aktuellen Logos + hinzufügen zur Datenbank + download in vorhergesehen ordner dafür
  - Adapter für Änderungen von Fokus bei Apps. -> wenn fokus ändert wird ausgelöst (realsierbar mit hyprctl -j activewindow)
  - Adapter für Auschalt- oder ABmeldeerkennung
  - Adapter zum hinzufügen von Productivität also in der Tabelle und zu apps
  - Adapter zum herrausfinden wie lange man an Apps war die als productiv gekenzeichnet wurden und an wie vielen unproduktiven man gesessen hat
- Addierung der Bildschirmzeit um die aktuelle gesamtbildschirmzeit herrauszufinden
- Vergleich ob zu App bereits ein Logo exestiert oder nicht -> falls kein Logo exestiert muss Adapter hizufügen zur datenbank genutzt werden mit download, ansonten wird der wert von 
- Nutzte Adapter für Änderungen am Fokus um die Start und Endzeit von Fenstern und Apps zu erkennen
- Nutzte Adapter für Auschalt -und Abmeldeerkennung um das pausieren einer app festzustellen
  

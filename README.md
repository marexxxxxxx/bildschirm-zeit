# bildschirm-zeit
## Beschreibung
Ein Bildschirmzeit-App im Apple Style. Fokus hierbei liegt auf einem System welches unter Linux Arch Funktionsfähig ist. 
## Technologie Stack
Für das Forntend wird reines GTK4 verwendet. 
Das Backend besteht aus Python (mit uv,venv) und einer sql lite datenbank.
nutzte die schnitstelle hyperland sockets um die events mit dem bildschirmändern mitzubekommen


### Phase 0
Schaue dir pahse 1 an und baue dir grundlagen, also mit uv etc, eine ordner struktur mit einem gesunden naming gitignore und alles was dazugehört. Du gehst in die rolle eines entwickler der alles vorbeireitet damit dannach reibungslos entwickelt werden kann. also lege auch fest welche versionen von was verwendet werden
### Phase 1
Init Table: 
Aktionen(AktionsID: Serial Primary Key, Datum: date Beginn_Aktion: float, Ende_Aktion: float, AppID: Foreign Key (AppID))
App(AppID: Serial Primary Key, name_fenster: string, name_tab: string)

Ports:
Get_current_time() // Aktuelle Uhrzeit
Get_current_date() // Aktuelles Datum
Change_of_focus() // Wenn sich der aktuelle Fokus des Fensters ändert, wird das ausgelöst
Write_Aktion() // schreibt den Inhalt von Aktion  nieder
register_app() // legt einen Eintrag für eine app in der tabelle app an()
is_app_registered() // findet herraus ob die zu niederschreibende App schon in der Datenbank steht, falls nicht  wird mithilfe von register_app() etwas angelegt
get_daytime_of() // gibt die Bildschirmzeit von einer spezifischen app zurück
get_all_daytime() gibt die gesamte Bildschirmzeit des Tages zurück
fenster_fokus() wird ausgelöst wenn sich das fenster ändert

Adapter:
Get_current_time() -> verwendet die aktuelle systemzeit
Get_current_date() -> verwendet das aktuelle systemdatum
Change_of_focus() -> nutzt hyperlandsocket um über fenster veränderungen informiert zu werden
Write_Aktion() -> schreibt den inhalt einer AKtion also von bis in eine Tabelle mit dem app namen
register_app() -> erstellt einen app eintrag in der sql tabelle app
is_app_registered() returnt true oder false ob es den eintrag schon gibt von der app oder nciht
get_daytime_of() nutzt einen sql befehl um die bildschirmzeit einer app zurückgegeben zu bekommen
get_all_daytime() ntutzt einen sql befehl und sumiert alle verwendeteten apps auf um herrauszufinden wie viel man wirklcih am laptop war

Geschäftslogik:
Wenn sich der Fenster Fokus verändert wird der akteulle Timestem und datum notiert bei dem sich der Fenster fokus verschoben hat, sowie welche app das war es wird write aktion ausgeführt. 
Prüfe ob die app die verwendet wird registriert ist wenn nein, lege sie an
bei chrome oder anderen browsern soll nciht nur dastehen chrome sondern welchen tab man offen hatte, also youtbe, google gemini ...
bei vs code oder anderen editoren soll nciht nur vs code stehen sondern auch das aktuelle Projekt

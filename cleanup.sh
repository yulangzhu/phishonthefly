#!/bin/bash

# Verifica si el script s'executa com root
if [ "$(id -u)" != "0" ]; then
   echo "Aquest script ha de ser executar amb permisos de superusuari!" 
   exit 1
fi

# Atura el servidor d'Apache
echo "Aturant Apache..."
service apache2 stop

# Desactiva el lloc web de phishonthefly
echo "Desactivant el lloc web phishonthefly..."
a2dissite phishonthefly.conf

# Restaura l'arxiu /etc/apache2/ports.conf desde el backup
echo "Restaurant /etc/apache2/ports.conf ..."
if [ -f /etc/apache2/ports.conf.bak ]; then
    mv /etc/apache2/ports.conf.bak /etc/apache2/ports.conf
    echo "/etc/apache2/ports.conf ha estat restaurat."
else
    echo "Backup de /etc/apache2/ports.conf no trobat. La restauració no es posible."
fi

# Elimina el directori del lloc web i els arxius
echo "Eliminant el directori del lloc web i els seus arxius..."
rm -rf /var/www/phishonthefly

# Elimina l'arxiu de configuració del VirtualHost
echo "Eliminant l'arxiu de configuració del VirtualHost..."
rm -f /etc/apache2/sites-available/phishonthefly.conf

# Elimina els registres d'Apache
echo "Eliminant els registres d'Apache..."
rm -f /var/log/apache2/access.log
rm -f /var/log/apache2/error.log

# Neteja l'historial de comandes de l'usuari actual
echo "Netejant l'historial de comandes..."
history -c
history -w

# Neteja l'historial de comandes de la shell bash de root
if [ -f /root/.bash_history ]; then
    echo "Eliminant l'historial de comandes de root..."
    > /root/.bash_history
fi

# Neteja els logs del sistema (syslog, kern.log, auth.log...)
echo "Eliminant els logs del sistema..."
find /var/log -type f -exec truncate -s 0 {} \;

# Recarrega la configuración d'Apache
echo "Recarregant la configuració d'Apache..."
service apache2 restart

echo "Neteja completada!"

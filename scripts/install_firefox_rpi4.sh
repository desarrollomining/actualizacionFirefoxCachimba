#!/bin/bash
set -e

echo "🔧 Actualizando sistema..."
sudo apt update && sudo apt upgrade -y
sudo apt install curl wget gnupg apt-transport-https flatpak -y

echo "➕ Agregando Flathub..."
sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

echo "🦊 Instalando Firefox (Flatpak)..."
sudo flatpak install -y flathub org.mozilla.firefox

echo "🎞️ Instalando codecs ffmpeg-full..."
sudo flatpak install -y flathub org.freedesktop.Platform.ffmpeg-full//24.08

echo "✅ Instalación completada. Puede ejecutar con:"
echo "flatpak run org.mozilla.firefox"


echo "📁 Reemplazando __main__.py en /home/pi/display..."

# Reemplaza el archivo __main__.py
cp /home/pi/scripts/__main__.py /home/pi/display/__main__.py

# Otorga permisos de ejecución por si es necesario
chmod +x /home/pi/display/__main__.py

echo "🟢 __main__.py reemplazado correctamente."


echo "🗑️ Eliminando Firefox ESR si existe..."
sudo apt purge -y firefox-esr || true
sudo apt autoremove -y


echo "🧽 Limpiando configuración anterior de Firefox..."
rm -rf ~/.var/app/org.mozilla.firefox


echo "♻️ Reiniciando sistema en 3 segundos..."
sleep 3
sudo reboot

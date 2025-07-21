# 🦊 Actualización de Firefox en Raspberry Pi 4 (Modo Kiosk)

Este repositorio contiene los archivos necesarios para instalar **Firefox (Flatpak)** en una Raspberry Pi 4, reemplazar el archivo principal `__main__.py` y configurar el entorno para funcionamiento en modo kiosco.

---

## 📁 Carpeta `scripts/`

Dentro de la carpeta [`scripts`](https://github.com/desarrollomining/actualizacionFirefoxCachimba/tree/main/scripts) encontrarás:

- `__main__.py`: script principal que será copiado a `/home/pi/display/`.
- `install_firefox_rpi4.sh`: instalador automatizado que ejecuta todos los pasos necesarios.

---

## 📌 Instrucciones de uso

1. Copiar la carpeta `scripts` al dispositivo Raspberry Pi:

   Si estás en otro computador:

   ```bash
   scp -r scripts/ pi@tablet:/home/pi/

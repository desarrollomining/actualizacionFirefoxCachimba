import subprocess
import socket
import time
import urllib.request
import os
import glob
import json

# Identificacion del equipo
ID = subprocess.check_output(['machineid'])[:-1].decode('utf-8')
NAME = subprocess.check_output(['machinename'])[:-1].decode('utf-8')
print(ID)
print(NAME)
 
# Data to be written
dictionary ={
    "status":""
}
 

def addJson(data):
    dictionary['status'] = data
    
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)
 
    # Writing to sample.json
    with open("/home/pi/display/data.json", "w") as outfile:
        outfile.write(json_object)
    time.sleep(2)


def cleanCache():
    try:
        process = subprocess.Popen(['rm','-rf','/home/pi/.cache/chromium/Default'])
        process = subprocess.Popen(['rm','-rf','/home/pi/.config/chromium/Default/Login\ Data'])
        process = subprocess.Popen(['rm','-rf','/home/pi/.config/chromium//Default/Cookies'])
        process = subprocess.Popen(['rm','-rf','/home/pi/.config/chromium//Default/History'])
        process = subprocess.Popen(['rm','-rf','/home/pi/.config/chromium//Default/Web\ Data'])
        perfiles = glob.glob('/home/pi/.var/app/org.mozilla.firefox/cache/mozilla/firefox/*/cache2')
        for ruta in perfiles:
            subprocess.Popen(['rm', '-rf', ruta])
        print("Cache borrado")
    except:
        print("Error al eliminar el cache")


def checkPingMmr():
    address = "raspberrypi.local" 
    res = subprocess.call(['ping', '-c', '3', address])
    if res == 0:
        print( "ping to", address, "OK")
        return 1

    elif res == 2:
        print("no response from", address)
        return 0

    else:
        print("ping to", address, "failed!")
        return 0






def getMyIp():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        mi_ip = s.getsockname()[0]
        #print("mi ip es: " + str(mi_ip) )
        s.close()
        #ip_s=[]
        return mi_ip

    except:
        print("error")


def getMmrIp():
    ip_mmr = ""
    try:
        address = "raspberrypi.local" 
        res = subprocess.call(['ping', '-c', '3', address])
        if res == 0:
            print( "ping to", address, "OK")
            resOutput = subprocess.check_output(['ping', '-c', '3', address]).decode('utf-8')
            ip_mmr = resOutput.split(" ")[2][1:-1]

        elif res == 2:
            print("no response from", address)
        else:
            print("ping to", address, "failed!")

        print("ip  MMR es: " + str(ip_mmr) )

    except:
        print("error de red")
    
    return ip_mmr



def initLogo(file, delay):
 #   process = subprocess.Popen(['chromium-browser','--no-sandbox','--disable-infobars','--kiosk',file],stderr=subprocess.DEVNULL)
    #process = subprocess.Popen(['chromium-browser','main.html'])
    process = subprocess.Popen(['flatpak', 'run', 'org.mozilla.firefox', '--kiosk', file], stderr=subprocess.DEVNULL)

    print("sleep {} segundos".format(delay))
    time.sleep(delay)

def initLogoServer(file, delay):
    process = subprocess.Popen(['/usr/bin/python','/home/pi/display/server.py'])
    print('hola222222')
    file = "http://127.0.0.1:8000/display/index.html"
    time.sleep(10)
    process = subprocess.Popen(['flatpak','run','org.mozilla.firefox', '--kiosk', file], stderr=subprocess.DEVNULL)

#  process = subprocess.Popen(['chromium-browser','--no-sandbox','--disable-infobars','--kiosk',file],stderr=subprocess.DEVNULL)
    #process = subprocess.Popen(['chromium-browser','main.html'])
    print("sleep {} segundos".format(delay))
    time.sleep(delay)


def statusNet(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False

def inicializador_server(name, id, delay=10):
    try:
        cleanCache()
        initLogoServer('main.html', 10)
        addJson(name +" ID: " + id )
        time.sleep(5)
        return
    except:
        print('No se puede cargar el server')
        inicializador_server(name,id)


if __name__ == "__main__":
    
    inicializador_server(NAME,ID)
    
    lastStatus = 0
    primero=0
    while True:
   
        status = statusNet()
        if status:
            miIp = getMyIp()
            if primero==0:
                print("Mi ip es: " + str(miIp))
                addJson("Equipo conectado")
                primero=1
                time.sleep(2)
            addJson("Mi IP: "+ str(miIp))
            time.sleep(2)
 
            ip_mmr = getMmrIp()
            addJson("Buscando MMR...")
            time.sleep(2)
            if ip_mmr!='':
                addJson("Equipo MMR Encontrado")
                time.sleep(2)
                addJson("MMR IP: "+ str(ip_mmr))
                time.sleep(2)
                #process = subprocess.Popen(['flatpak','run','org.mozilla.firefox', '--kiosk', 'http://tunel.mine-360.com:20892'], stderr=subprocess.DEVNULL)
                process = subprocess.Popen(['flatpak','run','org.mozilla.firefox', '--kiosk', 'http://'+ ip_mmr+'/'], stderr=subprocess.DEVNULL)

                #process = subprocess.Popen(['chromium-browser','--disable-infobars','--kiosk', 'http://'+ ip_mmr+'/'],stderr=subprocess.DEVNULL)
                #process = subprocess.Popen(['chromium-browser','--disable-infobars','--kiosk', 'http://tunel.mine-360.com:20892'],stderr=subprocess.DEVNULL)
                lastStatus =1
                break


        else:
            addJson(NAME +" ID: " + ID )
            primero=0
            print("no internet!" )
    
    while True:
        checkNet =statusNet()
        checkPing =checkPingMmr()

        if  checkNet==0:
            print("no internet!" )
            lastStatus=0

        elif checkPing==0:
            print("No encuentro MMR!" )
            lastStatus=0

        elif checkNet==1 and checkPing==1 and lastStatus==0:
            ip_mmr_actual = getMmrIp()
            if ip_mmr_actual != ip_mmr and ip_mmr_actual!='':
                print("La ip del MMR ha cambiado, hay que abrir una nuevamente en el browser")
                process = subprocess.Popen(['flatpak', 'run','org.mozilla.firefox', '--kiosk', 'http://' + ip_mmr_actual + '/'], stderr=subprocess.DEVNULL)
            
#    process = subprocess.Popen(['chromium-browser','--disable-infobars','--kiosk', 'http://'+ ip_mmr_actual+'/'], stderr=subprocess.DEVNULL)
                lastStatus = 1
            else:
                print("Haremos un refresh de la pagina")
                #xdotool key "ctrl+F5" &
                process = subprocess.Popen(['xdotool', 'key', 'ctrl+F5'])
                lastStatus = 1

        else:
            print("Todo esta ok!!!")

        print("sleep 60 segundos")
        time.sleep(60)


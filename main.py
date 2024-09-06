import network
import socket
import time

from machine import Pin

led = Pin("LED", Pin.OUT)
on_air = Pin(22, Pin.OUT) 

ssid='ENTER_WIFI_SSID'
password='ENTER_WIFI_PASSWORD'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

html = """<!DOCTYPE html>
<html>
  <head><title>Aditi ON-AIR</title></head>
  <body>
    <table id="tblGraphic" width="400" height="100"
           style="color: white;
                  background-color: red;
                  font-family: arial;
                  border-collapse: separate;
                  border-radius: 20px;
                  border: solid black 3px;">
      <th style="font-size:5em;">ON AIR</td>
    </table>

    <p id="lblState"></p>
    <p>
        <a id="btnToggle" href="#">TOGGLE</a>
        <script type="text/javascript">
            state = "%s"
            btn = document.getElementById("btnToggle")
            lbl = document.getElementById("lblState")
            gph = document.getElementById("tblGraphic")
            lbl.innerHTML = "Light is " + state
            if (state == "ON") {
              btn.href="/light/off"
              btn.innerText = "OFF"
              gph.style["background-color"] = "red"
            }
            else {
              btn.href="/light/on"
              btn.innerText = "ON"
              gph.style["background-color"] = "darkred"
            }
        </script>
    </p>
  </body>
</html>"""

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection')
    time.sleep(1)
    
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])

sinfo = socket.getaddrinfo('0.0.0.0', 80)
addr = sinfo[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)
        
        request = str(request)        
        led_on = request.find('/light/on')
        led_off = request.find('/light/off')
        print('led on = ' + str(led_on))
        print('led off = ' + str(led_off))
        
        stateis = 'ON' if led.value() else 'OFF'
        
        if led_on == 6:
            print('led on')
            led.on()
            on_air.on()
            stateis = 'ON'
        
        if led_off == 6:
            print('led off')
            led.off()
            on_air.off()
            stateis = 'OFF'
        
        response = html % stateis
        
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()
    except OSError as e:
        cl.close()
        print('connection closed')
        

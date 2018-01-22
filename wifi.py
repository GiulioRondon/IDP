import os
loop = 0
while loop < 10: # aantal keer dat de signaalsterkte getest moet worden
    Command= os.popen('sudo iwlist wlan0 scan | grep -E "ESSID|Quality"')
    SSID_Quality = Command.read()

    lines = SSID_Quality.split('\n')

    lineNR = 1
    QualityList = []
    SSIDList = []
    for line in lines:
        if lineNR % 2 == 1:
            QualityList.append(line[-9:-1]) #<<< Vul hier -29:-24 in voor signaal in sterkte op een schaal van 1 tot 70
        else:
            SSIDList.append(line[27:-1])
        lineNR += 1

    lineNR = 0
    for ssid in SSIDList:
        if ssid == 'NAAM NETWERK': #<<< Vul hier de naam in van het wifi netwerk
            print(ssid)
            print(QualityList[lineNR])
            lineNR += 1
        else:
            lineNR += 1
            pass
    loop += 1
    
    

    

import yaml
import schedule
import time
import datetime
import requests
import sys


def yaml_loader(filepath):
    with open(filepath, "r") as f:
        fileData = yaml.load(f, Loader=yaml.FullLoader)
    return fileData



filepath = str(sys.argv[1])
fileData = yaml_loader(filepath)
lengthF = len(fileData['Steps'])
time = fileData['Scheduler']['when'].split()
firstId = fileData['Scheduler']['step_id_to_execute'][0]

if(lengthF >1):
    if( fileData['Steps'][0][1]['method'] == "GET"):
        fileData = fileData['Steps'][(int(firstId)-1)][firstId]
        r = requests.get(fileData['outbound_url'])
else:
    if( fileData['Steps'][0]['method'] == "GET"):
        fileData = fileData['Steps'][(int(firstId)-1)]
        r = requests.get(fileData['outbound_url'])
           






def job():
    global fileData
    global r
    if( str(r.status_code) == str(fileData['condition']['if']['equal']['right']) and type(r) is requests.models.Response):
        if(fileData['condition']['then']['action'] == '::print'):
            whichheader = fileData['condition']['then']['data']
            if(whichheader.startswith("http.response.headers")):
                getheader = whichheader.split("http.response.headers.")
                print(r.headers[str(getheader[1])])
        elif (fileData['condition']['then']['action'].startswith("::invoke")):
            getStep = fileData['condition']['then']['action'].split("::invoke:step:")[1]
            data = fileData['condition']['then']['data']
            fileData = yaml_loader(filepath)
            fileData = fileData['Steps'][int(getStep)-1][int(getStep)]
            # print( "fileData is now {}".format(fileData['outbound_url']) )
            if(str(fileData['outbound_url']) != '::input:data'):
                r = requests.get(fileData['outbound_url'])
            else:
                r= requests.get(data)
            job()
    else:
            if(fileData['condition']['else']['action'] == '::print'):
                whichheader = fileData['condition']['else']['data']
                print(whichheader)
            elif (fileData['condition']['else']['action'].startswith("::invoke")):
                getStep = fileData['condition']['else']['action'].split("::invoke:step:")[1]
                print("work on step : " + str(getStep))
                fileData = yaml_loader(filepath)
                fileData = fileData['Steps'][int(getStep)-1][int(getStep)]
                job()



    # print(datetime.datetime.now())



def getTime(timeArray):
    if( timeArray[0] != "*"):
        if( timeArray[1] != "*"):
            if( timeArray[2] != "*"):
                time = "{}:{}".format(timeArray[1], timeArray[0])
                #1 1 1
                if(int(timeArray[2]) == 0):
                    print("working at every Sun " + time)
                    schedule.every().sunday.at(time).do(job)
                elif(int(timeArray[2])== 1):
                    print("working at every mon " + time)
                    schedule.every().monday.at(time).do(job)
                elif(int(timeArray[2]) == 2):
                    print("working at every tues " + time)
                    schedule.every().tuesday.at(time).do(job)
                elif(int(timeArray[2]) == 3):
                    print("working at every wed " + time)
                    schedule.every().wednesday.at(time).do(job)
                elif(int(timeArray[2]) == 4):
                    print("working at every thur " + time)
                    schedule.every().thursday.at(time).do(job)
                elif(int(timeArray[2]) == 5):
                    print("working at every fri " + time)
                    schedule.every().friday.at(time).do(job)
                elif(int(timeArray[2]) == 6):
                    print("working at every sat " + time)
                    schedule.every().saturday.at(time).do(job)
                else:
                    print("wrong input format")
            else:
                #1 1 *
                time = "{}:{}".format(timeArray[1], timeArray[0])
                print("working today at " + time)
                schedule.every().day.at(time).do(job)
        else:
            #1 * 1
            if( timeArray[2] != "*"):
                time = "00:{}".format(timeArray[0])
                if(int(timeArray[2]) == 0):
                    print("working at every Sun " + time)
                    schedule.every().sunday.at(time).do(job)
                elif(int(timeArray[2])== 1):
                    print("working at every mon " + time)
                    schedule.every().monday.at(time).do(job)
                elif(int(timeArray[2]) == 2):
                    print("working at every tues " + time)
                    schedule.every().tuesday.at(time).do(job)
                elif(int(timeArray[2]) == 3):
                    print("working at every wed " + time)
                    schedule.every().wednesday.at(time).do(job)
                elif(int(timeArray[2]) == 4):
                    print("working at every thur " + time)
                    schedule.every().thursday.at(time).do(job)
                elif(int(timeArray[2]) == 5):
                    print("working at every fri " + time)
                    schedule.every().friday.at(time).do(job)
                elif(int(timeArray[2]) == 6):
                    print("working at every sat " + time)
                    schedule.every().saturday.at(time).do(job)
                else:
                    print("wrong input format")
            else:
                # 1 * * 
                print("working at every {} minutes".format(timeArray[0]))
                schedule.every(int(timeArray[0])).minutes.do(job)
    else:
        if( timeArray[1] != "*"):
            if( timeArray[2] != "*"):
                # * 1 1
                time = "{}:00".format(timeArray[1])
                if(int(timeArray[2]) == 0):
                    print("working at every Sun " + time)
                    schedule.every().sunday.at(time).do(job)
                elif(int(timeArray[2])== 1):
                    print("working at every mon " + time)
                    schedule.every().monday.at(time).do(job)
                elif(int(timeArray[2]) == 2):
                    print("working at every tues " + time)
                    schedule.every().tuesday.at(time).do(job)
                elif(int(timeArray[2]) == 3):
                    print("working at every wed " + time)
                    schedule.every().wednesday.at(time).do(job)
                elif(int(timeArray[2])== 4):
                    print("working at every thur " + time)
                    schedule.every().thursday.at(time).do(job)
                elif(int(timeArray[2]) == 5):
                    print("working at every fri " + time)
                    schedule.every().friday.at(time).do(job)
                elif(int(timeArray[2]) == 6):
                    print("working at every sat " + time)
                    schedule.every().saturday.at(time).do(job)
                else:
                    print("wrong input format")
            else:
                # * 1 * 
                time = "{}:00".format(timeArray[1])
                print("working today at " + time)
                schedule.every().day.at(time).do(job)
        else:
            if( timeArray[2] != "*"):
                # * * 1
                time = "00:00"
                if(int(timeArray[2]) == 0):
                    print("working at every Sun " + time)
                    schedule.every().sunday.at(time).do(job)
                elif(int(timeArray[2])== 1):
                    print("working at every mon " + time)
                    schedule.every().monday.at(time).do(job)
                elif(int(timeArray[2]) == 2):
                    print("working at every tues " + time)
                    schedule.every().tuesday.at(time).do(job)
                elif(int(timeArray[2]) == 3):
                    print("working at every wed " + time)
                    schedule.every().wednesday.at(time).do(job)
                elif(int(timeArray[2]) == 4):
                    print("working at every thur " + time)
                    schedule.every().thursday.at(time).do(job)
                elif(int(timeArray[2]) == 5):
                    print("working at every fri " + time)
                    schedule.every().friday.at(time).do(job)
                elif(int(timeArray[2]) == 6):
                    print("working at every sat " + time)
                    schedule.every().saturday.at(time).do(job)
                else:
                    print("wrong input format")

                

getTime(time)





# def getYaml(yamlList):


while True:
    schedule.run_pending()
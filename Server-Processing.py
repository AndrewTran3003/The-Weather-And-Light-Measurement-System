from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import Error
import MySQLdb
import time
import datetime
import serial
import threading
from threading import Timer
import requests
import json


app = Flask(__name__)


def updateDatabase(datatype, value):
    serverName = 'localhost'
    username = 'root'
    password = 'root'
    dbName = 'assignment1'
    
    dbConn = mysql.connector.connect(host=serverName,
                                         database=dbName,
                                         user=username,
                                         password = password)
    table = ''
    if(datatype == 'a'):
        table = 'AmbientValue'
    elif(datatype == 't'):
        table = 'TempValue'
    elif(datatype == 'ana'):
        table = 'Analysis'
    
    query = 'INSERT INTO ' + table +' (value,dateCreated) VALUES ("'+ value +'",NOW());'    
    print (query)
    cursor = dbConn.cursor()
    cursor.execute(query)
    dbConn.commit()
    cursor.close()
    dbConn.close()

class Response:
    def __init__(self, value, dateCreated):
        self.value = value
        self.dateCreated = dateCreated



fan = 'F'

buttonMode= ''
arduino =''
time1 = ''
stringResponse = ''

def getDataFromApi():
    Url = 'api.openweathermap.org/data/2.5/weather?q=Melbourne,aus&APPID=cca201a177b66c9ad424f4072fb1ace7'
    Url = 'http://' + Url
    ApiResponse = requests.get(Url)
    return ApiResponse


def GetCurrentTemperatureFromApi():
    global time1
    global stringResponse
    time2 = datetime.datetime.now()
    if(stringResponse == '' or( stringResponse != '' and (time2.minute-time1.minute) > 10)):
        data = getDataFromApi()
        print('API request has been made')
        if (data.status_code == 200):
            json_data = data.json()
            time1 = time2
            stringResponse =  str(json_data['main']['temp']-273)
            
    
    return stringResponse

def WeatherDataAnalytic(LatestTemp, ApiTemp):
    Result = ''
    if (LatestTemp > ApiTemp):
        Result = 'The current temperature inside (' + str(LatestTemp)+ ' degree Celcius) is higher than that of the Api (' + str(ApiTemp) +' degree Celcius)' 
    elif (LatestTemp == ApiTemp):
        Result = 'The current temperature inside (' + str(LatestTemp)+ ' degree Celcius) is lower than that of the Api (' + str(ApiTemp) +' degree Celcius)' 
    else:
        Result = 'The current temperature inside  is equal to that of the Api'
    updateDatabase('ana', str(Result))
    return Result
    



def getDataFromArduino():
    global arduino 
    device = '/dev/ttyS2'
    arduino = serial.Serial(device,9600,timeout = 1)
    arduino.flush()
    while(1==1):
        if(arduino.inWaiting()>0):
            data = arduino.readline()
            dataInstring = str(data).rstrip()
            
            arrayData = dataInstring.split(',')
            if(len(arrayData) == 2 ):
                if(len(arrayData[1]) != 0):
                    if (arrayData[0] == 'a'):
                        updateDatabase('a',arrayData[1])
                        
                    elif (arrayData[0] == 't'):
                        updateDatabase('t',arrayData[1])
                        if(fan == 'A'):
                            if (float(arrayData[1]) > 20):
                                TurnOnTheFan(arduino)
                                time.sleep(1)
                            else:
                                TurnOffTheFan(arduino)
                                time.sleep(1)
    

def TurnOnTheFan(arduino):
    arduino.write(str(1).encode('utf-8'))

def TurnOffTheFan(arduino):
    arduino.write(str(0).encode('utf-8'))

    

def RetriveData(tableName):
    response = []
    serverName = 'localhost'
    username = 'root'
    password = 'root'
    dbName = 'assignment1'
    
    connection = mysql.connector.connect(host=serverName,
                                         database=dbName,
                                         user=username,
                                         password = password)
    sql = 'SELECT value,dateCreated  FROM ( SELECT * FROM ' + tableName + ' ORDER BY dateCreated DESC LIMIT 10) detail ORDER BY dateCreated DESC'  
    cursor = connection.cursor()
    cursor.execute(sql)    
    results = cursor.fetchall()
    for result in results:
        obj = Response(result[0],str(result[1]))
        response.append(obj)
    cursor.close()
    connection.close()
    return response


'''
'''



@app.route('/', defaults = {'fanmode': None})
@app.route('/<fanmode>/', defaults = {'fandata': None})
@app.route('/<fanmode>/<fandata>')
def dataFunction(fanmode, fandata):
    global fan
    global buttonMode
    tempData = RetriveData('TempValue')
    ambientData = RetriveData('AmbientValue')
    analysisData = RetriveData('Analysis')
    ApiData = GetCurrentTemperatureFromApi()
    Comparison = 'No Comparison Yet'
    LatestTemp = tempData[9].value
    
    CurrentApiTemp = GetCurrentTemperatureFromApi()
    if (CurrentApiTemp != '' and LatestTemp != ''):
        Comparison = WeatherDataAnalytic(LatestTemp,CurrentApiTemp)
    
        
    if fanmode == 'FM':
        buttonMode= 'FM'
        if(fandata == 'T'):
            fan = 'T'
            TurnOnTheFan(arduino)
        else:
            fan = 'F'
            TurnOffTheFan(arduino)
    elif fanmode == 'FA':
        buttonMode= 'FA'
        fan = 'A'
    else:
        button = 'Not Valid!'
    
    
    
    return render_template('main.html', tempData = tempData,ambientData= ambientData, Comparison = Comparison,buttonMode= buttonMode, analysisData = analysisData )


if __name__== '__main__':
    time1 = datetime.datetime.now()
    arduinoThread = threading.Thread(target = getDataFromArduino)
    arduinoThread.start()
    
    app.run(debug=True, host = '0.0.0.0')
    
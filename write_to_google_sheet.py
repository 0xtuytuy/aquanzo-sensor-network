import pygsheets
import pandas as pd
from datetime import date
import os
import glob
import time

class TempReading: 
    def __init__(self,_sensorId, _dateInUnix, _readingInCelcius, _readingInFahrenheit, ): 
        self.readingInCelcius = _readingInCelcius 
        self.dateInUnix = _dateInUnix
        self.readingInFahrenheit = _readingInFahrenheit
        self.sensorId = _sensorId

def writeDatatToGoogle(tempReading):
    #authorization
    gc = pygsheets.authorize(service_file='../aquanzo-test-network-googleDrive-api-creds.json')

    # Create empty dataframe
    df = pd.DataFrame()

    #open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
    sh = gc.open('aquanzo-sensor-network-test')

    #select the first sheet 
    wks = sh[0]

    new_row = [tempReading['readingInCelcius'], tempReading['dateInUnix'], tempReading['readingInFahrenheit'], tempReading['sensorId']]
    cells = wks.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
    last_row = len(cells)
    wks = wks.insert_rows(last_row, number=1, values= new_row)

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def main():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
 
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    
    while True:
	    temp_c, temp_f = read_temp()
        testReading = TempReading('test_1', date.today(), temp_c, temp_f)
        writeDatatToGoogle(testReading)
	    time.sleep(1)
	
if __name__ == "__main__":
    main()
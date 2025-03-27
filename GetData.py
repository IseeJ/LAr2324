from influxdb_client import InfluxDBClient
import csv
from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd

#url = "http://localhost:8086"                                                                                                                                                    
url = "http://johnson.wellesley.edu:8086"
token = "8ntFp7miIHtdHOGA1b308NRJ3SuVAUY0EXZfJnDAJx6Ija441sGMHItFN8oXv3kpfWmH0HiogNXlivhWxDH5wQ=="
org = "largon"
bucket = "slowcontrol"

#stoptime = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")                                                                                                                      
#starttime = (datetime.utcnow() - timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%SZ")                                                                                              


starttime = '2025-02-23T04:12:38Z'
stoptime = '2025-03-20T21:11:38Z'


#client = InfluxDBClient(url=url, token=token, org=org)                                                                                                                           

with InfluxDBClient(url=url, token=token, org=org) as client:
    query_api = client.query_api()
    query = f'''from(bucket: "{bucket}")                                                                                                                                          
  |> range(start: {starttime}, stop: {stoptime})                                                                                                                                  
  |> filter(fn: (r) => r["_measurement"] == "pressures" or r["_measurement"] == "voltages")                                                                                       
  |> filter(fn: (r) => r["_field"] == "value")                                                                                                                                    
  |> filter(fn: (r) => r["device"] == "OmegaDPI8" or r["device"] == "RevPi1" or r["device"] == "Waveshare485")                                                                    
  |> filter(fn: (r) => r["sensor"] == "Hornet_ConvectionGauge" or r["sensor"] == "Pressure_Transducer" or r["sensor"] == "Hornet_IonGauge")                                       
  |> filter(fn: (r) => r["subsystem"] == "cryostat" or r["subsystem"] == "purity_monitor")'''
    result = query_api.query_csv(query, org=org)



data=[]

def parse(result):
    for row in result:
        if not row[0].startswith("#") and len(row) > 10:
            data.append({"time": row[5], "sensor": row[10], "value": row[6]})

parse(result)
df = pd.DataFrame(data)
df.sort_values(by="time", inplace=True, na_position='first')
df.to_csv(f"{starttime}_{stoptime}.csv", index=False)
print(df)
print("OK")

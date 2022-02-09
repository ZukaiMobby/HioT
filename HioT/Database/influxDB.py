from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from HioT.Plugins.get_config import influxDB_config
from rich import print

token = influxDB_config['token']
org = influxDB_config['org']
bucket = influxDB_config['bucket']
url = influxDB_config['url']

def influx_write(data: str):
    #data = "mem,host=host1 used_percent=23.43234543"
    with InfluxDBClient(url=url, token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket, org, data)

def influx_query():
    with InfluxDBClient(url=url, token=token, org=org) as client:
        query_api = client.query_api()
        query = f' from(bucket:"{bucket}")\
        |> range(start: -10m)\
        |> filter(fn:(r) => r._measurement == "my_measurement")\
        |> filter(fn: (r) => r.location == "Prague")\
        |> filter(fn:(r) => r._field == "temperature" ) '

        result = query_api.query(org=org, query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append((record.get_field(), record.get_value()))
        """ 
        Use the get_value() method to return values.
        Use the get_field() method to return fields.
        
        """

def influx_query_by_device(did):
    #返回数据所有历史数据
    with InfluxDBClient(url=url, token=token, org=org) as client:
        query_api = client.query_api()
        query = ' from(bucket: "HioT") \
        |> range(start: -1d) \
        |> filter(fn: (r) => r["did"] == "1") '

        print(query)
        result = query_api.query(org=org, query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append((record.get_field(), record.get_value(), record.get_time()))
    print(results)

"""
query = 'from(bucket: "HioT") |> range(start: -1h)'
tables = client.query_api().query(query, org=org)
for table in tables:
    for record in table.records:
        print(record)

"""

if __name__ == '__main__':
    pass
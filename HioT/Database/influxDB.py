from logging import LogRecord
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

from HioT.Plugins.get_config import influxDB_config
from HioT.Plugins.get_logger import logger

"""
data = "mem,host=host1 used_percent=23.43234543"
<measurement>[,<tag_key>=<tag_value>[,<tag_key>=<tag_value>]] <field_key>=<field_value>[,<field_key>=<field_value>] [<timestamp>]
"""

token = influxDB_config['token']
org = influxDB_config['org']
bucket = influxDB_config['bucket']
url = influxDB_config['url']

def influx_write(data: str):
    with InfluxDBClient(url=url, token=token, org=org) as client:
        logger.info(f"INFLUX执行:{data}")
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket, org, data)

def _influx_query():
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
        query = f' from(bucket: "HioT") \
        |> range(start: -1d) \
        |> filter(fn: (r) => r["did"] == "{did}") '

        result = query_api.query(org=org, query=query)
        results = []
        for table in result:
            for record in table.records:
                results.append((record.get_field(), record.get_value(), record.get_time()))
                #[(x,y,z),(...),(...)]
    return results



if __name__ == '__main__':
    pass
    from rich import print
    
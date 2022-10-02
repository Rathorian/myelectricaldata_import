import os


from config import *
from dependencies import *
from models.config import config

logo(VERSION)

# def init_database(cur):
#     ## CONFIG
#     cur.execute('''CREATE TABLE config (
#                         key TEXT PRIMARY KEY,
#                         value json NOT NULL)''')
#     cur.execute('''CREATE UNIQUE INDEX idx_config_key
#                     ON config (key)''')
#
#     ## ADDRESSES
#     cur.execute('''CREATE TABLE addresses (
#                         pdl TEXT PRIMARY KEY,
#                         json json NOT NULL,
#                         count INTEGER)''')
#     cur.execute('''CREATE UNIQUE INDEX idx_pdl_addresses
#                     ON addresses (pdl)''')
#
#     ## CONTRACT
#     cur.execute('''CREATE TABLE contracts (
#                         pdl TEXT PRIMARY KEY,
#                         json json NOT NULL,
#                         count INTEGER)''')
#     cur.execute('''CREATE UNIQUE INDEX idx_pdl_contracts
#                     ON contracts (pdl)''')
#     ## CONSUMPTION
#     # DAILY
#     cur.execute('''CREATE TABLE consumption_daily (
#                         pdl TEXT NOT NULL,
#                         date TEXT NOT NULL,
#                         value INTEGER NOT NULL,
#                         fail INTEGER)''')
#     cur.execute('''CREATE UNIQUE INDEX idx_date_consumption
#                     ON consumption_daily (date)''')
#
#     # DETAIL
#     cur.execute('''CREATE TABLE consumption_detail (
#                         pdl TEXT NOT NULL,
#                         date TEXT NOT NULL,
#                         value INTEGER NOT NULL,
#                         interval INTEGER NOT NULL,
#                         measure_type TEXT NOT NULL,
#                         fail INTEGER)''')
#     cur.execute('''CREATE UNIQUE INDEX idx_date_consumption_detail
#                     ON consumption_detail (date)''')
#     ## PRODUCTION
#     # DAILY
#     cur.execute('''CREATE TABLE production_daily (
#                         pdl TEXT NOT NULL,
#                         date TEXT NOT NULL,
#                         value INTEGER NOT NULL,
#                         fail INTEGER)''')
#     cur.execute('''CREATE UNIQUE INDEX idx_date_production
#                     ON production_daily (date)''')
#     # DETAIL
#     cur.execute('''CREATE TABLE production_detail (
#                         pdl TEXT NOT NULL,
#                         date TEXT NOT NULL,
#                         value INTEGER NOT NULL,
#                         interval INTEGER NOT NULL,
#                         measure_type TEXT NOT NULL,
#                         fail INTEGER)''')
#     cur.execute('''CREATE UNIQUE INDEX idx_date_production_detail
#                     ON production_detail (date)''')
#
#     ## Default Config
#     config_query = f"INSERT OR REPLACE INTO config VALUES (?, ?)"
#     config = {
#         "day": datetime.now().strftime('%Y-%m-%d'),
#         "call_number": 0,
#         "max_call": 500,
#         "version": VERSION
#     }
#     cur.execute(config_query, ["config", json.dumps(config)])
#     con.commit()
#
#
# def run(pdl, pdl_config):
#     f.logLine()
#     f.title(pdl)
#
#     global offpeak_hours
#
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': pdl_config['token'],
#         'call-service': "enedisgateway2mqtt",
#         'version': VERSION
#     }
#
#     f.logLine()
#     f.log("Get contract :")
#     contract = cont.getContract(headers, client, cur, con, pdl, pdl_config)
#     offpeak_hours = []
#     f.log(contract, "debug")
#     if "error_code" in contract:
#         f.publish(client, f"error", str(1))
#         for key, data in contract["detail"].items():
#             f.publish(client, f"errorMsg/{key}", str(data))
#         f.log("-- Stop import --")
#     else:
#         f.publish(client, f"error", str(0))
#
#         for pdl, contract_data in contract.items():
#             for key, data in contract_data.items():
#                 if key == "last_activation_date":
#                     last_activation_date = data
#                 if key == "offpeak_hours":
#                     offpeak_hours = data
#                 if "home_assistant" in config and "discovery" in config['home_assistant'] and config['home_assistant'][
#                     'discovery'] == True:
#                     ha.haAutodiscovery(config=config, client=client, type="sensor", pdl=pdl, name=key, value=data)
#
#         f.logLine()
#         f.log("Get Addresses :")
#         addresse = addr.getAddresses(headers, client, con, cur, pdl, pdl_config)
#         if "error_code" in addresse:
#             f.publish(client, f"addresses/error", str(1))
#             for key, data in addresse["detail"].items():
#                 f.publish(client, f"addresses/errorMsg/{key}", str(data))
#         else:
#             f.publish(client, f"addresses/error", str(0))
#
#         if pdl_config['consumption'] == True:
#             f.logLine()
#             f.log("Get Consumption :")
#             ha_discovery_consumption = day.getDaily(headers, cur, con, client, pdl, pdl_config, "consumption",
#                                                     last_activation_date)
#             f.logLine1()
#             f.log("                        SUCCESS : Consumption daily imported")
#             f.logLine1()
#             if config['home_assistant']['discovery'] == True:
#                 f.logLine()
#                 f.log("Home Assistant auto-discovery (Consumption) :")
#                 for pdl, data in ha_discovery_consumption.items():
#                     for name, sensor_data in data.items():
#                         if "attributes" in sensor_data:
#                             attributes = sensor_data['attributes']
#                         else:
#                             attributes = None
#                         if "unit_of_meas" in sensor_data:
#                             unit_of_meas = sensor_data['unit_of_meas']
#                         else:
#                             unit_of_meas = None
#                         if "device_class" in sensor_data:
#                             device_class = sensor_data['device_class']
#                         else:
#                             device_class = None
#                         if "state_class" in sensor_data:
#                             state_class = sensor_data['state_class']
#                         else:
#                             state_class = None
#                         if "value" in sensor_data:
#                             ha.haAutodiscovery(config=config, client=client, type="sensor", pdl=pdl, name=name,
#                                                value=sensor_data['value'],
#                                                attributes=attributes, unit_of_meas=unit_of_meas,
#                                                device_class=device_class, state_class=state_class)
#             f.log(" => HA Sensor updated")
#         # f.logLine()
#
#         if pdl_config['consumption_detail']:
#             f.log("Get Consumption Detail:")
#             ha_discovery_consumption = detail.getDetail(headers, cur, con, client, pdl, pdl_config, "consumption",
#                                                         last_activation_date, offpeak_hours=offpeak_hours)
#             f.logLine1()
#             f.log("                   SUCCESS : Consumption detail imported")
#             f.logLine1()
#             if config['home_assistant']['discovery'] == True:
#                 f.logLine()
#                 f.log("Home Assistant auto-discovery (Consumption Detail) :")
#                 for pdl, data in ha_discovery_consumption.items():
#                     for name, sensor_data in data.items():
#                         if "attributes" in sensor_data:
#                             attributes = sensor_data['attributes']
#                         else:
#                             attributes = None
#                         if "unit_of_meas" in sensor_data:
#                             unit_of_meas = sensor_data['unit_of_meas']
#                         else:
#                             unit_of_meas = None
#                         if "device_class" in sensor_data:
#                             device_class = sensor_data['device_class']
#                         else:
#                             device_class = None
#                         if "state_class" in sensor_data:
#                             state_class = sensor_data['state_class']
#                         else:
#                             state_class = None
#                         if "value" in sensor_data:
#                             ha.haAutodiscovery(config=config, client=client, type="sensor", pdl=pdl, name=name,
#                                                value=sensor_data['value'],
#                                                attributes=attributes, unit_of_meas=unit_of_meas,
#                                                device_class=device_class, state_class=state_class)
#                 f.log(" => HA Sensor updated")
#         # f.logLine()
#
#         if pdl_config['production'] == True:
#             f.logLine()
#             f.log("Get production :")
#             ha_discovery_production = day.getDaily(headers, cur, con, client, pdl, pdl_config, "production",
#                                                    last_activation_date)
#             f.logLine1()
#             f.log("             SUCCESS : Production daily imported")
#             f.logLine1()
#             if config['home_assistant']['discovery'] == True:
#                 f.logLine()
#                 f.log("Home Assistant auto-discovery (Production) :")
#                 for pdl, data in ha_discovery_production.items():
#                     for name, sensor_data in data.items():
#                         if "attributes" in sensor_data:
#                             attributes = sensor_data['attributes']
#                         else:
#                             attributes = None
#                         if "unit_of_meas" in sensor_data:
#                             unit_of_meas = sensor_data['unit_of_meas']
#                         else:
#                             unit_of_meas = None
#                         if "device_class" in sensor_data:
#                             device_class = sensor_data['device_class']
#                         else:
#                             device_class = None
#                         if "state_class" in sensor_data:
#                             state_class = sensor_data['state_class']
#                         else:
#                             state_class = None
#                         ha.haAutodiscovery(config=config, client=client, type="sensor", pdl=pdl, name=name,
#                                            value=sensor_data['value'],
#                                            attributes=attributes, unit_of_meas=unit_of_meas,
#                                            device_class=device_class, state_class=state_class)
#                 f.log(" => HA Sensor updated")
#
#         if pdl_config['production_detail'] == True:
#             f.logLine()
#             f.log("Get production Detail:")
#             ha_discovery_consumption = detail.getDetail(headers, cur, con, client, pdl, pdl_config, "production",
#                                                         last_activation_date)
#             f.logLine1()
#             f.log("              SUCCESS : Production detail imported")
#             f.logLine1()
#             if config['home_assistant']['discovery'] == True:
#                 f.logLine()
#                 f.log("Home Assistant auto-discovery (Production Detail) :")
#                 for pdl, data in ha_discovery_consumption.items():
#                     for name, sensor_data in data.items():
#                         if "attributes" in sensor_data:
#                             attributes = sensor_data['attributes']
#                         else:
#                             attributes = None
#                         if "unit_of_meas" in sensor_data:
#                             unit_of_meas = sensor_data['unit_of_meas']
#                         else:
#                             unit_of_meas = None
#                         if "device_class" in sensor_data:
#                             device_class = sensor_data['device_class']
#                         else:
#                             device_class = None
#                         if "state_class" in sensor_data:
#                             state_class = sensor_data['state_class']
#                         else:
#                             state_class = None
#                         if "value" in sensor_data:
#                             ha.haAutodiscovery(config=config, client=client, type="sensor", pdl=pdl, name=name,
#                                                value=sensor_data['value'],
#                                                attributes=attributes, unit_of_meas=unit_of_meas,
#                                                device_class=device_class, state_class=state_class)
#                 f.log(" => HA Sensor updated")
#
#         if "influxdb" in config and config["influxdb"] != {}:
#             f.logLine()
#             f.log("Push data in influxdb")
#             influx.influxdb_insert(cur, con, pdl, pdl_config, influxdb, influxdb_api)
#             f.log(" => Data exported")
#
#         if "home_assistant" in config and "card_myenedis" in config['home_assistant'] and config['home_assistant'][
#             'card_myenedis'] == True:
#             f.logLine()
#             f.log("Generate Sensor for myEnedis card")
#             my_enedis_data = myenedis.myEnedis(cur, con, client, pdl, pdl_config, last_activation_date,
#                                                offpeak_hours=offpeak_hours)
#             for pdl, data in my_enedis_data.items():
#                 for name, sensor_data in data.items():
#                     if "attributes" in sensor_data:
#                         attributes = sensor_data['attributes']
#                     else:
#                         attributes = None
#                     if "unit_of_meas" in sensor_data:
#                         unit_of_meas = sensor_data['unit_of_meas']
#                     else:
#                         unit_of_meas = None
#                     if "device_class" in sensor_data:
#                         device_class = sensor_data['device_class']
#                     else:
#                         device_class = None
#                     if "state_class" in sensor_data:
#                         state_class = sensor_data['state_class']
#                     else:
#                         state_class = None
#                     if "value" in sensor_data:
#                         ha.haAutodiscovery(config=config, client=client, type="sensor", pdl=pdl, name=name,
#                                            value=sensor_data['value'],
#                                            attributes=attributes, unit_of_meas=unit_of_meas,
#                                            device_class=device_class, state_class=state_class)
#             f.log(" => Sensor generated")
#
#         if "home_assistant" in config and "hourly" in config['home_assistant'] and config['home_assistant'][
#             'hourly'] == True:
#             f.logLine()
#             f.log("Generate Hourly Sensor")
#             hourly_data = hourly.Hourly(cur, con, client, pdl, pdl_config, last_activation_date,
#                                         offpeak_hours=offpeak_hours)
#             for pdl, data in my_enedis_data.items():
#                 for name, sensor_data in data.items():
#                     if "attributes" in sensor_data:
#                         attributes = sensor_data['attributes']
#                     else:
#                         attributes = None
#                     if "unit_of_meas" in sensor_data:
#                         unit_of_meas = sensor_data['unit_of_meas']
#                     else:
#                         unit_of_meas = None
#                     if "device_class" in sensor_data:
#                         device_class = sensor_data['device_class']
#                     else:
#                         device_class = None
#                     if "state_class" in sensor_data:
#                         state_class = sensor_data['state_class']
#                     else:
#                         state_class = None
#                     if "value" in sensor_data:
#                         ha.haAutodiscovery(config=config, client=client, type="sensor", pdl=pdl, name=name,
#                                            value=sensor_data['value'],
#                                            attributes=attributes, unit_of_meas=unit_of_meas,
#                                            device_class=device_class, state_class=state_class)
#             f.log(" => Sensor generated")
#
#         query = f"SELECT * FROM consumption_daily WHERE pdl == '{pdl}' AND fail > {fail_count} ORDER BY date"
#         rows = con.execute(query)
#         if rows.fetchone() is not None:
#             f.logLine()
#             f.log(f"Consumption data not found on enedis (after {fail_count} retry) :")
#             # pprint(rows.fetchall())
#             # pprint(rows)
#             for row in rows:
#                 f.log(f"{row[0]} => {row[1]}")
#     con.commit()
#
#     f.logLine()
#     f.log("IMPORT FINISH")
#     f.logLine()
#
#
# if __name__ == '__main__':
#
#     if lost_params != []:
#         f.log(f'Some mandatory parameters are missing :', "ERROR")
#         for param in lost_params:
#             f.log(f'- {param}', "ERROR")
#         f.log("", "ERROR")
#         f.log("You can get list of parameters here :", "ERROR")
#         f.log(f" => https://github.com/m4dm4rtig4n/enedisgateway2mqtt#configuration-file", "ERROR")
#         f.log("-- Stop application --", "CRITICAL")
#
#     f.logLine()
#     f.logo(VERSION)
#     if "mqtt" in config:
#         f.log("MQTT")
#         for id, value in config['mqtt'].items():
#             if id == "password":
#                 value = "** hidden **"
#             f.log(f" - {id} : {value}")
#     else:
#         f.log("MQTT Configuration missing !", "CRITICAL")
#
#     if "home_assistant" in config:
#         f.logLine()
#         f.log("Home Assistant")
#         for id, value in config['home_assistant'].items():
#             f.log(f" - {id} : {value}")
#
#     if "influxdb" in config:
#         f.logLine()
#         f.log("InfluxDB")
#         for id, value in config['influxdb'].items():
#             if id == "token":
#                 value = "** hidden **"
#             f.log(f" - {id} : {value}")
#
#     if "enedis_gateway" in config:
#         f.logLine()
#         f.log("Enedis Gateway")
#         for pdl, data in config['enedis_gateway'].items():
#             f.log(f" - {pdl}")
#             for id, value in data.items():
#                 if id == "token":
#                     value = "** hidden **"
#                 f.log(f"     {id} : {value}")
#     else:
#         f.log("Enedis Gateway Configuration missing !", "CRITICAL")
#     f.logLine()
#
#     # SQLlite
#     f.log("Check database/cache")
#
#     if not os.path.exists('/data'):
#         os.mkdir('/data')
#
#     if "wipe_cache" in config and config["wipe_cache"] == True:
#         if os.path.exists('/data/enedisgateway.db'):
#             f.logLine()
#             f.log(" => Reset Cache")
#             os.remove("/data/enedisgateway.db")
#             config["wipe_cache"] = False
#
#     if not os.path.exists('/data/enedisgateway.db'):
#         f.log(" => Init SQLite Database")
#         con = sqlite3.connect('/data/enedisgateway.db', timeout=10)
#         cur = con.cursor()
#         init_database(cur)
#
#     else:
#         f.log(" => Connect to SQLite Database")
#         con = sqlite3.connect('/data/enedisgateway.db', timeout=10)
#         cur = con.cursor()
#
#         # Check database structure
#         try:
#
#             config_query = f"INSERT OR REPLACE INTO config VALUES (?, ?)"
#             cur.execute(config_query, ["lastUpdate", datetime.now()])
#             con.commit()
#
#             list_tables = ["config", "addresses", "contracts", "consumption_daily", "consumption_detail",
#                            "production_daily", "production_detail"]
#
#             query = f"SELECT name FROM sqlite_master WHERE type='table';"
#             cur.execute(query)
#             query_result = cur.fetchall()
#             tables = []
#             for table in query_result:
#                 tables.append(str(table).replace("('", "").replace("',)", ''))
#             for tab in list_tables:
#                 if not tab in tables:
#                     msg = f"Table {tab} is missing"
#                     f.log(msg)
#                     raise msg
#             cur.execute("INSERT OR REPLACE INTO config VALUES (?,?)", [0, 0])
#             cur.execute("INSERT OR REPLACE INTO addresses VALUES (?,?,?)", [0, 0, 0])
#             cur.execute("INSERT OR REPLACE INTO contracts VALUES (?,?,?)", [0, 0, 0])
#             cur.execute("INSERT OR REPLACE INTO consumption_daily VALUES (?,?,?,?)", [0, '1970-01-01', 0, 0])
#             cur.execute("INSERT OR REPLACE INTO consumption_detail VALUES (?,?,?,?,?,?)",
#                         [0, '1970-01-01', 0, 0, "", 0])
#             cur.execute("INSERT OR REPLACE INTO production_daily VALUES (?,?,?,?)", [0, '1970-01-01', 0, 0])
#             cur.execute("INSERT OR REPLACE INTO production_detail VALUES (?,?,?,?,?,?)",
#                         [0, '1970-01-01', 0, 0, "", 0])
#             cur.execute("DELETE FROM config WHERE key = 0")
#             cur.execute("DELETE FROM addresses WHERE pdl = 0")
#             cur.execute("DELETE FROM contracts WHERE pdl = 0")
#             cur.execute("DELETE FROM consumption_daily WHERE pdl = 0")
#             cur.execute("DELETE FROM consumption_detail WHERE pdl = 0")
#             cur.execute("DELETE FROM production_daily WHERE pdl = 0")
#             cur.execute("DELETE FROM production_detail WHERE pdl = 0")
#             cur.execute("DELETE FROM production_detail WHERE pdl = 0")
#             config_query = f"SELECT * FROM config WHERE key = 'config'"
#             cur.execute(config_query)
#             query_result = cur.fetchall()
#             query_result = json.loads(query_result[0][1])
#         except Exception as e:
#             f.log("=====> ERROR : Exception <======")
#             f.log(e)
#             f.log('<!> Database structure is invalid <!>')
#             f.log(" => Reset database")
#             con.close()
#             os.remove("/data/enedisgateway.db")
#             f.log(" => Reconnect")
#             con = sqlite3.connect('/data/enedisgateway.db', timeout=10)
#             cur = con.cursor()
#             init_database(cur)
#
#     # MQTT
#     f.logLine()
#     client = f.connect_mqtt()
#     client.loop_start()
#
#     # INFLUXDB
#     if "influxdb" in config and config["influxdb"] != {}:
#         f.logLine()
#         f.log("InfluxDB connect :")
#
#         date_utils.date_helper = DateHelper(timezone=tzlocal())
#         if "scheme" not in config['influxdb']:
#             scheme = "http"
#         else:
#             scheme = config['influxdb']['scheme']
#         influxdb = influxdb_client.InfluxDBClient(
#             url=f"{scheme}://{config['influxdb']['host']}:{config['influxdb']['port']}",
#             token=config['influxdb']['token'],
#             org=config['influxdb']['org'],
#             timeout="600000"
#         )
#         health = influxdb.health()
#         if health.status == "pass":
#             f.log(" => Connection success")
#         else:
#             f.log(" => Connection failed", "CRITICAL")
#
#         influxdb_api = influxdb.write_api(write_options=ASYNCHRONOUS)
#
#     if "wipe_influxdb" in config and config["wipe_influxdb"] == True:
#         f.log(f"Reset InfluxDB data")
#         delete_api = influxdb.delete_api()
#         start = "1970-01-01T00:00:00Z"
#         stop = datetime.utcnow()
#         delete_api.delete(start, stop, '_measurement="enedisgateway_daily"', config['influxdb']['bucket'],
#                           org=config['influxdb']['org'])
#         start = datetime.utcnow() - relativedelta(years=2)
#         delete_api.delete(start, stop, '_measurement="enedisgateway_detail"', config['influxdb']['bucket'],
#                           org=config['influxdb']['org'])
#         f.log(f" => Data reset")
#         config["wipe_influxdb"] = False
#
#     while True:
#
#         con = sqlite3.connect('/data/enedisgateway.db', timeout=10)
#         cur = con.cursor()
#
#         for pdl, pdl_config in config['enedis_gateway'].items():
#             run(pdl, pdl_config)
#
#         con.close()
#
#         with open("/data/config.yaml", 'r+') as f:
#             text = f.read()
#             text = re.sub('wipe_cache:.*', 'wipe_cache: false', text)
#             text = re.sub('wipe_influxdb:.*', 'wipe_influxdb: false', text)
#             text = re.sub('    refresh_contract:.*', '    refresh_contract: false', text)
#             text = re.sub('    refresh_addresses:.*', '    refresh_addresses: false', text)
#             f.seek(0)
#             f.write(text)
#             f.truncate()
#
#         time.sleep(config['cycle'])

import configparser
import os
import requests
import subprocess
import time

PARSER = configparser.ConfigParser()
PARSER.read(os.path.join(
  os.path.dirname(os.path.abspath(__file__)), 'conf.cfg'))
CONF = PARSER['officelight']

HASS_HOST = CONF['hass_host']
HASS_PORT = int(CONF['hass_port'])
SECURITY_TOKEN = CONF['security_token']
CAMERA_STATUS_SENSOR_NAME = CONF['camera_status_sensor_name']
CAMERA_STATUS_SENSOR_FRIENDLY_NAME = CONF['camera_status_sensor_friendly_name']
MONITOR_STATUS_SENSOR_NAME = CONF['monitor_status_sensor_name']
MONITOR_STATUS_SENSOR_FRIENDLY_NAME = CONF['monitor_status_sensor_friendly_name']
POLLING_INTERVAL_SECONDS = float(CONF['polling_interval_seconds'])


def post_entity_status(device_name, friendly_name, state):
  url = f'http://{HASS_HOST}:{HASS_PORT}/api/states/binary_sensor.{device_name}'

  headers = {
    'Authorization': f'Bearer {SECURITY_TOKEN}',
    'content-type': 'application/json'
  }

  data = {
    'state': 'on' if state else 'off',
    'attributes': {
      'friendly_name': friendly_name,
    }
  }

  return requests.post(url, headers=headers, json=data)


def get_camera_status():
  raw = None
  with open('/sys/module/uvcvideo/refcnt', 'r') as f:
    raw = f.read().strip()
  return False if raw == '0' else True


def get_monitor_status():
  process_result = subprocess.run(
    ['xset', '-display', ':0', '-q'], capture_output=True)
  if process_result.returncode != 0:
    print(process_result)
  stdout = process_result.stdout.decode('utf8')
  return 'Monitor is On' in stdout


def main():
  monitor_status = None
  camera_status = None
  while True:
    current_camera_status = get_camera_status()
    if current_camera_status != camera_status:
      camera_status = current_camera_status
      print('camera became', camera_status)
      print(post_entity_status(
        CAMERA_STATUS_SENSOR_NAME, CAMERA_STATUS_SENSOR_FRIENDLY_NAME,
        camera_status))

    current_monitor_status = get_monitor_status()
    if current_monitor_status != monitor_status:
      monitor_status = current_monitor_status
      print('monitor became', monitor_status)
      print(post_entity_status(
        MONITOR_STATUS_SENSOR_NAME, MONITOR_STATUS_SENSOR_FRIENDLY_NAME,
        monitor_status))


    time.sleep(POLLING_INTERVAL_SECONDS)


if __name__ == '__main__':
  main()

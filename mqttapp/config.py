import argparse
import os
import aiomqtt
from typing import Any, Dict


def get_config() -> Dict[str, Any]:
    parser = argparse.ArgumentParser()
    parser.add_argument('--component', default=os.getenv('COMPONENT', 'mqttapp'))
    parser.add_argument('--log-level', default=os.getenv('LOG_LEVEL', 'INFO'))
    return parser.parse_args()


def get_mqtt_client(component: str, will_topic: str) -> aiomqtt.Client:
    will = aiomqtt.Will(topic=will_topic, payload='offline', qos=2, retain=True)
    return aiomqtt.Client(
        os.getenv('MQTT_HOSTNAME', '127.0.0.1'),
        port=int(os.getenv('MQTT_PORT', '1883')),
        username=os.getenv('MQTT_USERNAME', None),
        password=os.getenv('MQTT_PASSWORD', None),
        identifier=os.getenv('MQTT_IDENTIFIER', 'mqttapp'),
        will=will,
    )

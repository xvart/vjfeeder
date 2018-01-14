
import os
import logging
import asyncio
import json

from hbmqtt.client import MQTTClient, ClientException
from hbmqtt.mqtt.constants import QOS_1, QOS_2
from hbmqtt.broker import Broker


import pyvjoy

logger = logging.getLogger(__name__)

#Pythonic API, item-at-a-time
j = pyvjoy.VJoyDevice(1)

#Also implemented:
j.reset()
# ~ j.reset_buttons()
# ~ j.reset_povs()

#
# This sample shows how to subscbribe a topic and receive data from incoming messages
# It subscribes to '$SYS/broker/uptime' topic and displays the first ten values returned
# by the broker.
#

myoptions = [
        ('$SYS/broker/uptime', QOS_1),
        ('$SYS/broker/load/#', QOS_2),
    ]
    
myoptions = [
    ('/vjoy/#', QOS_2),
]

config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': '0.0.0.0:1883',
        },
        'ws-mqtt': {
            'bind': '0.0.0.0:8883',
            'type': 'ws',
            'max_connections': 10,
        },
    },
    'sys_interval': 10,
    'auth': {
        'allow-anonymous': True,
        'password-file': os.path.join(os.path.dirname(os.path.realpath(__file__)), "passwd"),
        'plugins': [
            'auth_file', 'auth_anonymous'
        ]

    }
}

broker = Broker(config)

@asyncio.coroutine
def broker_coro():
    yield from broker.start()
    pass


@asyncio.coroutine
def uptime_coro():
    C = MQTTClient()
    yield from C.connect('mqtt://localhost/')
    # Subscribe to '/vjoy/#' with QOS=2
    yield from C.subscribe(myoptions)
    logger.info("Subscribed")
    try:
        mybool = True
        while True:
            message = yield from C.deliver_message()
            packet = message.publish_packet
            # Work starts here
            jstr = json.loads( packet.payload.data.decode("utf-8") )
            if jstr['type'] == "j":
                print("%s => %d => %d" % (jstr['type'], getattr(pyvjoy,jstr['index']), int(jstr['value'])))
                j.set_axis(getattr(pyvjoy,jstr['index']), int(jstr['value']))
                pass
            elif jstr['type'] == "b":
                print("%s => %s => %d" % (jstr['type'], jstr['index'], int(jstr['value'])))
                j.set_button(int(jstr['index']),jstr['value'])
            pass
        yield from C.unsubscribe(myoptions)
        logger.info("UnSubscribed")
        yield from C.disconnect()
    except ClientException as ce:
        logger.error("Client exception: %s" % ce)


if __name__ == '__main__':
    formatter = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(broker_coro())
    yield from asyncio.sleep(2)
    asyncio.get_event_loop().run_until_complete(uptime_coro())



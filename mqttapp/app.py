import asyncio
from .config import get_config, get_mqtt_client
from .log import get_logger


class App:
    def __call__(self):
        config = get_config()
        self.logger = get_logger('App', level=config.log_level)
        self.logger.debug('Config: {}'.format(config))
        self._component = config.component
        self._availability_topic = '{}/status'.format(self._component)
        self.logger.info('Starting')
        self._loop = asyncio.get_event_loop()
        self.mqtt_client = get_mqtt_client(component=self._component, will_topic=self._availability_topic)
        self._loop.run_until_complete(self._main())

    async def _main(self):
        await asyncio.sleep(1)
        async with self.mqtt_client:
            self.logger.info('Connected to broker.')
            await self.mqtt_client.publish(topic=self._availability_topic, payload='online', qos=2, retain=True)
            self.logger.info('Wait for initialize')
            await self.initialize()
            self.logger.info('Started')
            async for message in self.mqtt_client.messages:
                self.logger.debug('mqtt message received - {}: {}'.format(message.topic, message.payload.decode()))

    async def initialize(self):
        pass

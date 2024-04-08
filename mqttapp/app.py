import asyncio
from . import config
from .log import get_logger


class App:
    def __call__(self):
        app_config = config.get_config()
        self.logger = get_logger('App', level=app_config.log_level)
        self.logger.debug('config: {}'.format(app_config))
        self.component = app_config.component
        self.availability_topic = '{}/status'.format(self.component)
        self.logger.info('started')
        self.loop = asyncio.get_event_loop()
        self.client = config.get_mqtt_client(component=self.component, will_topic=self.availability_topic)
        self.loop.run_until_complete(self._main())

    async def _main(self):
        await asyncio.sleep(1)
        async with self.client:
            self.logger.info('connected to broker.')
            await self.client.publish(topic=self.availability_topic, payload='online', qos=2, retain=True)
            await self.initialize()
            async for message in self.client.messages:
                self.logger.debug('mqtt message received - {}: {}'.format(message.topic, message.payload.decode()))

    async def initialize(self):
        pass

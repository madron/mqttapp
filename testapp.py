import mqttapp


class App(mqttapp.App):
    async def initialize(self):
        await self.mqtt_client.subscribe('temperature/outside')


if __name__ == '__main__':
    App()()

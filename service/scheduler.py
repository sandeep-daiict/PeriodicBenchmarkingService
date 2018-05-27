from service_configuration import ServerConfiguration
from service import AsynchronousApiCalls
import time

class ScheduleService:
    def __init__(self):
        self.config = ServerConfiguration()
        self.service = AsynchronousApiCalls()

    def start(self):
        while True:
            self.service.call_api()
            time.sleep(self.config.period)






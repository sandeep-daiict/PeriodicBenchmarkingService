import yaml
import os.path


class RedisConfiguration:
    def __init__(self):
        current_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(current_path, "redis_config.yaml")
        with open(path) as f:
            configurations = yaml.safe_load(f)
            if configurations['debug'] == "0":
                self.local = False
                redis_config = configurations['production']
            else:
                redis_config  = configurations['local']
            self.record_expiry = redis_config['record_expiry']
            self.record_size = redis_config['record_size']
            self.response_time_expiry = redis_config['response_time_expiry']
            self.response_time_record_size = redis_config['response_time_record_size']
            self.host = redis_config['host']
            self.port = redis_config['port']

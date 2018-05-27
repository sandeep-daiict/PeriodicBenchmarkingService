import yaml
import os.path


class ServerConfiguration:
    def __init__(self):
        current_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(current_path, "service_config.yaml")
        with open(path) as f:
            configurations = yaml.safe_load(f)
            if configurations['debug'] == "0":
                self.local = False
                server_run_mode = configurations['production']
            else:
                server_run_mode = configurations['local']
            scheduler_config = server_run_mode['scheduler']
            third_party_api_config = server_run_mode['thirdpartyapi']
            self.period = scheduler_config['period']
            self.max_balance = third_party_api_config['balance_max']
            self.parallel_calls = third_party_api_config['parallel_calls']
            self.max_record = third_party_api_config['max_record']
            self.third_party_url = third_party_api_config['protocol'] + "://" \
                                   + third_party_api_config['host'] + ":" \
                                   + str(third_party_api_config['port']) \
                                   + third_party_api_config['url']
            self.record_size = third_party_api_config['record_size']

    def __repr__(self):
        """ Current server configuration"""
        return "period: " + str(self.period) + " max balance: " + str(self.max_balance)\
               + " parallel calls: " + str(self.parallel_calls) + " max records: "\
               + str(self.max_record) + " api: " + self.third_party_url + " record size:" + self.record_size
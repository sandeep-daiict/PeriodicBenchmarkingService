import yaml
import os.path


class AppConfiguration:
    def __init__(self):
        current_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(current_path, "app_config.yaml")
        with open(path) as f:
            configurations = yaml.safe_load(f)
            if configurations['debug'] == "0":
                self.local = False
                server_run_mode = configurations['production']
            else:
                server_run_mode = configurations['local']
        api_config = server_run_mode["restapi"]
        self.port = api_config["port"]
        self.host = api_config["host"]

    def __repr__(self):
        """ Current API Server configuration"""
        return "API Server Running at: " + str(self.host) + " on Port:" + str(self.port) \
               + "/records: Return records\n" + "/response_time: Return All response_times\n" \
               + "/response_time/max: Return max response_times\n" \
               + "/response_time/min: Return min response_times\n" \
               + "/response_time/average: Return average response_times\n" \
               + "/response_time/all_stats: Return tuple of(min, max, average) response_times\n"





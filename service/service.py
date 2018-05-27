import grequests
import random
import json
import sys

from service_configuration import ServerConfiguration
from model.redis_model import DataModel

class AsynchronousApiCalls:
    def __init__(self):
        self.config = ServerConfiguration()
        self.model = DataModel()

    def get_data(self):
        """
           For bank data in elastic search generating random API calls with bank balance greater than x
           maximum balance"""

        rand = lambda _: random.randint(0, self.config.max_balance)
        header = json.dumps({"query":
                      {"range" :
                           {"balance" :
                                {"gte": rand(0)}
                            }

                      },
                  "size": self.config.max_record
                })
        return header

    def call_api(self):
        """
        Calls third part API and saves the records and response time in redis
        :return:
        """
        requests = (grequests.get(self.config.third_party_url,
                     data = self.get_data()) for i in range(self.config.parallel_calls))

        responses = grequests.map(requests,
                                  exception_handler = self.failed_requests_handler)
        response_time = []
        records = []
        number_of_records = self.config.record_size
        max_time = 0
        min_time = sys.maxint
        average_time = 0
        count = 1
        for i in range(len(responses)-1, -1, -1):
            res = responses[i]
            # Failed case, We can cache this URL in redis for retrying
            if type(res) is str:
                    continue

            time_taken = res.elapsed.total_seconds()
            if number_of_records > 0:
                records.append(res.json())
                number_of_records = number_of_records - 1

            response_time.append(time_taken)#response time of all records not just small size
            if max_time < time_taken:
                max_time = time_taken
            if min_time > time_taken:
                min_time = time_taken
            average_time = (average_time + time_taken)/count
            count = count + 1
        self.model.insert_records(records)
        self.model.insert_response_time(response_time)
        self.model.insert_response_time_min(min_time)
        self.model.insert_response_time_max(max_time)
        self.model.insert_response_time_average(average_time)
        print "Data inserted in Redis Sucessfully!!"

    def failed_requests_handler(self, request, exception):
        """ For failed API request we are sending request URL as a
        return value. We can cache them in redis/other DB for retry.
         Out of scope for this poject"""
        failed_url = request.url
        return failed_url

import redis
from redis_configuration import RedisConfiguration


class DataModel:
    def __init__(self):
        self.configuration = RedisConfiguration()
        self.connection = redis.Redis(host=self.configuration.host, port=self.configuration.port, db=0)
        self.count_key = "count"
        self.record_key = "records"
        self.response_time_key = "rtime"
        self.min_response_time_key = "minrtime"
        self.max_response_time_key = "maxrtime"
        self.average_response_time_key = "averagertime"

    def insert_records(self, records):
        for record in records:
            self.connection.lpush(self.record_key, record)
            self.connection.ltrim(self.record_key, 0, self.configuration.record_size - 1)

    def get_records(self):
        return self.connection.lrange(self.record_key, 0, self.configuration.record_size - 1)

    def insert_response_time(self, response_time):
        """inserts all response time with expiry. all
        response time for api calls are added as seperate
        key with increasing counter saved in redis as count key"""

        count = self.connection.incr(self.count_key)
        # to avoid count key overflow.
        if count > 1000:
            count = 1
            self.connection.set(self.count_key, count)

        key = self.response_time_key + str(count)
        self.connection.lpush(key, response_time)
        self.connection.expire(key, self.configuration.response_time_expiry)

    def get_response_time_records(self):
        """
        get all keys which are not expired with rtime prefix and returns all record times
        :return: list of all response time records
        """
        keys = self.connection.keys(self.response_time_key + "*")
        response_times = []
        for k in keys:
            response_times.append(self.connection.lrange(k,0,-1))
        return response_times

    def insert_response_time_min(self, min_rtime):
        """
        Inserts a record of min,max and average response times
        :return:
        """
        self.__insert_response_time_stats(self.min_response_time_key, min_rtime,
                                     self.configuration.response_time_record_size)


    def insert_response_time_max(self, max_rtime):
        """
        Inserts a record of min,max and average response times
        :return:
        """
        self.__insert_response_time_stats(self.max_response_time_key, max_rtime,
                                     self.configuration.response_time_record_size)

    def insert_response_time_average(self, avergae_rtime):
        """
        Inserts a record of min,max and average response times
        :return:
        """
        self.__insert_response_time_stats(self.average_response_time_key, avergae_rtime,
                                     self.configuration.response_time_record_size)

    def __insert_response_time_stats(self, key, rtime, size):
        self.connection.lpush(key, rtime)
        # To keep fix size
        self.connection.ltrim(key, 0, size - 1)

    def __get_record_time_stats(self, key):
        return self.connection.lrange(key, 0, self.configuration.response_time_record_size - 1)

    def get_response_time_min(self):
        return self.__get_record_time_stats(self.min_response_time_key)

    def get_response_time_max(self):
        return self.__get_record_time_stats(self.max_response_time_key)

    def get_response_time_average(self):
        return self.__get_record_time_stats(self.average_response_time_key)

    def get_response_time_all_stats(self):
        return zip(self.get_response_time_min(), self.get_response_time_max(), self.get_response_time_average())


if __name__ == "__main__":
    D = DataModel()

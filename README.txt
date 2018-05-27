Python Project to store 3rd Party API responses for purpose of benchmarking.
Components:-

1) Third Party API:
	Used Local Elastic search For Third party API. It can handle much more than 1000 parallel requests.
	Bank data is used to store in elsatic search(data/accounts.json) and randomly generated
	Balance to call Elastic search REST API with balance > random generated number.
	This gives randomness in API call. service_config Files handles Third party API related configs.


2) Service:(service.py) This handles making 1000 asynchronous requests(using grequests) to third party API.
   number of parallel calls can be changed from config

3) Scheduler: This continuously  calls service to fetch data from third party API. Period can be configured,
    Its set as 0sec now.

4) Redis Cache(model package): This is used to store records and response time related information return by
    third party API. Service use this model to insert in redis cache.

5) Flask Rest API: Flask endpoint to provide REST API's to get data from redis.
    API's Are: All API's return json with "data" as array of record. Response json has count and status fields also.
        /response_time: Return All response_times
        /response_time/max: Return max response_times
        /response_time/min: Return min response_times
        /response_time/average: Return average response_times
        /response_time/all_stats: Return tuple of(min, max, average) response_times

Third Party API setup For test using elastic search:
    1. Download elastic search: curl -L -O https://download.elastic.co/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.4.6/elasticsearch-2.4.6.tar.gz
        Elastic search needs java. or use elastic search folder.
    2. tar -xvf elasticsearch-2.4.6.tar.gz
    3. cd elasticsearch-2.4.6/bin
    4. ./elasticsearch --cluster.name third_party_api_cluster --node.name third_party_api_node
        (this run in default port) it can be changed
    5. To load data: curl -H 'Content-Type: application/x-ndjson' -XPOST 'localhost:9200/bank/account/_bulk?pretty' --data-binary @accounts.json
    6. Check by command
            GET /_cat/indices?v   : It will show Bank indices. This means third API is ready

Dependecies:
1) install grequests There maybe issue with gevent in installation
2) install flask (Rest API)
3) Download redis and run server
4) install redis (pip install redis)

How to run
1) Run elastic search: ./elasticsearch --cluster.name third_party_api_cluster --node.name third_party_api_node
2) Run Redis server: redis-server
3) python start.py
4) python app.py

USE curl api calls to check the result
/response_time
/response_time/max
/response_time/min
/response_time/average
/response_time/all_stats

Future Work.
1. No Exception Handling like Redis Connection fail.
2. If third Party API call fails cache failed URl in redis and retry.




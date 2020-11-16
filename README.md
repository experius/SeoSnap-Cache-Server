# Rendertron Cache Server
Cache server for between the rendertron cache server and the client. 
Caches rendertron urls using file cache. No documents are preserved in memory.

## Setup (Docker)
* (Optional) Update env.docker variables to match your preferred configuration. (Like cache path)
* Update the docker compose file. Comment / uncomment startup of the rendertron server
* Run `docker compose up`

## Usage
Route should be formatted as follows: `/render/your url`
* GET - Retrieves and caches the page (if cached the cache will be used)
* PUT - Invalidates cache for given url and retrieves it's content
* DELETE - Invalidates cache for given url and all it's sub paths
* GET with route /list/url - Lists all cached pages and their children.

## Benchmarks Results
 ```
Running 30s test @ http://172.18.17.200:5000/render/http://www.google.com/
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   101.97ms  237.27ms   1.99s    92.62%
    Req/Sec   533.00    382.37     3.08k    85.50%
  125325 requests in 30.08s, 5.44GB read
Requests/sec:   4168.54
Transfer/sec:    201.045MB

```

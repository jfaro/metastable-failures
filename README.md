# Metastable Failure Testing

Metastable failure testing in microservice architectures. 

# Getting started

Clone this repository and our DeathStarBench fork, [jfaro/DeathStarBench](https://github.com/jfaro/DeathStarBench).
```bash
git clone https://github.com/jfaro/metastable-failures
git clone https://github.com/jfaro/DeathStarBench
```

## Benchmark setup

Navigate into the `DeathStarBench/socialNetwork` directory.

```bash
cd ./DeathStarBench/socialNetwork
```

Follow the setup steps detailed [in the original README](https://github.com/jfaro/DeathStarBench/tree/master/socialNetwork). Ensure you have all the requirements listed.

Rebuild the `wrk` workload generation executable.
```bash
cd ./wrk2; make
```

Use the included makefile (`DeathStarBench/socialNetwork/Makefile`) for convenience when executing the following commands. 

```bash
make rebuild            # docker build -t jfaro:test .
make compose-up         # docker-compose -p jfaro up -d
make compose-down       # docker-compose -p jfaro down
make logs               # docker logs jfaro_compose-post-service_1`
```

*Note:*, `jfaro` can be replaced with whatever tag you choose. Just ensure you use the same tag in the `metastable-failures/src/config.py`.

## Setting up the workload generator

Navigate into the freshly cloned `metastable-failures` directory.

```bash
cd metastable-failures
```

Create a virtual environment and install dependencies.
```bash
# Navigate into the cloned repository
cd ./metastable-failures

# Create and activate a virtual environment
python -m venv env
source env/bin/activate

# Install dependencies
make init
```


# Running workload experiments

Setup your experiment configuration in `metastable-failures/src/config.py`.

**Example configuration:**
```python3
PATH_TO_SOCIAL_NETWORK = '/home/jfaro/src/DeathStarBench/socialNetwork'
WRK_DIR = 'wrk2'

# Workload configuration
NUM_THREADS = 1
NUM_CONNECTIONS = 10
DURATION = 40
REQUESTS_PER_SECOND = 100
SCRIPT_TO_RUN = './scripts/social-network/compose-post.lua'
URL = 'http://localhost:8090/wrk2-api/post/compose'

# Docker
CONTAINER_TO_MONITOR = 'jfaro_compose-post-service_1'
CONTAINER_TO_DISCONNECT = 'jfaro_post-storage-mongodb_1'
DOCKER_NETWORK = 'jfaro_default'
NETWORK_OUTAGE_START = 10           # Start outage after _ seconds
NETWORK_OUTAGE_DURATION = 20        # Outage duration
```

Start DeathStarBench social network.

```bash
pwd                     # src/DeathStarBench/socialNetwork
make rebuild
make compose-up
```

Run workload.
```bash
pwd                     # src/metastable-failures

# python src/main.py
make run
```

Results are printed to stdout and figures are saved in `metastable-failures/results`.

<img src="/results-cache/latencies-t0.png" style="width: 320px;" alt="latency per request" />

A set of figures is created for each thread running the workload, or `config.NUM_THREADS` total sets. Each set contains the following:
- Latency per request plot (`results/latencies-t<THREAD_NUM>.png`)
- Latency distribution (`results/latency-hist-t<THREAD_NUM>.png`)

Additionally, a plot is generated displaying the `config.CONTAINER_TO_MONITOR` container's memory usage over the duration of the workload
- Memory usage over time (`results/memory-usage.png`)

## Project structure

```
├── src/
|   |── cmd.py          # easy command line interaction
|   |── config.py       # project configuration
|   |── docker.py       # docker manipulation
|   |── main.py         # program driver
|   |── parser.py       # wrk parsing
|   |── plots.py        # plot generation
|   └── wrk.py          # workload generation
|
├── results/
|
|── Makefile            # for convenience
└── requirements.txt    # dependencies
```

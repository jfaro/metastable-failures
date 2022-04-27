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
make logs               # docker logs jfaro_compose-post-service_`
```

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

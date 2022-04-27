# Metastable Failure Testing

Metastable failure testing in microservice architectures. 

## Getting started

Clone this repository and our DeathStarBench fork, [jfaro/DeathStarBench](https://github.com/jfaro/DeathStarBench).
```bash
git clone https://github.com/jfaro/metastable-failures
git clone https://github.com/jfaro/DeathStarBench
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

### Benchmark setup

Navigate into the `DeathStarBench/socialNetwork` directory.

```bash
cd ../DeathStarBench
```
follow the setup steps detailed [in the original README](https://github.com/jfaro/DeathStarBench/tree/master/socialNetwork). Ensure you have all the requirements listed.

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



###



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
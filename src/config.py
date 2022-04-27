import os


# Paths
SRC = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SRC)
RESULTS = os.path.join(ROOT, 'results')

# wrk location
PATH_TO_SOCIAL_NETWORK = '/home/jfaro/src/DeathStarBench/socialNetwork'
WRK_DIR = 'wrk2'

# Workload configuration
NUM_THREADS = 1
NUM_CONNECTIONS = 10
DURATION = 120
REQUESTS_PER_SECOND = 100
SCRIPT_TO_RUN = './scripts/social-network/compose-post.lua'
URL = 'http://localhost:8090/wrk2-api/post/compose'

# Docker
CONTAINER_TO_MONITOR = 'jfaro_compose-post-service_1'
CONTAINER_TO_DISCONNECT = 'jfaro_post-storage-mongodb_1'
DOCKER_NETWORK = 'jfaro_default'
NETWORK_OUTAGE_START = 10           # Start outage after _ seconds
NETWORK_OUTAGE_DURATION = 20        # Outage duration

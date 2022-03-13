import os
import subprocess
from time import sleep


# Configuration
PATH_TO_SOCIAL_NETWORK = '/home/jfaro/src/DeathStarBench/socialNetwork'
WRK_DIR = 'wrk2'


# Process management
# TODO: append new processes here
processes = [
    # workload
    # start/stop network connection
]


def main():
    # Change to wrk directory
    wrk_dir = os.path.join(PATH_TO_SOCIAL_NETWORK, WRK_DIR)
    os.chdir(wrk_dir)

    # Run workload
    NUM_THREADS = 1
    NUM_CONNECTIONS = 1000
    DURATION = 10
    REQUESTS_PER_SECOND = 50
    SCRIPT_TO_RUN = './scripts/social-network/compose-post.lua'

    command = ['./wrk', '-D', 'exp',
        '-t', str(NUM_THREADS),
        '-c', str(NUM_CONNECTIONS),
        '-d', str(DURATION),
        '-L', '-s',
        SCRIPT_TO_RUN, 
        'http://localhost:8080/wrk2-api/post/compose',
        '-R', str(REQUESTS_PER_SECOND)
    ]

    print("Generating workload...")
    process = subprocess.run(command, stdout=subprocess.PIPE, universal_newlines=True)
    sleep(.5)

    print("Disconnecting from network")
    change_network_connection('disconnect')
    sleep(5)

    print("Reconnecting network")
    change_network_connection('connect')

    print(process.stdout)


# Action: 'disconnect' | 'connect'
def change_network_connection(action='disconnect'):
    assert(action == 'disconnect' or action == 'connect')
    container = 'socialnetwork_post-storage-service_1'

    command = [
        'docker', 'network', action,
        'socialnetwork_default',
        container
    ]
    subprocess.run(command, stdout=subprocess.PIPE, universal_newlines=True)


main()
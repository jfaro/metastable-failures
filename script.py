import os
import subprocess
import json
from time import sleep
from wrk_parser import parse_wrk_output

PATH_TO_SOCIAL_NETWORK = '/home/jfaro/src/DeathStarBench/socialNetwork'
WRK_DIR = 'wrk2'

# Run workload
NUM_THREADS = 1
NUM_CONNECTIONS = 100
DURATION = 10
REQUESTS_PER_SECOND = 50
SCRIPT_TO_RUN = './scripts/social-network/compose-post.lua'
URL = 'http://localhost:8080/wrk2-api/post/compose'


def cmd_output(command_list):
    process = subprocess.run(command_list, stdout=subprocess.PIPE, universal_newlines=True)
    return process.stdout


# Generate workload with wrk
def run_wrk():

    # Change to wrk directory
    wrk_dir = os.path.join(PATH_TO_SOCIAL_NETWORK, WRK_DIR)
    os.chdir(wrk_dir)

    print("Active directory:", cmd_output(['pwd']))

    # wrk2 command
    args = [
        './wrk', 
        '-D', 'exp',                    # fixed, exp, norm, zipf
        f'-t {NUM_THREADS}',            # Number of threads to use
        f'-c {NUM_CONNECTIONS}',        # Connections to keep open
        f'-d {DURATION}s',              # Duration to test
        '--latency',                    # Output latency information
        f'-R {REQUESTS_PER_SECOND}',    # Work rate (throughput) in requests/sec (total)

        f'-s {SCRIPT_TO_RUN}',
        URL,
    ]

    print("Generating workload...")
    print(" ".join(args))
    args_str = " ".join(args)
    process = subprocess.Popen(args_str, stdout=subprocess.PIPE, text=True, shell=True)
    return process


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


def main():

    # Create workload
    wrk_process = run_wrk()

    # Wait for process to complete
    while wrk_process.poll() is None:
        print("wrk running...")
        sleep(2)

    # Get output
    stdout, stderr = wrk_process.communicate()
    print(stdout)

    wrk_output_dict = parse_wrk_output(stdout)
    print(json.dumps(wrk_output_dict, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
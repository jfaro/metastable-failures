import os
import re
import subprocess
import threading
import time
import config
import cmd
from docker import get_container_stats
from parser import parse_wrk_output

# Generate workload with wrk
# Returns parent process


def generate_workload():

    # Change to wrk directory
    wrk_dir = os.path.join(config.PATH_TO_SOCIAL_NETWORK, config.WRK_DIR)
    os.chdir(wrk_dir)
    print("Active directory:", cmd.get_process_output(['pwd']))

    # wrk2 command
    args = [
        './wrk',
        '-D', 'exp',                           # fixed | exp |norm | zipf
        '-P',                                  # Print each request's latency
        f'-t {config.NUM_THREADS}',            # Number of threads to use
        f'-c {config.NUM_CONNECTIONS}',        # Connections to keep open
        f'-d {config.DURATION}s',              # Duration to test
        '--latency',                           # Output latency information
        # Work rate (throughput) in requests/sec (total)
        f'-R {config.REQUESTS_PER_SECOND}',
        f'-s {config.SCRIPT_TO_RUN}',          # Lua script to run
        config.URL,
    ]

    # Convert above list to str
    args_str = " ".join(args)

    print("Generating workload")
    print(args_str)
    process = subprocess.Popen(args_str,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True, shell=True)
    return process


# Generate a workload
# Return stdout, stderr
class WorkloadThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stdout = None
        self.stderr = None
        self.output_dict = None
        self.stats = []
        self.starttime = time.time()

    def run(self):
        wrk_process = generate_workload()

        # Wait for workload to finish
        while wrk_process.poll() is None:
            time.sleep(.2)
            stats = get_container_stats(config.CONTAINER_TO_MONITOR)
            stats['timestamp'] = time.time() - self.starttime
            self.stats.append(stats)

        self.stdout, self.stderr = wrk_process.communicate()
        self.output_dict = parse_wrk_output(self.stdout)

    def join(self, *args):
        threading.Thread.join(self, *args)
        return self.stdout, self.stderr, self.output_dict, self.stats

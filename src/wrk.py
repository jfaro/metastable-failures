import os
import subprocess
import config


def cmd_output(command_list):
    process = subprocess.run(command_list, stdout=subprocess.PIPE, 
                             universal_newlines=True)
    return process.stdout


# Generate workload with wrk
# Returns parent process 
def generate_workload():

    # Change to wrk directory
    wrk_dir = os.path.join(config.PATH_TO_SOCIAL_NETWORK, config.WRK_DIR)
    os.chdir(wrk_dir)
    print("Active directory:", cmd_output(['pwd']))

    # wrk2 command
    args = [
        './wrk', 
        '-D', 'exp',                           # fixed | exp |norm | zipf
        '-P',                                  # Print each request's latency
        f'-t {config.NUM_THREADS}',            # Number of threads to use
        f'-c {config.NUM_CONNECTIONS}',        # Connections to keep open
        f'-d {config.DURATION}s',              # Duration to test
        '--latency',                           # Output latency information
        f'-R {config.REQUESTS_PER_SECOND}',    # Work rate (throughput) in requests/sec (total)
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

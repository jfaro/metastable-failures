import os
import json
from time import sleep
import config
from wrk import generate_workload
from parser import parse_wrk_output
from plots import plot_latency_distribution, plot_latency_per_request


def main():
    # Create workload
    wrk_process = generate_workload()

    # Wait for process to complete
    while wrk_process.poll() is None:
        sleep(2)

    # Print output
    stdout, stderr = wrk_process.communicate()
    if stdout:
        print("Workload stdout\n", stdout)
    if stderr:
        print("Workload stderr\n", stderr)

    # Generate plots
    print("Workload output dict:")
    wrk_output_dict = parse_wrk_output(stdout)
    print(json.dumps(wrk_output_dict, indent=4, sort_keys=True))

    # Clear results folder
    dir = os.path.join(config.ROOT, 'results')
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    # Plot latency information
    plot_latency_per_request()
    plot_latency_distribution()


if __name__ == "__main__":
    main()

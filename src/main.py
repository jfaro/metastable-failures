import os
import json
import config
from wrk import WorkloadThread
from docker import NetworkOutageThread
from plots import plot_latency_distribution, plot_latency_per_request, plot_memory_usage


def main():

    # Handle network outage
    networkOutageThread = NetworkOutageThread(
        config.CONTAINER_TO_DISCONNECT,
        config.DOCKER_NETWORK,
        config.NETWORK_OUTAGE_START,
        config.NETWORK_OUTAGE_DURATION
    )

    # Handle workload generation
    workloadThread = WorkloadThread()

    # Start threads
    workloadThread.start()
    networkOutageThread.start()

    # Wait for all threads to complete
    stdout, stderr, output_dict, stats = workloadThread.join()
    networkOutageThread.join()

    # Print output
    if stdout:
        print("Workload stdout\n", stdout)
    if stderr:
        print("Workload stderr\n", stderr)

    # Print output dictionary
    print("Workload output dict:")
    print(json.dumps(output_dict, indent=4, sort_keys=True))

    # Clear results folder
    dir = os.path.join(config.ROOT, 'results')
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

    # Print stats
    # print(json.dumps(stats, indent=4, sort_keys=True))

    # Plot latency information
    plot_latency_per_request()
    plot_latency_distribution()
    plot_memory_usage(stats)


if __name__ == "__main__":
    main()

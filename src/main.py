import os
import json
from time import sleep, time
import config
from wrk import generate_workload
from parser import parse_wrk_output
from plots import plot_latency_distribution, plot_latency_per_request
from docker import get_container_stats, update_network_connection
from cmd import get_process_output


def main():
    # Create workload
    wrk_process = generate_workload()
    start_time = time()
    network_disabled = False
    network_reenabled = False

    # Wait for process to complete
    while wrk_process.poll() is None:
        current_time = time()
        elapsed_time = current_time - start_time

        print("Current:", current_time, "| Start :",
              start_time, "| Elapsed", elapsed_time)
        # print(get_container_stats(config.CONTAINER_TO_MONITOR))

        # Disable network
        if elapsed_time > config.DISCONNECT_NET_AFTER_SEC and not network_disabled:
            print("Disconnect network", current_time)
            update_network_connection(config.CONTAINER_TO_DISCONNECT,
                                      config.DOCKER_NETWORK,
                                      enable_connection=False)
            print("DISCONNECT COMMAND DONE")
            sleep(2)
            output = get_process_output(
                ['docker', 'inspect', config.CONTAINER_TO_DISCONNECT, '-f', '{{json .NetworkSettings.Networks }}'])
            print("DOCKER INSPECT OUTPUT:", output)
            network_disabled = True

        # Enable network
        time_to_reconnect = config.DISCONNECT_NET_AFTER_SEC + config.NETWORK_OUTAGE_DURATION
        if elapsed_time > time_to_reconnect and not network_reenabled:
            print("Reconnect network", current_time)
            update_network_connection(config.CONTAINER_TO_DISCONNECT,
                                      config.DOCKER_NETWORK,
                                      enable_connection=True)
            network_reenabled = True

        # Go to bed
        sleep(.5)

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

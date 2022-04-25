import re
import os
import time
import threading
import config
from cmd import get_process_output


# Run docker stats for a container
def get_container_stats(container_name):
    os.chdir(config.PATH_TO_SOCIAL_NETWORK)
    command_list = ['docker', 'stats', container_name, '--no-stream']
    stdout = get_process_output(command_list)
    stats = parse_container_stats(stdout)
    return stats


def parse_container_stats(stats_str):
    stats_str = stats_str.splitlines()[1]       # Only need second line
    str_list = stats_str.split()                # Split by whitespace
    float_pattern = "[0-9]*\.?[0-9]*"           # Match for floats

    res = {
        'container_id': str_list[0],
        'container_name': str_list[1],
        'cpu_usage': float(re.findall(float_pattern, str_list[2])[0]),
        'mem_usage': float(re.findall(float_pattern, str_list[3])[0]),
        'mem_capacity': float(re.findall(float_pattern, str_list[5])[0]),
        'net_io_usage': float(re.findall(float_pattern, str_list[7])[0]),
        'net_io_capacity': float(re.findall(float_pattern, str_list[9])[0]),
    }

    return res


# Connect/disconnect container with name <container>, from network with name
# <network>.
# enable_connection=True  : connect
# enable_connection=False : disconnect
def update_network_connection(container, network, enable_connection=True):
    os.chdir(config.PATH_TO_SOCIAL_NETWORK)
    connect_command = ['docker', 'network', 'connect',
                       network, container]
    disconnect_command = ['docker', 'network', 'disconnect', '-f',
                          network, container]

    command_list = connect_command if enable_connection else disconnect_command

    print(" ".join(command_list))
    stdout = get_process_output(command_list)
    return stdout


# Disconnect container from network after <start_after> seconds.
# Outage will last <duration> seconds before reconnecting
class NetworkOutageThread(threading.Thread):
    def __init__(self, container, network, start_after, duration):
        threading.Thread.__init__(self)
        self.container = container
        self.network = network
        self.start_after = start_after
        self.duration = duration

    def run(self):
        time.sleep(self.start_after)
        update_network_connection(self.container, self.network, False)
        time.sleep(self.duration)
        update_network_connection(self.container, self.network, True)

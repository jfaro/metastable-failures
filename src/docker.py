import os
import config
from cmd import get_process_output


def get_container_stats(container_name):
    os.chdir(config.PATH_TO_SOCIAL_NETWORK)
    command_list = ['docker', 'stats', container_name, '--no-stream']
    stdout = get_process_output(command_list)
    return stdout


def update_network_connection(container_name, network_name, enable_connection=True):
    os.chdir(config.PATH_TO_SOCIAL_NETWORK)
    connect_command = ['docker', 'network', 'connect',
                       network_name, container_name]
    disconnect_command = ['docker', 'network', 'disconnect', '-f',
                          network_name, container_name]

    command_list = connect_command if enable_connection else disconnect_command

    print(" ".join(command_list))
    stdout = get_process_output(command_list)
    return stdout

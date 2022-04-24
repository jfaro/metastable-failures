import subprocess


def get_process_output(command_list):
    process = subprocess.run(command_list, stdout=subprocess.PIPE,
                             universal_newlines=True)
    return process.stdout

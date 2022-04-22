import os
import glob
import matplotlib.pyplot as plt
import numpy as np
from config import PATH_TO_SOCIAL_NETWORK, WRK_DIR, RESULTS

# Plot each request's latency
# Takes as input a filepath to a file that contains the list of latencies


def plot_latency_per_request():

    data_filepath = os.path.join(
        PATH_TO_SOCIAL_NETWORK, WRK_DIR, 'latencies.txt')

    with open(data_filepath, 'r') as latencies_file:

        # Read lines from file
        lines = [line.strip() for line in latencies_file]

        for i, line in enumerate(lines):
            request_latencies_list = line.split(sep=' ')

            # Create data
            num_requests = len(request_latencies_list)
            x = np.linspace(0, num_requests, num_requests)
            y = [int(latency) for latency in request_latencies_list]

            # Create plot
            fig, ax = plt.subplots()
            ax.plot(x, y, linewidth=2.0)
            ax.set_xlabel('Request')
            ax.set_ylabel('Latency (μs)')

            # Save
            plt.savefig(os.path.join(RESULTS, f'latencies-t{i}.png'))
            print(f"Saved 'latencies-t{i}.png'")


# Plot request latency distribution
def plot_latency_distribution():

    data_filepath = os.path.join(
        PATH_TO_SOCIAL_NETWORK, WRK_DIR, 'latencies.txt')

    with open(data_filepath, 'r') as latencies_file:

        # Read lines from file
        lines = [line.strip() for line in latencies_file]

        for i, line in enumerate(lines):
            request_latencies_list = line.split(sep=' ')

            # Create data
            num_requests = len(request_latencies_list)
            latencies = [int(line) for line in request_latencies_list]
            num_bins = 100

            # Create plot
            fig, ax = plt.subplots()
            ax.hist(latencies, bins=num_bins)
            ax.set_xlabel('Latency (μs)')
            ax.set_ylabel('Frequency')

            # Save
            plt.savefig(os.path.join(RESULTS, f'latency-hist-t{i}.png'))
            print(f"Saved 'latency-hist-t{i}.png'")

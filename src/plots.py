import os
import matplotlib.pyplot as plt
import numpy as np
from config import PATH_TO_SOCIAL_NETWORK, WRK_DIR, RESULTS

# Plot each request's latency
# Takes as input a filepath to a file that contains the list of latencies
def plot_latency_per_request():

    data_filepath = os.path.join(PATH_TO_SOCIAL_NETWORK, WRK_DIR, '0.txt')

    with open(data_filepath, 'r') as latencies_file:

        # Read lines from file
        lines = [ line.strip() for line in latencies_file ]

        # Create data
        num_requests = len(lines)
        x = np.linspace(0, num_requests, num_requests)
        y = [ int(line) for line in lines]

        # Create plot
        fig, ax = plt.subplots()
        ax.plot(x, y, linewidth=2.0)
        ax.set_xlabel('Request')
        ax.set_ylabel('Latency (μs)')

        # Save
        plt.savefig(os.path.join(RESULTS, 'latency-per-req.png'))
        print("Saved 'latency-per-request.png'")


# Plot request latency distribution
def plot_latency_distribution():
    
    data_filepath = os.path.join(PATH_TO_SOCIAL_NETWORK, WRK_DIR, '0.txt')

    with open(data_filepath, 'r') as latencies_file:

        # Read lines from file
        lines = [ line.strip() for line in latencies_file ]

        # Create data
        num_requests = len(lines)
        latencies = [ int(line) for line in lines]
        num_bins = 100

        # Create plot
        fig, ax = plt.subplots()
        ax.hist(latencies, bins=num_bins)
        ax.set_xlabel('Latency (μs)')
        ax.set_ylabel('Frequency')

        # Save
        plt.savefig(os.path.join(RESULTS, 'latency-per-req-hist.png'))
        print("Saved 'latency-per-req-hist.png'")

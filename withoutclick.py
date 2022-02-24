import os
import csv
from pythonping import ping
from tcp_latency import measure_latency
from matplotlib import pyplot as plt
import sys

# import click
# from rich.console import Console


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n]: "
    elif default == "yes":
        prompt = " [Y/n]: "
    elif default == "no":
        prompt = " [y/N]: "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write(
                "Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")


def plot_latency_graph(latency_data, time_values):
    plt.style.use("seaborn")

    plt.figure(figsize=(10, 5))
    plt.tight_layout()

    plt.plot(time_values, latency_data, linestyle="solid")
    plt.xlabel("Time (in secs)")
    plt.ylabel("Latency (in ms)")

    plt.savefig('network_latency.png')
    plt.show()


def cli():
    FILE_NAME = "output.txt"
    latency_data = []
    count_data = []
    time_data = []

    host = input("Enter the host IP address: ")
    protocol = input("Select Protocol [TCP(t) | ICMP(i)]: ").lower()
    dynamic = query_yes_no(
        "Do you want to send multiple segments of packets")
    graph = query_yes_no(
        "Do you want to plot a latency vs time graph?")

    if protocol == "tcp" or "t":
        port = int(input("Enter port number: "))

    if dynamic:
        segment = int(input("\nEnter the number of segments: "))

        for i in range(segment):
            if(segment > 1):
                print("\nFor segment " + str(i+1) + ": ")
            count_data.append(
                int(input("Enter the number of packets to be sent: ")))
            time_data.append(
                int(input("Enter the time (in secs) for which packets are to be sent: ")))
    else:
        count_data.append(
            int(input("\nEnter the number of packets to be sent: ")))
        time_data.append(
            int(input("Enter the time (in secs) for which packets are to be sent: ")))

    try:
        print("Pinging " + str(host) + "...")
        if(protocol == "icmp" or protocol == "i"):
            for count, time in zip(count_data, time_data):
                with open(FILE_NAME, "w") as f:
                    ping(host, verbose=True,
                         interval=time / count, count=count, out=f)

                with open(FILE_NAME, "r") as f:
                    data = f.read()

                    for x in data.split():
                        if "ms" in x:
                            latency_data.append(float(x.replace("ms", "")))
                        if x == "Request":
                            latency_data.append(0)
            if os.path.exists(FILE_NAME):
                os.remove(FILE_NAME)
        elif protocol == "tcp" or protocol == "t":
            for count, time in zip(count_data, time_data):
                latency_data.extend([round(x, 2) for x in measure_latency(
                    host, runs=count, wait=time / count, human_output=False, port=port)])
        else:
            raise Exception("[ERROR]: Invalid Protocol")

        if len(latency_data) == 0:
            raise Exception(
                "[ERROR]: The host does not exist or Request timed out")

        print("\nMinimum Latency: " + str(min(latency_data)) + "ms")
        print("Maximum Latency: " + str(max(latency_data)) + "ms")
        print("Average Latency: " +
              str(round(sum(latency_data) / len(latency_data), 2)) + "ms\n")

        time_values = []
        value = 0
        while value < sum(time_data):
            time_values.append(value)
            value += round(sum(time_data) / sum(count_data), 2)
        print("Latency Data: ", latency_data)
        # print("Time Data: ", time_values)

        with open('network_latency.csv', 'w', encoding='UTF8', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(latency_data)
            writer.writerow(time_values)

        if graph:
            plot_latency_graph(latency_data, time_values)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    cli()

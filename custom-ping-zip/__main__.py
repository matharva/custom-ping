import csv
from pythonping import ping
from tcp_latency import measure_latency
# from matplotlib import pyplot as plt
import click


# def plot_latency_graph(latency_data, time_values):
#     plt.style.use("seaborn")

#     plt.figure(figsize=(10, 5))
#     plt.tight_layout()

#     plt.plot(time_values, latency_data, linestyle="solid")
#     plt.xlabel("Time (in secs)")
#     plt.ylabel("Latency (in ms)")

#     plt.savefig('network_latency.png')
#     plt.show()


@click.command()
@click.option('-D', '--dynamic', help='Send multiple segments of packets', is_flag=True)
@click.option('-P', '--protocol', default="ICMP", help="Default: ICMP", type=click.Choice(['ICMP', 'TCP'], case_sensitive=False))
@click.option('-O', '--output', help='Get the latency v/s time data in a CSV', is_flag=True)
@click.argument('host')
def cli(host, protocol, dynamic, output):
    FILE_NAME = "output.txt"
    latency_data = []
    count_data = []
    time_data = []

    if protocol == "TCP":
        port = input("Enter port number: ")

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
        if(protocol == "ICMP"):
            for count, time in zip(count_data, time_data):
                ping_data = ping(host, verbose=False,
                                 interval=time / count, count=count, out_format=None)

                for x in str(ping_data).split():
                    if "ms=" in x:
                        latency_data.append(float(x.replace("ms=", "")))
                    if x == "Timed":
                        latency_data.append(0)

        elif protocol == "TCP":
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

        time_values_temp = []
        value = 0
        while value < sum(time_data):
            time_values_temp.append(value)
            value += round(sum(time_data) / sum(count_data), 2)
        print("Latency Data: ", latency_data)

        time_values = [round(float(i), 2) for i in time_values_temp]

        print("Time Data: ", time_values)

        if output:
            with open('network_latency.csv', 'w', encoding='UTF8', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(latency_data)
                writer.writerow(time_values)

        # plot_latency_graph(latency_data, time_values)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    cli()

# import click  
# from matplotlib import pyplot as plt
import csv
from vendor_dependencies.pythonping import ping
# from vendor_dependencies.rich.console import Console
from vendor_dependencies.tcp_latency import measure_latency
# from vendor_dependencies.numpy import arange  

# https://stackoverflow.com/questions/21981796/cannot-ping-aws-ec2-instance


# def plot_latency_graph(latency_data, time_values):
#     plt.style.use("seaborn")

#     plt.figure(figsize=(10, 5))
#     plt.tight_layout()

#     plt.plot(time_values, latency_data, linestyle="solid")
#     plt.xlabel("Time (in secs)")
#     plt.ylabel("Latency (in ms)")

#     plt.savefig('network_latency.png')
#     plt.show()


# @click.command()
# @click.option('-c', '--count', default=4, help='Number of packets to be sent')
# @click.option('-S', '--segment', help='Number of segments', default=1)
# # @click.option('-s', '--size', help='Packet size for each packet sent', default=32)
# @click.option('-t', '--time', help='Send packets for what period of time (in secs)', default=4)
# # @click.option('-l', '--preload', help='Send number of packets without waiting for a response', default=3)
# @click.argument('host')
# def cli(host: str, count: int, time: int, segment: int):
def cli():
    latency_data = []
    count_data = []
    time_data = []
    host = input("Enter the host: ").strip()
    segment = int(input("Enter the number of segments: "))

    for i in range(segment):
        if(segment > 1):
            print(f"For segment {i+1}: ")
        count_data.append(
            int(input("Enter the number of packets to be sent: ")))
        time_data.append(int(
            input("Enter the time (in secs) for which packets are to be sent: ")))
    
    protocol = input("Select a protocol(TCP(t) / ICMP(i)): ")

    # console = Console()
    # with console.status(f"[bold green]Pinging {host} ...") as status:

    if(protocol == "i"):
        for count, time in zip(count_data, time_data):
            with open("output.txt", "w") as f:
                ping(host, verbose=True,
                    interval=time / count, count=count, out=f)

            with open("output.txt", "r") as f:
                data = f.read()

                for x in data.split():
                    if "ms" in x:
                        latency_data.append(float(x.replace("ms", "")))
                    if x == "Request":
                        latency_data.append(0)
    else: 
        for count, time in zip(count_data, time_data):
            latency_data.extend([round(x, 2) for x in measure_latency(host, runs=count, wait=time / count, human_output=False)])

    print(f"Minimum Latency: {min(latency_data)}ms")
    print(f"Maximum Latency: {max(latency_data)}ms")
    print(f"Average Latency: {round(sum(latency_data) / len(latency_data), 2)}ms")

    # time_values = [round(x, 1) for x in arange(

    #     0, sum(time_data), sum(time_data) / sum(count_data))]
    # time_values = [x + sum(time_data) / sum(count_data) for x in range(sum(time_data))]
    time_values = []
    value = 0
    while value < sum(time_data):
        time_values.append(value)
        value += round(sum(time_data) / sum(count_data), 1)
    print("Latency Data: ", latency_data)
    print("Time Data: ", time_values)

    with open('network_latency.csv', 'w', encoding='UTF8', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(latency_data)
        writer.writerow(time_values)

    # plot_latency_graph(latency_data, time_values)


if __name__ == '__main__':
    cli()

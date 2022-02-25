from pythonping import ping

data = ping("google.com", out_format=None)
a = []
for i in str(data).split():
    if("ms=" in i):
        a.append(float(i.replace("ms=", "")))
    if("Timed" in i):
        a.append(0)
print(a)
# print("data: ", len(list(data)))

import psutil
from tabulate import tabulate

def makelist(pid):
    line = []
    p = psutil.Process(pid)
    line.append(p.username())
    line.append(pid)
    line.append(p.cpu_percent())
    line.append(p.memory_percent())
    line.append(p.name())
    return line


headers = ['User', 'Pid', 'Cpu%', 'Mem%', 'Command']
pids = psutil.pids()
lines = []
print(pids)
lines = map(makelist, pids)
tablelines = tabulate(list(lines), headers).split('\n')
for line in tablelines:
    print(line)
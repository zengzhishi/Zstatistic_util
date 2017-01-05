import subprocess
import os

def systemcall(command):
    # p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    # output = p.stdout.readlines()
    popen=subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # f = os.popen(command)
    # output = f.readlines()
    returncode = popen.poll()
    output = []
    while returncode is None:
        line = popen.stdout.readline()
        returncode = popen.poll()
        line = line.strip()
        output.append(line.decode('utf-8'))
    return output[:-1]

# test code
def main():
    cmd = 'uptime'
    result = systemcall(cmd)
    for line in result:
        print(line)

if __name__ == '__main__':
    main()
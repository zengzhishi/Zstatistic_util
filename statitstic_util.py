"""Test

Usage: 
  docfile2.py [-h | --help]

Options:
  -h --help    show this
  -s --sorted  sorted output
  -o FILE      specify output file [default: ./test.txt]
  --quiet      print less text
  --verbose    print more text
  --debug      debug

"""
import curses
from tabulate import tabulate
from utils import systemcall
import threading
import time
import psutil

stdscr = curses.initscr()
action = ''
threadLock = threading.Lock()
threads = []

def jobStatistic():
    '''获取作业信息'''
    cmd = 'uptime'
    info = systemcall(cmd)
    result = "Jobinfo: " + info[0]
    return result


def memoryInfo():
    '''内存信息'''

    return


def cpuinfo():
    '''获取CPU信息'''
    cpu_num = psutil.cpu_count()    # CPU核心数
    cpu_percent = psutil.cpu_percent()   # cpu每个核心的使用率
    # cpu_percent_avg = cpu_percent.count() / len(cpu_percent)    # cpu平均使用率
    cpu_time = psutil.cpu_times()
    cpu_time_percent = psutil.cpu_times_percent()     # cpu
    cpu_result = "Cpus:" + str(cpu_num) + " per:" + str(cpu_percent) + " time%per: user " \
                 + str(cpu_time.user) + "%" + str(cpu_time_percent.user) + " system" \
                 + str(cpu_time.system) + "%" + str(cpu_time_percent.system) \
                 + " idle" + str(cpu_time.idle) + "%" + str(cpu_time_percent.idle)
    return cpu_result


def makelist(pid):
    '''构造进程的监控参数'''
    line = []
    p = psutil.Process(pid)
    line.append(p.username())
    line.append(pid)
    line.append(round(p.cpu_percent(),2))
    line.append(round(p.memory_percent(), 3))
    line.append(p.name())
    return line


def psInfo():
    '''进程监控'''
    pids = psutil.pids()
    lines = map(makelist, pids)
    headers = ['User', 'Pid', 'Cpu%', 'Mem%', 'Command']
    tablelines = tabulate(list(lines), headers).split('\n')
    return tablelines[0], tablelines[2:]


def display_info(str, x, y, colorpair=2):
    '''''使用指定的colorpair显示文字'''
    global stdscr
    stdscr.addstr(y, x, str, curses.color_pair(colorpair))
    stdscr.refresh()
    return


def process():
    global stdscr
    jobstatic = jobStatistic()
    '''''填充主要的显示逻辑'''
    cpustatic = cpuinfo()
    # memstatic = memoryInfo()
    pstitle, psstatic = psInfo()
    display_info(jobstatic, 0, 0, 1)
    display_info(cpustatic, 0, 1, 1)
    display_info(pstitle, 0, 3, 2)
    i = 4
    for line in psstatic:
        if len(line) <= 80 and i <= 22:
            display_info(line, 0, i, 4)
            i = i + 1
        elif len(line) > 80 and i <= 21:
            display_info(line, 0, i, 4)
            i = i + 2
        else:
            break
    # display_info("Press any key to continue...", 0, 20)
    stdscr.refresh()
    return


def pre_exit_process():
    '''退出前的处理'''
    # process()
    display_info("Now program is exiting...", 0, 23)
    stdscr.refresh()
    return


class OutputThread(threading.Thread):
    '''屏幕输出线程,采用轮询的方式来更新页面元素'''
    def __init__(self, threadId, name, interval):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.interval = interval
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True

    def run(self):
        while self.__running.isSet():
            threadLock.acquire()
            process()
            threadLock.release()
            time.sleep(self.interval)
            # if action is ord('q'):
            #     self.exit()

    def stop(self):
        self.__running.clear()        # 设置为False


class InputThread(threading.Thread):
    '''接受输入的线程,用于控制线程设置'''
    def __init__(self, threadId, name, thread):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.outputThread = thread
        self.__running = threading.Event()      # 用于停止线程的标识
        self.__running.set()      # 将running设置为True

    def run(self):
        while self.__running.isSet():
            time.sleep(0.01)
            action = stdscr.getch()
            if action is ord('q'):
                threadLock.acquire()
                pre_exit_process()
                threadLock.release()
                self.outputThread.stop()
                self.stop()

    def stop(self):
        self.__running.clear()        # 设置为False




def set_win():
    '''''控制台设置'''
    global stdscr
    # 使用颜色首先需要调用这个方法
    curses.start_color()
    # 文字和背景色设置，设置了两个color pair，分别为1和2
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    # 关闭屏幕回显
    curses.noecho()
    # 输入时不需要回车确认
    curses.cbreak()
    # 设置nodelay，使得控制台可以以非阻塞的方式接受控制台输入，超时1秒
    stdscr.nodelay(1)


def unset_win():
    '''控制台重置'''
    global stdstr
    #恢复控制台默认设置（若不恢复，会导致即使程序结束退出了，控制台仍然是没有回显的）
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    #结束窗口
    curses.endwin()


def main():
    '''主函数,负责创建和调用进程,以及控制终端环境的设置'''
    outputThread = OutputThread(1, 'thread-1', 5)
    inputThread = InputThread(2, 'thread-2', outputThread)

    try:
        set_win()

        outputThread.start()
        inputThread.start()
        threads.append(outputThread)
        threads.append(inputThread)
        for t in threads:
            t.join()

    except Exception:
        raise
    finally:
        unset_win()

if __name__ == '__main__':
    main()

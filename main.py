import os
import time
import ctypes
import subprocess
from colorama import init, Fore
from net_optimizer import run

init()

def launch_cs2_with_options(options):
    steam_uri = f'steam://rungameid/730//{options}'
    os.system(f"start {steam_uri}")
    print(Fore.GREEN + f"Done : CS2 prepared with noreflex option")

def set_process_priority(pid, priority):
    handle = ctypes.windll.kernel32.OpenProcess(0x0200 | 0x0400, False, pid)
    
    if handle:
        ctypes.windll.kernel32.SetPriorityClass(handle, priority)
        print(Fore.GREEN + f"Done : Process {pid} priority set.")
    else:
        print(Fore.RED + f"Fail : Failed to open process {pid}.")

def set_cpu_affinity(pid, cpu_index):
    handle = ctypes.windll.kernel32.OpenProcess(0x0200 | 0x0400, False, pid)
    
    if handle:
        affinity_mask = 1 << cpu_index
        result = ctypes.windll.kernel32.SetProcessAffinityMask(handle, affinity_mask)
        
        if result != 0:
            print(Fore.GREEN + f"Done : Process {pid} affinity set to CPU {cpu_index}.")
        else:
            print(Fore.RED + f"Fail : Failed to set affinity for process {pid}.")
    else:
        print(Fore.RED + f"Fail : Failed to open process {pid}.")

def find_process_pid(process_name):
    pid = None
    result = subprocess.run("tasklist", capture_output=True, text=True)

    for line in result.stdout.splitlines():
        if process_name in line.lower():
            pid = int(line.split()[1])
            break
    return pid

run()

launch_cs2_with_options('-noreflex')

time.sleep(5)

# REALTIME_PRIORITY_CLASS (0x00000100) : Real-time priority.
# HIGH_PRIORITY_CLASS (0x00000080) : High priority.
# NORMAL_PRIORITY_CLASS (0x00000020) : Normal priority.
# IDLE_PRIORITY_CLASS (0x00004000) : Below normal priority.

cs2_pid = find_process_pid('cs2.exe')

if cs2_pid:
    set_process_priority(cs2_pid, 0x00000100)
else:
    print(Fore.RED + "Fail : CS2 is not running.")
    input(Fore.RED + "Press any key to exit...")
    exit()

faceitclient_pid = find_process_pid('faceitclient.exe')

if faceitclient_pid:
    set_cpu_affinity(faceitclient_pid, 0)
    print(Fore.GREEN + "Done : Faceit client affinity set to CPU 0")
    set_process_priority(faceitclient_pid, 0x00004000)
    print(Fore.GREEN + "Done : Faceit client priority set to 'below normal'")
else:
    print(Fore.RED + "Fail : Faceit client not found.")
    input(Fore.RED + "Press any key to exit...")
    exit()

print()
print(Fore.CYAN + "Everything went successfully, CS2 will now launch.")
print()

time.sleep(10)

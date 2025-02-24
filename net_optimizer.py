import ctypes
import subprocess
from colorama import init, Fore

init(strip=False)

def run_command(command, success_msg, error_msg):
    try:
        result = subprocess.run(["powershell", "-Command", command], check=True, capture_output=True, text=True)
        print(Fore.GREEN + f"Done : {success_msg}" + Fore.RESET)
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Fail : {error_msg}" + Fore.RESET)
        print(Fore.YELLOW + f"Erreur : {e.stderr}" + Fore.RESET)
        print(Fore.YELLOW + f"Sortie standard : {e.stdout}" + Fore.RESET)

def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin()

if not is_admin():
    print(Fore.RED + "Fail : This software must be run in administrator mode." + Fore.RESET)
    input(Fore.RED + "Press any key to exit...")
    exit()

print(Fore.YELLOW + "***************************************************")
print(Fore.YELLOW + "You are currently running Faceit Optimizer software")
print(Fore.YELLOW + "https://www.cstrainer.io")
print(Fore.YELLOW + "***************************************************")

print(Fore.CYAN + "\nOptimizing network settings for cs2.exe process...\n" + Fore.RESET)

def run():
    run_command(
        'New-Item -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Psched" -Force; '
        'Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Psched" -Name "NonBestEffortLimit" -Value 0 -Type DWord',
        "Default 20% windows bandwidth removed",
        "Failed to update default bandwidth settings"
    )

run_command(
    "gpupdate /force",
    "Group policy update completed.",
    "Failed to update group policies."
)

run_command(
    "netsh int tcp set global autotuninglevel=normal",
    "TCP auto-tuning set to 'normal'.",
    "Failed to modify autotuning level."
)

run_command(
    'if (-not (Get-NetQoSPolicy -Name "CS2" -ErrorAction SilentlyContinue)) { '
    'New-NetQosPolicy -Name "CS2" -AppPathNameMatchCondition "cs2.exe" -PriorityValue8021Action 5 }',
    "CS2 prioritized in network QoS.",
    "Failed to create QoS policy for CS2."
)

run_command(
    "Stop-Service -Name QWAVE -Force; Start-Service -Name QWAVE",
    "QoS service restarted.",
    "Failed to restart QoS service."
)

print()
print(Fore.GREEN + "Network optimization done.\n" + Fore.RESET)
print()

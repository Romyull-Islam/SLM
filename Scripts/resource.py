import psutil
import csv
import time
import threading
import subprocess

def get_cpu_data():
    cpu_times = psutil.cpu_times_percent(interval=0, percpu=False)
    return [cpu_times.user, cpu_times.system, cpu_times.idle, getattr(cpu_times, 'iowait', 0)]

def get_memory_data():
    memory = psutil.virtual_memory()
    return [
        f"{memory.total / (1024 ** 2):.2f}",
        f"{memory.active / (1024 ** 2):.2f}",
        f"{memory.used / (1024 ** 2):.2f}",
        f"{memory.free / (1024 ** 2):.2f}",
        f"{memory.inactive / (1024 ** 2):.2f}"
    ]

"""def get_virtual_memory_usage():
    vmemory = psutil.virtual_memory()
    return [
        f"{vmemory.total / (1024 ** 2):.2f}",
        f"{vmemory.used / (1024 ** 2):.2f}"
    ]"""

def get_disk_data():
    disk = psutil.disk_usage('/')
    return [disk.total, disk.used, disk.free, disk.percent]
    
def get_disk_busy_percentage(interval=1):
    # Capture the start time
    start_time = time.time()
    
    disk_time = psutil.disk_io_counters(perdisk=False)
    initial_read_time = disk_time.read_time
    initial_write_time = disk_time.write_time
    
    # Sleep for the specified interval reduced by the execution time
    time.sleep(max(0, interval - (time.time() - start_time)))
    
    disk_time = psutil.disk_io_counters(perdisk=False)
    delta_read_time = disk_time.read_time - initial_read_time
    delta_write_time = disk_time.write_time - initial_write_time
    end_time = time.time()  # Capture the end time after collecting data
    
    # Calculate the total time elapsed in milliseconds
    elapsed_time = (end_time - start_time) * 1000
    
    # Calculate busy time as the sum of read and write time
    busy_time = delta_read_time + delta_write_time
    
    # Calculate the disk busy percentage
    busy_percentage = (busy_time / elapsed_time) * 100 if elapsed_time > 0 else 0
    return busy_percentage
    
def get_swap_data():
    swap = psutil.swap_memory()
    return [swap.total, swap.used, swap.free, swap.percent]

def get_context_switch_data():
    switches = psutil.cpu_stats()
    return [switches.ctx_switches]

def get_process_count():
    return [len(list(psutil.process_iter(['pid'])))]
    
    
def get_mac_swap_data():
    # Execute the sysctl command and capture the output
    result = subprocess.run(['sysctl', 'vm.swapusage'], stdout=subprocess.PIPE)
    swap_data_str = result.stdout.decode().strip()

    # Initialize an empty list to hold swap values
    swap_metrics = []

    # Split the result string into parts based on spaces
    parts = swap_data_str.split()

    # Extract numerical values for 'total', 'used', and 'free' and append to list
    for i in range(len(parts)):
        if parts[i] in ['total', 'used', 'free']:
            # Extract the number (assume the format is 'total = 2048.00M' etc.)
            try:
                # Extract the value, remove the 'M', and convert to float
                value = float(parts[i + 2].replace('M', ''))
                swap_metrics.append(value)
            except ValueError as e:
                print(f"Error converting swap data to float: {e}")
                swap_metrics.append(0.0)  # Append zero if there's an error

    return swap_metrics

swap_info = get_mac_swap_data()
print("Parsed swap data:", swap_info)  # Check the parsed output



def write_data_to_csv(header, data_getter, filename, interval=1):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        while True:
            data = data_getter()
            if isinstance(data, list):  # Check if data is already a list
                writer.writerow(data)
            else:
                writer.writerow([data])  # Wrap data in a list if it's not a list
            file.flush()  # Force buffer to write to disk
            time.sleep(interval)



# Headers for CSV files
cpu_header = ["User CPU%", "System CPU%", "Idle CPU%", "I/O Wait CPU%"]
memory_header = ["Total Memory", "Active Memory", "Used Memory", "Free Memory", "Inactive Memory"]
#virtual_memory_header = ["Total Virtual Memory", "Used Virtual Memory"]
disk_header = ["Total Disk", "Used Disk", "Free Disk", "Disk Usage %"]
swap_header = ["Total Swap", "Used Swap", "Free Swap"]
context_switch_header = ["Context Switches"]
process_header = ["Total Processes"]
disk_busy_header = ["Disk Busy %"]

# Create threads for each metric collection
cpu_thread = threading.Thread(target=write_data_to_csv, args=(cpu_header, get_cpu_data, 'cpu_usage.csv'))
memory_thread = threading.Thread(target=write_data_to_csv, args=(memory_header, get_memory_data, 'memory_usage.csv'))
#virtual_memory_thread = threading.Thread(target=write_data_to_csv, args=(virtual_memory_header, get_virtual_memory_usage, 'virtual_memory_usage.csv'))
disk_thread = threading.Thread(target=write_data_to_csv, args=(disk_header, get_disk_data, 'disk_usage.csv'))
#swap_thread = threading.Thread(target=write_data_to_csv, args=(swap_header, get_swap_data, 'swap_usage.csv'))
context_switch_thread = threading.Thread(target=write_data_to_csv, args=(context_switch_header, get_context_switch_data, 'context_switches.csv'))
process_thread = threading.Thread(target=write_data_to_csv, args=(process_header, get_process_count, 'process_count.csv'))
swap_thread = threading.Thread(target=write_data_to_csv, args=(swap_header, get_mac_swap_data, 'swap_usage.csv'))
disk_busy_thread = threading.Thread(target=write_data_to_csv, args=(disk_busy_header, get_disk_busy_percentage, 'disk_busy_percentage.csv'))



# Start threads to execute the data logging
cpu_thread.start()
memory_thread.start()
#virtual_memory_thread.start()
disk_thread.start()
#swap_thread.start()
context_switch_thread.start()
process_thread.start()
swap_thread.start()
disk_busy_thread.start()

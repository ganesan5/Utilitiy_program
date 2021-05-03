import os
import psutil
import threading
import time


dir_name = "/home/username/dir1"  # give your directory to store
eth_name = 'eno1'			# check in your terminal with ip add command


def record_cpu_mem_netio(stop_event):
	# model_dir = "/home/user/NMS/code/tmp/"
	filepath = dir_name +  "cpu_mem_net_values_.txt" 
	filepath1 = dir_name + "cpu_mem_net_logs_.txt"
	filewriter = open(filepath, 'w+') 
	filewriter1 = open(filepath1, 'w+')

	counter = 0
	net_bytes_sent, net_bytes_received = 0, 0
	after_pgm_bytes_sent, after_pgm_bytes_received = 0, 0
	start_time = time.time()
	cpu_count = os.cpu_count()
	filewriter.write(str("\nCount, Current_time, Elapsed_time, CPU Percent, CPU cores, Memory Percent, Bytes sent,Bytes Received,Bytes sent since program starts,Bytes Received since program starts"))
	filewriter1.write(str("\nCPU cores, {}".format(cpu_count)))
	while not stop_event.is_set():
		cpu_perc = psutil.cpu_percent()
		
		mem_info = psutil.virtual_memory()
		mem_perc = psutil.virtual_memory().percent
		io_count = psutil.net_io_counters(pernic=True)
		active_ethernet = io_count.get(eth_name)
		if(counter == 0):
			net_bytes_sent = active_ethernet.bytes_sent
			net_bytes_received = active_ethernet.bytes_recv

		after_pgm_bytes_sent = active_ethernet.bytes_sent - net_bytes_sent
		after_pgm_bytes_received = active_ethernet.bytes_recv - net_bytes_received
		curr_time = time.time()
		curr_elap_time = int(curr_time - start_time)


		filewriter1.write(str("\nMemory info, {}".format(mem_info)))
		filewriter1.write(str("\nNet IO info, {}".format(active_ethernet)))
		# filewriter.write(str("\nBytes sent, {}, Bytes Received, {}".format(active_ethernet.bytes_sent, active_ethernet.bytes_recv)))
		
		filewriter.write(str("\n{}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(counter, curr_time, curr_elap_time, cpu_perc, cpu_count, mem_perc, active_ethernet.bytes_sent, active_ethernet.bytes_recv, after_pgm_bytes_sent, after_pgm_bytes_received)))
		# filewriter.write(str("\nBytes sent since program starts, {}, Bytes Received since program starts, {}".format(after_pgm_bytes_sent, after_pgm_bytes_received)))
		filewriter.flush()
		filewriter1.flush()
		counter += 1
		time.sleep(2)

	filewriter.close()
	filewriter1.close()
	print("Stopping the thread.")


def main():
	stop_thread = threading.Event()			# the monitoring program starts as a thread 
	log_cpu_mem_thread1 = threading.Thread(target=record_cpu_mem_netio, name="Record_CPU_Mem", args=(stop_thread, ))
	log_cpu_mem_thread1.start()
	for i in range(5):
		time.sleep(5)		# your main program goes here.. 

	stop_thread.set()

main()
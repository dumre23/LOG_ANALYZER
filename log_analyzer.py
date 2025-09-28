import csv
from datetime import datetime
import re

def analyze_log(file_path):
    # Regex pattern for log files
    log_pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s'           # IP Address
        r'[^[]*\['                                 # Skip until [
        r'(?P<timestamp>[^\]]+)\]'                 # Timestamp inside []
    )

    ip_data = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                match = log_pattern.match(line)
                if not match:
                    continue  # Skip lines that don't match
                
                ip_address = match.group("ip")
                timestamp_str = match.group("timestamp").split()[0]  # Drop timezone

                try:
                    timestamp = datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S') # Parse timestamp to python from string for comparison
                except ValueError:
                    continue
                
                if ip_address not in ip_data:
                    ip_data[ip_address] = []
                ip_data[ip_address].append(timestamp)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None

    return ip_data

def check_for_brute_force(log_data, time_window_seconds=60, min_requests=5):
    suspicious_ips = {}
    
    for ip, timestamps in log_data.items():
        timestamps.sort()
        for i in range(len(timestamps) - min_requests + 1):
            time_diff = (timestamps[i + min_requests - 1] - timestamps[i]).total_seconds()
            if time_diff <= time_window_seconds:
                suspicious_ips[ip] = timestamps
                break 
    return suspicious_ips

def print_suspicious_activity(suspicious_ips, min_requests, time_window):
    
    print("=" * 70)
    print(f"Brute-Force Detection Analysis: >{min_requests} requests in {time_window}s")
    print("=" * 70)

    if not suspicious_ips:
        print("✅ No suspicious activity detected.")
    else:
        for ip, timestamps in suspicious_ips.items():
            print(f"🚨 Potential Brute-Force Attack from IP: {ip}")
            print(f"  Total requests found: {len(timestamps)}")
            print("  Timestamps (first 5 shown):")
            for ts in timestamps[:5]:
                print(f"    - {ts.strftime('%Y-%m-%d %H:%M:%S')}")
            if len(timestamps) > 5:
                print("    ...")
            print("-" * 70)

def export_to_csv(data, filename='suspicious_ips.csv'):
    """
    Exports suspicious IP data to a CSV file.
    """
    if not data:
        print("No suspicious data to export to CSV.")
        return

    # To simplify, we will just export the IP and the total count.
    # Exporting all timestamps would be too complex for a simple CSV.
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['IP_Address', 'Total_Requests']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for ip, timestamps in data.items():
            writer.writerow({'IP_Address': ip, 'Total_Requests': len(timestamps)})

    print(f"Successfully exported suspicious IPs to '{filename}'.")

if __name__ == "__main__":
    log_file_path = 'access.log'
    time_window_seconds = 60
    min_requests_threshold = 5

    log_data = analyze_log(log_file_path)

    if log_data:
        suspicious_ips = check_for_brute_force(log_data, time_window_seconds, min_requests_threshold)
        print_suspicious_activity(suspicious_ips, min_requests_threshold, time_window_seconds)
        
        # New line to call the CSV export function
        export_to_csv(suspicious_ips)
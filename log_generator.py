# # # log_generator.py
# # import random
# # from datetime import datetime, timedelta

# # def generate_log_entry():
# #     """Generates a single, realistic log entry."""
    
# #     # 1. Generate a random IP address
# #     ip_parts = [str(random.randint(0, 255)) for _ in range(4)]
# #     ip_address = ".".join(ip_parts)
    
# #     # 2. Generate a random timestamp
# #     end_date = datetime.now()
# #     start_date = end_date - timedelta(days=7) # Generate logs for the last 7 days
# #     random_date = start_date + (end_date - start_date) * random.random()
# #     timestamp = random_date.strftime("%d/%b/%Y:%H:%M:%S +0530")
    
# #     # 3. Generate a random HTTP method and path
# #     methods = ["GET", "POST", "PUT", "DELETE"]
# #     paths = ["/", "/home", "/about", "/contact", "/products", "/images/logo.png"]
# #     http_method = random.choice(methods)
# #     http_path = random.choice(paths)
    
# #     # 4. Generate a random status code and size
# #     status_codes = [200, 404, 500, 301]
# #     status_code = random.choices(status_codes, weights=[0.7, 0.2, 0.05, 0.05])[0]
# #     size = random.randint(10, 5000)
    
# #     # 5. Format the log entry
# #     return f'{ip_address} - - [{timestamp}] "{http_method} {http_path} HTTP/1.1" {status_code} {size}'

# # def create_log_file(filename, num_entries):
# #     """Creates a log file with a specified number of entries."""
# #     with open(filename, 'w') as file:
# #         for _ in range(num_entries):
# #             file.write(generate_log_entry() + '\n')
# #     print(f"Successfully created {filename} with {num_entries} entries.")

# # if __name__ == "__main__":
# #     log_filename = "access.log"
# #     num_lines = 1000 # You can increase this to 10000 or more
# #     create_log_file(log_filename, num_lines)



# # log_generator.py - Modified for repetition
# import random
# from datetime import datetime, timedelta

# def generate_log_entry():
#     """Generates a single, realistic log entry with repeated IPs."""
    
#     # Define a few frequent IP addresses
#     frequent_ips = ["10.0.0.1", "192.168.1.50", "203.0.113.10"]
    
#     # 1. Generate an IP address with a bias towards frequent ones
#     # Use random.choices to pick from the lists with a certain weight
#     # 70% chance to pick a frequent IP, 30% chance for a random one
#     if random.choices([True, False], weights=[0.7, 0.3], k=1)[0]:
#         ip_address = random.choice(frequent_ips)
#     else:
#         # Generate a random IP address
#         ip_parts = [str(random.randint(0, 255)) for _ in range(4)]
#         ip_address = ".".join(ip_parts)
    
#     # (The rest of the function remains the same)
#     end_date = datetime.now()
#     start_date = end_date - timedelta(days=7)
#     random_date = start_date + (end_date - start_date) * random.random()
#     timestamp = random_date.strftime("%d/%b/%Y:%H:%M:%S +0530")
    
#     methods = ["GET", "POST", "PUT", "DELETE"]
#     paths = ["/", "/home", "/about", "/contact", "/products", "/images/logo.png"]
#     http_method = random.choice(methods)
#     http_path = random.choice(paths)
    
#     status_codes = [200, 404, 500, 301]
#     status_code = random.choices(status_codes, weights=[0.7, 0.2, 0.05, 0.05])[0]
#     size = random.randint(10, 5000)
    
#     return f'{ip_address} - - [{timestamp}] "{http_method} {http_path} HTTP/1.1" {status_code} {size}'

# def create_log_file(filename, num_entries):
#     """Creates a log file with a specified number of entries."""
#     with open(filename, 'w') as file:
#         for _ in range(num_entries):
#             file.write(generate_log_entry() + '\n')
#     print(f"Successfully created {filename} with {num_entries} entries.")

# if __name__ == "__main__":
#     log_filename = "access.log"
#     num_lines = 5000 # Let's increase the size for better results
#     create_log_file(log_filename, num_lines)

# log_generator.py - Modified to simulate a brute-force attack

import random
from datetime import datetime, timedelta

def generate_log_entry(ip_address, timestamp):
    """Generates a single log entry with a specified IP and timestamp."""
    
    methods = ["GET", "POST", "PUT", "DELETE"]
    paths = ["/", "/login", "/about", "/contact", "/products", "/images/logo.png"]
    http_method = random.choice(methods)
    
    # Make /login a frequent path for a more realistic attack simulation
    if random.random() < 0.7:  # 70% chance to be a login attempt
        http_path = "/login"
    else:
        http_path = random.choice(paths)
        
    status_codes = [200, 404, 500, 301]
    # In a brute-force attack, many attempts will fail (404, etc.)
    status_code = random.choices(status_codes, weights=[0.2, 0.6, 0.1, 0.1])[0] 
    size = random.randint(10, 5000)
    
    return f'{ip_address} - - [{timestamp.strftime("%d/%b/%Y:%H:%M:%S +0530")}] "{http_method} {http_path} HTTP/1.1" {status_code} {size}'

def create_log_file(filename, num_entries, attack_ip=None):
    """Creates a log file with a specified number of entries, including an attack simulation."""
    with open(filename, 'w') as file:
        
        # Determine the time and size of the attack simulation
        attack_time = datetime.now() - timedelta(minutes=random.randint(5, 50)) # An attack 5-50 minutes ago
        num_attack_entries = random.randint(10, 20) # 10-20 requests for the attack
        
        # Step 1: Generate background noise (normal log entries)
        for _ in range(num_entries - num_attack_entries):
            # Create a random IP for normal entries
            ip_parts = [str(random.randint(0, 255)) for _ in range(4)]
            ip_address = ".".join(ip_parts)
            
            # Random timestamp for normal entries (not clustered)
            random_date = datetime.now() - timedelta(days=random.randint(1, 7), seconds=random.randint(0, 86400))
            
            file.write(generate_log_entry(ip_address, random_date) + '\n')
            
        # Step 2: Generate the attack entries
        print(f"Injecting a simulated attack of {num_attack_entries} requests from {attack_ip} at {attack_time.strftime('%H:%M:%S')}")
        
        for i in range(num_attack_entries):
            # The attack requests happen in a short, consecutive burst
            attack_timestamp = attack_time + timedelta(seconds=random.uniform(0.1, 2))
            file.write(generate_log_entry(attack_ip, attack_timestamp) + '\n')
            
    print(f"Successfully created {filename} with {num_entries} entries, including a simulated attack.")

if __name__ == "__main__":
    log_filename = "access.log"
    num_lines = 1000 # Total number of log entries
    
    # The IP address that will simulate the attack
    attack_ip_address = "20.10.30.40" 
    
    create_log_file(log_filename, num_lines, attack_ip=attack_ip_address)
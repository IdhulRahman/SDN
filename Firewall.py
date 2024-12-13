import sys
import csv
import requests

# REST API url and headers
host = "10.0.2.15"
port = "8181"
username = "onos"
password = "rocks"
url = f"http://{host}:{port}/onos/v1/acl/rules"
headers = {'Content-type': 'application/json'}

# Read policy file
policy_file = "firewall-policies.csv"
firewall_rules = []

try:
    with open(policy_file, 'r') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        next(rows)  # Skip header row

        for row in rows:
            if len(row) >= 2:  # Ensure the row has enough columns
                src_ip = row[0].strip()
                dst_ip = row[1].strip()

                if src_ip and dst_ip:  # Validate IP addresses are not empty
                    firewall_rules.append((src_ip, dst_ip))
                else:
                    print(f"Invalid data in row: {row}")
except FileNotFoundError:
    print(f"Error: Policy file '{policy_file}' not found.")
    sys.exit(1)
except Exception as e:
    print(f"Error reading policy file: {e}")
    sys.exit(1)

# Add each firewall rule to the ACL using the REST API
for rule in firewall_rules:
    src_ip, dst_ip = rule

    try:
        response = requests.post(
            url,
            json={
                "srcIp": src_ip,
                "dstIp": dst_ip
            },
            auth=(username, password),
            headers=headers
        )

        if response.status_code == 201:
            print(f"Rule added successfully: srcIp={src_ip}, dstIp={dst_ip}")
        else:
            print(f"Failed to add rule: srcIp={src_ip}, dstIp={dst_ip}, Response: {response.status_code}, {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error sending request for rule: srcIp={src_ip}, dstIp={dst_ip}, Error: {e}")

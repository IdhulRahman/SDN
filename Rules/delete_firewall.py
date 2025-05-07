import requests

# REST API url and headers
host = "10.0.2.15"
port = "8181"
username = "onos"
password = "rocks"
url = f"http://{host}:{port}/onos/v1/acl/rules"

# remove all rules from the ACL using the REST API
resp = requests.delete(url, auth=(username, password))
print(resp.text)
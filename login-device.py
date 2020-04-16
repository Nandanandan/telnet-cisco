import telnetlib
from login_data import creds

# import credentials

host_ip = creds["host_ip"]
username = creds["username"]
password = creds["password"]

# commands to be executed on device
commands = {
            "command1": "terminal length 0",
            "command2": "show int description"
           }

print(f"Telnet to device: {host_ip}")

"""
code section  to login and to device and get the output
"""
 
tn = telnetlib.Telnet(host_ip)
tn.read_until(b"Username: ")
tn.write(username.encode('ascii') + b"\n")
tn.read_until(b"Password: ")
tn.write(password.encode('ascii') + b"\n")
for key in commands:
    tn.write(commands[key].encode('ascii') + b"\n")
tn.write(b"exit\n")

data = tn.read_all().decode('ascii')

print(data)

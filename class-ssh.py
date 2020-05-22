from netmiko import ConnectHandler
import getpass

class ssh:

    def __init__(self):
        pass

    def ssh_device(self, **device, execution_cmd):
        net_connect = []
        try:
            net_connect = ConnectHandler(**device)
            with open('output_file', "a+") as file:
                output = net_connect.send_config_set(execution_cmd)
                file.write(output)
        finally:
            print("--- Execution Completed ---")
            net_connect.disconnect()

if __name__ == "__main__":

    ip = input(r"IP:")
    usern = input(r"user:")
    passw = getpass.getpass("Pass:")
    execution_cmd = []
    command_file = "config_ssh"

    device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': usern,
        'password': passw,
    }
    with open(command_file, "r") as cmd:
        execution_cmd = cmd.readlines()
    obj = ssh()
    data = obj.ssh_device(**device, execution_cmd)


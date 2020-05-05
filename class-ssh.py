from netmiko import ConnectHandler
import getpass

class ssh:

    def __init__(self):
        pass

    def ssh_device(self, **device):
        try:
            net_connect = ConnectHandler(**device)
            commands = ['show version', 'sh ip int brief']
            with open('output_file', "a+") as file:
                for i in range(len(commands)):
                    output = net_connect.send_command(commands[i])
                    file.write(output)
        finally:
            net_connect.disconnect()


if __name__ == "__main__":

    ip = input(r"IP:")
    usern = input(r"user:")
    passw = getpass.getpass("Pass:")

    device = {
        'device_type': 'cisco_ios',
        'host': ip,
        'username': usern,
        'password': passw,
    }
    obj = ssh()
    data = obj.ssh_device(**device)


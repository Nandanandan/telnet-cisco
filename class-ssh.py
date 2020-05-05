from netmiko import ConnectHandler
import getpass

class ssh:

    def __init__(self):
        pass

    def ssh_device(self, **device):
        net_connect = ConnectHandler(**device)
        output = net_connect.send_command('show ip int brief')
        return output


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
    print(data)
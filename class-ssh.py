from netmiko import ConnectHandler
import getpass

class ssh:

    def __init__(self):
        self.command_file = "config_ssh"
    def ssh_device(self, device_type, host, username, password, secret):

        net_connect = ""
        with open(self.command_file, "r") as cmd:
            execution_cmd = cmd.readlines()

        try:
            net_connect = ConnectHandler(device_type=device_type,ip=host,username=username,password=password,secret=secret)
            #net_connect.send_command("enable"+'\n', expect_string=r"Password:")
            #net_connect.send_command(self.epass)
            net_connect.enable() 
            with open('output_file', "a+") as file:
                output = net_connect.send_config_set(execution_cmd)
                file.write(output)
        except Exception as e:
               print(e)
        finally:
            print("--- Execution Completed ---")
            net_connect.disconnect()

if __name__ == "__main__":

    ip = input(r"IP:")
    usern = input(r"user:")
    passw = getpass.getpass("Pass:")
    epass = getpass.getpass("Enable:") 
    device_type = "cisco_ios"
    host = ip
    username = usern
    password = passw
    secret = epass

    obj = ssh()
    data = obj.ssh_device(device_type, host, username, password, secret)


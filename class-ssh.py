import paramiko
import getpass

class ssh:

    def __init__(self):
        pass

    def ssh_device(self, host_ip, username, password):
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client = session.connect(hostname=host_ip, username=username, password=password)
        stdin, stdout, stderr = client.exec_command('show run')
        return stdout

if __name__ == "__main__":
    ip = getpass.getpass("IP:")
    usern = getpass.getpass("user:")
    passw = getpass.getpass("Pass:")
    data = ssh().ssh_device(ip,usern,passw)
    print(data)
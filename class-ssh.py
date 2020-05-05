import paramiko

class ssh:

    def __init__(self):
        pass

    def ssh_device(self, host_ip, username, password):
        session = paramiko.SSHClient()
        client = session.connect(hostname=host_ip, username=username, password=password)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        stdin, stdout, stderr = client.exec_command('show run')
        return stdout

if __name__ == "__main__":
    data = ssh().ssh_device()
    print(data)
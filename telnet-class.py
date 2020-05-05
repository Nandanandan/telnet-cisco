"""
Objective of Code:

Login to cisco devices with telnet: Done
Get current config: Done
Change configuration using telnet: Done
Login to device using SSH(TELNET disabled after config change): Pending
Compare before after config change: Done

"""
from netmiko import ConnectHandler
import telnetlib
import pandas as pd
import os
import xlsxwriter
import diffios
import getpass
import time


# Variables defined here

"""
file path + name of the input file
Data of input file contains destination ip and telnet credentials.

"""
class telnet:

    def __init__(self):
        self.input_file = "device_input_data.xlsx"
        self.command_file = 'config'
        self.output_file = "output_file.xlsx"
        self.output_dir = 'output_data'
        self.system_dir = 'system_data'

    def ping_check(self,host_ip):
        '''Ping to host_ip and return boolean output'''
        response = os.system("ping -c 2 " + host_ip)
        if response == 0:
            return True
        else:
            return False

    def compare_config(self, precheck_file, postcheck_file,host_ip):
        '''

        This section of code is used to compare configuration before and after change.
        Post comparision it sill share output with listed changes.

        '''
        diff_file = os.path.join(self.output_dir, host_ip + "_config_diff_file_" + time.strftime("%Y%m%d-%H%M%S") + "_.txt")
        diff_config = diffios.Compare(precheck_file, postcheck_file)
        with open(diff_file, "a+") as diff:
            diff.writelines(diff_config.delta())

    def telnet_to_device(self, host_ip, username, password, epass, commands):
        """
        This section of code will help to telnet and execute commands on cisco devices and return
        """

        tn = telnetlib.Telnet(host_ip)
        if username:
            tn.read_until(b"Username: ")
            tn.write(username.encode('ascii') + b"\n")
        else:
            print('\n---username not required or provided---\n')
        tn.read_until(b"Password: ")
        if password:
            tn.write(password.encode('ascii') + b"\n")
        else:
            print('\n---Login Password must be provided---\n')
            password = getpass.getpass("Please enter login password:")
            tn.write(password.encode('ascii') + b"\n")
        if epass:
            tn.write(b"enable\n")
            tn.read_until(b"Password: ")
            tn.write(epass.encode('ascii') + b"\n")
        else:
            print('\n---Enable Password must be provided---\n')
            epass = getpass.getpass("Please enter Enable password:")
            tn.write(b"enable\n")
            tn.read_until(b"Password: ")
            tn.write(epass.encode('ascii') + b"\n")

        for command in commands:
            tn.write(command.encode('ascii') + b"\n")
        tn.write(b"exit\n")

        data = tn.read_all().decode('ascii')
        return data

    def ssh_device(self, host_ip, username, password, check_cmd, ):

            device = {
                'device_type': 'cisco_ios',
                'host': host_ip,
                'username': username,
                'password': password,
            }
            postcheck_file = os.path.join(self.system_dir,host_ip + "_postcheck_file_" + time.strftime("%Y%m%d-%H%M%S") + "_.txt")
            try:
                net_connect = ConnectHandler(**device)
                with open(postcheck_file, "a+") as file:
                    for i in range(len(check_cmd)):
                        output = net_connect.send_command(commands[i])
                        file.write(output)
            finally:
                net_connect.disconnect()

    def primary_task(self):
        """
        Purpose of this code section is to login into the Cisco devices via telnet and execute the configuration data

        Part 01:
        Create a new excel file, get the IP data from the input excel file.
        based on device reachability add "YES" or "NO".

        Part 02:

        read data from input excel file to get device IP, hostname and password.
        execute Part 01.
        If ping result is success then execute telnet code to do necessary config changes.
        """

        if not os.path.isdir(self.output_dir): os.mkdir(self.output_dir)
        if not os.path.isdir(self.system_dir): os.mkdir(self.system_dir)
        of = os.path.join(self.output_dir, self.output_file)
        workbook = xlsxwriter.Workbook(of)
        worksheet = workbook.add_worksheet()
        worksheet.write(0, 0, "IP ADDRESS")
        worksheet.write(0, 1, "Reachability")
        worksheet.write(0, 2, "Config change")
        read_file = pd.read_excel(self.input_file, sheet_name='Sheet1', na_values=None, keep_default_na=False)
        for index in read_file.index:
            row = index + 1
            inventory = []
            for headers in read_file.columns:
                inventory.append(read_file[headers][index])
            host_ip, username, password, epass, region = inventory
            # host_ip, username, password, epass, region = inventory
            ping_result = self.ping_check(host_ip)
            if ping_result:
                worksheet.write(row, 0, host_ip)
                worksheet.write(row, 1, "Yes")
                print(f"\n\n---: {host_ip} is reachable, proceeding for config changes\n")
    # Precheck commands to be executed on device
                try:
                    check_cmd = [ "terminal length 0","show int description"]
                    precheck_data = self.telnet_to_device(host_ip, username, password, epass, check_cmd)
                    precheck_file = os.path.join(self.system_dir, host_ip + "_precheck_file" + time.strftime("%Y%m%d-%H%M%S") + "_.txt")
                    with open(precheck_file, "w+") as pref:
                        pref.write(precheck_data)
        # Following code is under test
                    with open(self.command_file, "r") as cmd:
                        execution_cmd = cmd.readlines()
                    ex_data_file = os.path.join(self.system_dir, host_ip + "_execution_file_" + time.strftime("%Y%m%d-%H%M%S") + "_.txt")
                    execution_data = self.telnet_to_device(host_ip, username, password, epass, execution_cmd)
                    with open(ex_data_file, "w") as pref:
                        pref.write(execution_data)
                    worksheet.write(row, 2, "Yes")
                    postcheck_data = self.telnet_to_device(host_ip, username, password, epass, check_cmd)
                    # postcheck = self.ssh_device(host_ip, username, password, check_cmd)
                    postcheck_file = os.path.join(self.system_dir, host_ip + "_postcheck_file_" + time.strftime("%Y%m%d-%H%M%S") + "_.txt")
                    with open(postcheck_file, "w+") as pref:
                        pref.write(postcheck_data)
                    self.compare_config(precheck_file, postcheck_file,host_ip)

                except Exception as e:
                    print({f"Error for {host_ip}: \n", e})


            else:
                worksheet.write(row, 0, host_ip)
                worksheet.write(row, 1, "No")
                worksheet.write(row, 2, "No")
                print(f"---: {host_ip} is not reachable.")
        workbook.close()
        print("\n\n---: Script execution completed :---")

# execution of task starts here
if __name__ == "__main__":
    task = telnet()
    task.primary_task()



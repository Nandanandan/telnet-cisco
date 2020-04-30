import telnetlib
# from login_data import creds
import pandas as pd
import os
import xlsxwriter
import diffios
import getpass


# Variables defined here

"""
file path + name of the input file
Data of input file contains destination ip and telnet credentials.

"""

input_file = "device_input_data.xlsx"
command_file = 'config'

def ping_check(host_ip):
    '''Ping to host_ip and return boolean output'''
    response = os.system("ping -c 2 " + host_ip)
    if response == 0:
        return True
    else:
        return False

def compare_config(precheck_file, postcheck_file,host_ip):
    '''

    This section of code is used to compare configuration before and after change.
    Post comparision it sill share output with listed changes.

    '''
    output_file = host_ip + "_config_diff_file"
    diff_config = diffios.Compare(precheck_file, postcheck_file)
    with open(output_file, "a+") as diff:
        diff.writelines(diff_config.delta())

def telnet_to_device(host_ip, username, password, commands):
    """
    This section of code will help to telnet and execute commands on cisco devices and return
    """

    tn = telnetlib.Telnet(host_ip)
    if username:
        tn.read_until(b"Username: ")
        tn.write(username.encode('ascii') + b"\n")
    else:
        print('username not required or provided')
    tn.read_until(b"Password: ")
    if password:
        tn.write(password.encode('ascii') + b"\n")
    else:
        print('Password must be provided')
        password = getpass.getpass("Please enter password:")
        tn.write(password.encode('ascii') + b"\n")

    tn.write(b"enable\n")
    tn.read_until(b"Password: ")
    epass = ""
    if epass:
        tn.write(epass.encode('ascii') + b"\n")
    else:
        print('Enable Password must be provided')
        epass = getpass.getpass("Please enter password:")
        tn.write(epass.encode('ascii') + b"\n")

    for command in commands:
        tn.write(command.encode('ascii') + b"\n")
    tn.write(b"exit\n")

    data = tn.read_all().decode('ascii')
    return data


def primary_task():
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
    of = "output_file.xlsx"
    workbook = xlsxwriter.Workbook(of)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "IP ADDRESS")
    worksheet.write(0, 1, "Reachability")
    worksheet.write(0, 2, "Config change")
    read_file = pd.read_excel(input_file, sheet_name='Sheet1', na_values=None, keep_default_na=False)
    for index in read_file.index:
        row = index + 1
        inventory = []
        for headers in read_file.columns:
            inventory.append(read_file[headers][index])
        host_ip, username, password = inventory
        ping_result = ping_check(host_ip)
        if ping_result:
            worksheet.write(row, 0, host_ip)
            worksheet.write(row, 1, "Yes")
            print(f"{host_ip} is reachable, proceeding for config changes")
# Precheck commands to be executed on device
            check_cmd = [ "terminal length 0","show int description"]
            precheck_data = telnet_to_device(host_ip, username, password, check_cmd)
            precheck_file = host_ip + "precheck_file.txt"
            with open(precheck_file, "w+") as pref:
                pref.write(precheck_data)
# Following code is under test
            with open(command_file, "r") as cmd:
                execution_cmd = cmd.readlines()
            ex_data_file = host_ip + "_execution_file.txt"
            execution_data = telnet_to_device(host_ip, username, password, execution_cmd)
            with open(ex_data_file, "w") as pref:
                pref.write(execution_data)
            worksheet.write(row, 2, "Yes")
            postcheck_data = telnet_to_device(host_ip, username, password, check_cmd)
            postcheck_file = host_ip + "_postcheck_file.txt"
            with open(precheck_file, "w+") as pref:
                pref.write(postcheck_data)
            compare_config(precheck_file, postcheck_file,host_ip)
        else:
            worksheet.write(row, 0, host_ip)
            worksheet.write(row, 1, "No")
            worksheet.write(row, 2, "No")
            print(f"{host_ip} is not reachable.")
    workbook.close()

# execution of task starts here
if __name__ == "__main__":
    primary_task()



import telnetlib
from login_data import creds
import pandas as pd
import os
import xlsxwriter

# import credentials


#
# host_ip = creds["host_ip"]
# username = creds["username"]
# password = creds["password"]

""" 
file path + name of the input file
Data of input file contains destination ip and telnet credentials.

"""
file_name = "device_input_data.xlsx"


def data_io():

    """
    read data from input excelfile.
    check ping response to ip addresses mentioned on input file.
    create a new output file and add IP, reachability status to the file.

    """
    of = "output_file.xlsx"
    workbook = xlsxwriter.Workbook(of)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, "IP ADDRESS")
    worksheet.write(0, 1, "Reachability")
    worksheet.write(0, 2, "Config change")
    read_file = pd.read_excel(file_name, sheet_name='Sheet1')
    for headers in read_file.columns:
        for index in read_file.index:
            row = index + 1
            if headers == "IP":
                device_ip = read_file[headers][index]
                response = os.system("ping -c 2 "+ device_ip)
                datawrite = ""
                if response == 0:
                    datawrite = "YES"
                    print("device is reachable")
                else:
                    datawrite = "NO"
                    print("device is not reachable")

                worksheet.write(row,0, device_ip)
                worksheet.write(row,1, datawrite)
    workbook.close()


if __name__ == "__main__":
    data_io()


# # commands to be executed on device
# commands = {
#             "command1": "terminal length 0",
#             "command2": "show int description"
#            }
#
# print(f"Telnet to device: {host_ip}")
#
# """
# code section  to login and to device and get the output

# """
#
# tn = telnetlib.Telnet(host_ip)
# tn.read_until(b"Username: ")
# tn.write(username.encode('ascii') + b"\n")
# tn.read_until(b"Password: ")
# tn.write(password.encode('ascii') + b"\n")
# for key in commands:
#     tn.write(commands[key].encode('ascii') + b"\n")
# tn.write(b"exit\n")
#
# data = tn.read_all().decode('ascii')
#
# print(data)

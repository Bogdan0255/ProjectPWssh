import paramiko
import pandas as pd
from IPs import device_ips
import openpyxl
from datetime import date

# Define the SSH connection parameters
username = "pi"  # replace with the username of the user whose password you want to change
current_password = "radiocompi"  # replace with the current password for the user
new_password = "radiocompi2"  # replace with the desired new password for the user

# Create empty lists to store the results
success_ips = []
failed_ips = []

# Loop through the IP addresses and run the password change command for each Raspberry Pi
for ip in device_ips:
    try:
        # Create an SSH client and connect to the Raspberry Pi
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, username=username, password=current_password)

        # Send the current and new passwords to the passwd command to change the user's password
        stdin, stdout, stderr = ssh.exec_command(f"echo '{current_password}\n{new_password}\n{new_password}' | passwd {username}")

        # Check if the command was successful
        if stdout.channel.recv_exit_status() == 0:
            success_ips.append(ip)
        else:
            failed_ips.append(ip)

    except Exception as e:
        # Print any errors that occur during the SSH connection or command execution
        print(f"Error occurred while changing password on {ip}: {str(e)}")
        failed_ips.append(ip)

    finally:
        # Close the SSH connection
        ssh.close()

# Create dataframes for the success_ips and failed_ips lists
success_df = pd.DataFrame(success_ips, columns=['IP address'])
failed_df = pd.DataFrame(failed_ips, columns=['IP address'])

# Get the current date and format it as a string to include in the Excel file name
today = date.today().strftime("%d-%m-%Y")

# Save the dataframes to Excel files with the current date in the file name
success_df.to_excel(f'update_succesfuly_{today}.xlsx', index=False)
failed_df.to_excel(f'update_not_possible_{today}.xlsx', index=False)

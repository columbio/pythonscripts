import paramiko
import csv
import logging

logging.basicConfig(filename='sshcli.log', encoding='utf-8', level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s',)

def connect_and_apply(host,user,secret):
    try:
        logging.info(f'Creating SSH Client')
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #
        logging.info(f'Connecting to host: {host}')
        client.connect(hostname=host,username=user,password=secret,port=22,timeout=10,banner_timeout=200, look_for_keys=False)
        #
        (stdin, stdout, stderr) = client.exec_command("hostname && adduser mpuser && echo Tyad2ffGGDDb5w4T | passwd --stdin mpuser")
        #
        for line in stdout.readlines():
            print(line)
            logging.info(f'command output: {line}')
    #
    except paramiko.AuthenticationException:
        print(f'Authentication failed, please verify your credentials for host: {host}')
        logging.error(f'Authentication failed, please verify your credentials for host: {host}')
    except paramiko.SSHException as sshException:
        print("Unable to establish SSH connection: %s" % sshException)
        logging.error("Unable to establish SSH connection: %s" % sshException)
    except paramiko.BadHostKeyException as badHostKeyException:
        print("Unable to verify server's host key: %s" % badHostKeyException)
        logging.error("Unable to verify server's host key: %s" % badHostKeyException)
    finally:
        client.close() 

with open('hosts.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, skipinitialspace=True)
    #
    for row in reader:
        logging.info(f'address: {row["address"]}\tlogin: {row["login"]}\tpassword: {row["password"]}')
        connect_and_apply(row["address"], row["login"], row["password"])
    #
    csvfile.close()


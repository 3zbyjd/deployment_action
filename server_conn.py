from configparser import ConfigParser
import time
import paramiko
import select

# Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")

# Get server config
serverconfig = config_object["SERVERCONFIG"]

host = serverconfig["host"]
username = serverconfig["username"]
sshPassword = serverconfig["password"]
sshKeyFilename = serverconfig["sshKeyFilename"]
sshKeyPassphrase = serverconfig["sshKeyPassphrase"]

clientSession = paramiko.SSHClient()
clientSession.set_missing_host_key_policy(paramiko.AutoAddPolicy())
sshpkey = paramiko.RSAKey.from_private_key_file(sshKeyFilename, sshKeyPassphrase)
clientSession.connect(hostname=host, username=username, pkey=sshpkey)

commands = ["cd www/rlomuniv/", "pwd"]

for cmd in commands:
    stdin, stdout, stderr = clientSession.exec_command(cmd)

    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
            if len(rl) > 0:
                tmp = stdout.channel.recv(1024)
                output = tmp.decode()
                print(output)

    # time.sleep(1)
    # stdout
    # print(stdout.read().decode())
    # print(stderr.read().decode())

clientSession.close()

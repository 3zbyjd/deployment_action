from configparser import ConfigParser
import time
import paramiko

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

stdin, stdout, stderr = clientSession.exec_command("pwd")
time.sleep(0.5)
print(stdout.read().decode())
print(stderr.read().decode())

clientSession.close()

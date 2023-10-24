from configparser import ConfigParser
import os.path
import time
import paramiko

#Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")

# Get server config
serverconfig = config_object["SERVERCONFIG"]

host = serverconfig["host"]
username = serverconfig["username"]
password = serverconfig["password"]
sshKeyFilename = os.path.join(os.path.expanduser('~'), ".ssh", "id_ed25519")
sshKeyPassphrase = serverconfig["sshKeyPassphrase"]

#print("Server IP address = {}".format(host))
#print("Password = {}".format(password))

clientSession = paramiko.SSHClient()
clientSession.set_missing_host_key_policy(paramiko.AutoAddPolicy())
clientSession.connect(hostname=host,
                      look_for_keys=True,
                      username=username,
                      password=password,
                      key_filename=sshKeyFilename,
                      passphrase=sshKeyPassphrase)

stdin, stdout, stderr = clientSession.exec_command('sudo cd /home/demond/.ssh')
time.sleep(.5)
print(stdout.read().decode())
print(stderr.read().decode())

stdin, stdout, stderr = clientSession.exec_command('pwd')
time.sleep(.5)
print(stdout.read().decode())
print(stderr.read().decode())

clientSession.close()
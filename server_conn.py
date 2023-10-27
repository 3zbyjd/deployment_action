from configparser import ConfigParser
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
sshKeyFilename = serverconfig["sshKeyFilename"]
sshKeyPassphrase = serverconfig["sshKeyPassphrase"]

#print("Server IP address = {}".format(host))
#print("Password = {}".format(password))
clientSession = paramiko.SSHClient()
clientSession.set_missing_host_key_policy(paramiko.AutoAddPolicy())
clientSession.connect(hostname=host,
                      username=username, 
                      password=password)

stdin, stdout, stderr = clientSession.exec_command('cd ~/.ssh')
time.sleep(.5)
print(stdout.read().decode())
print(stderr.read().decode())

stdin, stdout, stderr = clientSession.exec_command('pwd')
time.sleep(.5)
print(stdout.read().decode())
print(stderr.read().decode())

clientSession.close()
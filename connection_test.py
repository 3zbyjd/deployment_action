import paramiko
from configparser import ConfigParser

#Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")

# Get server config
serverconfig = config_object["SERVERCONFIG"]

command = serverconfig["command"]
host = serverconfig["host"]
username = serverconfig["username"]
password = serverconfig["password"]

print("Server IP address = {}".format(host))
print("Password = {}".format(password))
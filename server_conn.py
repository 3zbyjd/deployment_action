from configparser import ConfigParser
import time
import os
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
sftpRemoteDirectory = serverconfig["sftpRemoteDirectory"]
sftpLocalDirectory = serverconfig["sftpLocalDirectory"]

sshClient = paramiko.SSHClient()
sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
sshpkey = paramiko.RSAKey.from_private_key_file(sshKeyFilename, sshKeyPassphrase)

try:
    # Establish ssh connection to remote server
    print("Attempting to establish ssh connection")
    sshClient.connect(hostname=host, username=username, pkey=sshpkey)
    # sshClient.connect(hostname=host, username=username, password=sshPassword)
    print("Connection successfully established with", host)

    # Established sftp connection
    print("Transitioning to SFTP client")
    sftpClient = sshClient.open_sftp()
    print("Successfully transitioned to SFTP client")

    # Changing directory to target directory
    sftpClient.chdir(sftpRemoteDirectory)

    # Print current working directory
    print(sftpClient.getcwd())

    dirContentList = os.listdir(sftpLocalDirectory)
    if len(dirContentList) > 0:
        recurseContents(dirContentList)

except:
    print("[!] Connection attempt failed")
    exit()


def recurseContents(contentList):
    for contentItem in contentList:
        if os.path.isfile(contentItem):
            ftpClient.put(contentItem, sftpRemoteDirectory)
        else:
            sftpClient.mkdir(contentItem)
            sftpClient.chdir(contentItem)
            subContentList = os.listdir(contentItem)
            if len(subContentList) > 0:
                recurseContents(subContentList)
            sftpClient.chdir("../")

    pass


# commands = ["www/rlomuniv/", "pwd"]

# commands = ["pwd", "id", "uname -a", "df -h"]

# for cmd in commands:
#     print("=" * 50, cmd, "=" * 50)

#     stdin, stdout, stderr = clientSession.exec_command(cmd)

#     print(stdout.read().decode())

#     cmderror = stderr.read().decode()

#     if cmderror:
#         print(cmderror)

sshClient.close()

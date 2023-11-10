from configparser import ConfigParser
import time
import imghdr
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


def recurseContents(contentDir, contentList):
    fileExistsTF = False

    parentDirectory = contentDir
    workingDirectory = parentDirectory

    for contentItem in contentList:
        """if os.path.isfile(contentItem):
        sftpClient.put(contentItem, sftpRemoteDirectory)"""
        splitItems = contentItem.split(".")
        if len(splitItems) == 2:
            if splitItems[1] in (
                "gif",
                "jpeg",
                "jpg",
                "png",
                "js",
                "html",
                "htm",
                "json",
                "exe",
                "pdb",
                "dll",
                "pdf",
            ):
                sftpClient.put(contentItem, sftpRemoteDirectory)
        elif len(splitItems) == 3:
            if splitItems[2] in (
                "gif",
                "jpeg",
                "jpg",
                "png",
                "js",
                "html",
                "htm",
                "json",
                "exe",
                "pdb",
                "dll",
                "pdf",
            ):
                sftpClient.put(contentItem, sftpRemoteDirectory)

        else:
            try:
                sftpClient.stat(contentItem)
            except IOError as e:
                if "No such file" in str(e):
                    fileExistsTF = False
            else:
                fileExistsTF = True

            if not fileExistsTF:
                sftpClient.mkdir(contentItem, 755)
                sftpClient.chown(contentItem, 1000, 1000)
                sftpClient.chdir(contentItem)
                # Print current working directory
                print(sftpClient.getcwd())
            else:
                sftpClient.chdir(contentItem)
                # Print current working directory
                print(sftpClient.getcwd())

            workingDirectory = os.path.join(workingDirectory, contentItem)
            subContentList = os.listdir(workingDirectory)
            if len(subContentList) > 0:
                recurseContents(workingDirectory, subContentList)
            sftpClient.chdir("../")

    pass


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
        recurseContents(sftpLocalDirectory, dirContentList)

except:
    print("[!] Connection attempt failed")
    exit()

sshClient.close()

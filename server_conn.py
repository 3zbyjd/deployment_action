from configparser import ConfigParser

# import time
# import imghdr
import os
import paramiko
import select


def main():
    print("Hello from GitHub Actions!")
    host = os.environ.get("HOST")

    if not host:
        raise RuntimeError("HOST env var is not set!")
    print("Host = ", host)


if __name__ == "__main__":
    main()

# def main():
#     print("Begin python script")

#     # Read config.ini file
#     config_object = ConfigParser()
#     config_object.read("config.ini")

#     # Get server config
#     serverconfig = config_object["SERVERCONFIG"]

#     host = serverconfig["host"]
#     username = serverconfig["username"]
#     sshPassword = serverconfig["password"]
#     sshKeyFilename = serverconfig["sshKeyFilename"]
#     sshKeyPassphrase = serverconfig["sshKeyPassphrase"]
#     sftpRemoteDirectory = serverconfig["sftpRemoteDirectory"]
#     sftpLocalDirectory = serverconfig["sftpLocalDirectory"]

#     sshClient = paramiko.SSHClient()
#     sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     sshpkey = paramiko.RSAKey.from_private_key_file(sshKeyFilename, sshKeyPassphrase)
#     # sshpkey = paramiko.Ed25519Key.from_private_key_file(sshKeyFilename, sshKeyPassphrase)

#     try:
#         # Establish ssh connection to remote server
#         print("Attempting to establish ssh connection")
#         sshClient.connect(hostname=host, username=username, pkey=sshpkey)
#         # sshClient.connect(hostname=host, username=username, password=sshPassword)
#         print("Connection successfully established with", host)

#         # Established sftp connection
#         print("Transitioning to SFTP client")
#         sftpClient = sshClient.open_sftp()
#         print("Successfully transitioned to SFTP client")

#         # Changing directory to target directory
#         sftpClient.chdir(sftpRemoteDirectory)

#         # Print current working directory
#         print("Default working directory is {}".format(sftpClient.getcwd()))

#         for rootPath, dirs, fileItem in os.walk(sftpLocalDirectory):
#             if len(rootPath) > 56:
#                 dirPath = rootPath[56:].replace("\\", "/")
#                 remoteDirPath = sftpRemoteDirectory + dirPath
#             else:
#                 remoteDirPath = sftpRemoteDirectory

#             try:
#                 # currentDir = dirs[0]
#                 currentDir = remoteDirPath
#             except IndexError as e:
#                 print("No more directories to traverse")

#             try:
#                 sftpClient.stat(currentDir)
#             except IOError as e:
#                 if "No such file" in str(e):
#                     fileExistsTF = False
#             else:
#                 fileExistsTF = True

#             if not fileExistsTF:
#                 sftpClient.mkdir(currentDir, 755)
#                 sftpClient.chown(currentDir, 1000, 1000)
#                 sftpClient.chdir(currentDir)
#                 # Print current working directory
#                 print(
#                     "Transitioned to {} as working directory".format(
#                         sftpClient.getcwd()
#                     )
#                 )
#             else:
#                 sftpClient.chdir(currentDir)
#                 print(
#                     "Transitioned to {} as working directory".format(
#                         sftpClient.getcwd()
#                     )
#                 )
#                 # Print current working directory
#                 # print(sftpClient.getcwd())

#             # print(rootPath)
#             # print(currentDir)
#             # print(dirs)

#             for thisFile in fileItem:
#                 localFilePath = rootPath + "\\" + thisFile
#                 remoteFilePath = currentDir + "/" + thisFile
#                 sftpClient.put(localFilePath, remoteFilePath)
#                 print(
#                     "File {} has been uploaded to remote {}".format(
#                         thisFile, currentDir
#                     )
#                 )
#                 # print(fileItem)

#     except Exception as e:
#         print("[!] Connection attempt failed")
#         exit()

#     sshClient.close()

from paramiko import SSHClient, AutoAddPolicy, SFTPClient
from scp import SCPClient
from logger import Logger
import platform
import config
import time
import sys
import os

date = time.strftime(config.date_format)
logger = Logger(config.backup_log)

# This function check if the script is running on a unix based operating system.
def os_check():

    if sys.platform.startswith('linux'):

        return True

    else:

        return False

def backup():

    if len(config.backup_dirs) == 0:

        logger.log("INFO", "No directories to backup")

    else:

        counter = 0

        for dir in config.backup_dirs:
            
            backupFileName = getFileName('backup_' + str(counter + 1)) + '.tar.gz'
            counter += 1
            
            logger.log("INFO", "Starting backup for '"+dir+"'...")
            status = os.system("cd " + config.backup_tmp + " && tar -czvf " + backupFileName + " " + dir)
            
            if status != 0:
                logger.log("ERROR", "Failed to backup '"+ dir +"'")
            
            logger.log("INFO", "Sending backup '"+ backupFileName +"' for "+config.backup_remote_host+"...")

            ssh = createSSHClient()

            try:
                
                scp = SCPClient(ssh.get_transport(), progress=progress)
                scp.put(config.backup_tmp +"/"+ backupFileName, remote_path=config.backup_remote_location)
                logger.log("SUCCESS", "Backup for "+dir+" successfully")

            except Exception as e:

               logger.log("ERROR", "Failed to send backup '"+ backupFileName +"'")
        
        ssh.close()
        scp.close()


def createSSHClient():

    try:

        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())

        if config.backup_remote_ssh_key_file:

            client.load_system_host_keys(config.backup_remote_ssh_key_file)
            client.connect(config.backup_remote_host, config.backup_remote_port, config.backup_remote_user)

        else:
            
            client.connect(config.backup_remote_host, config.backup_remote_port, config.backup_remote_user, config.backup_remote_pass)

    except Exception as e:

        logger.log("ERROR", str(e))

    return client

def progress(filename, size, sent):

    sys.stdout.write("%s's progress: %.2f%%   \r" % (filename, float(sent)/float(size)*100) )

def getFileName(name):
    
    fileName = config.backup_name_format
    hostname = platform.node()
    fileName = fileName.replace('%hostname%', hostname)
    fileName = fileName.replace('%date%', date)
    fileName = fileName.replace('%backupName%', name)

    return fileName

if os_check():

    backup()
    logger.closeFile()

else:

    logger.log("ERROR", "Sorry but this script is only for Linux")
    logger.closeFile()

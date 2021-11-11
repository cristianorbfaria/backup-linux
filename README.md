# Backup Linux

## Installation
- Clone repository 
    ```console
    git clone https://github.com/cristianorbfaria/backup-linux.git
    ```
- Ubuntu
  - Install Python
    ```console
    apt install python3 python3-pip
    ```
- RHEL
  - Install Python
    ```console
    yum install python3 python3-pip
    ```
- Copy file ``config.py.example`` to ``config.py``
- Edit the ``config.py`` with a text editor
- Install dependencies
    ```console
    pip3 install -r requirements.txt
    ```
- Setup cronjob with ``crontab -e``. 
  - This cronjob backup your Linux server every day at 3 AM 
    ```console
    0 3 * * * python3 /opt/script/backup-linux/run.py
    ```
import os.path
import getpass

filename = '/etc/systemd/system/ping_log.service'

text = \
'[Unit]\n\
Description=Service Logging Ping-Results\n\
After=network.target\n\
StartLimitIntervalSec=10\n\
\n\
[Service]\n\
Type=simple\n\
Restart=always\n\
RestartSec=10\n\
WorkingDirectory={dir}\n\
User={user}\n\
ExecStart={exec}\n\
\n\
[Install]\n\
WantedBy=multi-user.target'

path = os.path.abspath('./show.py').replace('show.py','')

exec = 'python3 ./show.py'

user = getpass.getuser()

with open(filename, mode='w') as file:
    file.write(text.format(exec=exec, user=user, dir = path))

os.popen('systemctl enable ping_log')
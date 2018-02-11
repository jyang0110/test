import paramiko

t = paramiko.Transport('169.254.154.179','22')
t.connect(username = 'pi', password = '123')

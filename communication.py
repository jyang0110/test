import paramiko

#Sending data from PC to raspberry Pi
#t = paramiko.Transport('192.168.20.223','22')
#t.connect(username = 'pi', password = '123')
#sftp = paramiko.SFTPClient.from_transport(t)
#remotepath='checkbutton.txt'
#localpath='C:\Users\yangw\OneDrive\Desktop\checkbutton.txt'
#sftp.put(localpath,remotepath)
#t.close()

#Downloading data from raspberry Pi to PC
t = paramiko.Transport('192.168.20.223','22')
t.connect(username = 'pi', password = '123')
sftp = paramiko.SFTPClient.from_transport(t)
remotepath= 'checkbutton.txt'
localpath= 'C:\Users\yangw\OneDrive\Desktop\checkbutton.txt'
sftp.get(remotepath, localpath)
t.close()

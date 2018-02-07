import paramiko

#t = paramiko.Transport('192.168.20.223','22')
#t.connect(username = 'pi', password = '123')
#sftp = paramiko.SFTPClient.from_transport(t)
#remotepath='Windows.txt'
#localpath='C:\Users\yangw\OneDrive\Desktop\Windows.txt'
#sftp.put(localpath,remotepath)
#t.close()

t = paramiko.Transport('192.168.20.223','22')
t.connect(username = 'pi', password = '123')
sftp = paramiko.SFTPClient.from_transport(t)
remotepath= 'Windows.txt'
localpath= 'C:\Users\yangw\OneDrive\Desktop\Windows.txt'
sftp.get(remotepath, localpath)
t.close()

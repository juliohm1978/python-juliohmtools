import svn.remote

client = svn.remote.RemoteClient(url='file:///home/lamento/tmp/asdf/repo')

info = client.info()
print(info['entry#path']+' - '+str(info['entry#revision']))
print()

for entry in client.list():
    info = client.info(entry)
    print(info['entry#path']+' - '+str(info['entry#revision']))

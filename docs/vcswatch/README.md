# VCSWatch

A Version Control System (VCS) module that can watch a remote repository for changes and notify a list of callback handler functions.

It uses a polling mechanism to request information from the remote repository regularly.

Currently, only Subversion is a supported backend. Planning to add Git in the near future.

## Examples

```python
from juliohmtools import vcswatch
from juliohmtools import vcswatchclient
import logging

## Standard python logging. Format messages to your needs.
## Enable DEBUG level to see full stack traces if you come across any errors.
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)-8s] [%(name)s] [%(funcName)s] %(message)s')

## Handler function that will be notified whenever a change occurs in the remote repo
def myhandler(client, old_rev, new_rev):
    latest_tag = None
    rev = -1

    ## find the latest tag in the remote repo
    for entry in client.svnclient.list('/'):
        if entry['commit_revision'] > rev:
            rev = entry['commit_revision']
            latest_tag = entry['name']

    print('latest tag: '+latest_tag+' ('+str(rev)+')')

## Create a VCSWatchClient
client = vcswatchclient.VCSWatchClientSVN()
client.set_url('https:/myrepo.example.com/tags')

## Set your credentials (Optional)
client.set_username('myuser')
client.set_password('mysecret')

## Create a VCSWatch
w = vcswatch.VCSWatch()

## Only change this if you are unable to read+write to /var/lib/vcswatch.
## w.set_cachedir('/path/to/another/cache/directory')

## Define a polling interval. Default: 300 (5min)
w.set_polling_interval(5)

## Set your VCS client
w.set_client(client)

## Add your function to the handler list
w.add_handler(myhandler)

## Start background thread to watch for changes
w.watch_background()
```

## Directories and Permissions

By default, `VCSWatch` will keep cached information about the remote repository in `/var/lib/vcswatch`. Make sure thie directory exists and is provided with read/write permissions for the user running your python script.

You can change the cache directory using the method `VCSWatch.set_cachedir(string)`.

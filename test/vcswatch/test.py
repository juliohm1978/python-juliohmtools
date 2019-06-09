from juliohmtools import vcswatch
from juliohmtools import vcswatchclient
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)-8s] [%(name)s] [%(funcName)s] %(message)s')

def myhandler(client, old_rev, new_rev):
    latest_tag = None
    rev = -1
    for entry in client.svnclient.list('/'):
        if entry['commit_revision'] > rev:
            rev = entry['commit_revision']
            latest_tag = entry['name']
    print('latest tag: '+latest_tag+' ('+str(rev)+')')

client = vcswatchclient.VCSWatchClientSVN()
client.set_url('file:///home/lamento/tmp/asdf/repo/tags')

w = vcswatch.VCSWatch()
w.set_polling_interval(5)
w.set_client(client)
w.add_handler(myhandler)
w.watch_background()
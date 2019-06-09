import svn
import logging
import pathlib
import time
from vcswatchclient import VCSWatchClient

logger = logging.getLogger(__name__)

class VCSWatch():
    """
    A class that keeps watch over a remote Version Control System repository
    and delagates action to a handler when new commits or tags are created.

    It uses a polling mechanism to request the remote repository for the
    lastest commit revision. If there are changes, handler functions are called
    to notify any interested parties.
    """

    client = None
    handlers = list()
    cachedir = '/var/lib/vcswatch'

    polling_interval = 300

    def set_url(self, client: VCSWatchClient):
        '''
        Client that will be used to fetch information about the remote repository.
        '''
        self.client = client

    def add_handler(self, handler):
        '''
        Handler functions that will be called when new commits or tags are
        created in the remote repository.

        Handler signature
        ==================
        ```
        def my_handler(client, old_rev, new_rev):
            pass
        ```

        Handler parameters
        ===================
        `client`:
            VCSWatchClient object used to connect to the remote repository

        `old_rev`:
            Old revision number that was previously kept in cache for the watch.

        `new_rev`:
            New revision number that was found in the remote repository.
        '''
        self.handlers.append(handler)

    def set_cachedir(self, dir):
        '''
        Cache directory where VCSWatch keeps information about the remote
        repository. This is necessary in order to keep track of changes
        that happen between polls.

        Default: `/var/lib/vcswatch`
        '''
        self.cachedir = dir

    def set_polling_interval(self, interval_seconds):
        '''
        How long to wait between polling requests to the remote repository.

        Default: `300 (5min)`
        '''
        self.polling_interval = interval_seconds

    def watch(self):
        if not self.client:
            raise Exception('There are no clients defined. Use VCSWatch.set_client() to define one.')

        logging.info('Watching remote repository '+client)
        while True:
            try:
                clientrev = client.get_last_revision()
                clienthash = client.get_hash()

                if not clientrev:
                    logger.error('Not a valid revision '+client)

                if not clienthash:
                    logger.error('Not a valid hash '+client)

                local_cache_file = self.cachedir + '/' + clienthash + '.rev'
                localrev = pathlib.Path(local_cache_file).read_text()
                logging.debug('Old revision acquired from local cache ['+local_cache_file+'] '+localrev)

                if localrev != clientrev:
                    logging.debug('Revision changed for client '+client)
                    for h in self.handlers
                        h(client, localrev, clientrev)
                    pathlib.Path(local_cache_file).write_text(clientrev)
                    logging.debug('New revision written to local cache ['+local_cache_file+'] '+clientrev)
            except Exception as err:
                logging.error('Error watching remote repository: '+err)
                logging.debug(err, exc_info=True)
            finally:
                time.sleep(self.polling_interval)

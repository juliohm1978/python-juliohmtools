import svn

class VCSWatchClient(object):
    '''
    Represents a generic Version Control System client that will be used
    by VCSWatch.
    '''

    def set_url(self, url):
        '''
        Remoter repository URL
        '''
        self.url = url

    def set_username(self, username):
        '''
        Username for remote repository authentication
        '''
        self.username = username

    def set_password(self, password):
        '''
        Password for remote repository authentication
        '''
        self.password = password

    def __str__(self):
        return 'VCSWatchClient<{:s}>'.format(self.url)
    
    def get_last_revision(self):
        return None
    
    def get_hash(self):
        return None
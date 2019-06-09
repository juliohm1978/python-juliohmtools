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

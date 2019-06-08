import kubernetes
import os
import logging
import threading
import time

logger = logging.getLogger(__name__)

class Controller():
    '''
    A general purpose controller wrapped around the Kubernetes API.

    This controller will only listen to sepecific type of CRD, given its
    group, version, plural name and, optionally, a namespace.

    It will not listen to native Kubernetes objects.
    '''

    timeout_seconds = 300
    reconnect_interval_seconds = 15

    stop = False

    def __init__(self, group, name, version=None, namespace=None, kubeconfig_file=None):
        '''
        Parameters
        ----------
        kubeconfig_file:
            Kubernetes configuration used to access the cluster. If not
            provided, in-cluster configuration will be loaded.
        
        namespace:
            Restrict the actions of this controller to a specific namespace.

        group:
            Name of the CRD group to watch.
        
        version: (optional)
            Version of the CRD to watch. Default: v1

        name:
            Name of the object, or its plural name.
        
        namespace: (optional)
            Namespace to watch for resources. If empty, watch for events in
            all namespaces.
        '''
        if kubeconfig_file:
            logging.info('Using kubeconfig_file='+str(kubeconfig_file))
            self.kconfig = kubernetes.config.load_kube_config(config_file=kubeconfig_file)
        elif 'KUBERNETES_SERVICE_HOST' in os.environ:
            self.kconfig = kubernetes.config.load_incluster_config()
        else:
            raise Exception('Unable to load Kubernetes configuration')
        
        self.group     = group
        self.version   = version
        self.name      = name
        self.namespace = namespace

        if not self.version:
            self.version = 'v1'

    def set_api_timeout(timeout_seconds):
        '''
        Timeout waiting for Kubernetes API events. When this time expires, the
        controller will reloop, reconnect to the stream connection and keep
        watching for events.

        Parameters
        ----------
        timeout_seconds:
            Time in seconds to wait for API events. Default: 300 (5min)
        '''
        self.timeout_seconds=timeout_seconds

    def set_reconnect_interval(reconnect_interval_seconds):
        '''
        How long to wait and reconnect to the API server after a timeout.

        Parameters
        ----------
        reconnect_interval_seconds:
            Time in seconds to wait before reconnecting. Default: 15
        '''
        self.reconnect_interval_seconds=reconnect_interval_seconds

    def watch(self):
        '''
        Main loop that watches over CRD events.
        '''
        crdapi  = kubernetes.client.CustomObjectsApi()
        watch = kubernetes.watch.Watch()

        while not self.stop:
            try:
                stream = None
                if self.namespace:
                    logger.info('Watching for CRD group={:s} version={:s} name={:s} namespace={:s}'.format(self.group, self.version, self.name, self.namespace))
                    stream = watch.stream(
                        crdapi.list_namespaced_custom_object,
                        group=self.group,
                        version=self.version,
                        plural=self.name,
                        timeout_seconds=self.timeout_seconds
                        )
                else:
                    logger.info('Watching for CRD group={:s} version={:s} name={:s}'.format(self.group, self.version, self.name))
                    stream = watch.stream(
                        crdapi.list_cluster_custom_object,
                        group=self.group,
                        version=self.version,
                        plural=self.name,
                        timeout_seconds=self.timeout_seconds
                        )
                for event in stream:
                    obj_name      = event['object']['metadata']['name']
                    obj_namespace = event['object']['metadata']['namespace']
                    ev_type       = event['type']
                    onEvent(event, event['object'])
            except Exception as err:
                logging.error('Error watching: '+str(err))
                logging.debug(err, exc_info=True)
                time.sleep(self.reconnect_interval_seconds)
 
    def watchBackground(self):
        '''
        Start watch() in a background thread.

        Returns
        -------
        The thread object where the loop is running.
        '''
        th = threading.Thread(target=self.watch)
        th.start()
        return th

    def onEvent(self, event, obj):
        '''
        Default implementation for the CRD event handler. Override this method to implement your logic.
        '''
        logger.info('{:s}: {:s}/{:s} Nothing to do'.format(ev_type, obj['metadata']['namespace'], obj['metadata']['name']))


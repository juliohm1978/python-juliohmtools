from juliohmtools import k8scontroller
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(levelname)-8s] [%(name)s] [%(funcName)s] %(message)s')

c = k8scontroller.Controller()
c.set_group('kool.karmalabs.local')
c.set_name('guitars')
c.set_kubeconfig_file('/home/lamento/.kube/kind-config-kind')
c.set_api_timeout(0)
th = c.watch_background()

th.join()

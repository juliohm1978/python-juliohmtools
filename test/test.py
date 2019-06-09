from juliohmtools import k8scontroller
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(levelname)-8s] [%(name)s] [%(funcName)s] %(message)s')

def handle(event, obj):
    print(event)

c = k8scontroller.Controller()
c.set_group('my.example.resource')
c.set_name('guitars')
c.set_kubeconfig_file('/home/lamento/.kube/kind-config-kind')
c.add_handler(handle)
th = c.watch_background()

th.join()

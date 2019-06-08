from juliohmtools import k8scontroller
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(levelname)-8s] [%(name)s] [%(funcName)s] %(message)s')

c = k8scontroller.Controller('kool.karmalabs.local', 'guitars', kubeconfig_file='/home/lamento/.kube/kind-config-kind')
c.set_api_timeout(5)
th = c.watch_background()

time.sleep(10)

th.join()

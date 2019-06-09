# Kubernetes Controller Wrapper

Using the [python kubernetes-client](https://github.com/kubernetes-client/python), this library provides a quick and simple wrapper object that makes it easy to implement your own Kubernetes Controller for your Custom Resource Definitions (CRDs).

## Examples

The `test/k8scontroller` directory provides a couple of files you can use for a quick test:

* `guitarscrd.yaml`
* `guitars.yaml`

The first step is to create the CRD for `Guitar` objects.

```shell
kubectl apply -f guitarscrd.yaml
```

A custom controller for that resource can be improvised with a few lines of code.

```python
from juliohmtools import k8scontroller

def handle_event_function(event, obj):
    print(event)

c = k8scontroller.Controller()
c.set_kubeconfig_file('/path/to/kube/config')
c.set_group('my.example.resource')
c.set_name('guitars')
c.set_version('v1')

# Add as many handler functions as you want to the list.
# They will be called in order.
c.add_handler(handle_event_function)

c.watch()
```

Notes:

* `set_kubeconfig_file()` is optional and is only needed for local testing. If left empty, the controller will attempt to load in-cluster configuration.

* `set_version()` is also optional and assumes the default `v1`.

It is possible to run the `watch()` method in a background thread. Just use `watch_background()` instead.

```python
## snip...
threadObject = c.watch_background()
```

`watch_backgroun()` returns the Thread object so you can decide what to do with it in your code.

With a running controller connected to your Kubernetes cluster, you can create `Guitar` objects and see the controller reacting to events.

```shell
kubectl apply -f guitarscrd.yaml

## controller will react to ADD events

kubectl delete -f guitarscrd.yaml

## controller will react to DELETE events
```

## Logging and Debugging

The controller uses [python's default logging library](https://docs.python.org/3/library/logging.html). You can format log messages to your needs and see more details (including full stack traces) by increasing the level to `DEBUG`.

```python
import logging

logging.basicConfig(
  level=logging.DEBUG,
  format='[%(asctime)s] [%(levelname)-8s] [%(name)s] [%(funcName)s] %(message)s'
)
```

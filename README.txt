Pytest-MarkFiltration
=====================

The default py.test keyword filtering (-k) is _way_ too broad. You would think that it
would be based on the MarkInfo objects that are described alongside the filter option
but that would be incorrect. In fact, it chooses the method/function name of the script
as well.

This plugin introduces a -f flag for pytest that takes the name of a MarkInfo object to
either keep or remove from the collected scripts.

The syntax is the same as with -k. So...

To include a script with a MarkInfo object on it

py.test -f rhino

And to disclude one

py.test -f -hippo

To install, either
* pip install pytest-markfiltration
* python setup.py install

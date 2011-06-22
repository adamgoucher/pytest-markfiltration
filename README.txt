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

Just like with -k you can do an 'and' collection as well with

py.test -f "hippo rhino"

or

py.test -f "hippo -rhino"

But the built-in -k does not let you do an 'or' collection. -f does allow for it though through multiple instances of he flag

py.test -f hippo -f rhino

and perhaps a silly example of

py.test -f hippo -f -rhino

To install, either
* pip install pytest-markfiltration
* python setup.py install

import copy
import pytest, py
from _pytest.mark import MarkInfo

def pytest_addoption(parser):
    group = parser.getgroup("general")
    group._addoption('-f',
        action="append", dest="filter", default=[], metavar="FILTEREXPR",
        help="only run tests which have marks that match given"
             "keyword expression.  "
             "An expression consists of space-separated terms. "
             "Each term must match. Precede a term with '-' to negate.")

# blatantly lifted from _pytest.mark.py
def pytest_collection_modifyitems(items, config):
    filterlist = config.option.filter
    if not filterlist:
        return

    remaining = []
    deselected = []
    for filtr in filterlist:
        dirty_items = copy.copy(items)
        
        for item in dirty_items:
            if filtr and skipbykeyword(item, filtr):
                deselected.append(item)
            else:
                remaining.append(item)  
                
    if deselected:
        config.hook.pytest_deselected(items=deselected)
        items[:] = remaining

# blatantly lifted from _pytest.mark.py
def skipbykeyword(colitem, keywordexpr):
    """ return True if they given keyword expression means to
        skip this collector/item.
    """
    if not keywordexpr:
        return

    itemkeywords = getkeywords(colitem)
    for key in filter(None, keywordexpr.split()):
        eor = key[:1] == '-'
        if eor:
            key = key[1:]
        if not (eor ^ matchonekeyword(key, itemkeywords)):
            return True

# blatantly lifted from _pytest.mark.py but checks not for whether it is a MarkInfo object
def getkeywords(node):
    keywords = {}
    while node is not None:
        for keyword in node.keywords:
            if isinstance(node.keywords[keyword], MarkInfo):
                keywords[keyword] = node.keywords[keyword]
        node = node.parent
    return keywords

# blatantly lifted from _pytest.mark.py
def matchonekeyword(key, itemkeywords):
    for elem in key.split("."):
        for kw in itemkeywords:
            if elem in kw:
                break
        else:
            return False
    return True
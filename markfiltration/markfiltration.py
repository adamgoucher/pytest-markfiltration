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
    # the terminal reporter is looking for config.option.keyword specifically
    if len(config.option.filter) == 1:
        config.option.keyword = config.option.filter[0].strip()
    else:
        config.option.keyword = ", ".join([i.strip() for i in config.option.filter])
    
    filterlist = config.option.filter
    if not filterlist:
        return

    remaining = []
    deselected = []
    for filtr in filterlist:
        dirty_items = copy.copy(items)
        
        for item in dirty_items:
            if filtr[:1] != '-' and skipbykeyword(item, filtr):
                # skip
                deselected.append(item)
            elif filtr[:1] == '-' and skipbykeyword(item, filtr):
                # remove
                deselected.append(item)
                if item in remaining:
                    del remaining[remaining.index(item)]
            else:
                # keep
                remaining.append(item)

    deselected = [i for i in set(deselected)]
    remaining = [i for i in set(remaining)]
    if deselected:
        print(deselected)
        config.hook.pytest_deselected(items = deselected)
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
            if elem == kw:
                break
        else:
            return False
    return True
    
class MarkFiltration(object):
    pass
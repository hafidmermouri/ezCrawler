import unicodedata
import hashlib
import re


import re
TAG_RE = re.compile(r'<[^>]+>')

def md5(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    return m.hexdigest()

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

def htmlspecialchars(text):
    return (
        text.replace("&", "&amp;").
            replace('"', "&quot;").
            replace("<", "&lt;").
            replace(">", "&gt;")
    )

def remove_tags(text):
    return TAG_RE.sub('', text)

def remove_spaces(keyword):
    return re.sub('\n+', " ", keyword).strip()
import re

import xurl

VALID_URL = r'dramasq'

def getSource(url, fmt, ref):
    txt = xurl.load(url)
    m = re.search(r'm3u8url = \'([^\']*)\'', txt)
    return m.group(1) if m else None


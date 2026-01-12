import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

URL = "https://www.rfs.nsw.gov.au/feeds/fdrToban.xml"
OUTPUT = "greater-hunter-rss.xml"

print("Downloading RFS feed...")

data = urllib.request.urlopen(URL).read()
root = ET.fromstring(data)

print("Searching for Greater Hunter...")

region = None
for parent in root.iter():
    for child in parent:
        if child.tag.lower().endswith("name"):
            if child.text and "greater hunter" in child.text.lower():
                region = parent
                break

if region is None:
    print("❌ Greater Hunter not found")
    exit()

lines = []
for node in region.iter():
    if node.text and len(node.text.strip()) > 0:
        lines.append(node.text.strip())

content = "<br>".join(dict.fromkeys(lines))

from datetime import datetime, timezone
now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")

rss = f"""<?xml version="1.0"?>
<rss version="2.0">
<channel>
<title>NSW RFS – Greater Hunter</title>
<link>https://www.rfs.nsw.gov.au</link>
<description>Fire Danger Ratings &amp; Total Fire Ban – Greater Hunter</description>
<lastBuildDate>{now}</lastBuildDate>

<item>
<title>Greater Hunter Update</title>
<pubDate>{now}</pubDate>
<description><![CDATA[{content}]]></description>
</item>

</channel>
</rss>
"""

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(rss)

print("✅ RSS feed created:", OUTPUT)

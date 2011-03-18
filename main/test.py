import xml.etree.cElementTree as et
from pprint import pprint as pp

areaxml = et.parse('/tmp/area.xml').getroot()
for area in areaxml.findall('area'):
   pp(area.attrib['id'])

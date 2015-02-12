from collections import defaultdict
import os
from lxml.etree import fromstring

linecolors = {'1': 'C4008F',
 '12': '338C26',
 '13': '9EBFE3',
 '14': 'FF9EC2',
 '15': '36578C',
 '17': 'DE3B21',
 '19': 'DE3B21',
 '2': 'F57000',
 '20': 'E3BA12',
 '204': 'FF00FF',
 '205': '9978B8',
 '206': '00C8FF',
 '208': '94C9FD',
 '209': 'FF00FF',
 '21': 'F7E017',
 '210': 'D2FF0A',
 '211': '976A0E',
 '212': 'FC8306',
 '213': 'C30C3E',
 '216': '0A3C0A',
 '218': '64D214',
 '22': 'B5BA05',
 '25': '991F36',
 '27': '9EBFE3',
 '28': 'DE3B21',
 '29': 'E87D0D',
 '3': 'B5BA05',
 '31': 'E87D0D',
 '32': 'F7E017',
 '34': 'E3BA12',
 '36': '9EBFE3',
 '38': 'B085B3',
 '39': 'DE3B21',
 '4': 'F25482',
 '41': '9EBFE3',
 '42': '338C26',
 '43': '996308',
 '44': 'E3BA12',
 '45': 'B085B3',
 '46': 'DE3B21',
 '47': 'B085B3',
 '48': '338C26',
 '49': '36578C',
 '5': 'E6B012',
 '50': 'B5BA05',
 '51': 'E3BA12',
 '53': '338C26',
 '54': 'DE3B21',
 '55': 'E3BA12',
 '57': 'DE3B21',
 '58': '338C26',
 '59': '996308',
 '6': '0078AD',
 '60': 'FF9EC2',
 '61': 'F7E017',
 '62': 'FF9EC2',
 '63': '9EBFE3',
 '64': 'DE3B21',
 '65': 'E3BA12',
 '66': '36578C',
 '69': 'E87D0D',
 '7': 'FFF06E',
 '71': '338C26',
 '72': 'FF9EC2',
 '75': 'F7E017',
 '76': 'F7E017',
 '77': '338C26',
 '78': 'B085B3',
 '79': '36578C',
 '80': '338C26',
 '81': '338C26',
 '82': '9EBFE3',
 '83': 'B5BA05',
 '84': 'F7E017',
 '86': '338C26',
 '87': '338C26',
 '88': '991F36',
 '89': 'E87D0D',
 '92': 'DE3B21',
 '93': 'E87D0D',
 '94': 'F7E017',
 '95': '36578C',
 '97': '991F36',
 '98': 'FC8306'}

stops = {}
lines = defaultdict(lambda: [[],[]])

for name in os.listdir("."):
    if not name.endswith("xml"):
        continue
    xml = fromstring(file(name).read())
    for stop in xml.findall("stop"):
        id = stop.find("id").text
        name = stop.find("name").text
        line = xml.get("line")
        iti = int(xml.get("iti")) - 1

        longitude = stop.find("longitude").text
        latitude = stop.find("latitude").text

        if not longitude or not latitude:
            stops.setdefault(name, "")
        else:
            stops[name] = ', pos="%s,%s"' % (longitude, latitude)

        lines[line][iti].append(name)

print """
graph {
	graph [rankdir=LR bgcolor="#ffffff" fontname = "helvetica"];
	edge [dir=none];
	node [shape=box fontname = "helvetica"];
"""

print "\n".join('"%s" [weight="1.0"%s];' % (name, pos) for name, pos in stops.items())


edges = set()
for line, itis in lines.items():
    for itis, stops in enumerate(itis):
        prev = None
        for stop in stops:
            if prev:
                if prev == stop:
                    continue
                edge = (tuple(sorted([prev, stop])), line)
                if edge in edges:
                    continue
                edges.add(edge)
                print '"%s" -- "%s" [color="#%s", penwidth=2];' % (prev, stop, linecolors[line])
            prev = stop

print "}"

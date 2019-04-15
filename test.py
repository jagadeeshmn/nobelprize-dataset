import rdflib

g = rdflib.Graph()
g.parse("PeriodicTable.owl")
print("graph has %s statements." % len(g))


## Query 1: Find element name, element symbol, atomic weight and color of
## all elements from the group with group name "Halogen"

qres = g.query(
"""
PREFIX table:<http://www.daml.org/2003/01/periodictable/PeriodicTable#>
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
SELECT (str(?n) as ?GROUPNAME) (COUNT(?e) as ?NUMELEMENTS)
{ 
?g rdf:type table:Group.
?g table:name ?n.
?g table:element ?e.
}
GROUP BY ?n""")

for row in qres:
  print(" %s %s" % row)
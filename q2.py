import rdflib

g = rdflib.Graph()
g.parse("nobeldata.owl")
print("graph has %s statements." % len(g))

qres = g.query(
  """
    PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
    SELECT DISTINCT (str(?c) as ?CATEGORIES)
    { 
    ?g table:WonPrize ?c;
    }
    ORDER BY ?c
    """)
categories_set = set()
for row in qres:
  row = "%s"%row
  categories_set.add(row.split("/")[4])

print("LIST OF CATEGORIES:")
print(categories_set)
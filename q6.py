import rdflib
import sys


g = rdflib.Graph()
g.parse("nobeldata.owl")
print("graph has %s statements." % len(g))

qres = g.query(
  """
    PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
    SELECT DISTINCT (str(?n) as ?NAME) (str(?c) as ?CATEGORIES)
    { 
    ?g table:WonPrize ?c;
    table:name ?n;
    }
    ORDER BY ?c
    """)
print("LIST OF WINNERS FROM "+sys.argv[1]+" :")
for row in qres:
  name,category_data = "%s"%row[0],"%s"%row[1]
  category = category_data.split("/")[4]
  if category == sys.argv[1]:
    print(name)
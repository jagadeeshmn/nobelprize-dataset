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
    SELECT DISTINCT (str(?n) as ?NAME) (str(?c) as ?CATEGORIES) (str(?y) as ?YEAR)
    { 
    ?g table:WonPrize ?c;
    table:name ?n;
    table:WonPrize ?wp.
    ?wp table:yearWon ?y;
    FILTER (?y = """+sys.argv[1]+""" )
    }
    ORDER BY ?c
    """)
print("LIST OF WINNERS FROM "+sys.argv[2]+" AND IN "+sys.argv[1]+" ARE:")
for row in qres:
    # print("%s %s %s"%row)
    name,category_data,year = "%s"%row[0],"%s"%row[1],"%s"%row[2]
    category = category_data.split("/")[4]
    if category == sys.argv[2]:
        print(name,year)
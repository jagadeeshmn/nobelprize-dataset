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
    SELECT (str(?n) as ?NAME)
    { 
    ?g rdf:type table:PersonWinner;
       table:name ?n;
       table:WonPrize ?wp.
    ?wp table:yearWon ?y;
    FILTER (?y = """+sys.argv[1]+""" )
    }
    """)
print("LIST OF WINNERS IN "+sys.argv[1]+" :")
for row in qres:
  row = "%s"%row
  print(row)
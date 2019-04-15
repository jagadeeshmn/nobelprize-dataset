import rdflib

g = rdflib.Graph()
g.parse("nobeldata.owl")
print("graph has %s statements." % len(g))


qres = g.query(
  """
    PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
    SELECT DISTINCT (str(?n) as ?NATIONALITY)
    { 
    ?g table:nationality ?n;
    }
    ORDER BY ?n
    """)
print("LIST OF NATIONS:")
for row in qres:
  row = "%s"%row
  nation =row.split("/").pop()
  if nation !="(no_nationality_info)": 
    print(nation)
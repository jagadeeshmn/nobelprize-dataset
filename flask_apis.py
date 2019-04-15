from flask import Flask, request
from flask import jsonify
import rdflib
from flask_cors import CORS
import itertools


app = Flask(__name__)
CORS(app)

g = rdflib.Graph()
g.parse("nobeldata.owl")

@app.route("/nobel/nations")
def getAllNations():
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
    return_data = [str(row[0]).split("/").pop() for row in qres if str(row[0]).split("/").pop()!="(no_nationality_info)"]
    return jsonify({"result":return_data})

@app.route("/nobel/categories")
def getAllCategories():
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
    return jsonify({"result":list(sorted(categories_set))})

@app.route("/nobel/years")
def getAllYears():
    qres = g.query(
    """
    PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
    SELECT DISTINCT (str(?y) as ?YEARS)
    { 
    ?g table:yearWon ?y;
    }
    ORDER BY ?y
    """)
    return_data = [str(row[0]) for row in qres]
    return jsonify({"result":return_data})

@app.route("/nobel/years/<year>")
def getByYear(year):
    qres = g.query(
    """
    PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
    SELECT (str(?n) as ?NAME) (str(?wp) as ?CATEGORY) (str(?nt) as ?NATIONALITY)
    { 
    ?g rdf:type table:PersonWinner;
       table:name ?n;
       table:nationality ?nt;
       table:WonPrize ?wp.
    ?wp table:yearWon ?y;
    FILTER (?y = """+year+""" )
    }
    """)
    return_data = [{"name":str(row[0]),"year":year,"category":str(row[1]).split("/")[4],"nationality":str(row[2]).split("/").pop()} for row in qres]
    return_data = sorted(return_data, key=lambda k: k['nationality'])
    result = list()
    for key, group in itertools.groupby(return_data, key=lambda x:x['nationality']):
        result.append({key:list(group)})
    return jsonify({"listOfWinners":result})

@app.route("/nobel/nations/<nation>")
def getByNationality(nation):
    qres = g.query(
    """
    PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
    SELECT (str(?n) as ?NAME) (str(?wp) as ?CATEGORY) (str(?y) as ?YEAR) (str(?nt) as ?NATIONALITY)
    { 
    ?g rdf:type table:PersonWinner;
       table:name ?n;
       table:WonPrize ?wp;
       table:nationality ?nt.
    ?wp table:yearWon ?y;
    FILTER (?nt = 'http://dbpedia.org/resource/"""+nation+"""')
    }
    """)
    return_data = [{"name":str(row[0]),"category":str(row[1]).split("/")[4],"year":str(row[2]).split("/").pop(),"nationality":nation} for row in qres]
    return_data = sorted(return_data, key=lambda k: k['year'],reverse=True) 
    result = list()
    for key, group in itertools.groupby(return_data, key=lambda x:x['year']):
        result.append({key:list(group)})
    return jsonify({"listOfWinners":result})

@app.route("/nobel/categories/<category>")
def getByCategory(category):
    qres = g.query(
    """
    PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
    SELECT DISTINCT (str(?n) as ?NAME) (str(?c) as ?CATEGORY) (str(?nt) as ?NATIONALITY) (str(?y) as ?YEAR)
    { 
    ?g table:WonPrize ?c;
       table:name ?n;
       table:nationality ?nt;
       table:WonPrize ?wp.
    ?wp table:yearWon ?y;
    }
    ORDER BY ?c
    """)
    return_data = [{"name":str(row[0]),"category":category,"nationality":str(row[2]).split("/").pop(),"year":str(row[3]).split("/").pop()} for row in qres if str(row[1]).split("/")[4]==category]
    return_data = sorted(return_data, key=lambda k: k['year'],reverse=True)
    result = list()
    for key, group in itertools.groupby(return_data, key=lambda x:x['year']):
        result.append({key:list(group)})
    return jsonify({"listOfWinners":result})

@app.route("/nobel/<nation>/<category>")
def getByNationAndCategory(nation,category):
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
    FILTER (?y = """+nation+""" )
    }
    ORDER BY ?c
    """)
    return_data = [ str(row[0]) for row in qres if str(row[1]).split("/")[4]==category ]
    return jsonify({"listOfWinners":return_data})

@app.route('/nobel/winner', methods=['POST'])
def getWinner():
    input_name = request.json['winner']
    qres = g.query(
    """
    PREFIX table:<http://swat.cse.lehigh.edu/resources/onto/nobel.owl#>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
    SELECT DISTINCT (str(?o) as ?ORGANIZATION)(str(?by) as ?BIRTH)(str(?dy) as ?DEATH)(str(?p) as ?PHOTO)(str(?nt) as ?NATIONALITY)(str(?n) as ?NAME)(str(?c) as ?CATEGORY)(str(?y) as ?YEAR)
    { 
    ?g rdf:type table:PersonWinner;
    table:name ?n;
    table:WonPrize ?c.
    ?c table:yearWon ?y
    OPTIONAL {?g table:Association ?o;
    table:photo ?p;
    table:nationality ?nt;
    table:photo ?p;
    table:deathYear ?dy;
    table:birthYear ?by;
    }
    }""")
    result = []
    for row in qres:
        organizationData,birth,death,photo,nationalityData,name, categoryData, year = "%s"%row[0],"%s"%row[1],"%s"%row[2],"%s"%row[3],"%s"%row[4],"%s"%row[5],"%s"%row[6],"%s"%row[7]
        if organizationData != 'None':
            org = organizationData.split('#')
            organization = org[1].split(',')[0]
        nationality = nationalityData.split('/').pop()
        category = categoryData.split('/')[4]
        if name == input_name:
            result.append({'name':name,'year_won':year,'category':category,'birth_year':birth, 'death_year':death, 'photo':photo, 'organization':organization, 'nationality': nationality})
    return jsonify({'result':result})

if __name__ == '__main__':
    app.run(debug=True)
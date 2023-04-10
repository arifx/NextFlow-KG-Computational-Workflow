from rdflib import Graph, Namespace, Literal
from openpyxl import load_workbook
from rdflib.namespace import RDF, RDFS

ex = Namespace('http://purl.com/fsmon#')
g = Graph()
wb = load_workbook('/home/appuser/NextFlow-KG-Computational-Workflow/ENOSE.xlsx')
sheet = wb['Sheet1']
if 1==1:
    row= list(sheet.rows)[0]
    print(str(row))
#for row in sheet.iter_rows(min_row=2, values_only=True):
    subject_uri = row[0].value
    subject_name = row[1].value
    subject = ex[subject_uri]
    g.add((subject, RDF.type, ex[row[0]]))
    g.add((subject, ex['hasName'], Literal(subject_name)))

    for i in range(2, len(row)):
        if row[i]:
            #predicate = ex[f'hasMeasurementType{i-1}']
            predicate = ex[f'hasMeasurementType']
            object_uri = row[i].value
            object = ex[object_uri]
            g.add((subject, predicate, object))

f = open("FoodSafetyMonitoringKG.json", "w")
f.write(g.serialize(format='turtle'))
f.close()

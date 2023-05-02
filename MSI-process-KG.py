import pandas as pd #for handling csv and csv contents
from rdflib import Graph, Literal, RDF, URIRef, Namespace, BNode, OWL #basic RDF handling
from rdflib.namespace import FOAF , XSD #most common namespaces
import urllib.parse #for parsing strings to URI's

df = pd.read_csv("sample_sensors/Authentication_Chicken thigh_gt/MSI_fresh_frozen_chicken thigh.csv")
cols = df.columns
new_cols = [column.replace(" ", "_") for column in df.columns]
rename_cols = dict(zip(cols, new_cols))
df.rename(columns=rename_cols, inplace=True)

saref = Namespace('https://saref.etsi.org/core/')
fsmon = Namespace('https://purl.archive.org/purl/fsmon/Ontology#')
sio = Namespace("http://semanticscience.org/resource/")
sosa = Namespace("http://www.w3.org/ns/sosa/")
ncit = "http://purl.obolibrary.org/obo/NCIT_"
foodon = "http://purl.obolibrary.org/obo/FOODON_"

dataset_name = "MSI_fresh_frozen_chicken_thigh.csv"
folder = "Authentication_Chicken_thigh_gt/"
file_uri = folder+dataset_name
g = Graph()
g.bind("saref", saref)
g.bind("fsmon", fsmon)
g.bind("sio", sio)
g.bind("sosa", sosa)
g.bind("ncit", ncit)
g.bind("foodon", foodon)

g.add((URIRef(fsmon+dataset_name), RDF.type, URIRef(sio+"SIO_000089")))
g.add((URIRef(fsmon+dataset_name), URIRef(fsmon+"name"), Literal(str(dataset_name))))
g.add((URIRef(fsmon+dataset_name), URIRef(sio+"SIO_000061"), URIRef(fsmon+file_uri)))
g.add((URIRef(fsmon+file_uri), RDF.type, URIRef(ncit+"C42778")))
g.add((URIRef(fsmon+file_uri), URIRef(fsmon+"name"), Literal(str(file_uri))))
g.add((URIRef(fsmon+"chicken_thigh"), RDF.type, URIRef(foodon+"03400361")))

for index, row in df[["Sample_ID"]].iterrows(): #iter rows of first column, get sampleId
    sample = row['Sample_ID']
    feature = sample.split("_")
    temperature = feature[0]
    time = feature[1]
    package_type = feature[2]
    aId = feature[3]
    batch_n = feature[4]
    g.add((URIRef(fsmon+sample), RDF.type, URIRef(sosa+"Sample")))  #example: 0C_0h_air_a_b1 is type of Sample
    g.add((URIRef(fsmon+dataset_name), URIRef(fsmon+"hasSample"), URIRef(fsmon+sample)))  #example: dataset_name hasSample 0C_0h_air_a_b1
    g.add((URIRef(fsmon+sample), RDF.type, URIRef(sosa+"Sample")))  #example: 0C_0h_air_a_b1 is type of Sample
    g.add((URIRef(fsmon+sample), URIRef(fsmon+"hasSampleType"), (URIRef(fsmon+"chicken_thigh"))))
    g.add((URIRef(fsmon+sample), URIRef(fsmon+"hasSampleId"), Literal(str(sample))))
    g.add((URIRef(fsmon+sample), URIRef(fsmon+"hasTemperature"), Literal(temperature)))
    g.add((URIRef(fsmon+sample), URIRef(fsmon+"hasBatchNumber"), Literal(batch_n)))
    g.add((URIRef(fsmon+sample), URIRef(fsmon+"time"), Literal(time)))
    g.add((URIRef(fsmon+sample), URIRef(fsmon+"hasAdditionalID"), Literal(aId)))
    g.add((URIRef(fsmon+sample), URIRef(saref+"hasProperty"), URIRef(sio+"SIO_001109"))) #example: 0C_0h_air_a_b1 hasProperty Mean
    g.add((URIRef(fsmon+sample), URIRef(saref+"hasProperty"), URIRef(sio+"SIO_000770"))) #example: 0C_0h_air_a_b1 hasProperty StandardDeviation
    for col_index, column in enumerate(df.columns[1:]): # get column name
      g.add((URIRef(fsmon+sample), URIRef(saref+"hasMeasurement"), URIRef(fsmon+column))) #example: 0C_0h_air_a_b1 hasMeasurement Mean_01
      g.add((URIRef(fsmon+column), RDF.type, URIRef(saref+"Measurement"))) #Mean_01 a Measurement
      if "Mean" in column:
        g.add((URIRef(fsmon+column), URIRef(saref+"relatesToProperty"), URIRef(sio+"SIO_001109")))
      else:
        g.add((URIRef(fsmon+column), URIRef(saref+"relatesToProperty"), URIRef(sio+"SIO_000770")))

g.serialize(destination='result/msi_kg.owl', format='xml')
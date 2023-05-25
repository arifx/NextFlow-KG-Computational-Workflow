import pandas as pd #for handling csv and csv contents
from rdflib import Graph, Literal, RDF, URIRef, Namespace, BNode, OWL, RDFS #basic RDF handling
from rdflib.namespace import FOAF , XSD #most common namespaces
import urllib.parse #for parsing strings to URI's
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input", dest="input_path", help="Path to input file")
parser.add_argument("--output", dest="output_path", help="Path to output file")
args = parser.parse_args()
input_path = args.input_path
output_path = args.output_path

try:
  if "xlsx" in input_path: 
    df = pd.read_excel(input_path)
  else:
    df = pd.read_csv(input_path, ,encoding='utf-8')
except:
  sys.exit("problem with file")  

print("input:"+str(input_path)+"output:"+str(output_path))
cols = df.columns
new_cols = [column.replace(" ", "_") for column in df.columns]
rename_cols = dict(zip(cols, new_cols))
df.rename(columns=rename_cols, inplace=True)

saref = Namespace('https://saref.etsi.org/core/')
fsmon = Namespace('https://purl.archive.org/purl/fsmon/Ontology#')
sio = Namespace("http://semanticscience.org/resource/")
sosa = Namespace("http://www.w3.org/ns/sosa/")
obo = Namespace("http://purl.obolibrary.org/obo/")
om2 = Namespace("http://www.ontology-of-units-of-measure.org/resource/om-2/")


inp = input_path.split("/")
dataset_name = inp[-1]
folder = inp[:-1]
file_uri = input_path.replace(" ","_")
file_uri = file_uri.replace("/content/drive/MyDrive/23_FoodSafety/dataset", "FSM_fileRepository")
g = Graph()
g.bind("saref", saref)
g.bind("om2", om2)
g.bind("fsmon", fsmon)
g.bind("sio", sio)
g.bind("sosa", sosa)
g.bind("obo", obo)

tmp = dataset_name.split("_")
tmp =dataset_name.replace(tmp[0]+"_", "")
if "csv"in tmp:
    sample_name= tmp.replace(".csv", "")
elif "xlsx" in tmp:
    sample_name= tmp.replace(".xlsx", "")
format_ = dataset_name.split(".")[-1]
sensor="MSI"

g.add((URIRef(fsmon+dataset_name.replace(" ","_")), RDF.type, URIRef(sio+"SIO_000089")))
g.add((URIRef(fsmon+dataset_name.replace(" ","_")), URIRef(fsmon+"name"), Literal(str(dataset_name))))
g.add((URIRef(fsmon+dataset_name.replace(" ","_")), URIRef(sio+"SIO_000061"), Literal(str(file_uri))))
g.add((URIRef(fsmon+file_uri), RDF.type, URIRef(obo+"NCIT_C42778")))
g.add((URIRef(fsmon+file_uri), URIRef(fsmon+"name"), Literal(str(file_uri))))
g.add((URIRef(fsmon+dataset_name.replace(" ","_")), URIRef(fsmon+"has_format"), Literal(format_))) 
g.add((URIRef(obo+"CHMO_0000937"), URIRef(saref+"isMeasuredByDevice"), URIRef(fsmon+"Videometer_0000"))) #Reflectance
g.add((URIRef(obo+"CHMO_0000937"), URIRef(saref+"isMeasuredByDevice"), URIRef(fsmon+"Videometer_0001"))) 
g.add((URIRef(obo+"CHMO_0000937"), URIRef(saref+"isMeasuredByDevice"), URIRef(fsmon+"Videometer_0002"))) 
g.add((URIRef(obo+"CHMO_0000937"), URIRef(saref+"isMeasuredByDevice"), URIRef(fsmon+"Videometer_0003"))) 
g.add((URIRef(obo+"CHMO_0000937"), URIRef(saref+"isMeasuredByDevice"), URIRef(fsmon+"Videometer_0004"))) 
g.add((URIRef(obo+"CHMO_0000937"), URIRef(saref+"isMeasuredByDevice"), URIRef(fsmon+"Videometer_0005"))) 
g.add((URIRef(obo+"CHMO_0000937"), URIRef(saref+"isMeasuredByDevice"), URIRef(fsmon+"Videometer_0006"))) 
g.add((URIRef(obo+"CHMO_0000937"), URIRef(saref+"isMeasuredByDevice"), URIRef(fsmon+"Videometer_0007"))) 
g.add((URIRef(obo+"CHMO_0000937"), URIRef(saref+"isMeasuredByDevice"), URIRef(fsmon+"Videometer_0008"))) 
g.add((URIRef(obo+"CHMO_0000937"), URIRef(saref+"isMeasuredByDevice"), URIRef(fsmon+"Videometer_0009"))) 
g.add((URIRef(fsmon+"Videometer_0000"), RDF.type, URIRef(fsmon+"Videometer")))
g.add((URIRef(fsmon+"Videometer_0001"), RDF.type, URIRef(fsmon+"Videometer")))
g.add((URIRef(fsmon+"Videometer_0002"), RDF.type, URIRef(fsmon+"Videometer")))
g.add((URIRef(fsmon+"Videometer_0003"), RDF.type, URIRef(fsmon+"Videometer")))
g.add((URIRef(fsmon+"Videometer_0004"), RDF.type, URIRef(fsmon+"Videometer")))
g.add((URIRef(fsmon+"Videometer_0005"), RDF.type, URIRef(fsmon+"Videometer")))
g.add((URIRef(fsmon+"Videometer_0006"), RDF.type, URIRef(fsmon+"Videometer")))
g.add((URIRef(fsmon+"Videometer_0007"), RDF.type, URIRef(fsmon+"Videometer")))
g.add((URIRef(fsmon+"Videometer_0008"), RDF.type, URIRef(fsmon+"Videometer")))
g.add((URIRef(fsmon+"Videometer_0009"), RDF.type, URIRef(fsmon+"Videometer")))
g.add((URIRef(sio+"SIO_001109"), URIRef(saref+"relatesToMeasurement"), URIRef(obo+"CHMO_0000937"))) #Mean relatedToMeasurement Reflectance
g.add((URIRef(sio+"SIO_000770"), URIRef(saref+"relatesToMeasurement"), URIRef(obo+"CHMO_0000937"))) #Std relatedToMeasurement Reflectance
g.add((URIRef(obo+"CHMO_0000937"), URIRef(saref+"relatesToProperty"), URIRef(sio+"SIO_001109"))) #Reflectance relatesToProperty Mean 
g.add((URIRef(obo+"CHMO_0000937"), URIRef(saref+"relatesToProperty"), URIRef(sio+"SIO_000770"))) #Reflectance relatedToMeasurement Std
g.add((URIRef(fsmon+"Videometer"), URIRef(fsmon+"hasSensorType"), URIRef(fsmon+sensor)))
g.add((URIRef(fsmon+"PoultryAnalysis-1"), RDF.type, URIRef(obo+"NCIT_C42790"))) #experiment
g.add((URIRef(fsmon+"PoultryAnalysis-1"), URIRef(fsmon+"has_date"), Literal("22/8/2022"))) 
g.add((URIRef(fsmon+"MicroLab-ML1"), RDF.type, URIRef(obo+"ENVO_01001406"))) #Laboratory
g.add((URIRef(fsmon+"MicroLab-ML1"), URIRef(fsmon+"has_Email"), Literal("info@microlab-ml1.nl")))
g.add((URIRef(fsmon+"PoultryAnalysis-1"), URIRef(saref+"isPerformedAt"), URIRef(fsmon+"MicroLab-ML1")))
g.add((URIRef(fsmon+"MicroLab-ML1"), URIRef(fsmon+"hasAddress"), URIRef(fsmon+"Maastricht")))
g.add((URIRef(fsmon+"Maastricht"), RDF.type, URIRef(obo+"NCIT_C25341")))
g.add((URIRef(fsmon+"Maastricht"), URIRef(fsmon+"hasLatitude"), Literal("38.11257")))
g.add((URIRef(fsmon+"Maastricht"), URIRef(fsmon+"hasLongitude"), Literal("23.27307")))
if "chicken" in dataset_name:
  g.add((URIRef(fsmon+"chicken_thigh"), RDF.type, URIRef(obo+"FOODON_03400361"))) #sample type
else:
  g.add((URIRef(fsmon+"minced_beef"), RDF.type, URIRef(obo+"FOODON_03400361")))

for index, row in df[["Sample_ID"]].iterrows(): #iter rows of first column, get sampleId
    sample = row['Sample_ID']
    g.add((URIRef(fsmon+sample), RDF.type, URIRef(sosa+"Sample")))  #example: 0C_0h_air_a_b1 is type of Sample
    g.add((URIRef(fsmon+dataset_name.replace(" ","_")), URIRef(fsmon+"hasSample"), URIRef(fsmon+sample)))  #example: dataset_name hasSample 0C_0h_air_a_b1
    g.add((URIRef(fsmon+sample), RDF.type, URIRef(sosa+"Sample")))  #example: 0C_0h_air_a_b1 is type of Sample
    g.add((URIRef(fsmon+sample), URIRef(fsmon+"Sample_code_number"), Literal("PA-1-00011")))  #example: 0C_0h_air_a_b1 is type of Sample
    g.add((URIRef(fsmon+sample), URIRef(fsmon+"name"), Literal(sample_name))) 
    g.add((URIRef(obo+"NCIT_C42790"), URIRef(fsmon+"isPerformedOn"), URIRef(fsmon+sample)))    
    g.add((URIRef(fsmon+sample), URIRef(saref+"hasMeasurement"), URIRef(obo+"CHMO_0000937"))) 
    g.add((URIRef(fsmon+sample), URIRef(fsmon+"hasSampleId"), Literal(str(sample))))
    if "Adulteration" not in file_uri:
      feature = sample.split("_")
      temperature = feature[0]
      time = feature[1]
      package_type = feature[2]
      aId = feature[3]
      batch_n = feature[4]
      g.add((URIRef(fsmon+sample), URIRef(fsmon+"hasTemperature"), Literal(temperature)))
      g.add((URIRef(fsmon+sample), URIRef(fsmon+"hasBatchNumber"), Literal(batch_n)))
      g.add((URIRef(fsmon+sample), URIRef(fsmon+"time"), Literal(time)))
      g.add((URIRef(fsmon+sample), URIRef(fsmon+"hasAdditionalID"), Literal(aId)))
      g.add((URIRef(fsmon+sample), URIRef(fsmon+"hasPackageType"), Literal(package_type)))
    g.add((URIRef(fsmon+sample), URIRef(saref+"hasProperty"), URIRef(sio+"SIO_001109"))) #example: 0C_0h_air_a_b1 hasProperty Mean
    g.add((URIRef(fsmon+sample), URIRef(saref+"hasProperty"), URIRef(sio+"SIO_000770"))) #example: 0C_0h_air_a_b1 hasProperty StandardDeviation
    if "TVC" in dataset_name.replace(" ","_"):
       g.add((URIRef(fsmon+sample), URIRef(saref+"hasProperty"), URIRef(om2+"ViableCount")))
for col_index, column in enumerate(df.columns[1:]): # get column name
  if "Mean" in column:
    g.add((URIRef(fsmon+column), RDF.type, URIRef(sio+"SIO_001109"))) #Mean_01 a Mean
  elif "StdDev" in column:
    g.add((URIRef(fsmon+column), RDF.type, URIRef(sio+"SIO_000770"))) #Std_01 a Standard Deviation
  elif "TVC" in column:
    g.add((URIRef(fsmon+column), RDF.type, URIRef(om2+"ViableCount")))
 
g.serialize(destination=output_path+"KG_"+str(dataset_name.replace(" ","_"))+".owl", format='xml')

import pandas as pd #for handling csv and csv contents
from rdflib import Graph, Literal, RDF, URIRef, Namespace, BNode, OWL #basic RDF handling
from rdflib.namespace import FOAF , XSD #most common namespaces
import urllib.parse #for parsing strings to URI's
import argparse
from rdflib.plugins.sparql import prepareQuery

import os
parser = argparse.ArgumentParser()
parser.add_argument("--input", dest="input_path", help="Path to input file")
parser.add_argument("--output", dest="output_path", help="Path to output file")
args = parser.parse_args()
input_path = args.input_path
output_path = args.output_path

g = Graph()
g.parse(input_path)

saref = Namespace('https://saref.etsi.org/core/')
fsmon = Namespace('https://purl.archive.org/purl/fsmon/Ontology#')
sio = Namespace("http://semanticscience.org/resource/")
sosa = Namespace("http://www.w3.org/ns/sosa/")
obo = Namespace("http://purl.obolibrary.org/obo/")
om2 =  Namespace("http://www.ontology-of-units-of-measure.org/resource/om-2/")
rdfs= Namespace("http://www.w3.org/2000/01/rdf-schema#")
rdf= Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")

g.bind("saref", saref)
g.bind("fsmon", fsmon)
g.bind("sio", sio)
g.bind("sosa", sosa)
g.bind("obo", obo)
g.bind("om2", om2)
g.bind("rdf", rdf)
g.bind("rdfs", rdfs)

queries = [
"""
INSERT DATA {  
    fsmon:Amsterdam rdf:type obo:NCIT_C25341 ;
        fsmon:hasLatitude "52.3667" ;
        fsmon:hasLongitude "4.8945" .
    
    fsmon:Vienna rdf:type obo:NCIT_C25341 ;
        fsmon:hasLatitude "48.2082" ;
        fsmon:hasLongitude "16.3738" .
    
    fsmon:Rome rdf:type obo:NCIT_C25341 ;
        fsmon:hasLatitude "41.9028" ;
        fsmon:hasLongitude "12.4964" .
    
    fsmon:Berlin rdf:type obo:NCIT_C25341 ;       
        fsmon:hasLatitude "52.5200" ;
        fsmon:hasLongitude "13.4050" .    

    fsmon:Paris rdf:type obo:NCIT_C25341 ;       
        fsmon:hasLatitude "48.8566" ;
        fsmon:hasLongitude "2.3522" .
    
    fsmon:Hamburg rdf:type obo:NCIT_C25341 ;       
        fsmon:hasLatitude "53.5511" ;
        fsmon:hasLongitude "9.9937" . 
    
    fsmon:Stuttgart rdf:type obo:NCIT_C25341 ;       
        fsmon:hasLatitude "48.7758" ;
        fsmon:hasLongitude "9.1829" . 
    
    fsmon:Rotterdam rdf:type obo:NCIT_C25341 ;       
        fsmon:hasLatitude "51.9225" ;
        fsmon:hasLongitude "4.47917" . 
    
    fsmon:Brussels rdf:type obo:NCIT_C25341 ;       
        fsmon:hasLatitude "50.8503" ;
        fsmon:hasLongitude "4.3517" . 
    
    fsmon:Lyon rdf:type obo:NCIT_C25341 ;       
        fsmon:hasLatitude "45.75" ;
        fsmon:hasLongitude "4.85" . 
    
    fsmon:MicroLab-ML1  fsmon:hasAddress fsmon:Berlin.
    fsmon:MicroLab-ML1  fsmon:hasAddress fsmon:Paris.
    fsmon:MicroLab-ML1  fsmon:hasAddress fsmon:Lyon.
    fsmon:MicroLab-ML1  fsmon:hasAddress fsmon:Brussels.
    fsmon:MicroLab-ML1  fsmon:hasAddress fsmon:Rotterdam.
    fsmon:MicroLab-ML1  fsmon:hasAddress fsmon:Stuttgart.
    fsmon:MicroLab-ML1  fsmon:hasAddress fsmon:Hamburg.
    fsmon:MicroLab-ML1  fsmon:hasAddress fsmon:Rome.
    fsmon:MicroLab-ML1  fsmon:hasAddress fsmon:Vienna.
    fsmon:MicroLab-ML1  fsmon:hasAddress fsmon:Amsterdam.

}    
"""
,
    """
SELECT DISTINCT  ?Dataset_Name   ?Mean 
WHERE {
    ?d fsmon:name ?Dataset_Name .
    ?d fsmon:hasSample ?Sample_ID .
    ?Sample_ID saref:hasProperty ?M.
    ?Mean a sio:SIO_001109. 
    FILTER(?Mean = 	fsmon:Mean_01)

}
    
    """
    ,
    """
SELECT DISTINCT ?Dataset_file  ?label 
WHERE {
    ?d fsmon:name ?Dataset_file .
    ?d fsmon:hasSample ?Sample_ID .
    ?Sample_ID saref:hasMeasurement ?m .
    ?m rdfs:label ?label.
    FILTER(?label = "Reflectance"@en)
   
}
    
    """
    ,
    """

SELECT DISTINCT ?Temperature ?Time ?PackageType ?AdditionalID ?BatchNumber
WHERE {
     
    ?s fsmon:hasTemperature ?Temperature .
    ?s fsmon:hasBatchNumber ?BatchNumber .
    ?s fsmon:time ?Time .
    ?s fsmon:hasAdditionalID ?AdditionalID .
    ?s fsmon:hasPackageType  ?PackageType
    FILTER(?PackageType = "map")
   
}
    
"""
,
"""   
SELECT ?Address ?Laboratory
WHERE {
    ?Laboratory fsmon:hasAddress ?Address.
}    
"""   
,
"""
SELECT DISTINCT ?Device ?Device_Class ?Sensor 
WHERE {
    ?Device_Class  fsmon:hasSensorType ?Sensor.
    ?Device a ?Device_Class.
    FILTER(?Device_Class =fsmon:Videometer)
}
    """
    ,
    """

SELECT DISTINCT ?Analysis ?Laboratory ?Email ?Date ?Address ?latitude ?longitude  ?SampleName ?SampleType 
WHERE {
    ?Analysis  rdf:type  obo:NCIT_C42790.
    ?Analysis  fsmon:has_date  ?Date . 
    ?Laboratory  rdf:type  obo:ENVO_01001406.
    ?Laboratory  fsmon:has_Email  ?Email .
    ?Analysis  saref:isPerformedAt ?Laboratory.
        
    ?Laboratory  fsmon:hasAddress ?Address.
    ?Address rdf:type obo:NCIT_C25341.
          
    ?Address  fsmon:hasLatitude ?latitude.
    ?Address  fsmon:hasLongitude ?longitude.
    
    ?Sample  fsmon:Sample_code_number  ?SampleName.
    ?SampleType rdf:type obo:FOODON_03400361 . 
   
}   

    """
    ,
    """
SELECT DISTINCT * 
WHERE {
     ?Dataset rdf:type sio:SIO_000089 ;
           fsmon:name ?Name ;
           sio:SIO_000061 ?FileUri ;
           fsmon:has_format ?Format .
    
    ?SampleType rdf:type obo:FOODON_03400361 .

}    
    
    """
    ,
    """

SELECT DISTINCT ?SampleID  ?Measurement  ?File_Name  ?Format  ?Device  ?Sensor

WHERE {

  ?Sample  fsmon:Sample_code_number  ?SampleID.
    
  ?dataset fsmon:name ?File_Name ;
           sio:SIO_000061 ?fileUri ;
           fsmon:has_format ?Format .
    
  ?Device  fsmon:hasSensorType ?Sensor.
    
  obo:CHMO_0000937  rdfs:label  ?Measurement. 
  FILTER(?Measurement = "Reflectance"@en)
    

  }    
    """
    ,
    """
SELECT DISTINCT   ?Dataset   ?TVC
WHERE {
    ?d fsmon:name ?Dataset .
    ?d fsmon:hasSample ?Sample_ID .  
    ?TVC a om2:ViableCount.
 
}   
    """


]

results_folder = output_path
for i, query in enumerate(queries):
    if query.strip().startswith("INSERT"):
        # Execute the INSERT query
        g.update(query)
        # Manually create a file to indicate the INSERT query was executed successfully
        result_file = os.path.join(results_folder, f"query_result_{i}.txt")
        with open(result_file, "w") as file:
            file.write("INSERT query executed successfully.")

    elif query.strip().startswith("SELECT"):
       # Execute the SELECT query
        results = g.query(query)
        result_file = os.path.join(results_folder, f"query_result_{i}.csv")
        results.serialize(destination=result_file, format="csv")

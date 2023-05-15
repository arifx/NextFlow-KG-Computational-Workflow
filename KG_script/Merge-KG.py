from rdflib import Graph
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input", dest="input_path", nargs='*', help="Path to input file")
parser.add_argument("--output", dest="output_path", help="Path to output file")
args = parser.parse_args()
input_path = args.input_path
output_path = args.output_path

graph = Graph()
for path in input_path:
    graph.parse(path)

graph.serialize(destination=output_path, format='xml')
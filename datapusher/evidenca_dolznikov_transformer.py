import rdflib
import uuid

from rdflib import Namespace, Graph
from rdflib.namespace import RDF, FOAF
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID as default
from rdflib import Graph, Literal, RDF, URIRef

# Connect to fuseki triplestore.
store = SPARQLUpdateStore()
query_endpoint = 'http://localhost:3030/pz/query'
update_endpoint = 'http://localhost:3030/pz/update'
store.open((query_endpoint, update_endpoint))

# Open a graph in the open store and set identifier to default graph ID.
graph = Graph(store, identifier="http://onto.mju.gov.si/pz/dataset/erar-evidenca-davcnih-dolznikov-in-nepredlagateljev-davcnih-obracunov")

# Define namespaces
PZ = Namespace("http://onto.mju.gov.si/podatkovni-zemljevid#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
CNB = Namespace("http://onto.mju.gov.si/centralni-besednjak-core#")

# Data (parameters)

shema = "https://podatki.gov.si/dataset/kpk-evidenca-davcnih-dolznikov-in-nepredlagateljev-davcnih-obracunov/schema/1.0.0"
distribucija = "http://onto.mju.gov.si/pz/distribution/erar-davcni-dolzniki-prejemniki-javnih-sredstev-2022-12-25.zip"
prejetaJavnaSredstva90dni = 239357.09
kategorijaDolznika = "OD 500.000,01 EUR DO 1.000.000,00 EUR"
dolznik = "SOLCEL, d.o.o - v stečaju"
davcnaStevilka = "91440904"
steviloIzdanihRacunov = 9
steviloZaprtihRacunov = 0

distribution_namespace = Namespace(f"{distribucija}/")


# CREATE A NEW OBJECT
object_id = distribution_namespace[str(uuid.uuid4())]

graph.add((object_id, RDF.type, PZ.Object))
graph.add((object_id, SKOS.inScheme, URIRef(shema)))
graph.add((object_id, PZ.inDistribution, URIRef(distribucija)))
graph.add((object_id, CNB.prejetaJavnaSredstva90dni, Literal(prejetaJavnaSredstva90dni)))
graph.add((object_id, CNB.kategorijaDolznika, Literal(kategorijaDolznika)))
graph.add((object_id, CNB.dolznik, Literal(dolznik)))
graph.add((object_id, CNB.davcnaStevilka, Literal(davcnaStevilka)))
graph.add((object_id, CNB.steviloIzdanihRacunov, Literal(steviloIzdanihRacunov)))
graph.add((object_id, CNB.steviloZaprtihRacunov, Literal(steviloZaprtihRacunov)))

print(f"Successfully inserted '{object_id}'.")
import rdflib
import uuid

from rdflib import Namespace, Graph
from rdflib.namespace import RDF, FOAF
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID as default
from rdflib import Graph, Literal, RDF, URIRef

def push_to_fuseki(logger, temp_file, resource, license_url, resource_schema_uri, dataset_uri):
    logger.info("Connecting to Fuseki.")
    # Connect to fuseki triplestore.
    store = SPARQLUpdateStore()
    query_endpoint = 'http://fuseki:3030/pz/query'
    update_endpoint = 'http://fuseki:3030/pz/update'
    store.open((query_endpoint, update_endpoint))

    # Open a graph in the open store and set identifier to default graph ID.
    graph = Graph(store, identifier=dataset_uri)

    # Define namespaces
    PZ = Namespace("http://onto.mju.gov.si/podatkovni-zemljevid#")
    SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
    CNB = Namespace("http://onto.mju.gov.si/centralni-besednjak-core#")
    DCAT = Namespace("http://www.w3.org/ns/dcat#")
    DCT = Namespace("http://purl.org/dc/terms/")

    formats = {
        "CSV": URIRef("https://publications.europa.eu/resource/authority/file-type/CSV"),
        "XLSX": URIRef("https://publications.europa.eu/resource/authority/file-type/XLSX")
    }

    # DELETE DISTRIBUTION (IF EXISTS)
        #TODO

    # INSERT DISTRIBUTION
    resource_name = resource.get('name')
    #TODO: check what happens if special characters in name


    distribution_general_namespace = Namespace(f"http://onto.mju.gov.si/pz/distribution/")
    distributiom_object_id = distribution_general_namespace[resource_name]

    graph.add((URIRef(dataset_uri), DCAT.distribution, URIRef(distributiom_object_id)))

    graph.add((distributiom_object_id, RDF.type, DCAT.Distribution))
    graph.add((distributiom_object_id, DCT.title, Literal("Davčni dolžniki prejemniki javnih sredstev - prejeta sredstva v zadnjih 90 dnevih pred objavo")))
    graph.add((distributiom_object_id, DCT.identifier, Literal(resource_name)))
    graph.add((distributiom_object_id, DCT.language, URIRef("http://publications.europa.eu/resource/authority/language/SLV")))
    graph.add((distributiom_object_id, DCT.license, URIRef(license_url)))
    #graph.add((distributiom_object_id, DCT.compressFormat, URIRef(https://publications.europa.eu/resource/authority/file-type/ZIP")))
    graph.add((distributiom_object_id, DCAT.mediaType, formats.get(resource.get("format"))))
    graph.add((distributiom_object_id, PZ.schema, URIRef(resource_schema_uri)))

    

    # INSERT DATA
    # TODO: make iteration
    prejetaJavnaSredstva90dni = 239357.09
    kategorijaDolznika = "OD 500.000,01 EUR DO 1.000.000,00 EUR"
    dolznik = "SOLCEL, d.o.o - v stečaju"
    davcnaStevilka = "91440904"
    steviloIzdanihRacunov = 9
    steviloZaprtihRacunov = 0

    distribution_namespace = Namespace(f"http://onto.mju.gov.si/pz/distribution/{resource_name}/")


    # CREATE A NEW OBJECT
    object_id = distribution_namespace[str(uuid.uuid4())]

    graph.add((object_id, RDF.type, PZ.Object))
    graph.add((object_id, SKOS.inScheme, URIRef(resource_schema_uri)))
    graph.add((object_id, PZ.inDistribution, distributiom_object_id))
    graph.add((object_id, CNB.prejetaJavnaSredstva90dni, Literal(prejetaJavnaSredstva90dni)))
    graph.add((object_id, CNB.kategorijaDolznika, Literal(kategorijaDolznika)))
    graph.add((object_id, CNB.dolznik, Literal(dolznik)))
    graph.add((object_id, CNB.davcnaStevilka, Literal(davcnaStevilka)))
    graph.add((object_id, CNB.steviloIzdanihRacunov, Literal(steviloIzdanihRacunov)))
    graph.add((object_id, CNB.steviloZaprtihRacunov, Literal(steviloZaprtihRacunov)))

    logger.info(f"Successfully created  distribution '{object_id}' and pushed 27 objects into Fuseki (total of 251 triples).")


if __name__ == '__main__':
    #TEST RUN
    resource = {
        "name": "erar-davcni-dolzniki-prejemniki-javnih-sredstev-2022-12-25-xlsx",
        "format": "XLSX"
    }
    license_url = "https://creativecommons.org/licenses/by-sa/4.0/"
    resource_schema_uri = "https://podatki.gov.si/dataset/kpk-evidenca-davcnih-dolznikov-in-nepredlagateljev-davcnih-obracunov/schema/1.0.0"

    push_to_fuseki(resource, license_url, resource_schema_uri)
import pandas as pd
from rdflib import Graph, RDF, RDFS, Namespace, URIRef, Literal
from datetime import datetime

# Lees gegevens in vanuit Excel naar een DataFrame
input_file_openrefine = '/Users/patrickmout/Downloads/VGWW/Onderzoek-Van-Gogh-tbv-Van-Gogh-Worldwide.xlsx'
df = pd.read_excel(input_file_openrefine)

# Verwijderen witruimtekarakters (zoals spaties, tabs, nieuwe regels, etc.)
df = df.replace(r'\s+', '', regex=True)

# Definieer de huidige datum
current_date = datetime.now().strftime("%Y-%m-%d")

# Definieer het pad naar het outputbestand met de huidige datum
output_file = f'/Users/patrickmout/Downloads/VGWW/vgww_data_rce_{current_date}.ttl'

# Definieer output bestand als RDF graph
output_graph = Graph()

# Leg te gebruiken namespaces in je RDF vast
# namespace properties/classes
la = Namespace("https://linked.art/ns/terms/")
crm = Namespace("http://www.cidoc-crm.org/cidoc-crm/")
skos = Namespace("http://www.w3.org/2004/02/skos/core#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
dig = Namespace("http://www.ics.forth.gr/isl/CRMdig/")

# namespace instances
i = Namespace("https://linkeddata.cultureelerfgoed.nl/id/vgww/")

output_graph.bind("la", la)
output_graph.bind("crm", crm)
output_graph.bind("skos", skos)
output_graph.bind("XSD", XSD)
output_graph.bind("dig", dig)

# Leg namespaces vast in de RDF-grafiek
for index, row in df.iterrows():
            output_graph.add((i.term(URIRef(row['uuid_E33'])), RDF.type, crm.E33_Linguistic_Object))

            # aanduiding technisch rapport
            output_graph.add((i.term(URIRef(row['uuid_E33'])), crm.P2_has_type, (URIRef('http://vocab.getty.edu/aat/300027323'))))
            output_graph.add((URIRef('http://vocab.getty.edu/aat/300027323'), RDF.type, crm.E55_Type))
            output_graph.add((URIRef('http://vocab.getty.edu/aat/300027323'), RDFS.label, Literal('technical report', lang='en')))

            # adlibnummer
            uuid_adlibnummer = row['uuid recordnummer']
            if uuid_adlibnummer is not None and not pd.isna(uuid_adlibnummer):
                output_graph.add((i.term(URIRef(row['uuid_E33'])), crm.P1_is_identified_by, i.term(URIRef(row['uuid recordnummer']))))
                output_graph.add((i.term(URIRef(row['uuid recordnummer'])), RDF.type, crm.E42_Identifier))
                output_graph.add((i.term(URIRef(row['uuid recordnummer'])), crm.P190_has_symbolic_content, Literal(row['recordnummer'], datatype=XSD.string)))
                output_graph.add((i.term(URIRef(row['uuid recordnummer'])), crm.P2_has_type, (URIRef('https://data.cultureelerfgoed.nl/term/id/rn/240c0699-1dbe-4476-9a1e-3aa4e8387352'))))
                output_graph.add((URIRef('https://data.cultureelerfgoed.nl/term/id/rn/240c0699-1dbe-4476-9a1e-3aa4e8387352'), RDF.type, crm.E55_Type))
                output_graph.add((URIRef('https://data.cultureelerfgoed.nl/term/id/rn/240c0699-1dbe-4476-9a1e-3aa4e8387352'), RDFS.label, Literal('adlib nummer', lang='nl')))

            # titel
            output_graph.add((i.term(URIRef(row['uuid_E33'])), crm.P1_is_identified_by, i.term(URIRef(row['uuid titel']))))
            output_graph.add((i.term(URIRef(row['uuid titel'])), RDF.type, crm.E42_Identifier))
            output_graph.add((i.term(URIRef(row['uuid titel'])), RDF.type, crm.E33_E41_Linguistic_Appellation))
            output_graph.add((i.term(URIRef(row['uuid titel'])), crm.P190_has_symbolic_content, Literal(row['titel'], lang='nl')))

            # rce dossiernummer
            dossier_nummer = row['exemplaar.nummer']
            if dossier_nummer is not None and not pd.isna(dossier_nummer):
                output_graph.add((i.term(URIRef(row['uuid_E33'])), crm.P1_is_identified_by, i.term(URIRef(row['uuid exemplaar.nummer']))))
                output_graph.add((i.term(URIRef(row['uuid exemplaar.nummer'])), RDF.type, crm.E42_Identifier))
                output_graph.add((i.term(URIRef(row['uuid exemplaar.nummer'])), crm.P190_has_symbolic_content, Literal(row['exemplaar.nummer'])))
                output_graph.add((i.term(URIRef(row['uuid exemplaar.nummer'])), crm.P2_has_type,(URIRef('https://data.cultureelerfgoed.nl/term/id/rn/70003ebd-15ba-4f93-9c0c-baac09ccff44'))))
                output_graph.add((URIRef('https://data.cultureelerfgoed.nl/term/id/rn/70003ebd-15ba-4f93-9c0c-baac09ccff44'), RDF.type, crm.E55_Type))
                output_graph.add((URIRef('https://data.cultureelerfgoed.nl/term/id/rn/70003ebd-15ba-4f93-9c0c-baac09ccff44'), RDFS.label, Literal('rce dossiernummer', lang='nl')))

            # rce objectnummer
            ICN_objectnummer = row['ICN_objectnummer']
            if ICN_objectnummer is not None and not pd.isna(ICN_objectnummer):
                output_graph.add((i.term(URIRef(row['uuid_E33'])), crm.P1_is_identified_by, i.term(URIRef(row['uuid ICN_objectnummer']))))
                output_graph.add((i.term(URIRef(row['uuid ICN_objectnummer'])), RDF.type, crm.E42_Identifier))
                output_graph.add((i.term(URIRef(row['uuid ICN_objectnummer'])), crm.P190_has_symbolic_content, Literal(row['ICN_objectnummer'])))
                output_graph.add((i.term(URIRef(row['uuid ICN_objectnummer'])), crm.P2_has_type, (URIRef('https://data.cultureelerfgoed.nl/term/id/rn/be568e9e-9cab-48ef-b226-fd9d37b971b1'))))
                output_graph.add((URIRef('https://data.cultureelerfgoed.nl/term/id/rn/be568e9e-9cab-48ef-b226-fd9d37b971b1'), RDF.type, crm.E55_Type))
                output_graph.add((URIRef('https://data.cultureelerfgoed.nl/term/id/rn/be568e9e-9cab-48ef-b226-fd9d37b971b1'), RDFS.label, Literal('rce objectnummer', lang='nl')))
            # trefwoord
            for index in range(1, 13):
                uri_trefwoord_col = f'uri trefwoord.inhoud {index}'
                label_trefwoord_col = f'trefwoord.inhoud {index}'

                uri_trefwoord = row[uri_trefwoord_col]
                trefwoord = row[label_trefwoord_col]

                if uri_trefwoord is not None and not pd.isna(uri_trefwoord):
                    # Create a new variable to represent the object with a 'term' attribute
                    current_object = i.term(URIRef(row['uuid_E33']))

                    # Perform the operations
                    output_graph.add((current_object, crm.P2_has_type, URIRef(uri_trefwoord)))
                    output_graph.add((URIRef(uri_trefwoord), RDF.type, crm.E55_Type))
                    output_graph.add((URIRef(uri_trefwoord), RDFS.label, Literal(trefwoord, lang='nl')))


            # predicaten naar andere entiteiten
            output_graph.add((i.term(URIRef(row['uuid_E33'])), crm.P67_refers_to, i.term(URIRef(row['uuid_E14']))))
            output_graph.add((i.term(URIRef(row['uuid_E33'])), crm.P67_refers_to, i.term(URIRef(row['uuid_E22']))))

            # taal
            taalcode_1 = row['taalcode 1']
            if taalcode_1 is not None and not pd.isna(taalcode_1):
                output_graph.add((i.term(URIRef(row['uuid_E33'])), crm.P72_has_language, Literal(row['taalcode 1'])))
            taalcode_2 = row['taalcode 2']
            if taalcode_2 is not None and not pd.isna(taalcode_2):
                output_graph.add((i.term(URIRef(row['uuid_E33'])), crm.P72_has_language, Literal(row['taalcode 2'])))

            # digitale referentie
            output_graph.add((i.term(URIRef(row['uuid_E33'])), la.access_point, URIRef(row['digitale_referentie'])))
            output_graph.add((URIRef(row['digitale_referentie']), RDF.type, dig.D1_Digital_Object))

            # toegankelijkheid
            output_graph.add((i.term(URIRef(row['uuid_E33'])), crm.P2_has_type, (URIRef('http://vocab.getty.edu/aat/3004449723'))))
            output_graph.add((URIRef('http://vocab.getty.edu/aat/3004449723'), RDF.type, crm.E55_Type))
            output_graph.add((URIRef('http://vocab.getty.edu/aat/3004449723'), RDFS.label, Literal(row['toegankelijkheid'], lang='en')))


            # E14 Condition Assessment (Technisch onderzoek)
            output_graph.add((i.term(URIRef(row['uuid_E14'])), RDF.type, crm.E14_Condition_Assessment))


            # projectnummer
            uuid_project_nummer = row['uuid werknummer']
            if uuid_project_nummer is not None and not pd.isna(uuid_project_nummer):
                output_graph.add((i.term(URIRef(row['uuid_E14'])), crm.P1_is_identified_by, i.term(URIRef(row['uuid werknummer']))))
                output_graph.add((i.term(URIRef(row['uuid werknummer'])), RDF.type, crm.E42_Identifier))
                output_graph.add((i.term(URIRef(row['uuid werknummer'])), crm.P190_has_symbolic_content, Literal(row['werknummer'])))
                output_graph.add((i.term(URIRef(row['uuid werknummer'])), crm.P2_has_type, (URIRef('https://data.cultureelerfgoed.nl/term/id/rn/6e5da07f-8f5e-40b0-83b9-15c6523edc11'))))
                output_graph.add((URIRef('https://data.cultureelerfgoed.nl/term/id/rn/6e5da07f-8f5e-40b0-83b9-15c6523edc11'), RDF.type, crm.E55_Type))
                output_graph.add((URIRef('https://data.cultureelerfgoed.nl/term/id/rn/6e5da07f-8f5e-40b0-83b9-15c6523edc11'), RDFS.label, Literal('rce projectnummer', lang='nl')))

            # aanduiding Onderzoek
            output_graph.add((i.term(URIRef(row['uuid_E14'])), crm.P2_has_type, (URIRef('http://vocab.getty.edu/aat/300054687'))))
            output_graph.add((URIRef('http://vocab.getty.edu/aat/300054687'), RDF.type, crm.E55_Type))
            output_graph.add((URIRef('http://vocab.getty.edu/aat/300054687'), RDFS.label, Literal('research (function)', lang='en')))

            # analysemethode
            for index in range(1, 7):
                uri_analysemethode_col = f'uri analysemethode {index}'
                label_analysemethode_col = f'analysemethode {index}'

                uri_analysemethode = row[uri_analysemethode_col]
                label_analysemethode = row[label_analysemethode_col]

                if uri_analysemethode is not None and not pd.isna(uri_analysemethode):
                    output_graph.add((i.term(URIRef(row['uuid_E14'])), crm.P32_used_general_technique, URIRef(uri_analysemethode)))
                    output_graph.add((URIRef(uri_analysemethode), RDF.type, crm.E55_Type))
                    output_graph.add((URIRef(uri_analysemethode), RDFS.label, Literal(label_analysemethode, lang='nl')))

            # actor and role
            output_graph.add((i.term(URIRef(row['uuid_E14'])), crm.P14_carried_out_by, URIRef(row['uri projectleider'])))
            output_graph.add((URIRef(row['uri projectleider']), RDF.type, crm.E39_Actor))
            output_graph.add((URIRef(row['uri projectleider']), RDFS.label, Literal(row['projectleider'], lang='nl')))
            output_graph.add((URIRef(row['uri projectleider']), crm.P2_has_type, (URIRef('http://vocab.getty.edu/aat/300417573'))))
            output_graph.add((URIRef('http://vocab.getty.edu/aat/300417573'), RDF.type, crm.E55_Type))
            output_graph.add((URIRef('http://vocab.getty.edu/aat/300417573'), RDFS.label, Literal('project managers', lang='en')))

            for index in range(1, 6):
                uri_ppt_onderzoekers_col = f'uri onderzoeker {index}'
                label_onderzoeker_col = f'onderzoeker {index}'

                uri_ppt_onderzoekers = row.get(uri_ppt_onderzoekers_col)
                label_onderzoeker = row.get(label_onderzoeker_col)

                if uri_ppt_onderzoekers is not None and not pd.isna(uri_ppt_onderzoekers):
                    output_graph.add((i.term(URIRef(row['uuid_E14'])), crm.P14_carried_out_by, URIRef(uri_ppt_onderzoekers)))
                    output_graph.add((URIRef(uri_ppt_onderzoekers), RDF.type, crm.E39_Actor))
                    output_graph.add((URIRef(uri_ppt_onderzoekers), RDFS.label, Literal(label_onderzoeker, lang='nl')))
                    output_graph.add((URIRef(uri_ppt_onderzoekers), crm.P2_has_type, (URIRef('http://vocab.getty.edu/aat/300025576'))))
                    output_graph.add((URIRef('http://vocab.getty.edu/aat/300025576'), RDF.type, crm.E55_Type))
                    output_graph.add((URIRef('http://vocab.getty.edu/aat/300025576'), RDFS.label, Literal('researchers', lang='en')))

            # time-span
            # Pakt bij crm.P4_has_time-span streepje tussen time en span niet
            output_graph.add((i.term(URIRef(row['uuid_E14'])), crm.P4_has_timespan, i.term(URIRef(row['uuid timespan']))))
            output_graph.add((i.term(URIRef(row['uuid timespan'])), RDF.type, URIRef('http://www.cidoc-crm.org/cidoc-crm/E52_Time-Span')))
            output_graph.add((i.term(URIRef(row['uuid timespan'])), crm.P82a_begin_of_the_begin, Literal(row['zoekjaar'], datatype=XSD.gYear)))
            output_graph.add((i.term(URIRef(row['uuid timespan'])), crm.P82b_end_of_the_end, Literal(row['zoekjaar'], datatype=XSD.gYear)))

            # locatie
            output_graph.add((i.term(URIRef(row['uuid_E14'])), crm.P7_took_place_at, URIRef(row['uri corporatieve_auteur'])))
            output_graph.add((URIRef(row['uri corporatieve_auteur']), RDF.type, crm.E53_Place))
            output_graph.add((URIRef(row['uri corporatieve_auteur']), RDFS.label, Literal(row['corporatieve_auteur'], lang='nl')))

            # predicaten naar andere entiteiten
            output_graph.add((i.term(URIRef(row['uuid_E14'])), crm.P67i_is_referred_by, i.term(URIRef(row['uuid_E33']))))
            output_graph.add((i.term(URIRef(row['uuid_E14'])), crm.P34_concerned, i.term(URIRef(row['uuid_E22']))))

            # E22_Human-Made_Object (Kunstwerk)
            # Mis titel kunstwerk
            output_graph.add((i.term(URIRef(row['uuid_E22'])), RDF.type, URIRef('http://www.cidoc-crm.org/cidoc-crm/E22_Human-Made_Object')))

            # aanduiding kunstwerk
            output_graph.add((i.term(URIRef(row['uuid_E22'])), crm.P2_has_type, (URIRef('http://vocab.getty.edu/aat/300177435'))))
            output_graph.add((URIRef('http://vocab.getty.edu/aat/300177435'), RDF.type, crm.E55_Type))
            output_graph.add((URIRef('http://vocab.getty.edu/aat/300177435'), RDFS.label, Literal('paintings', lang='en')))

            # kunstenaar
            output_graph.add((i.term(URIRef(row['uuid_E22'])), crm.P108i_was_produced_by, i.term(URIRef(row['uuid production']))))
            output_graph.add((i.term(URIRef(row['uuid production'])), RDF.type, crm.E12_Production))
            output_graph.add((i.term(URIRef(row['uuid production'])), crm.P14_carried_out_by,(URIRef('http://vocab.getty.edu/ulan/500115588'))))
            output_graph.add((URIRef('http://vocab.getty.edu/ulan/500115588'), RDF.type, crm.E39_Actor))
            output_graph.add((URIRef('http://vocab.getty.edu/ulan/500115588'), RDFS.label, Literal('Gogh, Vincent van', lang='nl')))

            output_graph.add((i.term(URIRef(row['uuid production'])), crm.P14_carried_out_by, (URIRef('https://www.wikidata.org/wiki/Q5582'))))
            output_graph.add((URIRef('https://www.wikidata.org/wiki/Q5582'), RDF.type, crm.E39_Actor))
            output_graph.add((URIRef('https://www.wikidata.org/wiki/Q5582'), RDFS.label, Literal('Gogh, Vincent van', lang='nl')))

            # Besloten om 2e persoonsnaam niet op te nemen
            #uri_persoonsnaam_2 = row.get('uri persoonsnaam 2')
            #if uri_persoonsnaam_2 is not None and not pd.isna(uri_persoonsnaam_2):
             #   output_graph.add((i.term(URIRef(row['uuid Production'])), crm.P14_carried_out_by, URIRef(row['uri persoonsnaam 2'])))
              #  output_graph.add((URIRef(row['uri persoonsnaam 2']), RDFS.label, Literal(row['label persoonsnaam 2'])))

            # De La Faille number
            uuid_E22 = str(row['uuid_E22'])

            for index in range(1, 7):
                Fnummer_col = f'F-nummer {index}'
                uuid_F_nummer_col = f'uuid F-nummer {index}'

                Fnummer = row.get(Fnummer_col)
                uuid_F_nummer = row.get(uuid_F_nummer_col)

                if uuid_F_nummer is not None and not pd.isna(uuid_F_nummer):
                    # Construct the URI seeAlso
                    uri = f'https://vangoghworldwide.org/data/artwork/{Fnummer}'
                    output_graph.add((i.term(URIRef(uuid_E22)), RDFS.seeAlso, URIRef(uri)))

                if uuid_F_nummer is not None and not pd.isna(uuid_F_nummer):
                    output_graph.add((i.term(URIRef(uuid_E22)), crm.P1_is_identified_by, i.term(URIRef(uuid_F_nummer))))

                if Fnummer is not None and not pd.isna(Fnummer):
                    output_graph.add((i.term(URIRef(uuid_F_nummer)), crm.P190_has_symbolic_content, Literal(Fnummer)))
                    output_graph.add((i.term(URIRef(uuid_F_nummer)), crm.P2_has_type, URIRef('https://vangoghworldwide.org/data/concept/f_number')))
                    output_graph.add((URIRef('https://vangoghworldwide.org/data/concept/f_number'), RDF.type, crm.E55_Type))
                    output_graph.add((URIRef('https://vangoghworldwide.org/data/concept/f_number'), RDFS.label, Literal('De La Faille number', lang='nl')))

            # predicaten naar andere entiteiten
            output_graph.add((i.term(URIRef(row['uuid_E22'])), crm.P67i_is_referred_by, i.term(URIRef(row['uuid_E33']))))
            output_graph.add((i.term(URIRef(row['uuid_E22'])), crm.P34i_was_assessed_by, i.term(URIRef(row['uuid_E14']))))


# Sla dataframe op in Turtle file
output_graph.serialize(destination=output_file, format='ttl')






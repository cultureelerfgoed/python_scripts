import requests
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import datetime as dt

# Definieer de huidige datum
current_date = dt.datetime.now().strftime("%Y-%m-%d")

# output
output_file_cube = f"/Users/patrickmout/Downloads/EGM aantal rms/EGM_mon_rmgm_h_s_{current_date}.xlsx"
output_file_missing = f"/Users/patrickmout/Downloads/EGM aantal rms/missing_rms_{current_date}.xlsx"

# Functie om SPARQL-queryresultaten naar DataFrame te converteren
def sparql_to_df(query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    bindings = results["results"]["bindings"]
    df = pd.json_normalize(bindings)
    return df

# SPARQL endpoint URL
endpoint_url = "https://api.linkeddata.cultureelerfgoed.nl/datasets/rce/cho/services/cho/sparql"

# SPARQL-query voor het verkrijgen van gegevens
query_patrick = """
PREFIX owms: <http://standaarden.overheid.nl/owms/terms/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX graph: <https://linkeddata.cultureelerfgoed.nl/graph/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX ceo: <https://linkeddata.cultureelerfgoed.nl/def/ceo#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?rijksmonumentnummer  
    (REPLACE(STR(?CBSCodeGemeente), "^0+", "") AS ?CBSCodeGemeente)  
    (REPLACE(STR(?CBSCodeGemeente_s), "^0+", "") AS ?CBSCodeGemeente_s)
WHERE {
  ?rijksmonument ceo:rijksmonumentnummer ?rijksmonumentnummer ;
                   ceo:heeftBasisregistratieRelatie/ceo:heeftGemeente ?gemeente .

  # Minus monumentaard archeologisch
  MINUS { ?rijksmonument ceo:heeftMonumentAard <https://data.cultureelerfgoed.nl/term/id/rn/b673c8c1-5d93-496d-8f9e-89133d579d77> . }

  # Minus status voorbeschermd
  MINUS { ?rijksmonument ceo:heeftJuridischeStatus <https://data.cultureelerfgoed.nl/term/id/rn/2e93edd1-098f-4f31-ae7e-72cb77f4d2ca> . }

  # Minus status geen rijksmonument
  MINUS { ?rijksmonument ceo:heeftJuridischeStatus <https://data.cultureelerfgoed.nl/term/id/rn/3e79bb7c-b459-4998-a9ed-78d91d069227> . }

  GRAPH <https://triplydb.com/koop/owms/graphs/default> {
    ?gemeente rdf:type <http://standaarden.overheid.nl/owms/terms/Gemeente> ;
              <http://standaarden.overheid.nl/owms/terms/CBSCode> ?CBSCodeGemeente .

    OPTIONAL { ?gemeente <http://standaarden.overheid.nl/owms/terms/successor> ?successor .
               ?successor <http://standaarden.overheid.nl/owms/terms/CBSCode> ?CBSCodeGemeente_s . }
  }
}
"""

# Verkrijg de resultaten van de SPARQL-query en sla deze op in een DataFrame
all_dfs = []
offset = 0
limit = 10000

while True:
    query_with_offset = query_patrick + f" OFFSET {offset} LIMIT {limit}"
    df = sparql_to_df(query_with_offset)
    if df.empty:
        break  # Stop de lus als er geen resultaten meer zijn
    all_dfs.append(df)
    offset += limit

query_df = pd.concat(all_dfs, ignore_index=True)

# Hernoem kolommen
query_df.rename(columns={'rijksmonumentnummer.value': 'rijksmonumentnummer',
                         'CBSCodeGemeente.value': 'CBSCodeGemeente',
                         'CBSCodeGemeente_s.value': 'CBSCodeGemeente_s'}, inplace=True)

# Selecteer kolommen
df_select = query_df[['rijksmonumentnummer', 'CBSCodeGemeente', 'CBSCodeGemeente_s']]

# Aantal rijksmonumenten
aantal_rms_1 = df_select['rijksmonumentnummer'].nunique()
print("Aantal rijksmonumenten na query", aantal_rms_1)

# Lees het Excel-bestand in een DataFrame
df_functie = pd.read_excel("/Users/patrickmout/Downloads/EGM aantal rms/rm_func.xlsx")

def correctie_gemeentelijke_herindeling(df_select):
    df_select_copy = df_select.copy()
    for index, row in df_select_copy.iterrows():
        if pd.notna(row['CBSCodeGemeente_s']):
            df_select_copy.at[index, 'CBSCodeGemeente'] = row['CBSCodeGemeente_s']
    return df_select_copy

# Voer de correctie_gemeentelijke_herindeling functie uit op df_select
df_select = correctie_gemeentelijke_herindeling(df_select)

# Zorg ervoor dat 'rijksmonumentnummer' een string is in beide DataFrames
df_select['rijksmonumentnummer'] = df_select['rijksmonumentnummer'].astype(str)
df_functie['rijksmonument_nummer'] = df_functie['rijksmonument_nummer'].astype(str)

# Voer de merge-operatie uit met de nieuwe DataFrame
df_egm = pd.merge(df_select, df_functie, left_on="rijksmonumentnummer", right_on="rijksmonument_nummer", how="inner")

# Hernoem kolommen
df_egm.rename(columns={'CBSCodeGemeente': 'geoitem'}, inplace=True)

# Maak EGM cube
df_cube = df_egm[['geoitem', 'dnc_alg_cah', 'dnc_alg_cas']].copy()

# Add new columns to the cube
now = dt.datetime.now()
time = now.strftime('m' + '%m' + 'y' + '%Y')
df_cube.insert(loc=0, column='period', value=time)
df_cube.insert(loc=1, column='mon_rmgm_h_s', value=1)
df_cube.insert(loc=1, column='geolevel', value='gemeente')

# Group the rows
df_cube = df_cube.groupby(['period','geolevel', 'geoitem', 'dnc_alg_cah', 'dnc_alg_cas'], as_index=False).sum()

# Rearrange column order
df_cube = df_cube[['period', 'geolevel', 'geoitem','mon_rmgm_h_s', 'dnc_alg_cah', 'dnc_alg_cas']]

# Sorteer de DataFrame op de kolom 'geolevel' in oplopende volgorde
df_cube = df_cube.sort_values(by='geolevel')

# Aantal rijksmonumenten
aantal_rms_2 = df_egm['rijksmonumentnummer'].nunique()
print("Aantal rijksmonumenten na bewerking", aantal_rms_2)

# Vergelijk de rijksmonumentnummers in df_select en df_egm
missing_rms = df_select[~df_select['rijksmonumentnummer'].isin(df_egm['rijksmonumentnummer'])]

# Opslaan naar Excel
missing_rms.to_excel(output_file_missing, index=False)
df_cube.to_excel(output_file_cube, index=False)

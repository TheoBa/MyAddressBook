import spacy
import streamlit as st
from utils.session_state import update_state


# Charger le modèle de langue français de SpaCy
nlp = spacy.load("fr_core_news_sm")

# Fonction pour extraire les informations clés à partir de la description
def extract_information(description):
    doc = nlp(description)
    names = []
    positions = []
    companies = []
    contacts = []
    
    for entity in doc.ents:
        st.markdown(entity.label_ + ' | ' + entity.text)

    for ent in doc.ents:
        if ent.label_ == "PER":  # Personne
            names.append(ent.text)
        elif ent.label_ == "ORG":  # Organisation
            companies.append(ent.text)
        # Autres (peut être des postes ou des coordonnées)
        if "@" in ent.text or "tel" in ent.text or "email" in ent.text:
            contacts.append(ent.text)
        else:
            positions.append(ent.text)
    
    update_state("names", names)
    update_state("positions", positions)
    update_state("companies", companies)
    update_state("contacts", contacts)
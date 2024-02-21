import spacy
import sqlite3
import streamlit as st


st.set_page_config(page_title='My Address Book', page_icon='🤓', layout="wide")

def homepage_content():
    st.header("Address Book Inputs")
    with st.form("Collect unstructured inputs"):
        description = st.text_input('Contact description')
        submitted = st.form_submit_button("Submit")
        if submitted:
            names, positions, companies, contacts = extract_information(description)
    if submitted:
        with st.form("Confirm structured inputs"):
            name, position, company, contact = confirm_information(names, positions, companies, contacts)
            confirmed = st.form_submit_button("Confirm inputs")
            if confirmed:
                save_to_database(name, position, company, contact)


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
    
    return names, positions, companies, contacts

# Fonction pour confirmer les informations
def confirm_information(names, positions, companies, contacts):
    st.markdown("Please confirm data extraction !")
    name = st.radio("Contact name", names)
    position = st.radio("Contact position", positions)
    company = st.radio("Contact company", companies)
    contact = st.radio("Contact information", contacts)
    return name, position, company, contact


# Fonction pour enregistrer les informations dans la base de données SQLite
def save_to_database(names, positions, companies, contacts):
    conn = sqlite3.connect('person_info.db')
    c = conn.cursor()
    
    # Création de la table si elle n'existe pas
    c.execute('''CREATE TABLE IF NOT EXISTS person_info
                 (name text, position text, company text, contact text)''')
    
    # Insertion des données dans la table
    for i in range(max(len(names), len(positions), len(companies), len(contacts))):
        name = names[i] if i < len(names) else None
        position = positions[i] if i < len(positions) else None
        company = companies[i] if i < len(companies) else None
        contact = contacts[i] if i < len(contacts) else None
        
        c.execute("INSERT INTO person_info VALUES (?, ?, ?, ?)", (name, position, company, contact))
    
    # Valider les changements et fermer la connexion
    conn.commit()
    conn.close()

# # Exemple d'utilisation
# description = "Jean Dupont, CEO de la société ABC, son email est jean.dupont@example.com."
# names, positions, companies, contacts = extract_information(description)
# save_to_database(names, positions, companies, contacts)

if __name__ == '__main__':
    homepage_content()
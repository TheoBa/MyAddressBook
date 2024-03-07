import sqlite3


# Fonction pour enregistrer les informations dans la base de données SQLite
def save_to_database(name, position, company, contact):
    conn = sqlite3.connect('person_info.db')
    c = conn.cursor()
    
    # Création de la table si elle n'existe pas
    c.execute('''CREATE TABLE IF NOT EXISTS person_info
                 (name text, position text, company text, contact text)''')
    
    c.execute("INSERT INTO person_info VALUES (?, ?, ?, ?)", (name, position, company, contact))
    
    # Valider les changements et fermer la connexion
    conn.commit()
    conn.close()
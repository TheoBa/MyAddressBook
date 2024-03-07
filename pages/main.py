import streamlit as st 
from utils.database import save_to_database
from utils.extraction_spacy import extract_information
from utils.session_state import init_states, update_state, del_state
from utils.chain_local_llm import main_test_chain


def homepage_content():
    init_states()
    st.header("Address Book Inputs")
    with st.form("Collect unstructured inputs"):
        description = st.text_input('Contact description')
        submitted = st.form_submit_button("Submit")
        if submitted:
            update_state('text_submitted', True)
            main_test_chain(description)
            # extract_information(description)
    if st.session_state["text_submitted"]:
        with st.expander("Confirm inputs", expanded=True):
            name, position, company, phone = confirm_information()
            confirmed = st.button("Confirm inputs")
            st.markdown(confirmed)
            if confirmed:
                save_to_database(name, position, company, phone)
                update_state("last_submit", name)
                update_state("text_submitted", False)
    elif st.session_state["last_submit"]:
        st.markdown(f"✅ {st.session_state['last_submit']} submitted to your custom address book")


# Fonction pour confirmer les informations
def confirm_information():
    st.markdown("Please confirm data extraction !")
    name = confirm_field("name", st.session_state["names"])
    position = confirm_field("position", st.session_state["positions"])
    company = confirm_field("company", st.session_state["companies"])
    phone = confirm_field("phone", st.session_state["phone"])
    #email = confirm_field("email", st.session_state["email"])
    return name, position, company, phone#, email


def confirm_field(field_name, options):
    if "failed to retrieve correct" not in options[0]:
        options += [f"failed to retrieve correct {field_name}"]
    field = st.radio(f"**Contact {field_name}**", options)
    if "failed to retrieve correct" in field:
        user_input = st.text_input(f"Enter contact {field_name}")
        return user_input
    else:
        return field

# # Exemple d'utilisation
# description = "Jean Dupont, CEO de la société ABC, son email est jean.dupont@example.com."
# names, positions, companies, contacts = extract_information(description)
# save_to_database(names, positions, companies, contacts)
# desc = "Jean Dupont, CEO de la société ABC company, son email est jean.dupont@example.com. Et on peut le contacter au +33680602103"

if __name__ == '__main__':
    homepage_content()
    test_chain = st.toggle("test_chain ?")
    # if test_chain:
    #     infos = main_test_chain()
    #     st.markdown("OUTPUT")
    #     st.markdown(infos)
    #     # for key in infos:
    #     #     st.markdown(f"{key}: {infos[key]}")

from langchain_community.llms.llamafile import Llamafile
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import PromptTemplate
import streamlit as st
from utils.session_state import update_state
from langchain_core.exceptions import OutputParserException
import json

# Define your desired data structure.
class Contact_information(BaseModel):
    name: str = Field(description="Name of the contact")
    company: str = Field(description="Name of the company of the contact")
    position: str = Field(description="Position of the contact within its company")
    phone: str = Field(description="phone number of the contact if provided")
    #email: str = Field(description="email address of the contact if provided")


def main_test_chain(desc):
    llamafile = Llamafile()

    output_parser = JsonOutputParser(pydantic_object=Contact_information)
    format_instructions = output_parser.get_format_instructions()
    st.markdown("INFORMATIONS")
    st.markdown(format_instructions)

    # Prompt
    prompt = PromptTemplate(
        template="Extract core information, when available, from a contact description.\n{format_instructions}\nThe contact description: {desc}.",
        input_variables=["desc"],
        partial_variables={"format_instructions": format_instructions}
    )

    st.markdown("PROMPT")
    st.markdown(prompt)
    
    chain = (prompt | llamafile 
             | output_parser
             )

    # Run
    try:
        informations = chain.invoke({"desc": desc})
        st.markdown("CA A MARCHE")
        st.markdown(informations)
        informations = dict(informations)
        #informations = informations["properties"]
    except OutputParserException as e:
        st.markdown("ERROR: ")
        st.markdown(e)
        informations = {
            "name": "failed to retrieve correct name",
            "company": "failed to retrieve correct company",
            "position": "failed to retrieve correct position",
            "phone": "failed to retrieve correct phone",
            "email": "failed to retrieve correct email"
            }

    st.markdown("OUTPUTS")
    st.markdown(informations)

    # informations = json.loads(informations)
    update_state("names", [informations["name"]])
    update_state("companies", [informations["company"]])
    update_state("positions", [informations["position"]])
    update_state("phone", [informations["phone"]])
    #update_state("email", [informations["email"]])

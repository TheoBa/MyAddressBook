from dotenv import load_dotenv
import streamlit as st
import multiprocessing
from tempfile import NamedTemporaryFile
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from tempfile import NamedTemporaryFile
from jsonformer.format import highlight_values
from jsonformer.main import Jsonformer
import time
load_dotenv()


# 3. Extract structured info from text via LLM


class HuggingFaceLLM:
    def __init__(self, top_k=50, model_name="databricks/dolly-v2-12b"):
        self.model = AutoModelForCausalLM.from_pretrained(model_name, use_cache=True, device_map="auto")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True, use_cache=True)
        self.top_k = top_k

    def generate(self, prompt, max_length=1024):
        decoder_schema = {
            "title": "Decoding Schema",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "company": {"type": "string"},
                "position": {"type": "string"},
                "contacts": {
                    "type": "object",
                    "properties": {
                        "phone": {"type": "number"},
                        "email": {"type": "string"}
                    }
                },
            }
        }

        from langchain_experimental.llms import JsonFormer

        json_former = JsonFormer(json_schema=decoder_schema, pipeline=self.model)     

        print("Generating...")
        output = json_former()
        #highlight_values(output)
        #print(output)
        return output
    
def extract_structured_data(content: str, data_points):
    llm = HuggingFaceLLM(temperature=0)  # Choose the desired Hugging Face model
    
    template = """
    You are an expert admin people who will extract core information from people' profiles

    {content}

    Above is the content; please try to extract all data points from the content above:
    {data_points}
    """

    # Fill in the placeholders in the template
    formatted_template = template.format(content=content, data_points=data_points)
    #print(formatted_template)
    
    # Generate text using the formatted template
    
    results = llm.predict(formatted_template)

    return results

def main():
    default_data_points = """{
        "name": "name of the person this text is about",
        "company": "company that issued the invoice",
        "position": "the position of the person within its company",
        "contacts": [{
            "phone": "phone number of the person described",
            "email": "email address of the person described"
        }]
    }"""

    st.set_page_config(page_title="Doc extraction", page_icon=":bird:")

    st.header("Doc extraction :bird:")

    data_points = st.text_area(
        "Data points", value=default_data_points, height=170)

    folder_path = './pdfs'  # Replace this with your folder path containing PDFs

    pdf_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith('.pdf')]

    results = []

    if pdf_paths:
        total_start_time = time.time()
        with open("output_results.txt", "w") as output_file:
            for pdf_path in pdf_paths:
                with NamedTemporaryFile(dir='.', suffix='.csv') as f:
                    output_file.write(f"PDF Path: {pdf_path}\n")
                    start_time = time.time()  # Record the start time
                    content = extract_content_from_url(pdf_path)
                    data = extract_structured_data(content, default_data_points)
                    json_data = json.dumps(data)
                    if isinstance(json_data, list):
                        results.extend(json_data)
                    else:
                        results.append(json_data)
                    end_time = time.time()  # Record the end time
                    elapsed_time = end_time - start_time
                    output_file.write(f"Execution time: {elapsed_time:.2f} seconds\n")
                    output_file.write(f"Results: {json_data}\n")
                    output_file.write("\n")
            total_end_time = time.time()
            total_elapsed_time = total_end_time - total_start_time
            output_file.write(f"Total execution time: {total_elapsed_time:.2f} seconds\n")

        

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
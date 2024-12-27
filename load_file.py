from setup_ingestion_pipeline import create_or_load_pipeline
#from load_gdrive_files import load_data_from_gdrive
from llama_index.core import SimpleDirectoryReader
import os

def data_ingestion():
    processed_files_file = 'processed_files.txt'
    input_file = "restaurant_file.txt"

    # Check if the processed files list exists, if not create it
    if not os.path.exists(processed_files_file):
        open(processed_files_file, 'w').close()  # Create an empty file

    # Read the list of processed files
    with open(processed_files_file, 'r') as f:
        processed_files = f.read().splitlines()

    # If the file has already been processed, skip it
    if input_file in processed_files:
        print(f"{input_file} has already been processed. Skipping ingestion.")
        return
    else:
        reader = SimpleDirectoryReader(
                    input_files=[input_file]
                )

        documents = reader.load_data()

        pipeline = create_or_load_pipeline()

        # Process the documents using the pipeline
        nodes = pipeline.run(documents=documents)
        print(f"Ingested {len(nodes)} Nodes")

        # Add the file to the list of processed files
        with open(processed_files_file, 'a') as f:
            f.write(input_file + '\n')
from loguru import logger
from dotenv import load_dotenv
import os
from utils.logger_config import LoggerConfig
from ingest.dataloader import DocumentLoader
from ingest.chunker import DocumentChunker
from langchain.document_loaders import PyPDFLoader

RECREATE_CHROMA_DB = False

def main():
    try:
        # Step 1> Se configura el logger
        LoggerConfig.configure_logger()

        # Step 2> Se carga la configuración desde el archivo config.yaml y se cargan los documentos PDF
        loader = DocumentLoader(DocumentLoader.load_config, PyPDFLoader)
        documents = loader.load_documents()

        # Step 3> Se divide los documentos en fragmentos
        chunker = DocumentChunker(chunk_size=1000, chunk_overlap=200)
        split_documents = chunker.split_documents(documents)

    except Exception as e:
        logger.error(f"[bold red]An error occurred during startup: {e}[/bold red]")
        return     
    

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()

    # Run the main function
    main()
   
   
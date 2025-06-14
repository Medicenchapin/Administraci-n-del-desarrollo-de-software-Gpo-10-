import os
import sys
from loguru import logger

# Agregar la raíz del proyecto al sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
print("Raíz del proyecto:", project_root)

from src.utils.logger_config import LoggerConfig
from langchain.document_loaders import PyPDFLoader
import json
import yaml

class DocumentLoader:
    def __init__(self, config_loader, pdf_loader_cls):
        self.config_loader = config_loader
        self.pdf_loader_cls = pdf_loader_cls

    @staticmethod
    def load_config():
        """
        Load the application configuration from the 'config.yaml' file.

        Returns:
            A dictionary with the application configuration.
        """
        # Construir la ruta al archivo 'config.yaml' en el directorio raíz del proyecto
        logger.info("[cyan]Loading configuration from config.yaml...[cyan]")
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml'))
        with open(config_path) as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

    def load_documents(self):
        config = self.config_loader()
        pdf_paths = config.get("pdfs", {}).get("paths", [])
        pdf_list = []
        for path in pdf_paths:
            logger.info(f"[cyan]Starting to load the PDF file from {path}...[/cyan]")
            loader = self.pdf_loader_cls(path)
            logger.success("[bold green]Loader created, starting to load data...[/bold green]")
            pdf_list.extend(loader.load())
            logger.success("[bold green]Data loaded successfully[/bold green]")
            logger.success(f"[bold green]Loaded {len(pdf_list)} documents.[/bold green]")
        return pdf_list


if __name__ == "__main__":
    # Usar el método estático load_config de la clase DocumentLoader
    LoggerConfig.configure_logger()
    loader = DocumentLoader(DocumentLoader.load_config, PyPDFLoader)
    documents = loader.load_documents()
    print(f"Loaded {len(documents)} documents.")
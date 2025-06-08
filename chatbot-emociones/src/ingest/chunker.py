from langchain.text_splitter import RecursiveCharacterTextSplitter
from loguru import logger

class DocumentChunker:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def split_documents(self, documents):
        """
        Divide una lista de documentos en fragmentos usando RecursiveCharacterTextSplitter.

        Args:
            documents (list): Lista de documentos (cada uno debe tener un atributo 'page_content' o ser string).

        Returns:
            list: Lista de fragmentos de texto.
        """
        split_documents =  []
         
        if not documents:
            logger.warning("[bold yellow]No documents provided to split.[/bold yellow]")
            return []
        else:
            logger.info(f"[cyan]Splitting {len(documents)} documents into chunks...[/cyan]")
            split_documents =  self.splitter.split_documents(documents)
            logger.success(f"[bold green]Successfully split into {len(split_documents)} chunks.[/bold green]")
        return split_documents
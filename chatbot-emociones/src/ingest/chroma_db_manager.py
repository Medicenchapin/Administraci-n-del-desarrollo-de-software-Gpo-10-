from langchain.vectorstores import Chroma
from rich.console import Console
from loguru import logger
from langchain.embeddings import SentenceTransformerEmbeddings

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

class ChromaDBManager:
    def __init__(self, path: str = "./chatbot-emociones/src/chromadb", recreate_chroma_db=False, batch_size=166):
        """
        Inicializa el gestor de Chroma DB.

        Args:
            embeddings: Objeto de embeddings.
            path (str): Ruta o nombre de la base de datos.
            recreate_chroma_db (bool): Si se debe recrear la base de datos.
            batch_size (int): Tamaño máximo de lote para embeddings.
        """

        logger.info("[cyan]Initializing Chroma DB Manager...[/cyan]")
        self.embeddings_model_name = "paraphrase-MiniLM-L6-v2"
        self.path = path
        self.recreate_chroma_db = recreate_chroma_db
        self.batch_size = batch_size

    def create_embeddings(self, documents: list) -> Chroma:
        """
        Crea un objeto de embeddings utilizando SentenceTransformerEmbeddings y procesa en lotes.

        Returns:
            Un objeto de embeddings.
        """
        logger.info("[cyan]Creating embeddings...[/cyan]")

        if not self.embeddings_model_name:
            logger.error("[bold red]Embeddings model name is not set.[/bold red]")
            raise ValueError("Embeddings model name must be specified.")
        
        logger.info(f"[cyan]Using embeddings model: {self.embeddings_model_name}[/cyan]")
        if not isinstance(self.embeddings_model_name, str):
            logger.error("[bold red]Embeddings model name must be a string.[/bold red]")
            raise TypeError("Embeddings model name must be a string.")
        
        embeddings = SentenceTransformerEmbeddings(model_name=self.embeddings_model_name)
        if not embeddings:
            logger.error("[bold red]Failed to create embeddings.[/bold red]")
            raise RuntimeError("Failed to create embeddings with the specified model.")
        
        logger.info(f"[cyan] Creating Chroma DB with embeddings model: {self.embeddings_model_name}[/cyan]")

        # Procesar en lotes si es necesario
        if len(documents) > self.batch_size:
            logger.info(f"[yellow]Processing documents in batches of {self.batch_size}...[/yellow]")
            all_vectorstores = []
            for i, docs_batch in enumerate(batch(documents, self.batch_size)):
                vectorstore = self.get_chroma_db(
                    embeddings=embeddings,
                    documents=docs_batch,
                    recreate_chroma_db=(self.recreate_chroma_db if i == 0 else False),  # Solo el primer batch recrea la BD
                    collection_name="default_collection"
                )
                vectorstore.persist()
                all_vectorstores.append(vectorstore)
            logger.success("[bold green]All batches processed and persisted successfully.[/bold green]")
            return all_vectorstores
        else:
            vectorstore = self.get_chroma_db(
                embeddings=embeddings,
                documents=documents,
                recreate_chroma_db=self.recreate_chroma_db,
                collection_name="default_collection"
            )
            if not vectorstore:
                logger.error("[bold red]Failed to create or load Chroma DB.[/bold red]")
                raise RuntimeError("Failed to create or load Chroma DB with the specified embeddings.")
            
            vectorstore.persist()
            logger.info(f"[cyan]Chroma DB persisted at {self.path}[/cyan]")
            logger.success(f"[green] Embeddings saved successfully in Chroma DB at {self.path}[/green]")
            logger.success("[bold green]Embeddings created successfully.[/bold green]")
            return vectorstore

    def get_chroma_db(self, 
                      embeddings, 
                      documents, 
                      recreate_chroma_db=False, 
                      collection_name="default_collection"):
        """
        Crea o carga un vectorstore de Chroma para los documentos.

        Args:
            documents (list): Lista de objetos Document.

        Returns:
            Un vectorstore de Chroma.
        """
        texts = [doc.page_content for doc in documents]

        if recreate_chroma_db:
            logger.info("[cyan]Recreating Chroma DB[/cyan]")
            return Chroma.from_texts(
                texts=texts,
                embedding=embeddings,
                collection_name=collection_name
            )
        else:
            logger.info("[green]Loading Chroma DB[/green]")
            return Chroma(
                persist_directory=self.path,
                embedding_function=embeddings or SentenceTransformerEmbeddings(self.embeddings_model_name),
                collection_name=collection_name 
            )

### 2. README_TechnicalDecisions.md (SCRUM-32: Documenting Technical Decisions)

```markdown
# Chatbot-Emociones · Decisiones Técnicas Iniciales

> **Proyecto:** Sistema de clasificación emocional de texto con LLM (Together AI)  
> **Sprint 1 – Foco exclusivo en ingesta** – Cargamos *Marianela.pdf*, lo fragmentamos, generamos *embeddings* y los almacenamos en ChromaDB.

## Equipo

| Alumno                          | Matrícula |
|---------------------------------|-----------|
| Gustavo Adolfo Morales García   | A00828432 |
| Luis Axel González Hernández    | A01795321 |
| Ignacio José Aguilar García     | A00819762 |
| Edwin David Hernández Alejandre | A01794692 |

---

## 1 · Stack Tecnológico

- **Lenguaje**: Python 3.11
  - *Razón*: Soporte largo, compatibilidad con librerías modernas (ver `requirements.txt`).
  - *Alternativa*: Java descartado por menor ecosistema de IA.
- **Gestor de Entornos**: Conda
  - *Razón*: Manejo de dependencias complejas (e.g., `sentence-transformers`, `chromadb`).
  - *Alternativa*: Virtualenv descartado por menor gestión de versiones científicas.
- **Framework**: LangChain
  - *Razón*: Modularidad para loaders, splitters, embeddings, y futura integración RAG/LLM.
  - *Alternativa*: LlamaIndex descartado por menor flexibilidad en pipelines personalizados.

---

## 2 · Modelo de Embeddings

- **Elección**: `all-MiniLM-L6-v2` (384 dims, 61M params)
  - *Razón*: Ligero, open-source, eficiente para pruebas locales (ver `chroma_db_manager.py`).
  - *Alternativa*: `bert-base-uncased` (110M params) descartado por alto consumo de recursos.
  - *Trade-off*: Menor precisión que modelos más grandes, pero suficiente para prototipo.

---

## 3 · Librerías

- **Cargador**: `langchain_community.document_loaders.PyPDFLoader` (ver `dataloader.py`)
  - *Razón*: Extrae texto y metadatos de PDFs, integración nativa con LangChain.
  - *Alternativa*: `PyMuPDF` descartado por menor integración.
- **Splitter**: `langchain_text_splitters.RecursiveCharacterTextSplitter` (ver `chunker.py`)
  - *Razón*: Divide texto respetando frases/párrafos, con solape para contexto.
  - *Alternativa*: `CharacterTextSplitter` descartado por pérdida de contexto.
- **Vector Store**: `chromadb` v0.4.15 (ver `chroma_db_manager.py`)
  - *Razón*: Persistencia local (SQLite + parquet), HNSW para búsqueda O(log n).
  - *Alternativa*: FAISS descartado por menor persistencia y mayor complejidad.
- **Logging**: `loguru` + `rich` (ver `logger_config.py`)
  - *Razón*: Formato colorido, rotación de logs, trazabilidad (ver `logs/app.log`).
  - *Alternativa*: `logging` estándar descartado por menor visualización.

---

## 4 · Consideraciones Futuras

- **LLM**: Together AI (pendiente de API key en `.env`) para clasificación emocional.
- **UI**: FastAPI como backend, con frontend (e.g., Streamlit) para interacción.
- **Validación**: PyTest para verificar chunks, embeddings, y consultas RAG.

---

## 5 · Ejecución Paso-a-Paso

```bash
# 1. Clona el repo y entra
$ git clone https://github.com/<org>/chatbot-emociones.git
$ cd chatbot-emociones

# 2. Crea entorno Conda + instala deps
$ conda create -n chatbot-env python=3.11 -y
$ conda activate chatbot-env
$ pip install -r requirements.txt

# 3. Lanza la ingesta (solo una vez)
$ python -m src.main
# → logs/    # traza completa
# → src/chromadb/   # colección persistente
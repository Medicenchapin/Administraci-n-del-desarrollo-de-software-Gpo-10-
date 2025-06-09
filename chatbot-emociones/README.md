# Chatbot‑Emociones

> **Proyecto:**
> Sistema de clasificación emocional de texto con LLM (Together AI)

## Equipo

| Alumno                          | Matrícula |
| ------------------------------- | --------- |
| Gustavo Adolfo Morales García   | A00828432 |
| Luis Axel González Hernández    | A01795321 |
| Ignacio José Aguilar García     | A00819762 |
| Edwin David Hernández Alejandre | A01794692 |

---

# Chatbot‑Emociones · Pipeline de Ingesta & Embeddings

> **Sprint 1 – Foco exclusivo en ingesta**  – Cargamos *Marianela.pdf*, lo fragmentamos, generamos *embeddings* y los almacenamos en ChromaDB.
> Aún no interviene ninguna UI ni modelo LLM externo.

---

## 1 · ¿Por qué *Marianela*?

*Marianela* (Benito Pérez Galdós, 1878) narra emociones intensas — compasión, esperanza, injusticia.
Eso lo convierte en un texto ideal para:

1. **Probar segmentación**: capítulos largos + diálogos cortos.
2. **Validar embeddings**: semántica clara; chunks similares deben quedar cerca en el espacio vectorial.
3. **Próximas fases**: servirá como corpus para clasificación de emoción y resúmenes.

---

## 2 · Arquitectura general

```mermaid
flowchart TD
    %% Config y logging
    C(config.yaml):::file --> L[DocumentLoader]
    style C fill:#f9f,stroke:#333,stroke-width:1px

    %% Ingesta
    subgraph Ingesta
        L --> P[PyPDFLoader]:::ext
        P --> DL[LangChain Doc]:::obj
        DL --> S[RecursiveCharacterTextSplitter]
        S -->|chunks| EMB[Sentence‑Transformers ("all‑MiniLM‑L6-v2")]
        EMB -->|vectors| DB[(ChromaDB collection)]
    end

    classDef ext fill:#fff,border:2px dashed #aaa
    classDef obj fill:#eef,border:#668
```

### 2.1 Flujo paso a paso

El proceso arranca cuando config.yaml suministra la ruta de Marianela.pdf y los parámetros de chunking. El DocumentLoader usa esa ruta para invocar PyPDFLoader y transforma cada página en un objeto Document que guarda el contenido y metadatos como el número de página. A continuación, el DocumentChunker recibe la lista de documentos y aplica un divisor recursivo de caracteres para generar fragmentos de 1 000 caracteres con un traslape de 200, asegurando que cada trozo conserva contexto suficiente para futuros análisis. Cada uno de estos fragmentos se envía luego al módulo de embeddings de LangChain¹, basado en paraphrase-MiniLM-L6-v2, que produce vectores en un espacio de 384 dimensiones. Finalmente, el ChromaDBManager toma cada vector junto con su texto y metadatos asociados y los indexa en ChromaDB usando un índice HNSW (M=32, ef=200), de forma que sea posible buscar similitudes semánticas de manera eficiente.	A lo largo de todo este flujo, Loguru registra cada fase (carga, chunking, generación y persistencia), tanto en consola como en el fichero rotativo logs/app.log, proporcionando trazabilidad completa y facilitando la depuración y auditoría del pipeline.


| # | Paso                                             | Tecnología                   | Salida                          | Logs                              |
| - | ------------------------------------------------ | ---------------------------- | ------------------------------- | --------------------------------- |
| 1 | `DocumentLoader` lee **config.yaml**             | PyYAML                       | lista de rutas                  | `[INFO] Loading configuration…`   |
| 2 | Cada ruta se carga con **`PyPDFLoader`**         | LangChain Community          | `Langchain Document`            | `[SUCCESS] Loaded 117 documents.` |
| 3 | `RecursiveCharacterTextSplitter` divide cada doc | LangChain Text‑Splitters     | 405 chunks                      | `[INFO] Split into 405 chunks.`   |
| 4 | **Sentence‑Transformers** genera embeddings      | `all‑MiniLM‑L6-v2`           | matriz (n\_chunks × 384 floats) | `[INFO] Creating embeddings…`     |
| 5 | **ChromaDB** persiste la colección               | HNSW index + SQLite metadata | carpeta `src/chromadb/`         | `[SUCCESS] All chunks persisted.` |

---

## 3 · Detalle de tecnologías

| Capa             | Librería                               | Función clave                             | Notas                                                                |
| ---------------- | -------------------------------------- | ----------------------------------------- | -------------------------------------------------------------------- |
| **Cargador**     | `langchain_community.document_loaders` | `PyPDFLoader`                             | Extrae texto página ↦ `Document(page_content, metadata)`             |
| **Splitter**     | `langchain-text-splitters`             | `RecursiveCharacterTextSplitter`          | Breakpoint en frases y párrafos → chunks ≈ 1000 chars con solape 200 |
| **Embeddings**   | `sentence-transformers`                | `all-MiniLM-L6-v2` (384 dims, 61M params) | Ligero, open‑source, suficiente para pruebas locales                 |
| **Vector Store** | `chromadb` 0.4.15                      | `Chroma` + HNSW (M=16, ef=200)            | Persistencia en disco + API de similitud `query(k)`                  |
| **Logging**      | `loguru` + `rich`                      | `LoggerConfig` central                    | Color + rotación diaria en `logs/app.log`                            |

### Por qué LangChain

* **Modularidad** – separa loaders, splitters, embeddings y stores.
* **Future‑proof** – la misma abstracción permitirá añadir RAG y LLM chains en Sprint 2.

### Por qué ChromaDB

* **Persistencia local** simple (SQLite + parquet).
* **HNSW**: búsqueda vectorial O(log n) con recall alto.
* **Facilidad de actualización**: `collection.delete()` y re‑ingesta.

---

## 4 · Ejecución paso‑a‑paso

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
# → logs/      # traza completa
# → src/chromadb/   # colección persistente
```

> **Re‑ejecución rápida**: establece `RECREATE_CHROMA_DB=False` en `src/main.py` para cargar la BD sin regenerar embeddings.

---

## 5 · Carpetas relevantes

```
chatbot-emociones/
│
├── config.yaml                # rutas de PDFs + parámetros
├── data/pdfs/Marianela.pdf    # corpus base
│
├── src/
│   ├── main.py                # punto de entrada
│   ├── ingest/
│   │   ├── __init__.py
│   │   ├── dataloader.py      # lee config y PDF
│   │   ├── chunker.py         # splitter
│   │   └── chroma_db_manager.py# embeddings + Chroma
│   └── utils/logger_config.py # Loguru + Rich
│
└── logs/app.log               # bitácora rotativa
```

---

## 6 · Roadmap inmediato

1. **Dataset de pruebas**: CSV con chunk → etiqueta de emoción para medir *recall* de embeddings.
2. **Validación automática**: PyTest + fixtures que verifiquen nº de chunks, shape de embeddings y consultas de similitud.
3. **Integración LLM (Sprint 2)**: añadir un chain de LangChain que pase los chunks relevantes al LLM y devuelva clasificación + justificación.

---

© Equipo ADS Gpo‑10 (Gustavo A. Morales, Luis A. González, Ignacio J. Aguilar, Edwin D. Hernández) – Jun 2025

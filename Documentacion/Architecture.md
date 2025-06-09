# Chatbot-Emociones · Arquitectura General del Sistema

> **Proyecto:** Sistema de clasificación emocional de texto con LLM (Together AI)  
> **Sprint 1 – Foco exclusivo en ingesta** – Cargamos *Marianela.pdf*, lo fragmentamos, generamos *embeddings* y los almacenamos en ChromaDB. Futuras sprints integrarán UI y LLM.

## Equipo

| Alumno                          | Matrícula |
|---------------------------------|-----------|
| Gustavo Adolfo Morales García   | A00828432 |
| Luis Axel González Hernández    | A01795321 |
| Ignacio José Aguilar García     | A00819762 |
| Edwin David Hernández Alejandre | A01794692 |

---

## 1 · Visión General de la Arquitectura

El sistema *Chatbot-Emociones* está diseñado para clasificar emociones en texto mediante un pipeline de datos y un modelo de lenguaje, con una interfaz para interacción del usuario. La arquitectura se estructura en tres capas principales:

- **Modelo**: Un LLM (pendiente de integración con Together AI) procesará embeddings para clasificar emociones, apoyado en un vector store (ChromaDB).
- **Interfaz**: Una UI (por definir, posiblemente FastAPI + frontend web) permitirá ingresar texto y recibir clasificaciones.
- **Flujo de Datos**: Desde la carga de documentos hasta la interacción del usuario, pasando por procesamiento y almacenamiento vectorial.

---

## 2 · Pipeline de Ingesta (Sprint 1)

El flujo actual se centra en la ingesta de *Marianela.pdf*:

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
        S -->|chunks| EMB[SentenceTransformers ("all-MiniLM-L6-v2")]
        EMB -->|vectors| DB[(ChromaDB collection)]
    end

    %% Futuro RAG + UI
    subgraph RAG_UI [Futuro: RAG + Interfaz]
        DB --> Q[Query Engine] --> LLM[LLM (Together AI)]
        LLM --> UI[User Interface]
    end

    classDef ext fill:#fff,border:2px dashed #aaa
    classDef obj fill:#eef,border:#668
```
### 2.1 Flujo Paso a Paso
1. Carga de Configuración: config.yaml define rutas (e.g., data/pdfs/Marianela.pdf) y parámetros de chunking.
2. Carga de Documentos: DocumentLoader usa PyPDFLoader para convertir páginas en objetos LangChain Document.
3. Segmentación: DocumentChunker aplica RecursiveCharacterTextSplitter (chunk_size=1000, overlap=200) para generar fragmentos.
4. Generación de Embeddings: ChromaDBManager usa SentenceTransformers (all-MiniLM-L6-v2) para crear vectores de 384 dimensiones.
5. Almacenamiento: Los vectores se indexan en ChromaDB con HNSW (M=32, ef=200) para búsqueda semántica.
6. Futuro RAG: Un motor de consulta recuperará chunks relevantes para el LLM.
7. Interacción: La UI presentará clasificaciones emocionales (pendiente).
| # | Paso | Tecnología | Salida | Logs |
|---|---|---|---|---|
| 1 | DocumentLoader lee config.yaml | PyYAML | lista de rutas | [INFO] Loading configuration… |
| 2 | Carga con PyPDFLoader | LangChain Community | LangChain Document | [SUCCESS] Loaded 117 documents. |
| 3 | División con RecursiveCharacterTextSplitter | LangChain Text-Splitters | 405 chunks | [INFO] Split into 405 chunks. |
| 4 | Embeddings con SentenceTransformers | all-MiniLM-L6-v2 | matriz (405 × 384 floats) | [INFO] Creating embeddings… |
| 5 | Persistencia en ChromaDB | HNSW index + SQLite | carpeta src/chromadb/ | [SUCCESS] All chunks persisted. |
| 6 | Consulta RAG (futuro) | LangChain RAG | chunks relevantes | (pendiente) |
| 7 | Respuesta UI (futuro) | FastAPI + frontend | clasificación emocional | (pendiente) |

© Equipo ADS Gpo-10 (Gustavo A. Morales, Luis A. González, Ignacio J. Aguilar, Edwin D. Hernández) – Jun 2025
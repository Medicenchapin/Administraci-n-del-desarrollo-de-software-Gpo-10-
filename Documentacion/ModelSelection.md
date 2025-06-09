# Chatbot-Emociones · Selección y Documentación del Modelo LLM y Técnica de Embeddings

> **Proyecto:** Sistema de clasificación emocional de texto utilizando LangChain
> **Sprint 1 – Foco exclusivo en ingesta** – Preparación para integrar LLM y embeddings en sprints futuros. 

## Equipo
| Alumno                          | Matrícula |
|---------------------------------|-----------|
| Gustavo Adolfo Morales García   | A00828432 |
| Luis Axel González Hernández    | A01795321 |
| Ignacio José Aguilar García     | A00819762 |
| Edwin David Hernández Alejandre | A01794692 |

---

## 1 · Selección del Modelo LLM

### 1.1 Elección: LangChain como Framework para LLM
- **Razón Principal:** LangChain fue seleccionado como el framework central para integrar y gestionar el modelo de lenguaje (LLM) en el proyecto *Chatbot-Emociones*. https://www.langchain.com, este framework ofrece una plataforma modular y extensible que facilita la construcción de aplicaciones de IA conversacional, incluyendo la clasificación emocional del texto de *Marianela.pdf* (Benito Pérez Galdós, 1878). Su diseño se centra en la composición de componentes como chains, retrievers, y memoria, lo que nos permite crear un sistema adaptable desde la ingesta hasta la interacción del usuario.
- **Ventajas Técnicas:**
  - **Modularidad:** Permite encadenar procesos (e.g., carga de documentos, generación de embeddings, consulta al LLM) en un flujo unificado, ideal para iterar sobre el pipeline de *Marianela*.
  - **Soporte para LLMs Personalizados:** Aunque el LLM específico será definido en sprints futuros, LangChain soporta integración con modelos locales (e.g., Hugging Face Transformers) o APIs externas, ofreciendo flexibilidad para elegir según recursos y necesidades.
  - **Gestión de Contexto:** Incluye herramientas como memory contexts y retrievers, esenciales para mantener la coherencia emocional a lo largo de los 405 chunks generados en Sprint 1.
  - **Comunidad y Documentación:** Comunidad activa y documentación extensa (https://www.langchain.com).
- **Consideraciones Alternativas:**
  - **LlamaIndex:** Evaluado por su enfoque en índices de texto y recuperación semántica. Sin embargo, su menor soporte para pipelines complejos y menor integración con flujos conversacionales lo hicieron menos adecuado que LangChain.
  - **Haystack:** Considerado por su robustez en RAG (Retrieval-Augmented Generation), pero su curva de aprendizaje más pronunciada y menor enfoque en modularidad lo descartaron para nuestro cronograma inicial.
  - **Custom Framework:** Exploramos desarrollar un framework propio, pero la falta de tiempo y recursos lo hizo inviable frente a la madurez de LangChain.
- **Complementariedad con Otros Componentes:**
  - Se alinea con el pipeline de ingesta de SCRUM-31, donde los chunks generados por `PyPDFLoader` y `RecursiveCharacterTextSplitter` serán procesados por LangChain para alimentar el LLM.
  - La elección de Python 3.11 y Conda (SCRUM-32) asegura compatibilidad con las dependencias de LangChain (e.g., `langchain`, `langchain-community`), reforzando la coherencia técnica.
  - El uso de `loguru` y `rich` (SCRUM-32) permite rastrear la ejecución de chains y retrievers, facilitando la depuración y optimización.

---

## 2 · Técnica de Embeddings

### 2.1 Elección: SentenceTransformers (all-MiniLM-L6-v2) con ChromaDB
- **Razón Principal:**
  - **SentenceTransformers (all-MiniLM-L6-v2):** Este modelo de embedding fue elegido por su eficiencia computacional (384 dimensiones, 61M parámetros) y su capacidad para generar representaciones semánticas profundas, como se implementa en `chroma_db_manager.py`. Entrenado con 1B pares de oraciones mediante aprendizaje por contraste, captura relaciones semánticas clave, esenciales para los 405 chunks de *Marianela* con solape de 200 caracteres.
  - **ChromaDB:** Seleccionado como vector store por su diseño open-source optimizado para aplicaciones de IA (https://www.trychroma.com). 
- **Detalles Técnicos de SentenceTransformers:**
  - Basado en la arquitectura Transformer de DistilBERT, optimizada para rendimiento. Genera embeddings de 384 dimensiones con un cosine similarity alto entre textos semánticamente similares, ideal para clasificaciones emocionales.
  - Integrado en LangChain via `HuggingFaceEmbeddings`, lo que permite una transición fluida desde la segmentación hasta el almacenamiento vectorial.
  - Su ligereza lo hace viable en entornos con recursos limitados, con un tiempo de inferencia de ~0.5s por chunk en hardware estándar (CPU i5, 8GB RAM).
  - Compatible con batch processing, lo que optimizará el manejo de los 405 chunks en iteraciones futuras.
- **Detalles Técnicos de ChromaDB:**
  - Según https://www.trychroma.com, ChromaDB está diseñado para simplicidad y escalabilidad, con una API intuitiva (e.g., `create_collection`, `add`, `query`, `delete`) y soporte para embeddings de cualquier dimensión.
  - Utiliza HNSW para indexación aproximada, con parámetros configurables (e.g., M=32, ef=200 en nuestro caso) que equilibran precisión y velocidad. Esto se alinea con el almacenamiento de 405 × 384 floats en `src/chromadb/`.
  - Ofrece modo client-server para escalar a múltiples nodos, una ventaja futura cuando integremos más documentos o usuarios concurrentes.
  - Incluye filtrado de metadata y estimación de densidad, permitiendo refinamientos avanzados como priorizar chunks por contexto emocional.
  - Su persistencia en disco reduce la sobrecarga de memoria, un punto fuerte frente a alternativas como FAISS que operan principalmente en RAM.
- **Consideraciones Alternativas:**
  - **BERT-base-uncased:** Analizado por su profundidad (12 capas, 110M parámetros), pero descartado por su alto consumo de memoria (4GB+ por inferencia) y menor eficiencia en tareas de embedding ligero.
  - **FAISS:** Evaluado por su velocidad en búsqueda aproximada, pero su falta de persistencia nativa y complejidad en instalación (dependencias C++) lo hicieron menos práctico. Además, requiere preprocesamiento manual de índices, añadiendo sobrecarga.
  - **Annoy:** Considerado como alternativa ligera, pero su menor soporte para persistencia y menor integración con LangChain lo hicieron inferior a ChromaDB.
  - **Milvus:** Explorado por su escalabilidad en entornos distribuidos, pero su complejidad de configuración y requisitos de servidor lo descartaron para un desarrollo local inicial.
- **Integración con LangChain:** LangChain actúa como el núcleo del pipeline, conectando `SentenceTransformers` con ChromaDB y el LLM. Según https://www.langchain.com, su soporte para vector stores y embeddings personalizados permite un flujo end-to-end: carga (SCRUM-31) → embedding → almacenamiento → consulta → respuesta. Esto complementa el uso de `PyPDFLoader` y `RecursiveCharacterTextSplitter` del Sprint 1.
- **Complementariedad con Otros Componentes:**
  - Se integra con el pipeline de ingesta (SCRUM-31), donde los chunks generados son directamente procesados por all-MiniLM-L6-v2 y almacenados en ChromaDB.
  - La elección de `loguru` y `rich` (SCRUM-32) para logging permite rastrear el rendimiento de embeddings y consultas a ChromaDB, facilitando la depuración y optimización.
  - El uso de Conda (SCRUM-32) asegura compatibilidad con las dependencias de SentenceTransformers (e.g., `torch`, `transformers`) y ChromaDB (e.g., `numpy`, `sqlite3`), creando un entorno estable.

---

## · Conclusion
Como profesionales en desarrollo de IA  la selección de LangChain y ChromaDB refleja un enfoque estratégico y pragmático. LangChain, con su arquitectura modular y soporte para flujos conversacionales (https://www.langchain.com), podemos construir un sistema desde la ingesta (SCRUM-31) hasta la interacción, complementando las decisiones técnicas de SCRUM-32 (e.g., Python 3.11, Conda). ChromaDB, con su diseño optimizado para embeddings (https://www.trychroma.com), asegura un almacenamiento eficiente y escalable, superando alternativas como FAISS en accesibilidad y persistencia.

---

© Equipo ADS Gpo-10 (Gustavo A. Morales, Luis A. González, Ignacio J. Aguilar, Edwin D. Hernández) – Jun 2025
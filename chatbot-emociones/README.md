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

##  · Ejecución paso‑a‑paso

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

## Carpetas relevantes

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

© Equipo ADS Gpo‑10 (Gustavo A. Morales, Luis A. González, Ignacio J. Aguilar, Edwin D. Hernández) – Jun 2025

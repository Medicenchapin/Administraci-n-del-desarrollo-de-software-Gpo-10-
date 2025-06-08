# Chatbot‑Emociones

> **Proyecto:***
> Sistema de clasificación emocional de texto con LLM (Together AI)

## Equipo

| Alumno                          | Matrícula |
| ------------------------------- | --------- |
| Gustavo Adolfo Morales García   | A00828432 |
| Luis Axel González Hernández    | A01795321 |
| Ignacio José Aguilar García     | A00819762 |
| Edwin David Hernández Alejandre | A01794692 |

---

## ¿Qué hace este proyecto?

Chatbot‑Emociones es un prototipo académico que recibe texto en español, invoca un modelo de lenguaje de alto rendimiento hospedado en **Together AI** (modelo gratuito *EXAONE 3.5 32B Instruct*) y devuelve:

```json
{
  "label": "positive | negative | neutral",
  "explanation": "frase breve en español"
}
```

Se entrega una **UI en Streamlit** para pruebas manuales y un conjunto de **tests con PyTest** para asegurar que la lógica central no se rompa durante futuras iteraciones. En próximos sprints se añadirá recuperación semántica (embeddings + ChromaDB) y resumen automático.

---

## Arquitectura de carpetas

```text
chatbot-emociones/
│
├── app/                     # Capa de presentación (Streamlit)
│   └── main.py              # Página principal con formulario y resultados
│
├── src/                     # Lógica de negocio y servicios auxiliares
│   ├── __init__.py
│   ├── config.py            # Carga y validación de variables de entorno
│   ├── data/
│   │   └── preprocessing.py # (planificado para iteraciones futuras)
│   ├── services/
│   │   ├── __init__.py
│   │   └── llm_client.py    # Wrapper de la API de TogetherAI
│   ├── models/
│   │   ├── __init__.py
│   │   └── emotion_classifier.py # Orquestador de clasificación
│   └── utils/
│       ├── __init__.py
│       └── logger_config.py # Logging centralizado (planeado)
│
├── tests/                   # Pruebas unitarias
│   └── test_emotion_classifier.py
│
├── requirements.txt         # Dependencias Python
├── .env.example             # Plantilla de variables de entorno
└── README.md                # Este documento
```

---

## Guía rápida de instalación y prueba

> Requisitos previos: **Python ≥ 3.10** y **Git** instalados.

### 1 — Clonar el repositorio

```bash
git clone https://github.com/<tu‑org>/chatbot-emociones.git
cd chatbot-emociones
```

### 2 — Crear y activar entorno virtual

```bash
python3 -m venv .venv        # crear venv
source .venv/bin/activate    # activar (Windows: .venv\Scripts\activate)
```

### 3 — Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4 — Configurar variables de entorno

```bash
cp .env.example .env         # crea archivo local
# abre .env y pega tu clave gratuita de TogetherAI
# TOGETHERAI_API_KEY="xxxxxxxxxxxx"
```

| Variable             | Ejemplo                        | Descripción                      |
| -------------------- | ------------------------------ | -------------------------------- |
| `TOGETHERAI_API_KEY` | `together···abc`               | Clave desde dashboard TogetherAI |
| `MODEL_NAME`         | `lgai/exaone-3-5-32b-instruct` | Modelo gratuito recomendado      |
| `TEMPERATURE`        | `0.0`                          | Salida determinista              |

### 5 — Ejecutar pruebas unitarias

```bash
pytest -q          # debe mostrar ".. [100%] 2 passed"
```

### 6 — Probar interfaz Streamlit

```bash
streamlit run app/main.py
```

Visita [http://localhost:8501](http://localhost:8501), escribe un texto y pulsa **Analizar**.

---

## Cómo funciona internamente

1. `app/main.py` captura la entrada del usuario y la envía a `EmotionClassifier`.
2. `EmotionClassifier` llama a `ask_llm()` en `src/services/llm_client.py`.
3. `llm_client` construye el prompt y envía la petición a Together AI.
4. La respuesta se limpia (eliminando posibles bloques \`\`\`json) y se parsea a JSON.
5. Se validan la etiqueta y la explicación; cualquier error devuelve un resultado *neutral* seguro.

---


## Créditos

Trabajo desarrollado como parte de la asignatura *Administración del Desarrollo de Software* (Gpo 10).

* Gustavo A. Morales García — A00828432
* Luis Axel González Hernández — A01795321
* Ignacio José Aguilar García — A00819762
* Edwin David Hernández Alejandre — A01794692

# Chatbot‑Emociones

## Descripción general

**Chatbot‑Emociones** es un prototipo que utiliza modelos de lenguaje de gran tamaño (LLM) disponibles en TogetherAI para identificar la **emoción predominante** en un texto (positiva, negativa o neutral) y devolver una breve explicación en lenguaje natural. La interfaz está construida con **Streamlit** para ofrecer una experiencia web ligera y de rápido despliegue.

El proyecto está diseñado para evolucionar por etapas. En esta primera fase (MVP) se cubre la **clasificación de sentimientos**. Fases posteriores añadirán limpieza avanzada de datos, resúmenes de texto y visualizaciones interactivas.

---

## Estructura del repositorio

```
chatbot-emociones/
│
├── app/                     # Capa de presentación (Streamlit)
│   └── main.py              # Página principal con formulario de entrada y despliegue de resultados
│
├── src/                     # Lógica de negocio y servicios auxiliares
│   ├── __init__.py
│   ├── config.py            # Carga y validación de variables de entorno (pydantic.BaseSettings)
│   ├── data/
│   │   └── preprocessing.py # Funciones de limpieza y normalización (implementación futura)
│   ├── services/
│   │   ├── __init__.py
│   │   └── llm_client.py    # Wrapper de la API de TogetherAI con gestión de re‑intentos
│   ├── models/
│   │   ├── __init__.py
│   │   └── emotion_classifier.py # Orquestador que llama a llm_client y gestiona la respuesta
│   └── utils/
│       ├── __init__.py
│       └── logger_config.py # Configuración centralizada de logging (RotatingFileHandler)
│
├── tests/
│   └── test_emotion_classifier.py # Pruebas unitarias con pytest para la lógica de clasificación
│
├── requirements.txt         # Dependencias de Python (pip)
├── .env.example             # Plantilla de variables de entorno (TOGETHERAI_API_KEY, etc.)
└── README.md                # Documentación de uso
```

---

## Detalle de archivos clave

| Archivo                                | Función                                                                                     |
| -------------------------------------- | ------------------------------------------------------------------------------------------- |
| **app/main.py**                        | Renderiza la UI en Streamlit: recibe texto, invoca al clasificador y muestra el resultado.  |
| **src/config.py**                      | Encapsula parámetros de configuración: `TOGETHERAI_API_KEY`, `MODEL_NAME`, `TEMPERATURE`.   |
| **src/services/llm\_client.py**        | Implementa `ask_llm(text)`: prepara el prompt, invoca la API de TogetherAI y devuelve JSON. |
| **src/models/emotion\_classifier.py**  | Clase `EmotionClassifier` que valida la respuesta, controla errores y define etiquetas.     |
| **src/utils/logger\_config.py**        | Inicializa un logger único para todo el proyecto usando formato estructurado.               |
| **tests/test\_emotion\_classifier.py** | Pruebas unitarias básicas para etiquetas positivas y negativas con pytest.                  |

---

## Requisitos y dependencias

Las dependencias principales se listan en `requirements.txt`. Entre las más relevantes:

* `together`   – cliente oficial de TogetherAI.
* `streamlit`  – interfaz web rápida.
* `pydantic`   – validación de configuración.
* `pytest`     – ejecución de pruebas unitarias.

Para preparar un entorno mínimo:

```bash
python3 -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Configuración

1. Copie `.env.example` a `.env` y añada sus credenciales:

   ```ini
   TOGETHERAI_API_KEY="together...XYZ"
   MODEL_NAME="lgai/exaone-3-5-32b-instruct"
   TEMPERATURE=0.0
   ```
2. Asegúrese de que el archivo `.env` se encuentre en la raíz del proyecto.

---

## Ejecución local

```bash
streamlit run app/main.py
```

Abra el navegador en la URL que Streamlit indique (por defecto [http://localhost:8501](http://localhost:8501)). Ingrese un texto y presione **Analizar**.

---

## Pruebas

```bash
pytest -q
```

Estas pruebas verifican que el clasificador devuelve una etiqueta válida y una explicación. Se recomienda extenderlas con fixtures que simulen `ask_llm` para no consumir tokens en cada ejecución.

---

## Próximos pasos de desarrollo

* **Preprocesamiento avanzado** (`src/data/preprocessing.py`): manejo de emojis, normalización y spell‑check.
* **Persistencia**: almacenar historiales en SQLite o PostgreSQL.
* **Resúmenes de texto**: segundo módulo LLM (fase 2).
* **Visualización**: gráficos interactivos con Altair o Plotly.
* **CI/CD**: configurar GitHub Actions para ejecutar `pytest` y desplegar a Streamlit Cloud.

Con esta documentación, el proyecto cuenta con una base sólida y modular que facilita la colaboración y futuras iteraciones.

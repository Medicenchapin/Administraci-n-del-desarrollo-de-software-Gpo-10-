# Chatbot‑Emociones

## Descripción general

Chatbot‑Emociones es un prototipo que utiliza modelos de lenguaje de gran tamaño (LLM) para identificar la **emoción predominante** en un texto (positiva, negativa o neutral) y devolver una breve explicación en lenguaje natural. La aplicación está construida con **Streamlit** para ofrecer una interfaz web ligera y de rápido despliegue.

El proyecto está pensado para evolucionar por etapas; en esta primera fase se cubre la clasificación de sentimientos. Fases posteriores añadirán limpieza avanzada de datos, resúmenes de texto y visualizaciones.

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
│   │   └── preprocessing.py # Funciones de limpieza y normalización (se implementarán en la fase 2)
│   ├── services/
│   │   ├── __init__.py
│   │   └── llm_client.py    # Wrapper de la API (OpenAI u otra) con gestión de re‑intentos
│   ├── models/
│   │   ├── __init__.py
│   │   └── emotion_classifier.py # Orquestador que llama a llm_client y formatea la respuesta
│   └── utils/
│       ├── __init__.py
│       └── logger_config.py # Configuración centralizada de logging (RotatingFileHandler, JSON)
│
├── tests/
│   └── test_emotion_classifier.py # Pruebas unitarias con pytest para la lógica de clasificación
│
├── requirements.txt         # Dependencias de Python (pip)
├── .env.example             # Plantilla de variables de entorno (OPENAI_API_KEY, etc.)
└── README.md                # Este documento
```

### Detalle de archivos clave

| Archivo                                | Función                                                                                           | Comentarios adicionales                                               |
| -------------------------------------- | ------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **app/main.py**                        | Renderiza la UI en Streamlit; recibe texto, llama al clasificador y muestra resultados.           | Incluye spinner de progreso y manejo de errores básicos.              |
| **src/config.py**                      | Encapsula parámetros de configuración (modelo, temperatura, API key).                             | Permite sobrecarga mediante variables de entorno o archivo `.env`.    |
| **src/services/llm\_client.py**        | Implementa `ask_llm(text)`; prepara el prompt de sistema, invoca la API y devuelve JSON.          | Aísla cambios de proveedor o autenticación.                           |
| **src/models/emotion\_classifier.py**  | Clase `EmotionClassifier` que valida la respuesta, controla errores y define etiquetas aceptadas. | Punto de entrada para futuras estrategias (léxicos, modelos locales). |
| **src/utils/logger\_config.py**        | Inicializa un logger único para todo el proyecto usando formato estructurado.                     | Facilita trazabilidad en producción.                                  |
| **tests/test\_emotion\_classifier.py** | Pruebas unitarias básicas para etiquetas positivas y negativas.                                   | Ampliar con casos edge y pruebas de rendimiento.                      |

---

## Requisitos y dependencias

Las dependencias principales se listan en `requirements.txt`. Entre las más relevantes:

* `streamlit` – interfaz web rápida.
* `openai` – acceso al modelo GPT (puede sustituirse por `transformers` + modelo local).
* `pydantic` – validación de configuración.
* `pytest` – ejecución de pruebas unitarias.

Para un entorno mínimo:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Configuración

1. Copie `.env.example` a `.env` y añada su clave de API:

   ```env
   OPENAI_API_KEY="sk-..."
   ```
2. Ajuste parámetros opcionales (`MODEL_NAME`, `TEMPERATURE`) en `src/config.py` o vía variables de entorno.

---

## Ejecución local

```bash
streamlit run app/main.py
```

Abra el navegador en la URL que Streamlit indique (por defecto [http://localhost:8501](http://localhost:8501)). Introduzca un texto y presione **Analizar**.

---

## Pruebas

```bash
pytest -q
```

Las pruebas comprueban que el clasificador responde con etiquetas válidas. Se recomienda añadir fixtures simulados para no consumir tokens en cada corrida.

---

## Líneas de desarrollo futuras

* **Preprocesamiento avanzado** (`src/data/preprocessing.py`): normalización, manejo de emojis, spell‑check.
* **Persistencia**: almacenar historiales en SQLite/PostgreSQL.
* **Resúmenes de texto**: segundo módulo LLM (fase 2).
* **Visualización analítica**: dashboards con Altair o Plotly.
* **CI/CD**: flujo GitHub Actions que ejecute `pytest` y despliegue a Streamlit Cloud.

Con esta base, el repositorio proporciona una arquitectura clara y extensible que facilita la colaboración y el escalado del proyecto.

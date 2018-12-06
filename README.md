# Rasa Demo ComparaOnline

Esta demo requiere tener instalado conda, se recomienda instalar miniconda

## Instalar dependencias

Para instalar las dependencias usamos un ambiente nuevo en conda, basicamente se utilizan los siguientes paquetes: `rasa_nlu[spacy], `, pero se provee un archivo `requirements.txt` con las dependecias especificas usadas en la demo.

```
conda create -n rasa-demo python=3.6
source activate rasa-demo
pip install -r requirements.txt
```

Para descargar otro lenguaje para spacy, ya está presente en los requerimientos el idioma de la demo:
```
python -m spacy download en
```

Al momento de la demo había un bug con msgpack por lo que se debe utilizar una versión previa, si instalaste usando requirements.txt no necesitas hacer nada si no se puede forzar la versión con: `pip install msgpack==0.5.6`

## Rasa NLU

Para entrenar el modelo se debe ejecutar:

```
python -m rasa_nlu.train -c nlu_config.yml --data data/nlu.md -o models --fixed_model_name nlu --project rasa-demo-co --verbose
```

Para ejecutar el servidor http se debe ejecutar:

```
python -m rasa_nlu.server --path models --debug
```

Para testear usando curl, se debe especificar el proyecto y nombre del modelo:

```
curl -XPOST localhost:5000/parse -d '{"q":"hola","project":"rasa-demo-co", "model": "nlu"}'
curl -XPOST localhost:5000/parse -d '{"q":"cuanto cuesta un bitcoin","project":"rasa-demo-co", "model": "nlu"}'
curl -XPOST localhost:5000/parse -d '{"q":"cual es el precio del ether","project":"rasa-demo-co", "model": "nlu"}'
```

Respuesta

```
{
  "intent": {
    "name": "coin_value_search",
    "confidence": 0.9659252166748047
  },
  "entities": [
    {
      "start": 22,
      "end": 27,
      "value": "ether",
      "entity": "coin",
      "confidence": 0.9217739175348424,
      "extractor": "ner_crf"
    }
  ],
  "intent_ranking": [
    {
      "name": "coin_value_search",
      "confidence": 0.9659252166748047
    },
    {
      "name": "goodbye",
      "confidence": 0.12725260853767395
    },
    {
      "name": "thankyou",
      "confidence": 0.0
    },
    {
      "name": "greet",
      "confidence": 0.0
    }
  ],
  "text": "cual es el precio del ether",
  "project": "rasa-demo-co",
  "model": "nlu"
}
```

Para usar el modelo desde python se puede utilizar:
```
from rasa_nlu.model import Interpreter

interpreter = Interpreter.load('models/rasa-demo-co/nlu')
interpreter.parse(u"hello there")
```

## Rasa Core

Para entrenar el modelo se debe ejecutar:

```
python -m rasa_core.train -d domain.yml -s stories.md -o models/dialogue
```

Ejecutar el servidor de acciones:

```
python -m rasa_core_sdk.endpoint --actions actions
```

Despues de entrenar se puede ejecutar el servicio http para probar:

```
python -m rasa_core.run -d models/dialogue -u models/rasa-demo-co/nlu --port 5500 \
  --endpoints endpoints.yml \
  --credentials credentials.yml -vv
```

Abrir página de pruebas en el navegador

```
open static/index.html
```


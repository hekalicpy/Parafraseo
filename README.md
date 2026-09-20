# Parafraseador IA

Herramienta Python para reescribir textos en español manteniendo significado, orientación y datos.

## Uso

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py "La tecnología cambia la educación." 
```

Para usar un modelo remoto de Hugging Face:

```powershell
$env:HF_TOKEN = "tu_token"
python app.py "Texto original" --model "google/mt5-small"
```

Puedes añadir `--topic "tema" --show-context` para consultar el resumen de Wikipedia en español. Wikipedia se usa como contexto verificable, no como fuente para copiar contenido. El fallback local funciona sin credenciales.

## Criterios editoriales

La salida busca claridad, precisión, transiciones comprensibles, tono consistente y lenguaje natural. Debe revisarse por una persona, conservar atribuciones y citar las fuentes cuando corresponda. No se presenta como detector ni como garantía de que un texto sea "indetectable".

## Fuentes

- [MediaWiki REST API](https://www.mediawiki.org/wiki/API:REST_API)
- [Wikimedia REST API](https://www.mediawiki.org/wiki/Wikimedia_REST_API)
- [Hugging Face Inference Client](https://huggingface.co/docs/huggingface_hub/package_reference/inference_client)
- [Harvard Writing Center](https://writingcenter.fas.harvard.edu/)

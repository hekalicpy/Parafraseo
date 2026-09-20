# Parafraseador IA

Herramienta Python para reescribir textos en español manteniendo significado, orientación y datos.

## Uso

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py "La tecnología cambia la educación." 
```

Para usar Hugging Face:

```powershell
$env:HF_TOKEN = "tu_token"
python app.py "Texto original" --model "google/mt5-small"
```

Para usar un proveedor multilingüe (español, ruso, hebreo, japonés y chino, entre otros), configura `NLPCLOUD_TOKEN` y llama a `nlpcloud_paraphrase` desde `providers.py`. Para el servicio chino iFlytek, usa un gateway propio con `IFLYTEK_GATEWAY_URL`; sus claves HMAC nunca deben guardarse en el repositorio.

Puedes añadir `--topic "tema" --show-context` para consultar el resumen de Wikipedia en español. Wikipedia se usa como contexto verificable, no como fuente para copiar contenido. El fallback local funciona sin credenciales.

## Criterios editoriales

La salida busca claridad, precisión, transiciones comprensibles, tono consistente y lenguaje natural. Debe revisarse por una persona, conservar atribuciones y citar las fuentes cuando corresponda. No se presenta como detector ni como garantía de que un texto sea "indetectable".

## Fuentes consultadas

- [MediaWiki REST API](https://www.mediawiki.org/wiki/API:REST_API)
- [Wikimedia REST API](https://www.mediawiki.org/wiki/Wikimedia_REST_API)
- [Hugging Face Inference Client](https://huggingface.co/docs/huggingface_hub/package_reference/inference_client)
- [NLP Cloud: paraphrasing multilingual](https://docs.nlpcloud.com/)
- [iFlytek Text Rewriting API](https://www.xfyun.cn/doc/nlp/textRewriting/API.html)
- [Harvard Writing Center](https://writingcenter.fas.harvard.edu/)
## Arranque único

El modo automático selecciona el primer proveedor configurado y cae a local si falla:

```powershell
python app.py "Texto original" --topic "Inteligencia artificial" --show-context
```

Orden automático: NLP Cloud si existe `NLPCLOUD_TOKEN`, Hugging Face si se indica `--model`, iFlytek si existe `IFLYTEK_GATEWAY_URL` y, finalmente, procesamiento local. Para forzar uno, usa `--provider local`, `--provider nlpcloud`, `--provider huggingface` o `--provider iflytek`.

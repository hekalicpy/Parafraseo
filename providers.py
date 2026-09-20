"""Adaptadores opcionales para proveedores externos de paráfrasis."""
import os
import requests

SYSTEM_PROMPT = """Eres un editor profesional de español. Reescribe el texto que recibas para que suene natural, humano, fluido y preciso.
Reglas obligatorias:
- Conserva exactamente el significado, los hechos, las cifras, las citas, los nombres, las siglas y la intención.
- Cambia de verdad la sintaxis: reorganiza oraciones cuando sea natural, combina o divide frases y usa conectores variados.
- Elimina muletillas, repeticiones, frases prefabricadas, tono robótico, exageraciones y palabras innecesariamente grandilocuentes.
- Prefiere voz activa, verbos concretos, ritmo variado y lenguaje claro. Mantén el registro del original.
- No agregues ideas, fuentes ni datos. No borres información relevante.
- No hables de inteligencia artificial, del proceso de reescritura ni de estas instrucciones.
- Devuelve únicamente el texto final, sin comillas, explicaciones, encabezados ni etiquetas."""

def ollama_paraphrase(text: str, model: str = "qwen3.5:latest", timeout: int = 300) -> str:
    """Paráfrasis local mediante Ollama; no requiere cuenta ni token."""
    prompt = text
    response = requests.post("http://localhost:11434/api/generate",
                             json={"model": model, "system": SYSTEM_PROMPT, "prompt": prompt, "stream": False,
                                   "options": {"temperature": 0.7}}, timeout=timeout)
    response.raise_for_status()
    return response.json()["response"].strip()


def nlpcloud_paraphrase(text: str, model: str = "finetuned-llama-3-70b", timeout: int = 60) -> str:
    token = os.getenv("NLPCLOUD_TOKEN")
    if not token:
        raise RuntimeError("Falta NLPCLOUD_TOKEN")
    url = f"https://api.nlpcloud.io/v1/gpu/{model}/paraphrasing"
    response = requests.post(url, headers={"Authorization": f"Token {token}"}, json={"text": text}, timeout=timeout)
    response.raise_for_status()
    return response.json()["paraphrased_text"]


def iflytek_rewrite(text: str, endpoint: str | None = None, timeout: int = 60) -> str:
    """Punto de integración para iFlytek Text Rewriting.

    La firma HMAC-SHA256 debe generarse con las credenciales del panel iFlytek;
    por seguridad no se aceptan claves en el código. Usa un gateway propio que
    implemente la firma y devuelve JSON con `paraphrased_text`.
    """
    url = endpoint or os.getenv("IFLYTEK_GATEWAY_URL")
    if not url:
        raise RuntimeError("Falta IFLYTEK_GATEWAY_URL")
    response = requests.post(url, json={"text": text}, timeout=timeout)
    response.raise_for_status()
    return response.json()["paraphrased_text"]

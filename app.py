import os, re, argparse
from dataclasses import dataclass
from typing import Optional

import requests

WIKIMEDIA_BASE = "https://es.wikipedia.org/api/rest_v1"

@dataclass
class RewriteResult:
    text: str
    source: str
    context: Optional[str] = None


def wikipedia_context(topic: str, timeout: int = 10) -> Optional[str]:
    """Obtiene un resumen verificable de Wikipedia en español."""
    url = f"{WIKIMEDIA_BASE}/page/summary/{requests.utils.quote(topic, safe='')}"
    response = requests.get(url, headers={"User-Agent": "ParafraseadorIA/0.1 (local project)"}, timeout=timeout)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json().get("extract")


def hf_paraphrase(text: str, model: str, token: Optional[str] = None, timeout: int = 60) -> str:
    """Parafrasea mediante Hugging Face Inference API (token opcional según modelo/proveedor)."""
    from huggingface_hub import InferenceClient
    client = InferenceClient(model=model, token=token, timeout=timeout)
    prompt = (
        "Reescribe el siguiente texto en español con voz natural, clara y profesional. "
        "Conserva el significado, la orientación y los datos; no inventes información. "
        "Devuelve únicamente el texto reescrito:\n\n" + text
    )
    result = client.text_generation(prompt, max_new_tokens=700, temperature=0.65, do_sample=True)
    return result.strip()


def local_rewrite(text: str) -> str:
    """Fallback determinista: limpieza y mejoras conservadoras sin inventar contenido."""
    text = re.sub(r"\s+", " ", text.strip())
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"([.!?])([A-ZÁÉÍÓÚÑ])", r"\1 \2", text)
    replacements = {
        "debido a que": "porque",
        "con el fin de": "para",
        "en la actualidad": "hoy",
        "a nivel de": "en",
        "cabe destacar que": "",
    }
    for old, new in replacements.items():
        text = re.sub(rf"\b{old}\b", new, text, flags=re.IGNORECASE)
    return re.sub(r"\s{2,}", " ", text).strip()


def paraphrase(text: str, topic: Optional[str] = None, model: Optional[str] = None) -> RewriteResult:
    context = wikipedia_context(topic) if topic else None
    token = os.getenv("HF_TOKEN")
    if model:
        try:
            return RewriteResult(hf_paraphrase(text, model, token), "huggingface", context)
        except Exception as exc:
            if os.getenv("PARAFRASEADOR_STRICT") == "1":
                raise
            print(f"Aviso: no se pudo usar Hugging Face ({exc}); se aplica fallback local.")
    return RewriteResult(local_rewrite(text), "local", context)


def main() -> None:
    parser = argparse.ArgumentParser(description="Parafraseador profesional en español")
    parser.add_argument("text", nargs="?", help="Texto a reescribir; si se omite, se lee de stdin")
    parser.add_argument("--topic", help="Tema para enriquecer contexto con Wikipedia")
    parser.add_argument("--model", default=None, help="Modelo de Hugging Face, por ejemplo: google/mt5-small")
    parser.add_argument("--show-context", action="store_true")
    args = parser.parse_args()
    text = args.text or input("Texto: ")
    result = paraphrase(text, args.topic, args.model)
    print(result.text)
    if args.show_context and result.context:
        print("\\n[Contexto Wikipedia]\n" + result.context)


if __name__ == "__main__":
    main()

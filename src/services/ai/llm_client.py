import requests

from config.settings import settings

class LLMClient:
    def __init__(self):
        self.endpoint = settings.OLLAMA_ENDPOINT
        self.model_name = settings.LLM_MODEL_NAME

    def _parse_llm_response(self, payload: dict) -> str:
        if not isinstance(payload, dict):
            return "Não foi possível obter resposta do modelo."

        if "response" in payload:
            return payload["response"]

        results = payload.get("results") or payload.get("choices")
        if isinstance(results, list) and results:
            first = results[0]
            if isinstance(first, dict):
                return first.get("content") or first.get("text") or str(first)
            return str(first)

        if "output" in payload:
            output = payload["output"]
            if isinstance(output, str):
                return output
            return str(output)

        return "Não foi possível obter resposta do modelo."

    def _model_available(self) -> bool:
        try:
            response = requests.get(f"{self.endpoint}/v1/models", timeout=20)
            response.raise_for_status()
            payload = response.json()
            if isinstance(payload, list):
                return any(item == self.model_name or (isinstance(item, dict) and item.get("name") == self.model_name) for item in payload)
            if isinstance(payload, dict):
                models = payload.get("models") or payload.get("items") or []
                return any(item == self.model_name or (isinstance(item, dict) and item.get("name") == self.model_name) for item in models)
        except requests.RequestException:
            return False
        return False

    def generate_response(self, prompt: str) -> str:
        if not self._model_available():
            return (
                "Desculpe, o modelo de LLM não está disponível no servidor Ollama. "
                "Verifique se o modelo está instalado e o serviço Ollama está executando corretamente."
            )

        url = f"{self.endpoint}/v1/models/{self.model_name}/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            return self._parse_llm_response(response.json())
        except requests.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            response_text = e.response.text if e.response else str(e)
            print(f"[X] Erro ao chamar a LLM ({self.model_name}): {status_code} {response_text}")
            if status_code == 404:
                return (
                    "Desculpe, o modelo de LLM não está disponível. "
                    "Verifique se o modelo está instalado e o Ollama está configurado corretamente."
                )
            return "Desculpe, ocorreu um erro interno ao processar sua pergunta com a IA."
        except requests.RequestException as e:
            print(f"[X] Erro de conexão com a LLM ({self.model_name}): {str(e)}")
            return "Desculpe, não foi possível conectar ao servidor de LLM."
        except Exception as e:
            print(f"[X] Erro ao chamar a LLM ({self.model_name}): {str(e)}")
            return "Desculpe, ocorreu um erro interno ao processar sua pergunta com a IA."

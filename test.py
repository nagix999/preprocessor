import requests
import json
from pathlib import Path


path = Path("./data")
pdf_files = list(path.glob("*.*"))
files = [("files", open(file, "rb")) for file in pdf_files]


# files = [
#     ("files", open("./data/241203_제로트러스트_가이드라인_2.0.pdf", "rb")),
#     ("files", open("./data/thinkpython.pdf", "rb")),
# ]

# marker-options.txt 참고
config = {
    "workers": 1,
    "output_dir": "results",
    "output_format": "markdown",  # html/markdown/json
    "pagenate_output": True,
    "format_lines": False,
    "page_range": "3-4",  # 페이지 범위, None인 경우 전체 페이지 파싱
    "use_llm": True,  # parsing 간 LLM 사용 여부
    "llm_service": "marker.services.ollama.OllamaService",  # Ollama service 사용
    "ollama_base_url": "http://localhost:11434",  # Ollama host url
    "ollama_model": "gemma3:4b",  # Ollama Model
}


response = requests.post(
    "http://localhost:8000/documents/pipeline",
    files=files + [("config", (None, json.dumps(config), "application/json"))],
)

import os
import json
import logging
from typing import List
from tempfile import NamedTemporaryFile

from fastapi import FastAPI
from fastapi import UploadFile, File, Form
import uvicorn
import ollama
from preprocess.document_parser import parse
from preprocess.img2text import Image2Text
from preprocess.utils import get_stem_and_ext


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="preprocessor")


@app.get("/")
def root():
    return {"message": "ok"}


@app.post("/documents/pipeline")
async def pipeline(files: List[UploadFile] = File(...), config: str = Form(...)):
    try:
        config_dict = json.loads(config)

        for file in files:
            stem, suffix = get_stem_and_ext(file.filename)
            with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(await file.read())
                tmp_path = tmp.name

            # 문서 parsing
            filepath, images = parse(tmp_path, config_dict, stem)

            # parsing 후 이미지 존재하는 경우 image to text 실행
            if images:
                image_to_text = Image2Text(
                    ollama_client=ollama.Client(config_dict["ollama_base_url"]),
                    ollama_model=config_dict["ollama_model"],
                )

                results = {"filename": stem, "extention": suffix, "images": {}}

                for image in images:
                    caption, ocr = await image_to_text.run(filepath.parent / image)
                    results["images"][image] = {"caption": caption, "ocr": ocr}

                with open(filepath.parent / "images.json", "w") as json_file:
                    json.dump(results, json_file)

                logger.info("complete Image To Text")
        return {"message": "complete"}
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e
    finally:
        if tmp_path in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

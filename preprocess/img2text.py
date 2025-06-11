import logging
import ollama
import asyncio
from .utils import log_execution_time

OCR_PROMPT = """
You are a helpful assistant that can extract text from images.
You will be given an image and you need to extract the text from the image.
"""

CAPTION_PROMPT = """
You are a helpful assistant that can describe images.
You will be given an image and you need to describe the image.
Answer should be in Korean.
"""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Image2Text:
    def __init__(self, ollama_client, ollama_model):
        self.client = ollama_client
        self.model = ollama_model

    @log_execution_time(logger)
    async def _caption(self, image):
        logger.info(f"Captioning image: {image}")
        response = self.client.chat(
            model=self.model,
            messages=[
                {"role": "user", "content": CAPTION_PROMPT, "images": [image]},
            ],
        )
        return response.message.content

    @log_execution_time(logger)
    async def _ocr(self, image):
        logger.info(f"OCRing image: {image}")
        response = self.client.chat(
            model=self.model,
            messages=[
                {"role": "user", "content": OCR_PROMPT, "images": [image]},
            ],
        )
        return response.message.content

    async def run(self, image):
        caption, ocr = await asyncio.gather(self._caption(image), self._ocr(image))
        return caption, ocr


if __name__ == "__main__":
    image2text = Image2Text(
        ollama_client=ollama.Client(host="http://0.0.0.0:11434"),
        ollama_model="gemma3:4b",
    )
    image = "../results/241203_제로트러스트_가이드라인_2.0/_page_1_Picture_4.jpeg"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(image2text.run(image))
    loop.close()

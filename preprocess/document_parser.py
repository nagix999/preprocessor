from pathlib import Path
import logging

from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
from marker.config.parser import ConfigParser
from .utils import get_stem_and_ext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_converter(config):
    config_parser = ConfigParser(config)
    converter = PdfConverter(
        config=config_parser.generate_config_dict(),
        artifact_dict=create_model_dict(),
        processor_list=config_parser.get_processors(),
        renderer=config_parser.get_renderer(),
        llm_service=config_parser.get_llm_service(),
    )
    return converter


def get_output_filename(filepath, config, filename=None):
    filepath = Path(filepath)
    if filename is None:
        stem, _ = get_stem_and_ext(filepath)
    else:
        stem = filename

    output_dir = Path(config["output_dir"]) / stem
    output_dir.mkdir(parents=True, exist_ok=True)

    output_format = config["output_format"]

    if output_format == "markdown":
        output_format = "md"

    output_filename = output_dir / f"{stem}.{output_format}"

    return output_filename


def parse(filepath, config, filename=None):
    output_filename = get_output_filename(filepath, config, filename)
    logger.info(f"saved to {output_filename}")

    converter = load_converter(config)
    rendered = converter(str(filepath))
    text, _, images = text_from_rendered(rendered)

    with open(output_filename, "w") as f:
        f.write(text)

    logger.info(f"parsing complete - {output_filename}")

    for image_name, image in images.items():
        image.save(output_filename.parent / image_name)

    logger.info(f"Saved {len(images)} images")
    return output_filename, list(images.keys())


if __name__ == "__main__":
    config = {
        "output_dir": "./results",
        "output_format": "html",
        "page_range": "1-2",
    }
    parse(
        filepath="/home/nagix/projects/shieldus/data/241203_제로트러스트_가이드라인_2.0.pdf",
        config=config,
    )

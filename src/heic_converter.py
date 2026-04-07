import logging 
from pathlib import Path
import click 
from PIL import Image
from pillow_heif import register_heif_opener

logger = logging.getLogger(__name__)

def convert_heic_to_pdf(input_path: Path, output_path: Path) -> None:
    # Code sample from Gemini 
    register_heif_opener()
    
    # Open the HEIC image
    image = Image.open(input_path)

    # Convert to RGB (required for PDF saving)
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Save as PDF
    image.save(output_path, "PDF", resolution=100.0)


@click.command()
@click.option("--heic_directory_path", prompt="Path with HEIC files", type=Path)
@click.option("--output_directory_path", type=Path, default=Path("output"))
def convert_directory(heic_directory_path: Path, output_directory_path: Path):
    for f in heic_directory_path.iterdir():
        if f.is_file():
            if f.suffix.upper() == ".HEIC":

                convert_heic_to_pdf(
                    input_path=f, 
                    output_path=output_directory_path.joinpath(f"{f.stem}.pdf")
                )
            else:
                logger.warning("Discovered a none HEIC file: %s", f)
        else: 
            logger.debug("passing over nested directory: %s", f)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG, 
        format="%(asctime)s - %(levelname)s - %(module)s: %(message)s"
    )

    convert_directory()
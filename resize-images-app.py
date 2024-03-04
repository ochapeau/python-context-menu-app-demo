import argparse
import logging
import mimetypes
import sys
from pathlib import Path

from PIL import Image, UnidentifiedImageError


def setup_logging():
    """Configure the logger."""

    # Getting the operating system
    os_name = sys.platform

    # Defining the application name
    application_name = "ResizeImagesContextMenu"
    # Defining the log file name
    log_file_name = "main.log"

    if os_name == "win32":
        log_path = (
            Path.home()
            / "AppData"
            / "Local"
            / application_name
            / "Logs"
            / log_file_name
        )
    elif os_name == "darwin":  # macOS's system name from platform module
        log_path = Path.home() / "Library" / "Logs" / application_name / log_file_name
    else:  # Assuming Linux/Unix
        log_path = Path("/var") / "log" / application_name / log_file_name

    # Creating the directory if it does not exist
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        filename=str(log_path),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def resize_image(image_path, resize_factor):
    """Resize an image given a resize factor."""
    try:
        img = Image.open(image_path)
        width, height = img.size
        resized_img = img.resize(
            (int(width * resize_factor), int(height * resize_factor))
        )
        resized_name = (
            image_path.parent / f"{image_path.stem}_resized{image_path.suffix}"
        )
        resized_img.save(resized_name, quality=95)  # Adjust quality as needed
        logging.info(f"Resized image saved: {resized_name}")
    except UnidentifiedImageError:
        logging.error(f"Failed to identify image: {image_path}")
    except Exception as e:
        logging.error(f"Error processing {image_path}: {e}")


def is_image(file_path):
    """Verify if a given file is an image using the MIME type."""
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type and mime_type.split("/")[0] == "image":
        return True
    return False


def verify_resized_image(resized_name, expected_dimensions):
    """Check if the resized image exists and has the expected dimensions."""
    try:
        with Image.open(resized_name) as img:
            return img.size == expected_dimensions
    except IOError:
        return False


def calculate_expected_dimensions(original_path, resize_factor):
    """Calculate expected dimensions of the resized image."""
    with Image.open(original_path) as img:
        return tuple(int(dim * resize_factor) for dim in img.size)


def should_process_image(original_path, resized_name, resize_factor):
    """Determine if the image needs to be processed."""
    if resized_name.exists():
        expected_dimensions = calculate_expected_dimensions(
            original_path, resize_factor
        )
        if verify_resized_image(resized_name, expected_dimensions):
            logging.info(
                f"Resized image already exists and matches expected dimensions: {resized_name}, skipping"
            )
            return False
        else:
            logging.warning(
                f"Existing file {resized_name} does not match expected dimensions, resizing again"
            )
    return True


def process_image(original_path, resize_factor):
    """Process an individual image, resizing it if necessary."""
    resized_name = (
        original_path.parent / f"{original_path.stem}_resized{original_path.suffix}"
    )

    if should_process_image(original_path, resized_name, resize_factor):
        logging.info(f"Processing image: {original_path}")
        if is_image(original_path):
            resize_image(original_path, resize_factor)
        else:
            logging.info(f"Skipping non-image file: {original_path}")


def process_files(file_paths, resize_factor):
    for file_path in file_paths:
        if not file_path.is_file():
            logging.warning(f"Path is not a file: {file_path}")
            continue

        logging.info(f"Processing file: {file_path}")

        if is_image(file_path):
            process_image(file_path, resize_factor)
        else:
            logging.info(f"Skipping non-image file: {file_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Resize images to a specified factor of their original size."
    )
    parser.add_argument("files", nargs="+", help="File paths of the images to resize")
    parser.add_argument(
        "-f", "--factor", type=float, default=0.5, help="Resize factor (default: 0.5)"
    )
    args = parser.parse_args()

    setup_logging()

    file_paths = [Path(file) for file in args.files]
    process_files(file_paths, args.factor)


if __name__ == "__main__":
    main()

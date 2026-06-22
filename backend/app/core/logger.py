import logging
from rich.logging import RichHandler

def setup_logger():
    # Configure the standard Python logging to use RichHandler
    logging.basicConfig(
        level="INFO", # Change to DEBUG if you want more verbose logs
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                rich_tracebacks=True, # Makes tracebacks beautiful
                markup=True,          # Allows you to use [green] tags in logs
                show_path=False       # Hides the file path column to save space (optional)
            )
        ]
    )

    # Create and return a named logger for your application
    return logging.getLogger("my_fastapi_app")

# Initialize it once so we can import this specific instance anywhere
log = setup_logger()
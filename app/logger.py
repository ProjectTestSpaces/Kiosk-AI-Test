import logging

# Configure logging
logging.basicConfig(
    filename="admin_panel.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("admin_panel_logger")

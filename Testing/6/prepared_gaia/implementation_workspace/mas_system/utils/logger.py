import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mas_system.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def log_agent_action(agent_name, action, details=None):
    message = f"{agent_name}: {action}"
    if details:
        message += f" - Details: {details}"
    logger.info(message)


def log_system_event(event, details=None):
    message = f"SYSTEM EVENT: {event}"
    if details:
        message += f" - Details: {details}"
    logger.info(message)
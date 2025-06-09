import logging
import os

os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/casino.log", filemode="a",level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
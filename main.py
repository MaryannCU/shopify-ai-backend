from fastapi import FastAPI
import logging

# -------------------------
# Logging setup
# -------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------
# App
# -------------------------
app = FastAPI()

@app.get("/health")
def health_check():
    logger.info("Health check endpoint was called")
    return {"status": "ok"}

@app.post("/recommend")
def recommend():
    logger.info("Received recommendation request")
    return {
        "season": "Soft Autumn",
        "body_type": "Rectangle",
        "recommended_products": ["SKU123", "SKU456"]
    }

# from fastapi import FastAPI, UploadFile, File
# import logging
# import boto3
# from botocore.exceptions import ClientError
# import uuid

# # -------------------------
# # Logging setup
# # -------------------------
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # -------------------------
# # AWS S3 Setup
# # -------------------------
# s3 = boto3.client("s3")
# BUCKET_NAME = "shopify-ai-selfies"

# def upload_selfie(file_name, object_name):
#     try:
#         s3.upload_file(file_name, BUCKET_NAME, object_name)
#         url = s3.generate_presigned_url(
#             'get_object',
#             Params={'Bucket': BUCKET_NAME, 'Key': object_name},
#             ExpiresIn=3600  # 1 hour
#         )
#         return url
#     except ClientError as e:
#         logger.error(f"S3 upload failed: {e}")
#         return None

# # -------------------------
# # FastAPI App
# # -------------------------
# app = FastAPI()

# @app.get("/health")
# def health_check():
#     logger.info("Health check endpoint was called")
#     return {"status": "ok"}

# @app.post("/recommend")
# def recommend():
#     logger.info("Received recommendation request")
#     return {
#         "season": "Soft Autumn",
#         "body_type": "Rectangle",
#         "recommended_products": ["SKU123", "SKU456"]
#     }

# @app.post("/upload-selfie")
# async def upload_selfie_endpoint(file: UploadFile = File(...)):
#     logger.info(f"Received selfie upload request: {file.filename}")
#     temp_file_name = f"/tmp/{uuid.uuid4()}_{file.filename}"
    
#     with open(temp_file_name, "wb") as buffer:
#         buffer.write(await file.read())
    
#     object_name = f"selfies/{uuid.uuid4()}_{file.filename}"
#     url = upload_selfie(temp_file_name, object_name)
    
#     if url:
#         logger.info(f"Selfie uploaded successfully: {url}")
#         return {"url": url}
#     else:
#         logger.error("Failed to upload selfie")
#         return {"error": "Failed to upload selfie"}, 500
    
    
from fastapi import FastAPI, UploadFile, File, HTTPException
import logging
import boto3
from botocore.exceptions import ClientError
import uuid

# -------------------------
# Logging setup
# -------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------
# AWS S3 setup
# -------------------------
BUCKET_NAME = "shopify-ai-selfies"
s3 = boto3.client("s3")  # 👈 NO KEYS HERE (ECS ROLE WILL HANDLE IT)

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

# -------------------------
# Upload Selfie Endpoint
# -------------------------
@app.post("/upload-selfie")
async def upload_selfie(file: UploadFile = File(...)):
    try:
        # Generate unique filename
        object_name = f"selfies/{uuid.uuid4()}-{file.filename}"

        # Upload to S3
        s3.upload_fileobj(
            file.file,
            BUCKET_NAME,
            object_name,
            ExtraArgs={"ContentType": file.content_type}
        )

        # Generate signed URL
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": object_name},
            ExpiresIn=3600
        )

        return {
            "message": "Upload successful",
            "s3_key": object_name,
            "signed_url": url
        }

    except ClientError as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="S3 upload failed")

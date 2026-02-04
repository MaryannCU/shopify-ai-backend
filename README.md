Shopify AI Selfie Backend (FastAPI + AWS)

Production-ready backend for uploading user selfies, running AI-style inference, and storing results using AWS managed services.

📌 Project Overview

This project is a FastAPI backend deployed on AWS ECS Fargate.
It allows users to upload selfies, stores them securely in Amazon S3, runs a mock AI inference and saves metadata and results in Amazon DynamoDB.
The service is exposed via a custom HTTPS domain and monitored using Amazon CloudWatch.

🏗️ Architecture

Flow:

Client uploads selfie via API

FastAPI service receives request

Image uploaded to Amazon S3

Mock AI inference runs

Metadata & results saved to DynamoDB

Logs & metrics sent to CloudWatch

AWS Services Used:

ECS Fargate

Application Load Balancer

Amazon S3

Amazon DynamoDB

Amazon CloudWatch

IAM Roles

Route 53 + ACM (HTTPS)

🚀 Tech Stack

Backend: FastAPI (Python)

Containerization: Docker

Compute: AWS ECS Fargate

Storage: Amazon S3

Database: Amazon DynamoDB

Monitoring: Amazon CloudWatch

Security: IAM Roles (no hardcoded secrets)

Domain: HTTPS via ALB + ACM

🔐 Authentication & Security

No AWS credentials are hardcoded

ECS Task Role provides:

S3 access

DynamoDB access

HTTPS enforced using ACM certificate

IAM least-privilege permissions applied

📂 API Endpoints
Health Check
GET /health


Response

{ "status": "ok" }

Upload Selfie & Run Inference
POST /upload-selfie


Request

multipart/form-data

Field: file (image)

Response

{
  "request_id": "uuid",
  "message": "Upload & inference successful",
  "result": {
    "season": "Soft Autumn",
    "body_type": "Rectangle",
    "confidence": 0.87
  }
}

🐳 Docker Setup
Build Image
docker build -t shopify-ai-backend .

Run Locally
docker run -p 8000:8000 shopify-ai-backend

☁️ Deployment (ECS Fargate)

Build Docker image

Push image to Amazon ECR

Create ECS Task Definition

Create ECS Cluster (Fargate)

Create Service with Application Load Balancer

Assign IAM Task Role

Attach custom domain via Route 53

Enable HTTPS with ACM

Update service on new task revisions

📊 Monitoring & Observability (CloudWatch)
Logs

ECS container logs streamed to:

/ecs/shopify-ai-backend


Includes:

App startup logs

API requests

Upload activity

Errors

Metrics

CPU Utilization

Memory Utilization

Alarms

CPU alarm (>70%)

Memory alarm (>75%)

🧪 Testing
Local Test
curl -X POST "http://localhost:8000/upload-selfie" \
  -F "file=@image.jpg"

Production Test
curl -X POST "https://api.maryannsluxe.online/upload-selfie" \
  -F "file=@image.jpg"

📁 Data Storage
S3

Bucket: shopify-ai-selfies

Path: selfies/<uuid>-filename

DynamoDB

Table: shopify-ai-inference

Stores:

request_id

s3_key

image_url

inference result

status

timestamp

🧠 Future Improvements

Replace mock inference with real ML model

Add async processing with SQS

Add authentication (JWT / Cognito)

Add CI/CD pipeline

Add tracing with AWS X-Ray

👩🏽‍💻 Author

Maryann Chimuanya Unachukwu
Cloud / DevOps Engineer


⭐ Why This Project Matters

This project demonstrates:

Real-world cloud deployment

Secure AWS architecture

Production monitoring

API design

Container orchestration

DevOps best practices

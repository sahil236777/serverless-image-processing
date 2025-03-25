## 1. Project Description

### 1.1 Project
**Serverless Image Processing Application**

### 1.2 Description
This project implements a fully serverless cloud-native image processing solution using AWS. The application allows users to upload images via a REST API. Once uploaded, the images are automatically processed using AWS Lambda (resized, converted to grayscale, and watermarked), then stored securely in an S3 bucket. Metadata such as upload timestamps and processing status is stored in DynamoDB. The system is designed with scalability, security, and monitoring in mind, leveraging key AWS services and best practices for cloud architecture.

## 2. Overview

### 2.1 Purpose
The purpose of this project is to create an automated, serverless image processing pipeline that enables users to upload images and receive optimized versions without managing any backend infrastructure. It is aimed at developers and users who require scalable, secure, and efficient handling of image uploads and transformations.

### 2.2 Scope
This project covers:
- Development of an API using AWS API Gateway for image uploads.
- Image processing using AWS Lambda (resize, grayscale, watermark).
- Storing processed images in Amazon S3.
- Logging metadata in DynamoDB.
- Monitoring via AWS CloudWatch.
Optional enhancements include authentication via AWS Cognito and accelerated delivery via CloudFront.

### 2.3 Requirements

#### 2.3.1 Functional Requirements
- Users can upload images through an API.
- Uploaded images are processed automatically (resize, grayscale, watermark).
- Processed images are saved to S3.
- Metadata (filename, status, timestamp) is logged in DynamoDB.
- Images and metadata can be retrieved via API.

#### 2.3.2 Non-Functional Requirements
- **Scalability:** The system shall auto-scale via serverless infrastructure.
- **Availability:** 99.9% uptime with AWS-managed services.
- **Monitoring:** All system activity shall be logged in CloudWatch.

#### 2.3.3 Technical Requirements
- AWS Lambda with Python (Pillow library)
- AWS API Gateway, S3, DynamoDB, IAM
- AWS SDKs and boto3 for service integration

#### 2.3.4 Security Requirements
- S3 buckets are private and access-controlled.
- API endpoints are secured via IAM or Cognito (optional).
- Lambda runs in a VPC with least-privilege IAM roles.
- All data encrypted in transit and at rest.

#### 2.3.5 Estimates

| #  | Description                                      | Hrs. Est. |
|----|--------------------------------------------------|-----------|
| 1  | Lambda image processor (Python)                  | 4         |
| 2  | S3 + API Gateway setup                           | 3         |
| 3  | DynamoDB logging + schema config                 | 2         |
| 4  | CloudWatch logging & testing                     | 1.5       |
| 5  | README and documentation                         | 2         |
|    | **TOTAL**                                        | **12.5**  |

#### 2.3.6 Traceability Matrix

| SRS Requirement | SDD Module                        |
|-----------------|-----------------------------------|
| Req 1           | Lambda image_processor.py         |
| Req 2           | API Gateway + Lambda Integration  |
| Req 3           | DynamoDB Table Logging            |
| Req 4           | S3 Processed Image Storage        |


## 3. System Architecture

### 3.1 Overview
The system is designed using a fully serverless architecture. Users upload images via an API Gateway endpoint. The image is passed to an AWS Lambda function, which processes the image (resize, grayscale, watermark). Processed images are saved to an Amazon S3 bucket, while metadata (e.g., filename, timestamp, status) is stored in a DynamoDB table. CloudWatch tracks logs, performance, and anomalies.

### 3.2 Architectural Components

- **API Gateway** – Receives HTTP requests for image upload and routes to Lambda.
- **Lambda Function** – Handles image processing using the Pillow library in Python.
- **S3** – Stores both original and processed images securely.
- **DynamoDB** – Logs metadata like image name, upload time, and status.
- **CloudWatch** – Monitors system performance and execution logs.

### 3.3 Architectural Diagram

![architeture diagram](https://github.com/user-attachments/assets/b9982e47-3a2f-4590-b9d0-e57c63e667ed)


## 4. Data Dictionary

This section outlines the schema of the primary DynamoDB table used to store metadata for each processed image.

| Table     | Field Name | Notes                                 | Type     |
|-----------|------------|----------------------------------------|----------|
| Images    | ID         | Unique identifier (UUID or timestamp) | STRING   |
|           | Filename   | Name of the original uploaded image    | STRING   |
|           | Status     | Processing status (e.g., "processed") | STRING   |
|           | Timestamp  | Time of upload or processing           | DATETIME |
|           | S3Path     | Full S3 URI to the processed image     | STRING   |
|           | Size       | Image size in bytes (after processing) | NUMBER   |
|           | Format     | Output format (e.g., JPEG, PNG)        | STRING   |

- **ID** will serve as the primary key (partition key).
- Additional attributes can be indexed or queried as needed.

## 5. Data Design

### 5.1 Persistent/Static Data

The system stores image metadata in a DynamoDB table, while actual image files are stored in S3. The logical relationship is one-to-one: each image record in DynamoDB corresponds to a single processed image in S3.

### 5.1.1 Dataset Design

**Entity: Image**

| Attribute   | Description                                 |
|-------------|---------------------------------------------|
| ID          | Unique identifier for the image             |
| Filename    | Original name of the uploaded file          |
| Timestamp   | Time of upload or processing                |
| Status      | Current status (e.g., "processed")          |
| S3Path      | URI to the image in S3                      |
| Size        | Size in bytes                               |
| Format      | Format of the processed image (e.g., PNG)   |

#### Entity Relationship (ERD Summary):

![ERD Summary](https://github.com/user-attachments/assets/0be8f689-a98b-4036-ad23-6d88884e1ca0)

- **Primary Key:** ID
- **No secondary indexes** are used in the base implementation but can be added for optimization (e.g., query by filename or timestamp).

## 6. User Interface Design

### 6.1 User Interface Design Overview

This project is backend-focused and primarily designed to be accessed via HTTP APIs. A basic user interface (UI) may be implemented later for demonstration or testing purposes, such as a simple web form to upload images.

For now, users interact with the system using tools like Postman or `curl` to make POST requests to the API Gateway endpoint.

If time allows, a minimal web frontend using HTML and JavaScript can be built to:
- Select and upload image files
- Display upload status and processed image preview
- Show basic metadata from DynamoDB (e.g., filename, timestamp)

### 6.2 User Interface Navigation Flow

![User Interface Navigation Flow](https://github.com/user-attachments/assets/5ab612a6-6389-4f31-b5d2-f0b79f986f81)


### 6.3 Use Cases / User Function Description

#### Use Case: Upload Image
- **Actor:** User
- **Action:** Upload image via UI or API
- **System Response:** Image is processed by Lambda and stored in S3; metadata saved in DynamoDB

#### Use Case: View Processed Image (future)
- **Actor:** User
- **Action:** Request image via API
- **System Response:** Return image from S3 and metadata from DynamoDB

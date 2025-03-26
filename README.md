## 1. Project Description

### 1.1 Project
**Serverless Image Processing Application**

### 1.2 Description
This project implements a fully serverless cloud-native image processing solution using AWS. The application allows users to upload images via a REST API. Once uploaded, the images are automatically processed using AWS Lambda (resized, and converted to grayscale), then stored securely in an S3 bucket. Metadata such as upload timestamps and processing status is stored in DynamoDB. The system is designed with scalability, security, and monitoring in mind, leveraging key AWS services and best practices for cloud architecture.

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
- Uploaded images are processed automatically (resize, grayscale).
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

| #    | Description                      | Hrs. Est. |
| ---- | -------------------------------- | --------- |
| 1    | Lambda image processor (Python)  | 4         |
| 2    | S3 + API Gateway setup           | 3         |
| 3    | DynamoDB logging + schema config | 2         |
| 4    | CloudWatch logging & testing     | 1.5       |
| 5    | README and documentation         | 2         |
|      | **TOTAL**                        | **12.5**  |

#### 2.3.6 Traceability Matrix

| SRS Requirement | SDD Module                       |
| --------------- | -------------------------------- |
| Req 1           | Lambda image_processor.py        |
| Req 2           | API Gateway + Lambda Integration |
| Req 3           | DynamoDB Table Logging           |
| Req 4           | S3 Processed Image Storage       |


## 3. System Architecture

### 3.1 Overview
The system is designed using a fully serverless architecture. Users upload images via an API Gateway endpoint. The image is passed to an AWS Lambda function, which processes the image (resize, grayscale). Processed images are saved to an Amazon S3 bucket, while metadata (e.g., filename, timestamp, status) is stored in a DynamoDB table. CloudWatch tracks logs, performance, and anomalies.
Specifically, the architecture is based on the following workflow:

1. **Input**: The user converts an image to base64 using the command below and submits it to the API endpoint:

   ```bash
   base64 -w 0 input-1-lake-view.jpg > input-1-lake-view-encoded.txt
   ```

   The image selected for this demonstration is the lake-view image retrieved from unsplash shown below.

   ![input-1-lake-view](https://github.com/user-attachments/assets/bc0a7256-4378-4f74-b6fe-21663df121a2)


2. **API Gateway**: Receives POST requests containing base64-encoded image content.

3. **Lambda Function**: Decodes and processes the image (resize + grayscale using Pillow) and saves it as a PNG to an S3 bucket.

4. **S3**: Receives the processed image under the `processed/` folder.

5. **DynamoDB**: Logs metadata such as ID, filename, timestamp, status, image size, and format.

6. **CloudWatch**: Logs success and error events for traceability.

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

| Table  | Field Name | Notes                                  | Type     |
| ------ | ---------- | -------------------------------------- | -------- |
| Images | ID         | Unique identifier (UUID or timestamp)  | STRING   |
|        | Filename   | Name of the original uploaded image    | STRING   |
|        | Status     | Processing status (e.g., "processed")  | STRING   |
|        | Timestamp  | Time of upload or processing           | DATETIME |
|        | S3Path     | Full S3 URI to the processed image     | STRING   |
|        | Size       | Image size in bytes (after processing) | NUMBER   |
|        | Format     | Output format (e.g., JPEG, PNG)        | STRING   |

- **ID** will serve as the primary key (partition key).
- Additional attributes can be indexed or queried as needed.

## 5. Data Design

### 5.1 Persistent/Static Data

The system stores image metadata in a DynamoDB table, while actual image files are stored in S3. The logical relationship is one-to-one: each image record in DynamoDB corresponds to a single processed image in S3.

### 5.1.1 Dataset Design

**Entity: Image**

| Attribute | Description                               |
| --------- | ----------------------------------------- |
| ID        | Unique identifier for the image           |
| Filename  | Original name of the uploaded file        |
| Timestamp | Time of upload or processing              |
| Status    | Current status (e.g., "processed")        |
| S3Path    | URI to the image in S3                    |
| Size      | Size in bytes                             |
| Format    | Format of the processed image (e.g., PNG) |

#### Entity Relationship (ERD Summary):

![ERD Summary](https://github.com/user-attachments/assets/0be8f689-a98b-4036-ad23-6d88884e1ca0)

- **Primary Key:** ID
- **No secondary indexes** are used in the base implementation but can be added for optimization (e.g., query by filename or timestamp).

## 6. User Interface Design

### 6.1 User Interface Design Overview

- ### 6.1 Interaction Using Postman

  ![User Interface Navigation Flow](https://github.com/user-attachments/assets/5e6a3450-61c5-43a2-ac9c-d8d9536fdc1f)

  Users interact with the API using Postman. The steps to configure Postman are:

  1. **Open Postman** and select the HTTP method as `POST`.
  2. **Set the endpoint URL** pointing to your deployed API Gateway endpoint.
     The endpoint is: **`https://mj045ps15a.execute-api.us-west-2.amazonaws.com/default/imageProcessor`**
  4. **Set Headers**:
     - Key: `Content-Type`, Value: `text/plain`
        ![step-1-disable-the default-content-type-and-add-a-new-type-of-text-plain](https://github.com/user-attachments/assets/9f1a666e-dea9-45bf-a06d-4a8426655492)
  5. **Select Body tab**, choose `raw`, and paste the base64 content of the image.
     ![step-2-select-body-then-raw-and-change-the blue-part-next-to-graphql-to-text-and-paste-the-base64-image-content-therein](https://github.com/user-attachments/assets/a6d54a03-e15e-445c-9a0a-e0d1abb5d087)
  6. **Send Request**. A successful response returns HTTP 200 and a message containing the processed file path.
      ![output-4-ok-status](https://github.com/user-attachments/assets/d152d492-d3f7-4ab4-b1c4-9f327d1922d6)

  ### 6.2 Outputs

  After a successful image POST request:

  - **Output 1**: The processed image is uploaded to S3 
    ![output-1-s3-upload-files](https://github.com/user-attachments/assets/233aff9c-aede-4a93-a2fe-4aff92501903)
  - **Output 2**: The image's metadata is uploaded to DynamoDB 
    ![output-2-dynamodb-upload-meta](https://github.com/user-attachments/assets/075d3dbd-eedf-4984-a557-bc40f9073a77)
  - **Output 3**: API Gateway returns a `200 OK` status with confirmation 
    ![output-4-ok-status](https://github.com/user-attachments/assets/e11e2f63-3841-42aa-a5f2-739567b7ff7a)
  - **Output 4**: The gray scaled image output.

    ![output-3-lake-view-grayscale](https://github.com/user-attachments/assets/ab61f97c-58fa-4e11-bcb3-4966fb5b77a6)

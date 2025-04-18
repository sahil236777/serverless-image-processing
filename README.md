# Serverless Image Processing Application

## 1. Project Description

### 1.1 Project Overview and Backend Structure
**Serverless Image Processing Application**

### 1.2 Description
This project implements a fully serverless cloud-native image processing solution using AWS. The application allows users to upload images via a REST API. Once uploaded, the images are automatically processed using AWS Lambda (resized, and converted to grayscale), then stored securely in an S3 bucket. Metadata such as upload timestamps and processing status is stored in DynamoDB. The system is designed with scalability, security, and monitoring in mind, leveraging key AWS services and best practices for cloud architecture.

---

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

---

## 3. System Architecture

### 3.1 Overview
The system is designed using a fully serverless architecture. Users upload images via an API Gateway endpoint. The image is passed to an AWS Lambda function, which processes the image (resize, grayscale). Processed images are saved to an Amazon S3 bucket, while metadata (e.g., filename, timestamp, status) is stored in a DynamoDB table. CloudWatch tracks logs, performance, and anomalies.

Specifically, the architecture is based on the following workflow:

1. **Input**: The user converts an image to base64 using the command below and submits it to the API endpoint:

   ```bash
   base64 -w 0 input-1-lake-view.jpg > input-1-lake-view-encoded.txt
   ```

   ![input-1-lake-view](https://github.com/user-attachments/assets/bc0a7256-4378-4f74-b6fe-21663df121a2)

2. **API Gateway**: Receives POST requests containing base64-encoded image content.
3. **Lambda Function**: Decodes and processes the image (resize + grayscale using Pillow) and saves it as a PNG to an S3 bucket.
4. **S3**: Receives the processed image under the `processed/` folder.
5. **DynamoDB**: Logs metadata such as ID, filename, timestamp, status, image size, and format.
6. **CloudWatch**: Logs success and error events for traceability.

### 3.2 Architectural Components
- **API Gateway**
- **Lambda Function**
- **S3**
- **DynamoDB**
- **CloudWatch**

### 3.3 Architectural Diagram
![architeture diagram](https://github.com/user-attachments/assets/b9982e47-3a2f-4590-b9d0-e57c63e667ed)

---

## 4. Data Dictionary

| Field Name | Notes                                  | Type     |
|------------|----------------------------------------|----------|
| ID         | Unique identifier                      | STRING   |
| Filename   | Original uploaded file name            | STRING   |
| Status     | Processing status                      | STRING   |
| Timestamp  | ISO format of processing               | DATETIME |
| S3Path     | Full URI in S3                         | STRING   |
| Size       | File size in bytes                     | NUMBER   |
| Format     | Output format                          | STRING   |

---

## 5. Data Design

### 5.1 Persistent/Static Data
Each image corresponds to a single metadata record. Stored in S3 and DynamoDB respectively.

### 5.1.1 Entity Relationship Diagram
![ERD Summary](https://github.com/user-attachments/assets/0be8f689-a98b-4036-ad23-6d88884e1ca0)

---

## 6. User Interface Design

### 6.1 Postman Workflow

![User Interface Navigation Flow](https://github.com/user-attachments/assets/5e6a3450-61c5-43a2-ac9c-d8d9536fdc1f)

- Header: `Content-Type: text/plain`
- Body: raw base64
- Returns 200 with image key

![output-4-ok-status](https://github.com/user-attachments/assets/d152d492-d3f7-4ab4-b1c4-9f327d1922d6)

# FrontEnd and Hosting
## 7. Monitoring, Alarms, and Observability

### 7.1 Logging and Metrics Strategy

The system leverages **Amazon CloudWatch** for centralized logging and metric aggregation across all components. All image processing activities executed by the Lambda function are logged to CloudWatch, including timestamped success and error messages. This provides full traceability and operational transparency into each step of the processing pipeline.

In addition, custom metrics were integrated to track the number of successfully processed images and processing failures. These metrics were configured as CloudWatch logs using embedded log statements within the Lambda codebase. Logs are grouped and filtered by execution outcomes (`INFO`, `ERROR`), enabling near real-time insights into backend behavior.

### 7.2 CloudWatch Dashboard

To support monitoring, a **CloudWatch Dashboard** was created, visualizing key metrics such as:
- Number of invocations
- Duration per execution
- Throttles or errors over time
- Log volume by log group

This dashboard facilitates continuous observation of backend health and ensures that processing throughput remains consistent.

> ![cloudwatch-dashboard](https://github.com/user-attachments/assets/4eae7fe7-8b3f-4d7d-a919-66d38bf35f71)


---

## 8. Alarms Configuration

### 8.1 Overview

**CloudWatch Alarms** were implemented to proactively notify the system administrator of anomalies or degraded performance. These alarms are configured based on metrics such as function error count, duration spikes, and missing logs due to image size issues or API throttling.

### 8.2 Alarm Details

- **Error Rate Alarm**: Triggers when more than one invocation fails within a 5-minute period.
- **Duration Alarm**: Triggers when Lambda execution time exceeds 3 seconds, which may indicate high image payloads or downstream slowdowns.
- **Invocation Count Alarm**: Tracks usage trends for anomaly detection.

Each alarm is tied to an Amazon SNS topic (internally configured) that could be subscribed to via email, SMS, or Lambda responders for remediation in production.

---

## 9. UI Consideration.
Great effort was done to comply with the feedback from the previous submission. Consiquently a UI was introduced to seamlessly interact with the backend. the visuals are as follows:

### Input Flow
![input-before-processing](https://github.com/user-attachments/assets/74961041-5f18-4fc4-99ee-197792d938ad)

### Output Flow
![output-after-processing](https://github.com/user-attachments/assets/88a9f1db-0e3d-4e13-997d-b206b25c7d48)


## 10. Security Considerations

Security has been incorporated throughout the infrastructure in the following ways:

### 10.1 IAM Configuration

- The Lambda function was granted **least-privilege access** via a custom IAM role.
- The IAM policy allows:
  - `s3:PutObject` only to the processed bucket prefix
  - `dynamodb:PutItem` to the `Images` table
- The public-facing S3 bucket used for frontend hosting is restricted to **GET** operations only through a static bucket policy.

### 10.2 Encryption and Access Control

- **S3 Server-Side Encryption** (SSE-S3) was enabled for all objects in the bucket.
- All data is encrypted **in-transit** via HTTPS using the API Gateway.
- **API Gateway** was configured with CORS headers to avoid cross-origin vulnerability while enabling frontend interaction.
- Console and programmatic access are disabled for temporary review IAM accounts.

### 10.3 VPC Isolation (Optional)

Although Lambda functions in this project are not explicitly deployed inside a VPC (due to lack of need for private resources), the setup is compatible with VPC deployment for future enhancements involving RDS or private subnets.

---

## 11. Read-Only AWS Instructor Account

To facilitate grading and infrastructure review, a **read-only IAM user** named `instructor-review` has been created. This account has:

- **No console access** (by design)
- 11 AWS managed policies attached (e.g., `AmazonDynamoDBReadOnlyAccess`, `AmazonS3ReadOnlyAccess`, `CloudWatchReadOnlyAccess`)
- View-only access to:
  - Lambda executions
  - API Gateway configurations
  - S3 object structures
  - CloudWatch logs and alarms
  - DynamoDB table contents

The following link allows login access:

[https://463470959060.signin.aws.amazon.com/console](https://463470959060.signin.aws.amazon.com/console)

Credentials (username and password) will be shared securely via the Canvas submission form.

> ![read-only-account](https://github.com/user-attachments/assets/5177fb00-9fb8-4a03-a860-a1864b011ee4)'

You can try outthe UI at: [http://serverless-image-frontend.s3-website-us-west-2.amazonaws.com](http://serverless-image-frontend.s3-website-us-west-2.amazonaws.com)


---

## 12. Final Remarks

This project meets all functional and non-functional criteria outlined in the proposal and enhanced further with full-stack implementation and DevOps features:
- Fully serverless image processing with automated grayscale conversion
- Secure S3 storage and metadata logging
- Monitored via CloudWatch
- Operational transparency with alarms and dashboards
- Production-grade frontend hosted on S3
- Review access for instructors and evaluators

The deployment is expected to remain **operational through April 19–20** for instructor review.


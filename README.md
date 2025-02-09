# Face Recognition System using AWS Lambda, S3, DynamoDB, and Rekognition

This project implements a simple face recognition system using AWS services, including AWS Lambda, Amazon S3, Amazon Rekognition, and DynamoDB. The system detects faces in images uploaded to an S3 bucket, extracts information such as age range and emotion, and stores the extracted data in a DynamoDB table.

## Features

- **Image Upload to S3**: Upload an image to an S3 bucket to trigger the Lambda function.
- **Face Detection**: Using Amazon Rekognition, the Lambda function detects faces in the uploaded image.
- **Data Extraction**: Extracts the age range and dominant emotion from the detected face.
- **DynamoDB Storage**: Stores the face details (Face ID, Age, Emotion) in a DynamoDB table.

## Architecture Overview

1. **S3 Bucket**: Stores images that trigger the Lambda function when a new object is uploaded.
2. **AWS Lambda**: The core logic of the face recognition system. When an image is uploaded to S3, it processes the image using Rekognition and stores the results in DynamoDB.
3. **Amazon Rekognition**: Detects faces and extracts attributes (age, emotion) from the uploaded image.
4. **DynamoDB**: Stores the extracted data (Face ID, Age, Emotion) for each image.

## Setup Instructions

### Step 1: Create an S3 Bucket
1. Go to the **S3 Console** and create a new S3 bucket.
2. Enable event notifications to trigger the Lambda function whenever a new object is uploaded to the bucket.

### Step 2: Create a DynamoDB Table
1. Go to the **DynamoDB Console** and create a new table called `FaceData`.
2. The table should have the following attributes:
   - **Primary Key**: `FaceID` (String)

### Step 3: Create a Lambda Function
1. Go to the **Lambda Console** and create a new Lambda function.
2. Set the runtime to **Python 3.x**.
3. In the function code, paste the Python script provided.
4. Make sure the Lambda execution role has the following permissions:
   - `rekognition:DetectFaces`
   - `s3:HeadObject`
   - `dynamodb:PutItem`
5. Configure the Lambda trigger to be the S3 bucket you created in Step 1.

### Step 4: Test the System
1. Upload an image to the S3 bucket.
2. Check the Lambda logs in CloudWatch to ensure the function was triggered.
3. Verify that the face data (Face ID, Age, Emotion) is stored in the DynamoDB table.

## Code Walkthrough

### Lambda Function:
The Lambda function processes the S3 event, interacts with Rekognition to detect faces, and writes the detected face data (age and emotion) to DynamoDB.

#### Key Libraries:
- `boto3`: AWS SDK for Python, used to interact with AWS services like Rekognition, S3, and DynamoDB.
- `urllib.parse`: Used to handle URL encoding of S3 object keys.

### How the Lambda Function Works:
1. The Lambda function receives an event from S3 when a file is uploaded.
2. It checks the S3 bucket and object key, ensuring the image is accessible.
3. It calls Amazon Rekognition's `detect_faces` API to detect faces and extract attributes such as age and emotion.
4. If a face is detected, it stores the data in DynamoDB under the `FaceData` table.
5. If no face is detected, it logs an error and returns a `400` status code.

## Error Handling

- **No Faces Detected**: If no faces are detected in the image, the Lambda function will log an error and return a `400` HTTP status code indicating the issue.
- **Timeout Error**: If the Lambda function exceeds the execution time (timeout), check the Lambda function's configuration. The default timeout is usually set to **3 seconds**, which might be insufficient for Rekognition's face detection process, especially with larger images. Increase the timeout to **10 seconds** or more by following these steps:
  1. Go to the **Lambda Console**.
  2. Select your Lambda function.
  3. Under **Configuration** -> **General configuration**, click **Edit**.
  4. Increase the **Timeout** value from **3 seconds** to **10 seconds** (or as necessary).
  
- **Region and Parameter Mismatch**: Ensure that the AWS services (S3, Rekognition, DynamoDB) are all in the same region as specified in your Lambda function's configuration. For instance, if your S3 bucket is in `us-east-2`, your Rekognition client and DynamoDB resource should also be initialized in the same region (e.g., `region = 'us-east-2'`). A mismatch in regions might cause issues where resources cannot communicate with each other properly.

- **General Errors**: If any other exception occurs during execution (such as an issue with accessing the S3 object or a service failure), the Lambda function will log the error message and return a `500` HTTP status code, indicating an internal server error.

## Conclusion

This project demonstrates how to use AWS Lambda, S3, Rekognition, and DynamoDB to create a serverless face recognition system. You can extend it by adding more features such as additional face attributes, image filtering, or using other AWS services for more advanced processing.

## License

This project is licensed under the MIT License.

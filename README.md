# Serverless Library Management System

This project is a serverless library management system built using AWS services. It allows users to manage a library's collection of books, register users, and track borrowing and returning of books. The application is fully serverless and uses AWS Lambda, API Gateway, DynamoDB, S3, Cognito for authentication, and CloudFront for content delivery.

## Project Overview

The Serverless Library Management System is designed to be a simple and scalable solution for managing library resources. It enables functionalities like adding new books, registering users, borrowing and returning books, and searching for books by author.

### Key Technologies

- **AWS Lambda:** For executing backend logic without provisioning servers.
- **API Gateway:** For creating and managing RESTful APIs.
- **DynamoDB:** For storing and querying data about books, users, and borrowing records.
- **S3:** For storing and serving static content, such as book images.
- **Cognito:** For user authentication and authorization.
- **CloudFront:** For content delivery and caching.

## Architecture

The system is based on a fully serverless architecture using AWS services:

- **AWS Lambda** is used for all the backend logic.
- **Amazon DynamoDB** serves as the database for storing books, users, and borrowing records.
- **Amazon S3** is used to store book images and other static content.
- **Amazon API Gateway** manages the RESTful API.
- **Amazon Cognito** handles user authentication.
- **Amazon CloudFront** is used to distribute static content globally.

![Architecture Diagram](architecture-diagram-url)

## Features

- **Add and Manage Books:** Add new books to the library, update book details, and delete books.
- **User Registration:** Register and manage users, allowing them to borrow and return books.
- **Book Borrowing and Returning:** Track which users have borrowed which books, including due dates.
- **Search Books by Author:** Quickly find books by a specific author.

## Setup and Deployment

### Prerequisites

- **AWS Account:** You need an AWS account to deploy the infrastructure.
- **Node.js and npm:** Ensure you have Node.js installed for deploying the project.
- **AWS CLI:** Install and configure the AWS CLI for your account.

### Deployment Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repo/library-management-system.git
   cd library-management-system

# API Documentation for User Management

This documentation provides a comprehensive guide on how to use the User Management API. The API supports user registration, login, OTP verification, and password reset functionalities.

## Base URL

```
http://<your-domain>/accounts/
```

## Endpoints

### 1. User Registration

- **Endpoint:** `/register/`
- **Method:** `POST`
- **Description:** Registers a new user and sends an OTP for email verification.

#### Request Body
```json
{
    "email": "user@example.com",
    "password": "your_password"
}
```

#### Response
- **Success (201 Created)**
```json
{
    "status": 200,
    "message": "User created successfully. Check your email for OTP verification.",
    "data": {
        "email": "user@example.com"
    }
}
```

- **Error (400 Bad Request)**
```json
{
    "status": 400,
    "message": "Something went wrong",
    "data": {
        "email": ["This field must be unique."]
    }
}
```

### 2. User Login

- **Endpoint:** `/login/`
- **Method:** `POST`
- **Description:** Authenticates a user and returns access and refresh tokens.

#### Request Body
```json
{
    "email": "user@example.com",
    "password": "your_password"
}
```

#### Response
- **Success (200 OK)**
```json
{
    "status": 200,
    "message": "Login successful",
    "data": {
        "email": "user@example.com",
        "refresh": "<refresh_token>",
        "access": "<access_token>"
    }
}
```

- **Error (400 Bad Request)**
```json
{
    "status": 400,
    "message": "Invalid credentials: Incorrect password"
}
```

### 3. Verify OTP

- **Endpoint:** `/verify/`
- **Method:** `POST`
- **Description:** Verifies the OTP sent to the user's email.

#### Request Body
```json
{
    "email": "user@example.com",
    "otp": 1234
}
```

#### Response
- **Success (200 OK)**
```json
{
    "status": 200,
    "message": "User verified successfully."
}
```

- **Error (400 Bad Request)**
```json
{
    "status": 400,
    "message": "Invalid OTP."
}
```

### 4. Password Reset Request

- **Endpoint:** `/password-reset/request/`
- **Method:** `POST`
- **Description:** Sends a password reset email to the user.

#### Request Body
```json
{
    "email": "user@example.com"
}
```

#### Response
- **Success (200 OK)**
```json
{
    "status": 200,
    "message": "Password reset email sent."
}
```

- **Error (404 Not Found)**
```json
{
    "status": 404,
    "message": "Email not found."
}
```

### 5. Password Reset

- **Endpoint:** `/password-reset/`
- **Method:** `POST`
- **Description:** Resets the user's password using a token received in the password reset email.

#### Request Body
```json
{
    "token": "<token>",
    "new_password": "new_password"
}
```

#### Response
- **Success (200 OK)**
```json
{
    "status": 200,
    "message": "Password has been reset successfully."
}
```

- **Error (400 Bad Request)**
```json
{
    "status": 400,
    "message": "Invalid token."
}
```

## Error Handling

All endpoints return standardized error messages, including:
- `400 Bad Request`: Indicates invalid input data.
- `404 Not Found`: Indicates that the requested resource was not found.
  
## Conclusion

This API provides essential functionalities for user management, including registration, login, OTP verification, and password resetting. Ensure to handle responses appropriately and validate user input to improve the user experience. For any issues or feature requests, please contact the development team.





# API Documentation for Attendance Management

This documentation outlines how to use the Attendance Management API. This API allows you to retrieve attendance records from devices, providing insights into user attendance for a given day.

## Base URL

```
http://<your-domain>/api/
```

## Endpoints

### 1. Today's Attendance

- **Endpoint:** `/attendance/today/`
- **Method:** `GET`
- **Description:** Retrieves today's attendance records for a specified device based on the username.

#### Query Parameters
- **username** (required): The unique username of the device.

#### Example Request
```
GET /api/zkapi/attendance/today/?username=device_username
```

#### Response
- **Success (200 OK)**
```json
[
    {
        "user_id": 1,
        "user_name": "John Doe",
        "privilege": "Admin",
        "password": "hashed_password",
        "group_id": "group_1",
        "in_time": "2024-09-21T09:00:00Z",
        "out_time": "2024-09-21T17:00:00Z",
        "device_name": "Device Name",
        "device_area": "Device Area",
        "device_username": "device_username"
    },
    ...
]
```

- **Error (400 Bad Request)**
```json
{
    "error": "Username parameter is required."
}
```

- **Error (404 Not Found)**
```json
{
    "error": "Device not found."
}
```

- **Error (500 Internal Server Error)**
```json
{
    "error": "<error_message>"
}
```

## Authentication

This API requires authentication. Ensure that you include a valid token in the request headers:

### Example Header
```
Authorization: Bearer <your_access_token>
```

## Error Handling

The API returns standardized error messages, including:
- `400 Bad Request`: Indicates that the request is missing required parameters.
- `404 Not Found`: Indicates that the specified device does not exist.
- `500 Internal Server Error`: Indicates an unexpected error occurred on the server.

## Conclusion

The Attendance Management API provides a straightforward way to access today's attendance records from specified devices. Ensure proper authentication and provide the necessary parameters to retrieve the desired data. For any issues or feature requests, please contact the development team.


Certainly! Below is a structured documentation for the CRUD API for the `Device` model in your Django REST Framework application. This documentation includes endpoint descriptions, request/response formats, and example usage.

# Device CRUD API Documentation

## Overview

The Device CRUD API allows users to create, retrieve, update, and delete devices in the system. Each device has attributes such as name, area, username, IP address, and port.

### Base URL
```
http://<your-domain>/api/
```

## Authentication

This API requires authentication. Use token-based authentication (e.g., JWT) to access the endpoints. Include the token in the `Authorization` header as follows:

```
Authorization: Bearer <your_token>
```

## Endpoints

### 1. Create a New Device

- **Endpoint**: `/devices/`
- **Method**: `POST`
- **Description**: Creates a new device.
- **Request Headers**:
  - `Content-Type: application/json`
  - `Authorization: Bearer <your_token>`
- **Request Body**:
```json
{
    "name": "Device 1",
    "area": "Office",
    "username": "device1",
    "ip_address": "192.168.1.10",
    "port": 8080
}
```
- **Response**:
  - **Status Code**: `201 Created`
  - **Response Body**:
```json
{
    "id": "uuid_value",
    "name": "Device 1",
    "area": "Office",
    "username": "device1",
    "ip_address": "192.168.1.10",
    "port": 8080,
    "created_at": "2024-09-21T12:34:56Z",
    "updated_at": "2024-09-21T12:34:56Z"
}
```

### 2. Retrieve All Devices

- **Endpoint**: `/devices/`
- **Method**: `GET`
- **Description**: Retrieves a list of all devices.
- **Request Headers**:
  - `Authorization: Bearer <your_token>`
- **Response**:
  - **Status Code**: `200 OK`
  - **Response Body**:
```json
[
    {
        "id": "uuid_value_1",
        "name": "Device 1",
        "area": "Office",
        "username": "device1",
        "ip_address": "192.168.1.10",
        "port": 8080,
        "created_at": "2024-09-21T12:34:56Z",
        "updated_at": "2024-09-21T12:34:56Z"
    },
    {
        "id": "uuid_value_2",
        "name": "Device 2",
        ...
    }
]
```

### 3. Retrieve a Specific Device

- **Endpoint**: `/devices/<device_id>/`
- **Method**: `GET`
- **Description**: Retrieves details of a specific device by its ID.
- **Request Headers**:
  - `Authorization: Bearer <your_token>`
- **Response**:
  - **Status Code**: `200 OK`
  - **Response Body**:
```json
{
    "id": "uuid_value_1",
    "name": "Device 1",
    "area": "Office",
    "username": "device1",
    "ip_address": "192.168.1.10",
    "port": 8080,
    "created_at": "2024-09-21T12:34:56Z",
    "updated_at": "2024-09-21T12:34:56Z"
}
```
  
### Error Responses
If the device is not found:
  - **Status Code**: `404 Not Found`
  - **Response Body**:
```json
{
    "detail": "Not found."
}
```

### 4. Update a Device

- **Endpoint**: `/devices/<device_id>/`
- **Method**: `PUT` or `PATCH`
- **Description**: Updates details of a specific device.
- **Request Headers**:
  - `Content-Type: application/json`
  - `Authorization: Bearer <your_token>`
- **Request Body**:
```json
{
    "name": "Updated Device Name",
    "area": "Updated Area",
    "username": "updated_device_username",
    "ip_address": "192.168.1.20",
    "port": 9090
}
```
- **Response**:
  - **Status Code**: `200 OK`
  - **Response Body**:
```json
{
    "id": "uuid_value_1",
    ...
}
```

### Error Responses
If the device is not found:
  - **Status Code**: `404 Not Found`
  - **Response Body**:
```json
{
    "detail": "Not found."
}
```

### 5. Delete a Device

- **Endpoint**: `/devices/<device_id>/`
- **Method**: `DELETE`
- **Description**: Deletes a specific device by its ID.
- **Request Headers**:
  - `Authorization: Bearer <your_token>`
  
#### Response
If successful:
  - **Status Code**: `204 No Content`

If the device is not found:
  - **Status Code**: `404 Not Found`
  - **Response Body**:
```json
{
    "detail": "Not found."
}
```

## Conclusion

This documentation provides an overview of the CRUD operations available for managing devices in your Django REST Framework application. Ensure you have proper authentication set up to access these endpoints and test them using tools like Postman or cURL for effective development and debugging.

Feel free to customize this documentation further based on your project requirements!
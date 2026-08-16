# TestFlow Architecture

## Overview

TestFlow uses a layered full-stack architecture.

```text
Angular
  ↓
REST API
  ↓
Flask Routes
  ↓
Services
  ↓
Repositories
  ↓
MongoDB
```
Validation and data-processing components sit beside the service layer and normalize external input before persistence.
## Backend Layers
### Routes
Responsibilities:

- HTTP request parsing
- query parameter handling
- input validation at the HTTP boundary
- HTTP status codes
- response serialization

Routes do not contain database queries.
### Services
Responsibilities:

- application logic
- resource relationship validation
- test result status aggregation
- import orchestration
### Repositories
Responsibilities:

- MongoDB queries
- inserts
- updates
- deletes
- aggregation queries
### Validators
Responsibilities:

- JSON import validation
- Parquet parsing
- pandas-based validation
- PyArrow-based Parquet handling
- normalization into shared result structures
## Frontend Structure
```text
core/
  application-wide infrastructure

features/
  domain-specific pages and services

shared/
  reusable components and models
```
Angular uses standalone components, services, signals, Reactive Forms, Router and HttpClient.
## Status Aggregation
```text
ERROR > FAILED > PENDING > PASSED
```
The aggregation rule is implemented once in backend application logic and covered by automated tests.
## Import Architecture
Both JSON and Parquet are converted to a shared internal representation before persistence.

This avoids duplicating business logic between file formats.
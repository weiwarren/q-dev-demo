```
PROMPT:
Generate README based on the project src folder. Escape all the triple ticks, all the hash and empty line break
```

# Data Lake Platform

This project is a simple data lake platform that allows users to upload CSV files, preview data, trigger AWS Glue crawlers, and query data using Amazon Athena.

## Project Structure

```
src/
├── server/
│ ├── app/
│ │ ├── routes/
│ │ │ ├── __init__.py
│ │ │ ├── file_routes.py
│ │ │ └── query_routes.py
│ │ ├── services/
│ │ │ ├── __init__.py
│ │ │ ├── file_service.py
│ │ │ └── query_service.py
│ │ ├── utils/
│ │ │ ├── __init__.py
│ │ │ └── file_utils.py
│ │ ├── __init__.py
│ │ ├── config.py
│ │ └── main.py
│ ├── tests/
│ │ ├── __init__.py
│ │ └── test_routes.py
│ └── requirements.txt
└── client/
├── public/
├── src/
│ ├── components/
│ │ ├── FileUpload/
│ │ ├── DataPreview/
│ │ ├── GlueStatus/
│ │ └── QueryInterface/
│ ├── pages/
│ ├── styles/
│ ├── utils/
│ ├── _app.tsx
│ ├── _document.tsx
│ └── index.tsx
├── .gitignore
├── next-env.d.ts
├── next.config.js
├── package.json
└── tsconfig.json
```

## Backend (Python FastAPI)

The backend is built using FastAPI and provides APIs for file upload, data preview, Glue crawler triggering, and data querying.

### Setup

Navigate to the src/server directory.

Create a virtual environment: ``` python -m venv venv source venv/bin/activate # On Windows, use venv\Scripts\activate ```

Install dependencies: ``` pip install -r requirements.txt ```

Set up environment variables (AWS credentials, etc.).

### Running the Server

```
uvicorn app.main:app --reload
```

The server will start on http://localhost:8000.

### Key Components

app/main.py: Main FastAPI application entry point.

app/routes/: API route definitions.

app/services/: Business logic for file handling and querying.

app/utils/: Utility functions.

app/config.py: Configuration settings.

## Frontend (Next.js with TypeScript and shadcn/ui)

The frontend is built using Next.js, TypeScript, and shadcn/ui for a modern, responsive user interface.

### Setup

Navigate to the src/client directory.

Install dependencies: ``` npm install ```

### Running the Client

```
npm run dev
```

The client will start on http://localhost:3000.

### Key Components

src/components/: Reusable React components.

src/pages/: Next.js pages and API routes.

src/styles/: Global styles and CSS modules.

src/utils/: Utility functions and API calls.

## Features

CSV File Upload: Users can upload CSV files to the data lake.

Data Preview: After upload, users can preview a subset of the data.

Glue Crawler Triggering: The application can trigger AWS Glue crawlers to catalog the uploaded data.

Data Querying: Users can query the processed data using a list of available tables.

## Development Workflow

Make changes to the backend code in the src/server directory.

Update frontend components and pages in the src/client directory.

Test your changes locally using the development servers for both backend and frontend.

Write and run tests to ensure code quality and functionality.

## Deployment

(Add specific deployment instructions based on your infrastructure setup, e.g., AWS, Docker, etc.)

## Contributing

(Add guidelines for contributing to the project, if applicable)

## License

(Add license information for your project)
```


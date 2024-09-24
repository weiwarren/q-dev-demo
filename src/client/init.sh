# Create the components directory for FileUpload
mkdir -p src/components/FileUpload

# Create the FileUpload component
touch src/components/FileUpload/FileUpload.tsx
touch src/components/FileUpload/index.ts

# Create the components directory for FilePreview
mkdir -p src/components/FilePreview

# Create the FilePreview component
touch src/components/FilePreview/FilePreview.tsx
touch src/components/FilePreview/index.ts

# Create the components directory for JobStatus
mkdir -p src/components/JobStatus

# Create the JobStatus component
touch src/components/JobStatus/JobStatus.tsx
touch src/components/JobStatus/index.ts

# Create the components directory for Query
mkdir -p src/components/Query

# Create the Query component
touch src/components/Query/Query.tsx
touch src/components/Query/index.ts

# Create the lib directory for API and utility functions
mkdir -p src/lib

# Create the API client
touch src/lib/api.ts

# Create the utility functions
touch src/lib/utils.ts

# Create the pages directory for upload
mkdir -p src/pages/upload

# Create the upload page
touch src/pages/upload/index.tsx

# Create the pages directory for query
mkdir -p src/pages/query

# Create the query page
touch src/pages/query/index.tsx

# Create the API routes directory
mkdir -p src/pages/api

# Create the API routes
touch src/pages/api/upload.ts
touch src/pages/api/preview.ts
touch src/pages/api/submit.ts
touch src/pages/api/status.ts
touch src/pages/api/tables.ts

# Create the types directory for TypeScript types
mkdir -p src/types

# Create the types for API responses
touch src/types/api.ts

# Create the server folder
mkdir -p src/server

# Create the __init__.py file
touch src/server/__init__.py

# Create the app folder and its files
mkdir -p src/server/app \
&& touch src/server/app/__init__.py \
&& touch src/server/app/main.py

# Create the api folder and its files
mkdir -p src/server/app/api \
&& touch src/server/app/api/__init__.py \
&& touch src/server/app/api/routes.py \
&& touch src/server/app/api/schemas.py

# Create the services folder and its files
mkdir -p src/server/app/services \
&& touch src/server/app/services/__init__.py \
&& touch src/server/app/services/file_service.py \
&& touch src/server/app/services/data_service.py

# Create the utils folder and its files
mkdir -p src/server/app/utils \
&& touch src/server/app/utils/__init__.py \
&& touch src/server/app/utils/security.py

# Create the config.py file
touch src/server/app/config.py

# Create the tests folder and its files
mkdir -p src/server/tests \
&& touch src/server/tests/__init__.py \
&& touch src/server/tests/conftest.py

# Create the api folder and its files under tests
mkdir -p src/server/tests/api \
&& touch src/server/tests/api/__init__.py \
&& touch src/server/tests/api/test_routes.py

# Create the services folder and its files under tests
mkdir -p src/server/tests/services \
&& touch src/server/tests/services/__init__.py \
&& touch src/server/tests/services/test_file_service.py \
&& touch src/server/tests/services/test_data_service.py

# Create the utils folder and its files under tests
mkdir -p src/server/tests/utils \
&& touch src/server/tests/utils/__init__.py \
&& touch src/server/tests/utils/test_security.py

# Create the requirements.txt file
touch src/server/requirements.txt

# Create the client folder
mkdir -p src/client

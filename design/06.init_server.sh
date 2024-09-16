# Create the server folder
mkdir -p src/server

# Create the app folder and files
mkdir -p src/server/app \
&& touch src/server/app/__init__.py \
&& touch src/server/app/main.py \
&& mkdir -p src/server/app/api \
&& touch src/server/app/api/__init__.py \
&& touch src/server/app/api/routes.py \
&& touch src/server/app/api/schemas.py \
&& mkdir -p src/server/app/services \
&& touch src/server/app/services/__init__.py \
&& touch src/server/app/services/file_service.py \
&& touch src/server/app/services/data_service.py \
&& touch src/server/app/services/query_service.py \
&& mkdir -p src/server/app/utils \
&& touch src/server/app/utils/__init__.py \
&& touch src/server/app/utils/security.py \
&& touch src/server/app/config.py

# Create the tests folder and files
mkdir -p src/server/tests \
&& touch src/server/tests/__init__.py \
&& touch src/server/tests/conftest.py \
&& mkdir -p src/server/tests/api \
&& touch src/server/tests/api/__init__.py \
&& touch src/server/tests/api/test_routes.py \
&& mkdir -p src/server/tests/services \
&& touch src/server/tests/services/__init__.py \
&& touch src/server/tests/services/test_file_service.py \
&& touch src/server/tests/services/test_data_service.py \
&& mkdir -p src/server/tests/utils \
&& touch src/server/tests/utils/__init__.py \
&& touch src/server/tests/utils/test_security.py \
&& touch src/server/requirements.txt

mkdir -p src/client

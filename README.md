<hr>

<h1>📍How to install: </h1>

> ❗ONLY SUITABLE FOR CERTAIN TYPES OF PDF❗
>
>This tool provides a straightforward and efficient way to extract
> data from PDF documents and transform it into a structured Excel format.

<!-- DOCKER -->
<details><summary><h2>🐳Connect to Docker Compose:</h2></summary><br/>

<h3>Sign up for an account at [PDFTables.com](https://pdftables.com/) and then visit the
[API page](https://pdftables.com/pdf-to-excel-api) to see your API key.</h3>

<h3>Insert this command into cmd/terminal (in .env file set correct values):</h3>

```
cd backend/
echo "Creating .env file..."
cat <<EOL > .env
# Django configuration
SECRET_KEY=YOUR_SECRET_KEY
DEBUG=1

# PostgreSQL (docker/local)
DB_ENGINE=django.db.backends.postgresql_psycopg2
POSTGRES_DB=pdf_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=example
DB_PORT=5432

# pgadmin container
PGADMIN_DEFAULT_EMAIL=admin@gmail.com
PGADMIN_DEFAULT_PASSWORD=root

# https://pdftables.com/pdf-to-excel-api
API_PDF_TABLES=api_key_pdf
EOL
mkdir converted_files
cd ..
```

<h3>UP Docker-compose:</h3>

```
docker-compose -f docker/docker-compose.yml up --build
```

<h3>Login to the container console:</h3>

```
docker exec -it django-container bash
```

</details>
<!-- END DOCKER -->

# Endpoints

## Upload Endpoint

- **POST** `{home page}`: Upload File

## Management Endpoints

- **GET** `file/<uuid:pk>/`: Detail view of the pdf file.
- **GET** `file/<uuid:pk>/download_excel/`: Download converted excel table 

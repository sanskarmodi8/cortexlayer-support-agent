import os

# Helper functions

def create_dir(path):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)

def create_file(path, content=""):
    """Create file only if it doesn't already exist."""
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(content)


# Project structure definition

structure = [
    "backend/app/routes",
    "backend/app/rag",
    "backend/app/ingestion",
    "backend/app/services",
    "backend/app/models",
    "backend/app/core",
    "backend/app/utils",
    "backend/tests",
    "frontend/widget",
    "frontend/admin/src",
    "infra"
]

files = {
    # Backend core
    "backend/app/main.py": "# Entry point: FastAPI boot file\n",
    
    # Routes
    "backend/app/routes/query.py": "",
    "backend/app/routes/upload.py": "",
    "backend/app/routes/admin.py": "",
    "backend/app/routes/auth.py": "",

    # RAG pipeline
    "backend/app/rag/retriever.py": "",
    "backend/app/rag/prompt.py": "",
    "backend/app/rag/generator.py": "",
    "backend/app/rag/pipeline.py": "",

    # Ingestion
    "backend/app/ingestion/pdf_reader.py": "",
    "backend/app/ingestion/text_reader.py": "",
    "backend/app/ingestion/url_scraper.py": "",
    "backend/app/ingestion/chunker.py": "",
    "backend/app/ingestion/embedder.py": "",

    # Services
    "backend/app/services/billing.py": "",
    "backend/app/services/analytics.py": "",
    "backend/app/services/usage_limits.py": "",
    "backend/app/services/client_manager.py": "",

    # Models
    "backend/app/models/client.py": "",
    "backend/app/models/usage.py": "",
    "backend/app/models/documents.py": "",
    "backend/app/models/chat_logs.py": "",

    # Core
    "backend/app/core/config.py": "",
    "backend/app/core/database.py": "",
    "backend/app/core/vectorstore.py": "",
    "backend/app/core/auth.py": "",

    # Utils
    "backend/app/utils/file_utils.py": "",
    "backend/app/utils/rate_limit.py": "",
    "backend/app/utils/s3.py": "",
    "backend/app/utils/logger.py": "",

    # Tests
    "backend/tests/test_rag.py": "",

    # Frontend
    "frontend/widget/embed.js": "",
    "frontend/widget/styles.css": "",

    # Admin dashboard placeholder
    "frontend/admin/package.json": "{\n  \"name\": \"cortexlayer-admin\"\n}\n",

    # Infra
    "infra/docker-compose.yml": "",
    "infra/nginx.conf": "",
    "infra/README.md": "",

    # Root files
    ".env": "",
    "README.md": "",
}

# Create all directories

for d in structure:
    create_dir(d)

# Create all files

for path, content in files.items():
    create_file(path, content)

print("✔ Project structure created successfully!")

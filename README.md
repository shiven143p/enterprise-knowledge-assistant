# Enterprise Knowledge Assistant (EKA)

M.Tech AI-ML | API-driven Cloud Native Solutions

## Project Objective

Develop an API-driven enterprise knowledge assistant
using NLP, model fine-tuning, and Retrieval-Augmented
Generation (RAG).

## Technology Stack

- Python
- FastAPI
- Streamlit
- Hugging Face Transformers
- ChromaDB
- LLM API

## Project Status

## Step 1 — Environment setup
    python --version
    python -m venv .venv
    cmd: .\.venv\Scripts\Activate.ps1 / bash: source .venv/bin/activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    
## Step 2 — Build REST API using FastAPI    
    python -m pip show fastapi uvicorn
    mkdir -p app/backend
    touch app/__init__.py
    touch app/backend/__init__.py
    touch app/backend/main.py

    The __init__.py files mark the directories as Python packages.

1. FastAPI()

Creates our backend application.

2. @app.get("/")

Defines a REST API endpoint that responds to an HTTP GET request at /.

3. @app.get("/api/health")

Defines a second endpoint for checking whether the application is running.

4. Returning a Python dictionary

FastAPI automatically serializes the dictionary into a JSON response.

    python -m uvicorn app.backend.main:app --host 0.0.0.0 --port 8000 --reload
    curl http://127.0.0.1:8000/
    curl http://127.0.0.1:8000/api/health
    Interactive API documentation : http://localhost:8000/docs

    Argument	        Meaning
    app.backend.main	Python module containing our application
    :app	            FastAPI application object
    --host 0.0.0.0	    Listen on all network interfaces
    --port 8000	        Run on port 8000
    --reload	        Restart automatically when code changes

## Step 3 — Build the Streamlit Frontend and Connect It to FastAPI
![alt text](image.png)

    - The user opens the Streamlit application.
    - Streamlit sends an HTTP GET request to FastAPI.
    - FastAPI processes the request.
    - FastAPI returns a JSON response.
    - Streamlit displays the response.

    mkdir -p app/frontend
    touch app/frontend/__init__.py
    touch app/frontend/streamlit_app.py

## Step 4 — Preparing the Enterprise Knowledge Base
![alt text](image-1.png)

    mkdir -p data/documents

    Document 1 — Employee Leave Policy - Create data/documents/leave_policy.txt

    Document 2 — IT Support Policy - Create data/documents/it_support_policy.txt

    Document 3 — Expense Reimbursement Policy - Create data/documents/expense_policy.txt

    Document 4 — Business Travel Policy - Create data/documents/travel_policy.txt

Create a document service

    mkdir -p app/backend/services
    touch app/backend/services/__init__.py
    touch app/backend/services/document_service.py

    Path(__file__).resolve().parents[3] identifies the project root based on the service file's location.

    glob("*.txt") finds text documents in the directory.

    file_path.stem extracts the filename without its extension.

Create document API endpoints

    curl http://127.0.0.1:8000/api/documents
    curl http://127.0.0.1:8000/api/documents/leave_policy
    curl -i http://127.0.0.1:8000/api/documents/unknown_policy

Integrate the document explorer into Streamlit

## Step 5 — Preparing the Dataset for DistilBERT Fine-Tuning

![alt text](image-2.png)

We selected DistilBERT, a compact transformer-based language model, for classifying employee queries.
![alt text](image-3.png)
The classifier will help identify the domain of an employee's query, which can later guide our RAG document retrieval.

 This is a multi-class, single-label classification problem: each query receives exactly one category.
    Label ID	Category	            Example
    0	        HR & Leave	            "How do I apply for sick leave?"
    1	        IT Support	            "My VPN connection is failing."
    2	        Finance & Expenses	    "When will my claim be reimbursed?"
    3	        Travel & Operations	    "How do I book a business flight?"

 Dataset format CSV file with two columns:
    - text: Employee's query.
    - label: Numerical category identifier.

 Create the dataset directory

    mkdir -p data/training

 Create a file: data/training/employee_queries.csv

![alt text](image-4.png)

 Install the data-processing libraries

    python -m pip show pandas scikit-learn

 Create the dataset preparation script

    mkdir -p training
    touch training/prepare_dataset.py
    python training/prepare_dataset.py

## Step 6 — Fine-Tuning DistilBERT for Enterprise Query Classification
![alt text](image-5.png)

## Step 6A.1 — Build the Curated Intent Catalog
![alt text](image-6.png)

Each query will contain:
Field	        Purpose
text	        Employee's question
label	        Classification target: 0, 1, 2, or 3
intent_group	Groups queries that express the same underlying intent

Important distinction: The model will predict label, not intent_group. The intent group is used for dataset organization and leakage-aware evaluation.

 Create the intent catalog file

    mkdir -p data/training training
    Create: data/training/intent_catalog.json

 Create the dataset generation script

    touch training/generate_dataset.py

    It performs five operations:
    1. Reads the intent catalog from JSON.
    2. Iterates through categories, intents, and questions.
    3. Checks for empty queries and exact duplicates (ignoring case and repeated whitespace).
    4. Creates a structured dataset.
    5. Exports the dataset to CSV.

 Execute the dataset generator

    python training/generate_dataset.py

 Verify the generated CSV

    head -n 6 data/training/employee_queries.csv
![alt text](image-7.png)

## Step 6A.2 — Expand the Dataset to 400 Queries

Run the generator again after updating json with new intent each category

    python training/generate_dataset.py

## Step 6A.3 — Complete the Intent Catalog

 Create a script to expand the catalog

    touch training/expand_intents.py

 Run the expansion script

    python training/expand_intents.py

 Regenerate the dataset

    python training/generate_dataset.py

## Step 6A.4 — Expand to 400 queries

![alt text](image-8.png)

 Create a variation template

    Direct question
    Conversational request
    Scenario-based question
    Procedural question
    Indirect question

 Create an expansion worksheet

    touch training/create_expansion_template.py
    python training/create_expansion_template.py

 Populate the worksheet
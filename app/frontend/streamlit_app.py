
import os

import requests
import streamlit as st

# Backend API configuration
API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)

# Page configuration
st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="🧠",
    layout="wide"
)

# Application heading
st.title("Enterprise Knowledge Assistant")
st.caption("API-Driven AI Knowledge Management System")

st.divider()

# Sidebar
with st.sidebar:
    st.header("Navigation")

    page = st.radio(
        "Choose a feature",
        [
            "Dashboard",
            "Knowledge Chatbot",
            "Document Summarizer",
            "Workplace Draft Generator",
            "Document Explorer",
        ]
    )

    st.divider()
    st.info("M.Tech AI-ML | API-Driven Cloud Computing")

# Dashboard
if page == "Dashboard":

    st.header("System Dashboard")

    st.write(
        "Welcome to the Enterprise Knowledge Assistant. "
        "This application will help employees access and "
        "understand organizational knowledge using AI."
    )

    st.subheader("Backend Connection")

    if st.button("Check API Connection"):

        try:
            response = requests.get(
                f"{API_BASE_URL}/api/health",
                timeout=5
            )

            response.raise_for_status()

            data = response.json()

            if data.get("status") == "ok":
                st.success("Backend is connected successfully!")
                st.json(data)
            else:
                st.warning("Backend returned an unexpected status.")
                st.json(data)

        except requests.exceptions.RequestException as error:
            st.error("Unable to connect to FastAPI backend.")
            st.code(str(error))

# Knowledge Chatbot
elif page == "Knowledge Chatbot":

    st.header("Enterprise Knowledge Chatbot")

    st.info(
        "Coming soon: Ask questions using enterprise "
        "documents and Retrieval-Augmented Generation."
    )

# Document Summarizer
elif page == "Document Summarizer":

    st.header("Document Summarizer")

    st.info(
        "Coming soon: Summarize enterprise policies "
        "and organizational documents."
    )

# Workplace Draft Generator
elif page == "Workplace Draft Generator":

    st.header("Workplace Draft Generator")

    st.info(
        "Coming soon: Generate professional workplace "
        "communications using AI."
    )

elif page == "Document Explorer":

    st.header("Enterprise Document Explorer")

    try:
        response = requests.get(
            f"{API_BASE_URL}/api/documents",
            timeout=10
        )

        response.raise_for_status()

        data = response.json()
        documents = data["documents"]

        st.metric(
            "Available Documents",
            data["total"]
        )

        if not documents:
            st.info("No documents are available.")

        else:
            document_names = {
                doc["filename"]: doc["id"]
                for doc in documents
            }

            selected_name = st.selectbox(
                "Select a document",
                list(document_names.keys())
            )

            if st.button("View Document"):

                document_id = document_names[selected_name]

                doc_response = requests.get(
                    f"{API_BASE_URL}/api/documents/{document_id}",
                    timeout=10
                )

                doc_response.raise_for_status()

                document = doc_response.json()

                st.subheader(document["filename"])
                st.text_area(
                    "Document Content",
                    document["content"],
                    height=400
                )

    except requests.exceptions.RequestException as error:
        st.error("Unable to load enterprise documents.")
        st.code(str(error))

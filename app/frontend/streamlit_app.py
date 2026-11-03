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
            "SAP Support Assistant",
            "SAP Incident Ticket Generator",
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

    st.caption(
        "Ask questions about NovaTech Solutions "
        "enterprise policies."
    )

    # Initialize conversation history.
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Display previous messages.
    for message in st.session_state.chat_messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message.get("sources"):
                with st.expander("View supporting sources"):

                    for source in message["sources"]:
                        st.markdown(
                            f"**{source['source_id']} — "
                            f"{source['filename']}**"
                        )

                        st.text(source["excerpt"])
                        st.divider()

    # Chat input.
    user_query = st.chat_input(
        "Ask a question about company policies..."
    )

    if user_query:

        # Display and store user message.
        st.session_state.chat_messages.append({
            "role": "user",
            "content": user_query
        })

        with st.chat_message("user"):
            st.markdown(user_query)

        # Generate response.
        with st.chat_message("assistant"):

            with st.spinner("Searching enterprise knowledge..."):

                try:
                    response = requests.post(
                        f"{API_BASE_URL}/api/chat",
                        json={
                            "query": user_query,
                            "top_k": 4
                        },
                        timeout=90
                    )

                    response.raise_for_status()

                    result = response.json()

                    answer = result["answer"]
                    sources = result.get("sources", [])
                    classification = result.get("classification", {})

                    st.markdown(answer)
                    
                    if classification:
                        st.caption(
                            f"Detected knowledge domain: "
                            f"{classification.get('category', 'Unknown')} "
                            f"(score: {classification.get('confidence', 0):.2f})"
                        )



                    if sources:
                        with st.expander(
                            "View supporting sources"
                        ):
                            for source in sources:
                                st.markdown(
                                    f"**{source['source_id']} — "
                                    f"{source['filename']}**"
                                )

                                st.text(source["excerpt"])
                                st.divider()

                    st.session_state.chat_messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources
                    })

                except requests.exceptions.RequestException:
                    st.error(
                        "Unable to retrieve an answer. "
                        "Please check the backend connection."
                    )

                except (KeyError, ValueError):
                    st.error(
                        "The backend returned an invalid response."
                    )

# Document Summarizer
elif page == "Document Summarizer":

    st.header("Enterprise Document Summarizer")

    st.caption(
        "Generate AI-powered summaries of "
        "NovaTech Solutions policy documents."
    )

    try:
        response = requests.get(
            f"{API_BASE_URL}/api/documents",
            timeout=10
        )

        response.raise_for_status()

        documents = response.json()["documents"]

        if not documents:
            st.info("No documents available.")

        else:
            document_options = {
                doc["filename"]: doc["id"]
                for doc in documents
            }

            selected_document = st.selectbox(
                "Select a document",
                list(document_options.keys())
            )

            summary_type = st.radio(
                "Summary type",
                ["brief", "detailed"],
                horizontal=True
            )

            if st.button("Generate Summary"):

                with st.spinner("Generating summary..."):

                    result = requests.post(
                        f"{API_BASE_URL}/api/summarize",
                        json={
                            "document_id": (
                                document_options[selected_document]
                            ),
                            "summary_type": summary_type
                        },
                        timeout=90
                    )

                    result.raise_for_status()

                    summary_data = result.json()

                    st.subheader("Generated Summary")

                    st.markdown(
                        summary_data["summary"]
                    )

                    st.caption(
                        f"Source: {summary_data['filename']}"
                    )

    except requests.exceptions.RequestException:
        st.error(
            "Unable to connect to the summarization service."
        )

    except (KeyError, ValueError):
        st.error("Invalid response from the backend.")

# Workplace Draft Generator

elif page == "Workplace Draft Generator":

    st.header("Workplace Draft Generator")

    st.caption(
        "Create professional workplace communications "
        "using enterprise policy knowledge."
    )

    request_text = st.text_area(
        "Describe what you want to draft",
        placeholder=(
            "Example: Draft an email requesting "
            "three days of annual leave next month."
        ),
        height=120
    )

    col1, col2 = st.columns(2)

    with col1:
        draft_type = st.selectbox(
            "Draft type",
            [
                "email",
                "support_ticket",
                "formal_request"
            ]
        )

    with col2:
        tone = st.selectbox(
            "Tone",
            [
                "professional",
                "formal",
                "concise"
            ]
        )

    if st.button("Generate Draft"):

        if not request_text.strip():
            st.warning(
                "Please describe the communication "
                "you want to generate."
            )

        else:
            with st.spinner("Generating workplace draft..."):

                try:
                    response = requests.post(
                        f"{API_BASE_URL}/api/generate",
                        json={
                            "request": request_text,
                            "draft_type": draft_type,
                            "tone": tone
                        },
                        timeout=90
                    )

                    response.raise_for_status()

                    result = response.json()

                    st.subheader("Generated Draft")

                    st.text_area(
                        "Review and edit your draft",
                        value=result["draft"],
                        height=350
                    )

                    if result.get("sources"):
                        with st.expander(
                            "View retrieved policy references"
                        ):
                            for source in result["sources"]:
                                st.markdown(
                                    f"**{source['source_id']} — "
                                    f"{source['filename']}**"
                                )
                                st.text(source["excerpt"])
                                st.divider()

                except requests.exceptions.RequestException:
                    st.error(
                        "Unable to generate the draft. "
                        "Please check the backend service."
                    )

                except (KeyError, ValueError):
                    st.error(
                        "Invalid response from the backend."
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

# SAP Support Assistant
elif page == "SAP Support Assistant":

    st.header("SAP Finance Support Assistant")

    st.caption(
        "AI-powered troubleshooting using synthetic "
        "SAP Finance knowledge articles."
    )

    st.info(
        "Academic prototype. No live SAP connection. "
        "Do not enter confidential financial data."
    )

    if "sap_messages" not in st.session_state:
        st.session_state.sap_messages = []

    for message in st.session_state.sap_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message.get("sources"):
                with st.expander("View SAP KB references"):
                    for source in message["sources"]:
                        st.markdown(
                            f"**{source['source_id']} — "
                            f"{source['filename']}**"
                        )
                        st.text(source["excerpt"])

    query = st.chat_input(
        "Describe your SAP Finance issue..."
    )

    if query:
        st.session_state.sap_messages.append({
            "role": "user",
            "content": query
        })

        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            with st.spinner("Searching SAP knowledge base..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/api/sap/chat",
                        json={
                            "query": query,
                            "top_k": 4
                        },
                        timeout=90
                    )

                    response.raise_for_status()
                    result = response.json()

                    st.markdown(result["answer"])

                    sources = result.get("sources", [])

                    if sources:
                        with st.expander(
                            "View SAP KB references"
                        ):
                            for source in sources:
                                st.markdown(
                                    f"**{source['source_id']} — "
                                    f"{source['filename']}**"
                                )
                                st.text(source["excerpt"])

                    st.session_state.sap_messages.append({
                        "role": "assistant",
                        "content": result["answer"],
                        "sources": sources
                    })

                except requests.exceptions.RequestException:
                    st.error(
                        "SAP support service is unavailable."
                    )

                except (KeyError, ValueError):
                    st.error(
                        "Invalid response from SAP support API."
                    )

# SAP Incident Ticket Generator
elif page == "SAP Incident Ticket Generator":

    st.header("SAP Incident Ticket Generator")

    st.caption(
        "Generate structured SAP support tickets "
        "using AI and enterprise knowledge articles."
    )

    st.warning(
        "Academic prototype using synthetic data. "
        "No incident will be submitted to a live system."
    )

    issue_description = st.text_area(
        "Describe the SAP issue",
        placeholder=(
            "Example: Unable to post a vendor invoice "
            "because SAP displays a validation error."
        ),
        height=120
    )

    business_impact = st.text_area(
        "Business impact",
        placeholder=(
            "Example: Invoice processing is blocked."
        ),
        height=80
    )

    error_message = st.text_input(
        "Exact SAP error message (if available)"
    )

    if st.button("Generate Incident Draft"):

        if len(issue_description.strip()) < 10:
            st.warning(
                "Please provide a meaningful issue description."
            )

        else:
            with st.spinner("Preparing incident draft..."):

                try:
                    response = requests.post(
                        f"{API_BASE_URL}/api/sap/ticket-draft",
                        json={
                            "issue_description": issue_description,
                            "business_impact": business_impact,
                            "error_message": error_message
                        },
                        timeout=90
                    )

                    response.raise_for_status()

                    result = response.json()

                    st.success(
                        "Incident draft generated. "
                        "No ticket has been submitted."
                    )

                    st.text_area(
                        "Review and edit incident draft",
                        value=result["ticket_draft"],
                        height=500
                    )

                    st.caption(
                        f"Status: {result['status']}"
                    )

                    if result.get("sources"):
                        with st.expander(
                            "View supporting SAP KB articles"
                        ):
                            for source in result["sources"]:
                                st.markdown(
                                    f"**{source['source_id']} — "
                                    f"{source['filename']}**"
                                )
                                st.text(source["excerpt"])

                except requests.exceptions.RequestException:
                    st.error(
                        "Unable to generate incident draft."
                    )

                except (KeyError, ValueError):
                    st.error(
                        "Invalid response from the backend."
                    )

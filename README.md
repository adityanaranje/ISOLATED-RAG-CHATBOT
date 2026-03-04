# 🧠 Isolated Multi-Bot RAG System (LangGraph + Pinecone + Streamlit)

A production-ready **Retrieval Augmented Generation (RAG)** system built
with **LangGraph**, **LangChain**, **Pinecone**, and **Streamlit**.

This project allows users to **create and manage multiple isolated AI
bots**, where each bot has its own **independent knowledge base**. The
system dynamically decides whether to use **retrieval or direct LLM
answering**, improving efficiency and response accuracy.

The application is **containerized with Docker** and deployed on **AWS
EC2 with Nginx and Cloudflare**, including **automatic updates using
Watchtower**.

------------------------------------------------------------------------

## 🌐 Live Demo

**Live Application**\
https://adityanworld.org

**Docker Image**\
https://hub.docker.com/r/deltavenom/streamlit-rag-llm-ai-app

------------------------------------------------------------------------

## 🚀 Key Features

### 🤖 Multi-Bot System

Users can dynamically manage multiple chatbots.

Capabilities:

-   Create new bots
-   Delete bots
-   Each bot maintains its own document knowledge base
-   Queries are routed to the correct bot using `bot_id`

Architecture:

bot_id → Pinecone namespace → isolated vector store

Example:

HR Bot → hr_namespace\
Insurance Bot → insurance_namespace\
Research Bot → research_namespace

This design enables **SaaS-style AI assistants** on a single platform.

------------------------------------------------------------------------

### 🧩 LangGraph Based Decision Pipeline

Instead of a traditional linear RAG pipeline, the system uses
**LangGraph** to dynamically route queries.

The system decides:

-   Should retrieval be used?
-   Is retrieved context sufficient?
-   Should the LLM answer directly?
-   Should retrieval be retried?

This makes responses **more reliable and efficient**.

------------------------------------------------------------------------

### 📊 Context Relevance Scoring

Each retrieved document is evaluated by the LLM.

Scoring range: **0 → 1**

  Score    Meaning
  -------- -------------------------
  ≥ 0.8    Highly relevant context
  ≥ 0.4    Partially relevant
  \< 0.4   Irrelevant

Routing behavior:

Complete Context → Strict RAG Answer\
Partial Context → Hybrid Answer\
Zero Context → Direct LLM Answer

------------------------------------------------------------------------

### 🔁 Self-Healing Answer Loop

After generating an answer, the system verifies whether the response
actually answers the query.

Query → Generate Answer → Answer Validator → Retry Retrieval (if
incorrect)

Maximum retries: **3 attempts**

------------------------------------------------------------------------

## 🏗 System Architecture

User Query\
↓\
LangGraph Decision Node\
↓\
Direct LLM Answer OR Vector Retrieval\
↓\
Pinecone Vector DB\
↓\
Context Relevance Scoring\
↓\
Answer Generation\
↓\
Answer Validation

------------------------------------------------------------------------

## 📂 Project Structure

project\
├── app.py\
├── graph.py\
├── utils\
│ ├── config.py\
│ └── retrieval.py\
├── requirements.txt\
├── Dockerfile

------------------------------------------------------------------------

## ⚙️ Environment Variables

Create a `.env` file:

OPENAI_API_KEY=your_openai_key\
PINECONE_API_KEY=your_pinecone_key\
PINECONE_INDEX=rag-index

------------------------------------------------------------------------

## ⚡ Local Installation

Clone repository

git clone https://github.com/adityanaranje/ISOLATED-RAG-CHATBOT \
cd isolated-rag-chatbot

Install dependencies

pip install -r requirements.txt

Run Streamlit

streamlit run input.py

Application runs at:

http://localhost:8501

------------------------------------------------------------------------

## 🐳 Docker Deployment

Build Image

docker build -t deltavenom/streamlit-rag-llm-ai-app .

Run Container

docker run -d -p 8501:8501 deltavenom/streamlit-rag-llm-ai-app

------------------------------------------------------------------------

## ☁️ Cloud Deployment

Architecture:

User\
↓\
Cloudflare DNS\
↓\
Nginx Reverse Proxy\
↓\
Docker Container\
↓\
Streamlit RAG App\
↓\
LangGraph + Pinecone

------------------------------------------------------------------------

## 🔄 Automatic Deployment

Deployment pipeline:

Local Development\
↓\
Docker Build\
↓\
Docker Hub Push\
↓\
Watchtower detects new image\
↓\
Container auto-updates on server

------------------------------------------------------------------------

## 👨‍💻 Author

Aditya Naranje

AI/ML Engineer building:

-   LLM Applications
-   Retrieval Augmented Generation systems
-   LangGraph based AI agents
-   Production AI deployments

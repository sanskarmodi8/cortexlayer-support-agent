# **CortexLayer — AI Support & Knowledge Bot**

> Private backend repository for CortexLayer's first commercial AI service: an RAG-based automated support system with document ingestion, vector search, chat API, usage limits, and optional channel integrations.

---

## 🚀 **1. Overview**

CortexLayer Chat Support is a production-ready backend powering our AI customer support service.

Clients upload their documents → the system ingests, chunks, embeds, and stores them → end-users interact through our chat widget or WhatsApp → responses are generated using a controlled RAG pipeline with citations.

This repository contains:

- FastAPI backend
- RAG engine
- Document ingestion pipeline
- Embeddings + Vector DB
- Usage tracking + plan enforcement
- Admin dashboard (basic)
- Embeddable chat widget
- Optional WhatsApp integration

---

## 🧠 **2. Service Features (Production Specifications)**

### **Starter Plan**

- Website-embedded chatbot
- Up to **10 documents**
- Up to **1,000 conversations/month**
- Standard RAG (chunk → embed → retrieve)
- Basic analytics (usage count, daily tracking)
- Email fallback
- Model: **Groq Mixtral-8x7B**
- Setup: **$399**, Monthly: **$79**

**Internal Limits**

- Max doc size: 5MB
- Max chunks per doc: 250
- Rate limit: 15 req/min

---

### **Growth Plan**

Everything in Starter plus:

- WhatsApp integration (Meta/Twilio)
- Up to **50 documents**
- Up to **5,000 conversations/month**
- Advanced analytics (latency, top queries, doc relevance)
- Team inbox (simple human handoff)
- Custom widget branding
- Model: Mixtral + GPT-4o-mini fallback
- Setup: **$899**, Monthly: **$199**

**Internal Limits**

- Max doc size: 10MB
- Max chunks/doc: 500
- Rate limit: 50 req/min
- Max WhatsApp messages: 2,000/mo

---

### **Scale Plan**

Everything in Growth plus:

- CRM integration (HubSpot/Zoho/REST)
- High-volume document capacity
- Per-client API keys
- Multilingual support
- Soft SLA: 99.5% uptime
- 3-month post-delivery support
- Model: **GPT-4o (primary) + Mixtral fallback**
- Setup: **$1,499**, Monthly: **$349**

**Internal Limits**

- Max file size: 20MB
- Max chunks: 3,000 per doc
- Soft usage cap: 50,000 chats/mo (post-cap throttling)
- Overages billed manually per contract
- Rate limit: 100 req/min

---

## 🏗️ **3. Architecture**

```
Client Documents
     ↓
Ingestion Pipeline (PDF → text → chunking)
     ↓
Embeddings (OpenAI/Groq + FAISS)
     ↓
Vector DB (FAISS local; optional Pinecone)
     ↓
Retriever + RAG Prompt Builder
     ↓
LLM Response (Groq/OpenAI)
     ↓
Client Widget / WhatsApp / API
     ↓
Analytics + Plan Enforcement
```

Stack:

- FastAPI
- FAISS
- Groq / OpenAI LLMs
- PostgreSQL
- Redis (sessions + rate limit)
- DigitalOcean Spaces (storage)
- Docker

---

## 📦 **4. Repository Structure**

```
cortexlayer-chat-support/
│
├── backend/
│   ├── app/
│   │   ├── main.py               # API entry
│   │   ├── routes/               # chat, upload, admin, analytics
│   │   ├── rag/                  # embeddings, retrieval, RAG
│   │   ├── ingestion/            # PDF/URL/TXT parsing
│   │   ├── services/             # utilities, auth, rate limiting
│   │   ├── models/               # DB + Pydantic schemas
│   │   └── core/                 # config & middleware
│   ├── tests/
│   └── Dockerfile
│
├── frontend/
│   ├── widget/                   # embeddable chat widget
│   └── admin/                    # admin dashboard (React)
│
├── scripts/                      # migrations, ingestion
├── infra/                        # docker-compose + deployment infra
└── README.md
```

---

## 🔐 **5. Security Notes**

- JWT authentication for admin & clients
- HTTPS required end-to-end
- All uploads sanitized
- Presigned S3 URLs for document uploads
- Strict CORS rules
- Redis-based per-client isolation

---

## ⚙️ **6. Environment Variables**

```
OPENAI_API_KEY=
GROQ_API_KEY=
DO_SPACES_KEY=
DO_SPACES_SECRET=
DATABASE_URL=
REDIS_URL=
JWT_SECRET=
PINECONE_API_KEY=
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
META_WHATSAPP_TOKEN=
```

---

## ▶️ **7. Running Locally**

With Docker:

```
docker-compose up --build
```

Or manual:

```
cd backend
uvicorn app.main:app --reload
```

---

## 🧪 **8. API Examples**

Upload document:

```
POST /upload
multipart/form-data: file=<document>
```

Query:

```
POST /query
{
  "query": "refund policy?",
  "client_id": "abc123"
}
```

Admin analytics:

```
GET /admin/analytics?client_id=abc123
```

---

## 📊 **9. Usage Tracking & Enforcement**

Each request triggers:

1. Check plan limits (daily + monthly)
2. Check conversations quota
3. Check doc quota
4. Throttle or deny if exceeded
5. Log usage in PostgreSQL

Prevents:

- misuse
- DDOS
- clients generating huge LLM bills

---

## 🗄️ **10. Data Retention**

- Conversations stored for 30 days
- Documents stored until client deletes
- We do NOT use data for model training
- Clients can request deletion anytime

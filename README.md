# 🧠 CIS — Content Intelligence Service

CIS (Content Intelligence Service) is a standalone AI microservice responsible for analyzing content and generating intelligent insights such as intent, urgency, summaries, and AI-drafted replies.

CIS acts as the **independent brain** for applications like **Coffer**, allowing AI logic to evolve without touching product code.

---

## 🚀 Version

**Current Version:** v1.0.0  
**Status:** Stable (Production Ready)  
**Architecture:** Microservice  
**Framework:** FastAPI  
**AI Model:** Google Gemini  
**Database:** MongoDB  

---

## 🎯 Why CIS Exists

Before CIS, AI logic lived inside application code, which caused:

- Tight coupling between AI and product releases
- Hard-to-iterate prompts
- Risky deployments for small AI changes

CIS solves this by:

- Centralizing AI intelligence
- Providing stable APIs
- Allowing independent AI evolution
- Supporting multiple clients with the same intelligence

---

## ✨ Core Features

### 🧠 Content Analysis
CIS analyzes content (currently emails) and returns:

- **Intent** — short, snake_case classification  
- **Urgency** — `low | medium | high`  
- **Summary** — one concise sentence  
- **Suggested Action** — a single, clean, UI-ready sentence  

### ✉️ AI Reply Drafting
- Context-aware reply generation
- Uses analysis results (intent, urgency, summary)
- Professional, human-sounding replies
- Plain-text output (no placeholders, no explanations)

### 🔄 Job-Based Processing
All AI operations run as asynchronous jobs:

- `pending`
- `completed`
- `failed`

Clients poll job status for reliability and fault tolerance.

---

## 🧱 Architecture Overview

Client (Coffer / Others)
|
v
CIS API (FastAPI)
|
v
Gemini AI Engine
|
v
MongoDB


---

## 🗄 Data Model (Analysis Job)

```json
{
  "job_id": "cis_xxxxxxxx",
  "status": "completed",
  "content_type": "email",
  "content": {
    "title": "Invoice overdue",
    "body": "Please clear the pending invoice"
  },
  "metadata": {
    "source": "gmail",
    "messageId": "xxxx"
  },
  "result": {
    "intent": "payment_followup",
    "urgency": "high",
    "summary": "Request to clear a pending invoice.",
    "suggested_action": "Review the invoice and proceed with payment."
  }
}

```

API Endpoints:
POST /analyze -- analyze content
GET /analysis/{jobId} -- check analysis status
POST /reply/draft -- create reply draft
GET /reply/draft/{jobId} -- check reply status


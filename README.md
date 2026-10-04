# 🤖 A2A Multi-Agent Customer Support System

> A self-evaluating multi-agent customer support system where independent AI agents communicate over HTTP, use their own LLMs, memory, tools, and endpoints, and continuously improve responses through an evaluator-driven feedback loop.

---

## 🌟 Overview

This project demonstrates a practical **Agent-to-Agent (A2A) multi-agent architecture** using Python, FastAPI, and locally running open-source LLMs through Ollama.

Instead of implementing multiple agents as functions inside a single application, every agent runs as an **independent service** with its own:

- 🧠 LLM
- 💾 Memory
- 🛠️ Tools
- 🌐 HTTP endpoint
- 🐍 Python process
- 🎯 Specialized responsibility

The agents communicate using structured A2A-style messages over HTTP.

An additional **Evaluator Agent** acts as a quality gate. It evaluates generated customer responses and sends feedback to the Response Agent when the response does not meet the required quality threshold.

---

## 🏗️ Architecture

```text
Customer
   │
   │ Complaint
   ▼
┌──────────────────────┐
│   Classifier Agent   │
│      Port 8001       │
└──────────┬───────────┘
           │
           │ A2A / HTTP
           ▼
┌──────────────────────┐
│   Resolution Agent   │
│      Port 8002       │
└──────────┬───────────┘
           │
           │ A2A / HTTP
           ▼
┌──────────────────────┐
│    Response Agent    │◄───────────────┐
│      Port 8003       │                │
└──────────┬───────────┘                │
           │                            │
           │ A2A / HTTP                 │ Feedback
           ▼                            │
┌──────────────────────┐                │
│   Evaluator Agent    │                │
│      Port 8004       │                │
└──────────┬───────────┘                │
           │                            │
      Score ≥ 0.85?                     │
        /       \                       │
      YES        NO ────────────────────┘
       │
       ▼
┌──────────────────────┐
│    Final Response    │
└──────────────────────┘
```

---

## 🧩 Agents

### 🟣 Classifier Agent — `:8001`

The Classifier Agent receives the original customer complaint and determines the type of issue.

Supported categories include:

```text
product_issue
refund_request
delivery_issue
general_question
```

Its classification result is sent to the Resolution Agent.

---

### 🔵 Resolution Agent — `:8002`

The Resolution Agent determines the appropriate next action based on:

- Customer complaint
- Classification
- Available company policy
- Resolution rules

Policies are provided through tools instead of allowing the LLM to freely invent business rules.

For example:

```text
Product Issue
     ↓
Check policy
     ↓
Recommend replacement eligibility review
```

The resulting recommendation is sent to the Response Agent.

---

### 🟢 Response Agent — `:8003`

The Response Agent converts the internal resolution into a polite customer-facing response.

It is instructed not to invent:

- Refund approvals
- Replacement approvals
- Delivery dates
- Warranty information
- Company policies
- Order information

The generated response is **not immediately returned to the customer**.

Instead, it is sent to the Evaluator Agent.

---

### 🟠 Evaluator Agent — `:8004`

The Evaluator Agent acts as an independent quality-control layer.

It evaluates the response across multiple dimensions:

| Metric | Weight |
|---|---:|
| Groundedness | 25% |
| Policy Compliance | 25% |
| Relevance | 20% |
| Completeness | 15% |
| Response Quality | 15% |

The weighted scores produce an overall evaluation score.

```text
Overall Score ≥ 0.85
        │
        ▼
      PASS
        │
        ▼
Return Final Response
```

If the response fails:

```text
Overall Score < 0.85
        │
        ▼
      FAIL
        │
        ▼
Generate Feedback
        │
        ▼
Response Agent
        │
        ▼
Regenerate Response
        │
        ▼
Evaluator
```

The retry loop is limited to prevent infinite agent interactions.

---

## ✨ Key Features

### 🔗 Independent Agent Communication

Agents communicate through HTTP instead of directly calling Python classes.

```text
Agent A
   │
   │ HTTP
   ▼
Agent B
```

This allows agents to run independently and potentially on different machines or containers.

### 🧠 Independent LLMs

Each agent can use a different model.

For example:

```env
CLASSIFIER_MODEL=llama3.2:1b
RESOLUTION_MODEL=llama3.2:3b
RESPONSE_MODEL=llama3.2:3b
EVALUATOR_MODEL=llama3.2:3b
```

This allows smaller models to handle simple tasks while stronger models handle reasoning or evaluation.

### 💾 Independent Memory

Every agent maintains its own memory.

```text
data/
├── classifier/
├── resolution/
├── response/
└── evaluator/
```

The current implementation uses lightweight JSON storage and can later be replaced with Redis, PostgreSQL, MongoDB, or a vector database.

### 🛠️ Agent-Specific Tools

Each agent can expose specialized tools.

```text
Classifier
└── Classification rules

Resolution
├── Policies
└── Business rules

Response
└── Response formatting

Evaluator
├── Scoring
├── Validation
└── Feedback generation
```

### 🔁 Self-Evaluation Loop

The Evaluator Agent can reject low-quality responses and send actionable feedback to the Response Agent.

This creates a simple:

```text
Generate → Evaluate → Improve → Re-evaluate
```

workflow.

### 🔒 Local LLM Support

The project uses **Ollama**, so the system can run with open-source models locally without requiring an OpenAI API key.

---

## 📁 Project Structure

```text
a2a-multi-agent-customer-support/
│
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
│
├── common/
│   ├── __init__.py
│   ├── a2a.py
│   ├── config.py
│   ├── llm.py
│   └── memory.py
│
├── agents/
│   ├── __init__.py
│   │
│   ├── classifier/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── agent.py
│   │   ├── memory.py
│   │   └── tools.py
│   │
│   ├── resolution/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── agent.py
│   │   ├── memory.py
│   │   └── tools.py
│   │
│   ├── response/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── agent.py
│   │   ├── memory.py
│   │   └── tools.py
│   │
│   └── evaluator/
│       ├── __init__.py
│       ├── main.py
│       ├── agent.py
│       ├── memory.py
│       └── tools.py
│
├── orchestrator/
│   ├── __init__.py
│   └── main.py
│
└── data/
    ├── classifier/
    ├── resolution/
    ├── response/
    └── evaluator/
```

---

## ⚙️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application |
| FastAPI | Agent HTTP services |
| Ollama | Local LLM runtime |
| Llama 3.2 | Default open-source LLM |
| HTTPX | Async agent communication |
| Pydantic | Structured A2A messages |
| JSON | Lightweight agent memory |
| Uvicorn | ASGI server |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd a2a-multi-agent-customer-support
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it.

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🦙 Install Ollama

Install Ollama on your machine and pull the required model:

```bash
ollama pull llama3.2
```

You can verify that the model works with:

```bash
ollama run llama3.2
```

---

## 🔧 Environment Configuration

Copy the example configuration:

```bash
cp .env.example .env
```

Example:

```env
OLLAMA_HOST=http://localhost:11434

CLASSIFIER_MODEL=llama3.2
RESOLUTION_MODEL=llama3.2
RESPONSE_MODEL=llama3.2
EVALUATOR_MODEL=llama3.2

CLASSIFIER_URL=http://localhost:8001
RESOLUTION_URL=http://localhost:8002
RESPONSE_URL=http://localhost:8003
EVALUATOR_URL=http://localhost:8004

EVALUATION_THRESHOLD=0.85
MAX_RETRIES=2
```

---

## ▶️ Running the System

Each agent runs as a separate process.

Open separate terminal windows.

### Terminal 1 — Classifier Agent

```bash
uvicorn agents.classifier.main:app --port 8001
```

### Terminal 2 — Resolution Agent

```bash
uvicorn agents.resolution.main:app --port 8002
```

### Terminal 3 — Response Agent

```bash
uvicorn agents.response.main:app --port 8003
```

### Terminal 4 — Evaluator Agent

```bash
uvicorn agents.evaluator.main:app --port 8004
```

### Terminal 5 — Orchestrator

```bash
python -m orchestrator.main
```

---

## 🧪 Example

Enter a customer complaint:

```text
My wireless mouse stopped working after five days.
I would like a replacement.
```

The request travels through:

```text
Customer
   ↓
Classifier
   ↓
product_issue
   ↓
Resolution
   ↓
Replacement eligibility review
   ↓
Response
   ↓
Evaluator
```

The evaluator might produce:

```text
Groundedness       0.95
Policy Compliance  0.95
Relevance          0.98
Completeness       0.90
Response Quality   0.92

Overall Score      0.945

Status             PASS
```

The approved response is then returned to the customer.

---

## 🔁 Example of the Feedback Loop

Suppose the Response Agent generates:

```text
Your replacement has been approved and
will arrive tomorrow.
```

Neither claim has been verified.

The Evaluator Agent can detect the unsupported claims:

```json
{
  "groundedness": 0.2,
  "policy_compliance": 0.3,
  "relevance": 0.9,
  "completeness": 0.8,
  "response_quality": 0.9,
  "issues": [
    "Replacement approval was not verified.",
    "Delivery date was not provided by any trusted source."
  ],
  "feedback": "Do not guarantee replacement approval or invent a delivery date."
}
```

The Response Agent receives the feedback and generates a safer response:

```text
Sorry to hear that your mouse stopped working.

We can review the product for replacement eligibility.
Please provide the relevant order details so the request
can be checked.
```

The revised response is evaluated again before being returned.

---

## 🌐 Agent Endpoints

| Agent | Port | Endpoint |
|---|---:|---|
| Classifier | 8001 | `/a2a` |
| Resolution | 8002 | `/a2a` |
| Response | 8003 | `/a2a` |
| Evaluator | 8004 | `/a2a` |

Each service also exposes an Agent Card:

```text
/.well-known/agent-card.json
```

Example:

```text
http://localhost:8001/.well-known/agent-card.json
```

---

## 🧠 Why an Evaluator Agent?

Adding another LLM does not automatically improve factual accuracy.

The Evaluator becomes useful when it evaluates responses against explicit constraints such as:

- Known policies
- Retrieved facts
- Business rules
- Grounding context
- Expected output criteria

For that reason, the architecture separates:

```text
Generation
    ↓
Ground Truth / Policies
    ↓
Evaluation
    ↓
Feedback
```

rather than simply asking another model whether an answer "looks good."

---

## ⚠️ Current Limitations

This repository is intended as an educational and experimental A2A architecture.

The current version:

- Uses JSON files for lightweight memory.
- Uses simple local policy tools.
- Uses an LLM-as-a-judge evaluator.
- Does not provide production authentication.
- Does not provide distributed tracing.
- Does not use a persistent production database.
- Does not guarantee that evaluation scores correspond to real-world accuracy.
- Implements a lightweight A2A-style communication layer rather than full protocol interoperability.

---

## 🛣️ Roadmap

Future improvements can include:

- [ ] Official A2A SDK integration
- [ ] Dynamic Agent Discovery
- [ ] Agent Registry
- [ ] PostgreSQL / Redis memory
- [ ] Vector database integration
- [ ] RAG-based policy retrieval
- [ ] RAGAS evaluation
- [ ] Real order database tools
- [ ] Human-in-the-loop escalation
- [ ] Structured LLM outputs
- [ ] Authentication between agents
- [ ] Docker support
- [ ] Docker Compose
- [ ] Kubernetes deployment
- [ ] OpenTelemetry tracing
- [ ] Prometheus metrics
- [ ] Evaluation dashboard
- [ ] Model comparison
- [ ] Prompt optimization
- [ ] Automated regression evaluation

---

## 🔮 Long-Term Vision

The project can evolve from a customer-support demo into a general-purpose **self-evaluating A2A platform**.

```text
                        A2A Platform
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
           ▼                 ▼                 ▼
     Agent Registry      Task Manager      Observability
           │
           ▼
     Agent Discovery
           │
    ┌──────┼──────┐
    ▼      ▼      ▼
 Agent A Agent B Agent C
    │      │      │
    ▼      ▼      ▼
  LLM    LLM    LLM
    │      │      │
 Tools  Tools  Tools
    │      │      │
Memory Memory Memory
           │
           ▼
      Evaluation Layer
           │
      ┌────┴────┐
      ▼         ▼
    PASS      Feedback
                │
                ▼
          Agent Optimization
```

This would allow multiple independent agents to be evaluated, compared, monitored, and improved through a centralized evaluation layer.

---

## 🤝 Contributing

Contributions are welcome.

If you have ideas for better agent communication, evaluation strategies, memory systems, tools, or A2A integrations, feel free to open an issue or submit a pull request.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐.

It helps others discover the project and encourages further development.

---

## 📄 License

This project is intended for educational and experimental use.

Add your preferred open-source license, such as the **MIT License**, before distributing or accepting external contributions.

---

<p align="center">
  <b>Built with Python • FastAPI • Ollama • Local LLMs • A2A Architecture</b>
</p>

<p align="center">
  Generate → Communicate → Evaluate → Improve
</p>
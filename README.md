# Virtual People Market Analysis

An AI-powered market research system that simulates consumer behavior using **five distinct virtual personas**. Each persona independently evaluates a product and estimates their purchase probability, then results are consolidated into a professional market research summary.

Built on [AgentField](https://agentfield.ai/docs) with Gemini 2.5 Flash via LiteLLM.

## How It Works

The system takes a natural-language product description (e.g. *"Premium wireless headphones for $299"*), parses it into structured data, fans it out to five demographically diverse AI personas, and consolidates their independent evaluations into a single research report.

```mermaid
flowchart TD
    A["User Input\n(product + price)"] --> B["entrypoint()\nLanguage Parser AI"]
    B --> C{"Extract\nproduct_description + price"}
    C --> D1["Persona 1\n22M Urban Tech"]
    C --> D2["Persona 2\n26F Artisan/Eco"]
    C --> D3["Persona 3\n45M Suburban DIY"]
    C --> D4["Persona 4\n48F High-End Fashion"]
    C --> D5["Persona 5\n65 Retiree/Craft"]
    D1 --> E["Consolidation AI\nMarket Research Presenter"]
    D2 --> E
    D3 --> E
    D4 --> E
    D5 --> E
    E --> F["Research Summary\n+ Recommendation"]
```

### Two-Stage AI Pipeline

```mermaid
sequenceDiagram
    participant U as User
    participant EP as Entrypoint
    participant P as Parser AI
    participant A1 as Persona 1
    participant A2 as Persona 2
    participant A3 as Persona 3
    participant A4 as Persona 4
    participant A5 as Persona 5
    participant C as Consolidator AI

    U->>EP: "Leather bag for $150"
    EP->>P: Extract product + price
    P-->>EP: {product: "Leather bag", price: 150}

    EP->>A1: Evaluate (product, price)
    EP->>A2: Evaluate (product, price)
    EP->>A3: Evaluate (product, price)
    EP->>A4: Evaluate (product, price)
    EP->>A5: Evaluate (product, price)

    A1-->>EP: {probability: 0.35, reasoning: "..."}
    A2-->>EP: {probability: 0.70, reasoning: "..."}
    A3-->>EP: {probability: 0.45, reasoning: "..."}
    A4-->>EP: {probability: 0.85, reasoning: "..."}
    A5-->>EP: {probability: 0.60, reasoning: "..."}

    EP->>C: Consolidate 5 results
    C-->>EP: Professional summary + recommendation
    EP-->>U: ResearchResults
```

## Virtual Personas

Each persona is a richly described consumer archetype that evaluates products through their own lens:

| Persona | Profile | Buying Style |
|---------|---------|--------------|
| **Agent 1** | 22M, urban (LA/NYC) | Tech-savvy, trend-driven, budget-conscious |
| **Agent 2** | 26F, artisan fair shopper | Sustainability-focused, supports small businesses |
| **Agent 3** | 45M, suburban homeowner (IL/OH) | Utility-driven, values long-term efficiency |
| **Agent 4** | 48F, East Coast boutique shopper | Quality over quantity, classic style, brand loyalty |
| **Agent 5** | 65, retiree at crafts market | Comfort and craftsmanship, heirloom quality |

Each returns a structured `PurchaseResults`:
- **probability** (0.0–1.0) — likelihood of purchase
- **reasoning** — explanation of their decision

## Architecture

```mermaid
graph LR
    subgraph AgentField["AgentField Server (:8080)"]
        CP[Control Plane]
    end

    subgraph Agent["Python Agent (auto-port)"]
        M[main.py\nAgent Config]
        R[reasoners.py\nBusiness Logic]
        M --> R
    end

    Client -->|"POST /api/v1/execute/\nmy-agent.demo_entrypoint"| CP
    CP -->|route| Agent
    Agent -->|"Gemini 2.5 Flash\n(via LiteLLM)"| LLM[Google AI]
    Agent -.->|observability notes| CP
```

## Quick Start

### Prerequisites
- Python 3.10+
- [AgentField CLI](https://agentfield.ai/docs) (`pip install agentfield`)
- A Gemini API key (or any LiteLLM-supported provider)

### Setup

```bash
# Clone and install
git clone <repo-url>
cd virtual_people_market_analysis
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add: GEMINI_API_KEY=your-key-here
```

### Run

```bash
# Terminal 1: Start the AgentField control plane
af server

# Terminal 2: Start the agent
python main.py
```

The agent auto-discovers an available port (starting from 8000) and registers with AgentField.

## API Usage

### Market Analysis (main endpoint)

```bash
curl -X POST http://localhost:8080/api/v1/execute/my-agent.demo_entrypoint \
  -H "Content-Type: application/json" \
  -d '{"input": {"message": "Premium leather messenger bag for $150"}}'
```

**Response:**
```json
{
  "summary": "Market research summary with consolidated findings from 5 personas and purchase recommendation..."
}
```

### Echo (health check, no AI required)

```bash
curl -X POST http://localhost:8080/api/v1/execute/my-agent.demo_echo \
  -H "Content-Type: application/json" \
  -d '{"input": {"message": "Hello World"}}'
```

## Project Structure

```
├── main.py              # Agent config, AI model setup, server startup
├── reasoners.py         # All reasoner functions (personas + orchestration)
├── requirements.txt     # Dependencies (agentfield)
└── .env.example         # Environment variable template
```

| File | Purpose |
|------|---------|
| `main.py` | Configures the Agent with node ID, AI model (Gemini 2.5 Flash), and temperature. Includes the reasoner router and starts the HTTP server. |
| `reasoners.py` | Defines the `entrypoint` orchestrator, 5 persona reasoners, Pydantic schemas (`PurchaseResults`, `PriceAndProductDescription`, `ResearchResults`), and observability hooks. |

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | [AgentField](https://agentfield.ai/docs) |
| AI Model | Gemini 2.5 Flash (via [LiteLLM](https://docs.litellm.ai/)) |
| Validation | [Pydantic](https://docs.pydantic.dev/) structured outputs |
| Runtime | Python 3.10+ with async/await |

## Learn More

- [AgentField Documentation](https://agentfield.ai/docs)
- [AgentField SDK Reference](https://agentfield.ai/docs/sdk)
- [LiteLLM Supported Providers](https://docs.litellm.ai/docs/providers)

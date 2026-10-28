# AI-Powered Shipping Customer Support Agent

## Overview

The **Shipping Customer Support Agent** is an AI-powered assistant built using Google's Agent Development Kit (ADK). It helps customers with shipping-related questions, including package tracking, shipping rates, delivery procedures, and returns.

The system first identifies whether a customer's question is related to shipping. Shipping-related questions are routed to a dedicated support agent, which can use tools to track packages and calculate shipping rates. Unrelated questions receive a predefined response explaining the agent's purpose.

The project demonstrates how AI agents, tool integration, and workflow-based routing can automate common customer support tasks.

## Features

- **Query Classification:** Uses Gemini to determine whether a customer query is shipping-related.
- **Package Tracking:** Uses the `track_package` tool to handle package tracking requests.
- **Shipping Rate Calculation:** Uses the `calculate_shipping_rates` tool to handle shipping cost queries.
- **Shipping FAQs:** Answers questions about delivery procedures, returns, and other shipping topics using simulated company information.
- **Intelligent Routing:** Directs requests to the appropriate workflow path based on their classification.
- **Out-of-Scope Handling:** Politely declines unrelated questions.
- **Workflow-Based Architecture:** Separates classification, routing, and response generation into distinct components.
- **Testing and Evaluation:** Supports local development, automated testing, and agent evaluation through the Agents CLI.

## How It Works

The application follows a workflow with four main components:

```text
             Customer Query
                   |
                   v
           classify_agent
          (Gemini Classifier)
                   |
                   v
        route_classification()
                   |
            +------+------+
            |             |
            v             v
       Shipping       Unrelated
            |             |
            v             v
   shipping_faq_agent  decline_node()
            |
       +----+----+
       |         |
       v         v
 Package       Shipping
 Tracking       Rates
       |         |
       v         v
  track_package  calculate_shipping_rates
       |
       v
 Customer Response
```

### Workflow Explanation

1. **Receive a query:** The customer submits a question.
2. **Classify the query:** `classify_agent` uses Gemini to determine whether the question concerns shipping.
3. **Route the request:** `route_classification()` selects the shipping or unrelated path.
4. **Handle the request:** `shipping_faq_agent` answers shipping questions and uses the appropriate tool when needed. `decline_node()` handles unrelated questions.
5. **Return a response:** The workflow provides the appropriate result to the customer.

## Example Use Cases

| Customer Query | Expected Behavior |
|---|---|
| "Where is my package?" | Routes to the shipping support agent, which can use the tracking tool. |
| "How much does delivery cost?" | Routes to the shipping support agent, which can use the rate calculation tool. |
| "What is your return policy?" | Provides an answer using simulated shipping company information. |
| "How do I prepare a parcel for shipping?" | Provides relevant shipping guidance. |
| "Can you teach me Java?" | Returns a predefined message declining the unrelated request. |

Actual tracking results and shipping rates depend on the implementation of the tools in `app/tools.py`.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and workflow functions |
| Google Gemini | Classifies customer queries and generates responses |
| Google Agent Development Kit (ADK) | Builds and orchestrates AI agents |
| Pydantic | Defines and validates the classification output schema |
| Google Cloud / Vertex AI | Provides the configured model execution environment |
| Agents CLI | Supports development, testing, evaluation, and deployment |
| uv | Python dependency and environment management |
| pytest | Automated testing |

## Project Structure

```text
Customer-support-agent/
├── app/
│   ├── agent.py             # Main workflow and agent configuration
│   └── app_utils/           # Application utilities
├── tests/                   # Unit, integration, and load tests
├── Dockerfile               # Container configuration
├── GEMINI.md                # AI-assisted development instructions
├── README.md                # Project documentation
├── agents-cli-manifest.yaml # Agents CLI project configuration
├── pyproject.toml           # Project dependencies and settings
└── uv.lock                  # Locked dependency versions
```

The `app/tools.py` module, imported by `agent.py`, contains or exposes the package tracking and shipping rate calculation tools.

## Prerequisites

Install the following tools:

- [Python](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- [Google Agents CLI](https://github.com/google/adk-python)

You also need a Google Cloud project with the necessary permissions and APIs enabled for the configured Gemini/Vertex AI setup.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/shritijjaiswal27-collab/Customer-support-agent.git
cd Customer-support-agent
```

### 2. Install the Agents CLI

```bash
uv tool install google-agents-cli
```

Initialize the development setup if required:

```bash
uvx google-agents-cli setup
```

### 3. Install Project Dependencies

```bash
agents-cli install
```

### 4. Configure Google Cloud

Authenticate with Google Cloud:

```bash
gcloud auth login
gcloud config set project YOUR_GCP_PROJECT_ID
```

Configure Application Default Credentials if required by your local execution setup:

```bash
gcloud auth application-default login
```

The application configures the Google Cloud location as `global` and enables Vertex AI usage through environment variables in `app/agent.py`.

Ensure that your Google Cloud project has the required permissions and model access.

### 5. Run the Agent Locally

Start the development playground:

```bash
agents-cli playground
```

Use the playground to submit customer questions and observe how the agent classifies and handles them.

## Testing and Evaluation

### Run Unit and Integration Tests

```bash
uv run pytest tests/unit tests/integration
```

### Run Code Quality Checks

```bash
agents-cli lint
```

### Evaluate Agent Behavior

The Agents CLI provides evaluation workflows for checking agent responses and identifying issues.

```bash
agents-cli eval generate
agents-cli eval grade
agents-cli eval analyze
```

These commands depend on the evaluation datasets and configuration available in the project.

## Configuration

The application uses Google Cloud authentication and the Gemini model through Vertex AI.

The main configuration is located in `app/agent.py`:

- `GOOGLE_CLOUD_PROJECT` identifies the Google Cloud project.
- `GOOGLE_CLOUD_LOCATION` is configured as `global`.
- `GOOGLE_GENAI_USE_VERTEXAI` is set to `True`.
- `gemini-flash-latest` is the model specified for query classification and the shipping support agent.

Keep credentials and sensitive configuration out of source control.

## Deployment

Configure the target Google Cloud project:

```bash
gcloud config set project YOUR_GCP_PROJECT_ID
```

Deploy the application using the Agents CLI:

```bash
agents-cli deploy
```

Review the deployment target, IAM permissions, model configuration, and expected costs before deployment. Follow the project's `GEMINI.md` deployment approval guidelines.

For additional infrastructure and CI/CD workflows, consult the supported Agents CLI commands and project configuration.

## Limitations

- The classifier distinguishes shipping-related queries from unrelated questions; it does not independently resolve customer issues.
- Actual tracking information and shipping rates depend on the underlying tool implementations.
- Delivery and return guidance uses simulated company information rather than a confirmed connection to a real shipping company's policy database.
- The current workflow does not establish that real refunds, shipment modifications, or human-agent transfers are supported.

## Future Improvements

- Integrate real courier APIs for live tracking.
- Connect to a shipping database for accurate delivery estimates and rate calculations.
- Add a knowledge base for company-specific shipping and return policies.
- Introduce human-agent escalation for complex cases.
- Add conversation history for contextual follow-up questions.
- Expand evaluation datasets to measure classification accuracy and response quality.
- Add structured logging, monitoring, and production-ready error handling.

## Author

**Shritij Jaiswal**

GitHub: [shritijjaiswal27-collab](https://github.com/shritijjaiswal27-collab)

Repository: [Customer-support-agent](https://github.com/shritijjaiswal27-collab/Customer-support-agent)

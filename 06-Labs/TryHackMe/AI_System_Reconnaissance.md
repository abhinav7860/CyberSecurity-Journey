# AI System Reconnaissance

> **Platform:** TryHackMe
>
> **Room:** AI System Reconnaissance

---

# Overview

Modern AI applications introduce entirely new infrastructure into an organization's network. Unlike traditional web applications, AI deployments include model servers, experiment trackers, vector databases, notebook servers, object storage, and monitoring services.

Traditional reconnaissance tools such as **Nmap** and **curl** are still useful, but security professionals must understand what AI services look like, where they run, and what information they expose.

This room focuses on identifying AI infrastructure from a defender's perspective and understanding how attackers discover exposed AI systems.

---

# Scenario

You are a security engineer at **Cyphira**, a fintech company that recently deployed several AI-powered services without a security review.

Your CISO wants to know:

- What AI services exist?
- What information do they expose?
- How could an attacker discover them?

The objective is **not to exploit systems**, but to identify and enumerate AI infrastructure before attackers do.

---

# Learning Objectives

By the end of this room, you should be able to:

- Identify common AI/ML infrastructure components.
- Recognize the ports and protocols used by AI services.
- Fingerprint AI services using HTTP responses and API endpoints.
- Enumerate metadata from exposed AI platforms.
- Understand how AI infrastructure expands the attack surface.
- Detect reconnaissance activity targeting AI deployments.

---

# What is AI Reconnaissance?

AI reconnaissance is the process of discovering AI infrastructure and identifying what information it exposes.

Unlike traditional network reconnaissance, the focus is no longer limited to:

- Web Servers
- SSH
- Databases

Instead, attackers search for AI-specific services such as:

- Model servers
- Experiment tracking platforms
- Vector databases
- Notebook servers
- Object storage
- Monitoring endpoints

Traditional service detection often misses these components because it was designed before modern AI infrastructure became common.

---

# Why AI Reconnaissance Matters

AI services are increasingly exposed to the internet.

According to the room:

- A Shodan scan discovered **42,665 exposed AI agent instances**.
- **93.4%** of them were vulnerable.
- Many leaked API keys through unauthenticated access.
- GreyNoise observed over **91,000 AI-focused attack sessions** within three months.

Attackers are actively searching for exposed AI infrastructure.

---

# Questions This Room Answers

- What does AI infrastructure look like?
- Which ports identify AI services?
- How can AI services be fingerprinted?
- What information can be collected using simple tools like `curl`?
- How do attackers discover AI systems at scale?

---

# Task 2 – The AI Infrastructure Stack

## Understanding the AI Stack

A production AI system is rarely a single server.

Instead, it consists of multiple specialized services responsible for different stages of the machine learning lifecycle.

Each component exposes its own ports, APIs, and protocols, increasing the overall attack surface.

---

# 1. Model Serving Endpoints

These services load trained models into memory and provide prediction APIs.

They are usually the first target during reconnaissance because they directly expose machine learning models.

## Common Frameworks

### NVIDIA Triton

Ports:

- 8000 (HTTP)
- 8001 (gRPC)
- 8002 (Prometheus Metrics)

Recon Endpoints

```
/v2/health/ready
/v2/models
```

---

### TensorFlow Serving

Ports

- 8500 (gRPC)
- 8501 (HTTP)

Recon Endpoint

```
/v1/models/<model-name>
```

---

### TorchServe

Ports

- 8080
- 8081
- 8082

Recon Endpoints

```
/ping
/models
```

---

### Ollama

Port

```
11434
```

Recon Endpoints

```
/api/tags
/api/show
```

---

### vLLM

Port

```
8000
```

Recon Endpoint

```
/v1/models
```

---

## Why HTTP and gRPC?

Many AI platforms expose both protocols.

**HTTP**

- Easier for applications to consume
- REST-based communication

**gRPC**

- Faster communication
- Better for transferring large tensors
- Common for internal AI services

---

# 2. Orchestration & Experiment Tracking

These platforms manage the complete machine learning lifecycle.

They are valuable reconnaissance targets because they contain:

- Experiments
- Hyperparameters
- Metrics
- Model artifacts
- Deployment history

## MLflow

Port

```
5000
```

Stores

- Experiments
- Metrics
- Hyperparameters
- Model versions

If an MLflow server is publicly accessible, an attacker may gain insight into the organization's entire AI development process.

---

## Kubeflow

Runs on Kubernetes.

Ports

- 80
- 443

Responsible for

- ML pipelines
- Notebook servers
- Model deployment

---

## Ray

Dashboard Port

```
8265
```

Server

```
8000
```

The **ShadowRay** campaign specifically targeted exposed Ray dashboards.

---

# 3. Vector Databases

Vector databases store embeddings used by Retrieval-Augmented Generation (RAG) systems.

If an organization operates an AI chatbot, it likely has a vector database behind it.

Common products include:

| Database | Port |
|----------|------|
| Qdrant | 6333 / 6334 |
| Weaviate | 8080 |
| Milvus | 19530 |
| Chroma | 8000 |

Schema endpoints often reveal:

- Embedding model
- Collection names
- Stored data categories

Even collection names like:

```
internal-hr-policies
```

can provide valuable intelligence during reconnaissance.

---

# 4. Model Registries

A model registry stores:

- Serialized model files
- Version history
- Deployment stages
- Artifact locations
- Creator information

Common model formats include:

- `.pkl`
- `.pt`
- `.onnx`
- `.mar`

An exposed model registry provides attackers with a complete inventory of an organization's AI models.

---

# 5. Supporting Infrastructure

## Jupyter Notebook

Port

```
8888
```

Risks

- No authentication
- Remote terminal access
- Hardcoded credentials inside notebooks

---

## MinIO

Ports

```
9000
9001
```

Purpose

- S3-compatible object storage
- Stores datasets and model artifacts

---

## Prometheus Metrics

Common Ports

- 8002
- 8082

Metrics may reveal:

- Model names
- GPU utilization
- Batch sizes
- Inference latency

This information helps attackers map AI deployments without interacting with inference APIs.

---

# AI Infrastructure Port Reference

| Component | Default Ports |
|------------|--------------|
| NVIDIA Triton | 8000, 8001, 8002 |
| TensorFlow Serving | 8500, 8501 |
| TorchServe | 8080, 8081, 8082 |
| Ollama | 11434 |
| vLLM | 8000 |
| MLflow | 5000 |
| Kubeflow | 80, 443 |
| Ray | 8265, 8000 |
| Qdrant | 6333, 6334 |
| Weaviate | 8080 |
| Milvus | 19530 |
| Jupyter Notebook | 8888 |
| MinIO | 9000, 9001 |
| Prometheus Metrics | 8002, 8082 |

> AI infrastructure introduces **14+ components across more than 20 network ports**, significantly expanding the attack surface compared to traditional applications.

---

# Case Study – Exposed AI Infrastructure

Researchers discovered thousands of publicly exposed AI services.

Common findings included:

- Open MLflow dashboards
- Unauthenticated Jupyter notebooks
- Exposed Ray dashboards
- Triton inference servers

Many compromised environments shared a similar pattern:

```
Jupyter Notebook
        │
        ▼
MLflow Credentials
        │
        ▼
MLflow Server
        │
        ▼
Model Registry
        │
        ▼
S3 Storage
```

Once one component was compromised, attackers could often access the rest of the AI infrastructure.

---

# Common Shodan Queries

Find exposed MLflow servers

```
port:5000 "MLflow"
```

Find Jupyter notebooks

```
port:8888 title:"Home Page - Select or create a notebook"
```

Find Ray dashboards

```
http.title:"Ray Dashboard"
```

Find Triton servers

```
port:8001 "triton"
```

---

---

# Task 3 – Fingerprinting AI Services

## Overview

In Task 2, we learned where AI services usually run and which ports they expose.

Finding an open port is only the first step.

The next objective is to identify **what AI framework is actually running** behind that port.

Traditional service detection tools like:

- Nmap (`-sV`)
- Banner grabbing

often identify AI services as generic HTTP servers and fail to recognize the underlying AI framework.

Instead, AI fingerprinting focuses on analyzing:

- HTTP response headers
- JSON response structures
- Error messages
- Endpoint naming conventions
- gRPC services
- TLS fingerprints

---

# What is AI Fingerprinting?

AI fingerprinting is the process of identifying AI services by examining how they respond to requests.

Unlike normal web applications, AI frameworks expose unique identifiers that make them relatively easy to recognize.

These identifiers include:

- Custom HTTP headers
- API response formats
- Error messages
- API endpoint names
- gRPC reflection services

---

# 1. HTTP Header Fingerprinting

HTTP response headers are one of the quickest ways to identify an AI framework.

Many AI platforms advertise their identity unless administrators intentionally hide them behind a reverse proxy.

## Common HTTP Headers

### TorchServe

```
Server: TorchServe/0.x.x
```

Immediately identifies the service as TorchServe.

---

### NVIDIA Triton

Unique Header

```
NV-Status
```

Example

```http
HTTP/1.1 200 OK
NV-Status: OK
Content-Type: application/json
```

Unlike other frameworks, Triton can also return hardware telemetry when queried with specific request headers.

---

### FastAPI-based ML APIs

Header

```
Server: uvicorn
```

Common AI routes:

```
/predict
/embeddings
```

Usually indicates a Python-based ML application.

---

### OpenAI-Compatible APIs

Common products:

- vLLM
- LiteLLM
- Ollama

Typical response headers include:

```
x-request-id
```

---

# 2. API Response Fingerprinting

Different AI frameworks return different JSON structures.

These structures can identify the framework without needing access to the server itself.

---

## TensorFlow Serving

Example

```json
{
  "model_version_status": [
    {
      "version":"1",
      "state":"AVAILABLE"
    }
  ]
}
```

---

## Triton

Example

```json
{
  "name":"fraud_detector",
  "versions":["1"],
  "platform":"tensorflow_graphdef"
}
```

The **platform** field reveals which ML framework created the model.

---

## OpenAI-Compatible APIs

Example

```json
{
  "object":"model",
  "id":"llama-3.1-8b"
}
```

If `"object":"model"` appears, the API most likely follows the OpenAI specification.

---

# 3. Error Message Fingerprinting

One of the most reliable fingerprinting methods is intentionally sending malformed requests.

AI inference servers produce detailed error messages that reveal:

- Expected tensor shapes
- Data types
- Internal framework names
- File paths
- Stack traces

Traditional web applications usually hide these details.

---

## Examples

TensorFlow Serving

```
tensorinfo_map
```

appears inside its error messages.

---

MLflow

Stack traces reference:

```
mlflow.server
mlflow.tracking
```

---

Databricks Mosaic AI

May return Java exceptions such as:

```
IncorrectClaimException
```

---

# 4. Endpoint Naming Conventions

AI APIs expose endpoints that differ from traditional REST applications.

Instead of:

```
/users
/products
/accounts
```

AI applications commonly expose:

Inference

```
/predict
/infer
/generate
/score
/embeddings
/invocations
```

Model Management

```
/v1/models
/v2/models
```

MLflow

```
/api/2.0/mlflow/
```

Kubeflow

```
/pipeline/apis/v1beta1/
```

These paths are useful additions to tools like:

- ffuf
- feroxbuster

---

# 5. gRPC Fingerprinting

Many AI services expose gRPC alongside HTTP.

Examples

| Framework | Port |
|-----------|------|
| Triton | 8001 |
| TensorFlow Serving | 8500 |

Normal HTTP scanners cannot enumerate these services.

Instead, use:

```bash
grpcurl
```

Example

```bash
grpcurl -plaintext target:8001 list
```

If reflection is enabled, grpcurl can list every available service.

Example

```bash
grpcurl -plaintext target:8001 describe inference.GRPCInferenceService
```

This reveals:

- RPC methods
- Input tensors
- Output tensors
- API schema

Think of it as the gRPC equivalent of an OpenAPI specification.

---

# 6. TLS Fingerprinting

AI infrastructure also has recognizable TLS behavior.

Frameworks often use:

- Python requests
- urllib
- gRPC libraries

Instead of browser traffic.

Security teams use:

- JA3
- JA4

fingerprints to distinguish AI traffic from normal user activity.

---

# Case Study – GreyNoise AI Reconnaissance

Between October 2025 and January 2026, GreyNoise observed:

- 91,000+ reconnaissance sessions
- 80,000+ requests over 11 days
- 73 different LLM endpoints targeted

Attackers probed models including:

- GPT
- Claude
- Gemini
- Llama
- Mistral
- DeepSeek
- Qwen
- Grok

Instead of exploiting systems, they simply sent harmless prompts like:

```
hi
```

```
How many states are there in the United States?
```

```
How many letter 'r' are in the word strawberry?
```

The responses helped identify:

- Model type
- API format
- Proxy configuration
- Backend framework

This demonstrates that reconnaissance alone can reveal valuable intelligence.

---

# Practical Exercise

## Step 1 – Check HTTP Headers

```bash
curl -v http://10.10.45.12:5000/
```

Output

```http
HTTP/1.1 200 OK
Server: Werkzeug/3.0.1 Python/3.11.7
Content-Type: text/html
```

This indicates the service is running on a Python Werkzeug web server.

---

## Step 2 – Enumerate Models

```bash
curl http://10.10.45.15:8000/v2/models
```

Output

```json
{
  "models":[
    {
      "name":"fraud_detector",
      "version":"3",
      "state":"READY",
      "platform":"pytorch_libtorch"
    },
    {
      "name":"text_embedder",
      "version":"2",
      "state":"READY",
      "platform":"onnxruntime"
    }
  ]
}
```

The **platform** field identifies the framework used by each deployed model.

---

## Step 3 – Trigger an Error

```bash
curl -X POST http://10.10.45.15:8000/v2/models/fraud_detector/infer \
-d '{"bad":"data"}'
```

Output

```json
{
 "error":"expected input tensor 'transaction_features' shape [1,47] dtype FP32",
 "details":"parse error at line 1"
}
```

The detailed tensor information confirms the endpoint is an AI inference service.

---

## Step 4 – Check gRPC Reflection

```bash
grpcurl -plaintext 10.10.45.15:8001 list
```

Output

```
inference.GRPCInferenceService
grpc.health.v1.Health
grpc.reflection.v1alpha.ServerReflection
```

Reflection exposes the available gRPC services without prior knowledge.

---

## Step 5 – Probe Other AI Components

### Vector Database

```bash
curl http://10.10.45.18:6333/collections
```

Output

```json
{
 "result":{
   "collections":[
     {"name":"internal-kb-embeddings"},
     {"name":"customer-support-tickets"}
   ]
 }
}
```

Collection names can reveal the purpose of an organization's AI systems.

---

### NVIDIA Header Check

```bash
curl -v http://10.10.45.15:8000
```

Output

```http
HTTP/1.1 200 OK
NV-Status: OK
Content-Type: application/json
```

The **NV-Status** header uniquely identifies the service as **NVIDIA Triton Inference Server**.

---

# Commands Used

```bash
curl -v http://10.10.45.12:5000/

curl http://10.10.45.15:8000/v2/models

curl -X POST http://10.10.45.15:8000/v2/models/fraud_detector/infer \
-d '{"bad":"data"}'

grpcurl -plaintext 10.10.45.15:8001 list

curl http://10.10.45.18:6333/collections

curl -v http://10.10.45.15:8000
```

---

---

# Task 4 – Enumerating AI Systems

## Overview

After identifying AI services in Task 3, the next step is **enumeration**.

Fingerprinting tells us **what** a service is.

Enumeration tells us **what information it exposes**.

For example:

- Fingerprinting identifies an MLflow server.
- Enumeration reveals:
  - Experiments
  - Registered models
  - Artifact storage locations
  - Production models
  - Model creators
  - Hyperparameters
  - Training metrics

This stage transforms basic reconnaissance into actionable intelligence.

---

# MLflow Enumeration

MLflow is one of the most valuable AI services to enumerate because it stores nearly every aspect of the machine learning lifecycle.

A few REST API requests can reveal an organization's entire AI portfolio.

---

## Step 1 – List Experiments

Endpoint

```http
POST /api/2.0/mlflow/experiments/search
```

Purpose

- Lists every experiment
- Experiment IDs
- Experiment names
- Lifecycle status

Example

```json
{
  "experiments":[
    {
      "experiment_id":"1",
      "name":"fraud-detection-prod"
    }
  ]
}
```

Experiment names often reveal:

- Internal projects
- Business goals
- Product names

---

## Step 2 – List Registered Models

Endpoint

```http
GET /api/2.0/mlflow/registered-models/list
```

Purpose

Returns:

- Model names
- Versions
- Current deployment stage

Example

```json
{
  "name":"fraud-classifier",
  "current_stage":"Production"
}
```

---

## Step 3 – Model Version Details

Endpoint

```http
GET /api/2.0/mlflow/model-versions/search
```

This endpoint contains some of the most valuable intelligence.

Information includes:

- Artifact URI
- Model version
- Creator
- Creation time
- Deployment stage
- Tags

Example artifact location

```
s3://internal-ml-models/model.pkl
```

This reveals where model files are stored.

---

## Step 4 – Search Training Runs

Endpoint

```http
POST /api/2.0/mlflow/runs/search
```

Returns:

- Hyperparameters
- Training metrics
- Tags
- Git commit hashes
- Deployment environments

---

## Step 5 – List Artifacts

Endpoint

```http
GET /api/2.0/mlflow/artifacts/list
```

Lists downloadable model files stored by MLflow.

---

# Enumerating Inference Servers

Inference servers expose metadata describing exactly how clients should communicate with models.

---

## Triton

Endpoint

```http
GET /v2/models/<model>/config
```

Returns

- Input tensor names
- Shapes
- Data types
- Backend framework
- Maximum batch size

Example

```json
{
  "inputs":[
    {
      "name":"transaction_features",
      "datatype":"FP32",
      "shape":[1,47]
    }
  ]
}
```

This tells clients exactly how to build valid inference requests.

---

## TensorFlow Serving

Endpoint

```http
GET /v1/models/<model>/metadata
```

Returns

- Input tensors
- Output tensors
- Shapes
- Data types

---

# Enumerating Vector Databases

Vector databases reveal the data powering AI systems.

---

## Weaviate

Useful Endpoints

```http
GET /v1/meta
```

Returns

- Version
- Installed modules

---

```http
GET /v1/schema
```

Returns

- Collections
- Properties
- Embedding model

---

```http
GET /v1/graphql
```

Allows schema discovery and querying if authentication is disabled.

---

## Qdrant

Endpoints

```http
GET /collections
```

Lists all collections.

---

```http
GET /collections/<name>
```

Returns

- Vector dimensions
- Distance metric
- Point count

Example

```
Collection:
internal-hr-policies

Dimensions:
768

Points:
50,000
```

This provides valuable insight into the organization's RAG pipeline.

---

## Chroma

Older versions expose

```http
GET /api/v1/collections
```

without authentication.

---

# Prometheus Metrics

Many AI platforms expose metrics endpoints.

Common ports

- Triton → 8002
- TorchServe → 8082

Typical information exposed

- Model names
- Versions
- GPU utilization
- Request counts
- Latency
- Batch sizes

This allows attackers to understand deployment behavior without querying the inference API.

---

# Debug Interfaces

Many AI frameworks expose developer interfaces.

---

## FastAPI

Automatically generates

```
/docs
```

and

```
/openapi.json
```

These reveal:

- Endpoints
- Request schemas
- Response schemas
- Authentication methods

---

## MLflow

Historically exposed

```
/graphql
```

which could reveal:

- Internal usernames
- Source code paths
- Project information

---

Appending

```
?debug=true
```

or

```
?verbose=1
```

sometimes exposes:

- Stack traces
- Library versions
- Filesystem paths
- Configuration details

---

# Jupyter Notebook Enumeration

Endpoint

```http
GET /api/kernels
```

Returns

- Kernel IDs
- Running notebooks
- Last activity

The real value comes from notebook contents.

Developers often leave:

- MLflow credentials
- AWS keys
- Hugging Face tokens
- API keys

inside notebook cells.

---

# Case Study – IBM X-Force ML Attack Chain

IBM X-Force documented an attack demonstrating how multiple AI services can be chained together.

Attack flow

```
Phishing
      │
      ▼
Azure ML
      │
      ▼
Jupyter Notebook
      │
      ▼
MLflow Credentials
      │
      ▼
MLflow Tracking Server
      │
      ▼
Model Registry
      │
      ▼
S3 Model Storage
```

IBM developed **MLOKit**, a CLI tool capable of automating MLflow enumeration.

Functions included:

- list-models
- download-model
- list-notebooks
- add-notebook-trigger
- poison-model

The attack succeeded because trusted services shared credentials, not because of a software vulnerability.

---

# Practical Exercise

## Step 1 – Enumerate MLflow Experiments

```bash
curl -X POST \
http://10.10.45.12:5000/api/2.0/mlflow/experiments/search \
-H "Content-Type: application/json" \
-d '{}'
```

Output

```json
{
 "experiments":[
  {
   "experiment_id":"1",
   "name":"fraud-detection-prod"
  },
  {
   "experiment_id":"2",
   "name":"rag-embeddings-tuning"
  },
  {
   "experiment_id":"3",
   "name":"customer-churn-prototype"
  },
  {
   "experiment_id":"4",
   "name":"ab-test-recommendation-engine"
  }
 ]
}
```

---

## Step 2 – Registered Models

```bash
curl \
http://10.10.45.12:5000/api/2.0/mlflow/registered-models/list
```

Output

| Model | Stage |
|---------|------------|
| cyphira-fraud-classifier | Production |
| internal-kb-embedder | Staging |
| churn-predictor | Archived |

---

## Step 3 – Model Version Information

```bash
curl \
http://10.10.45.12:5000/api/2.0/mlflow/model-versions/search
```

Important findings

- Artifact locations
- Model creators
- Git commit hashes
- Deployment environments

Example

```
Artifact

s3://cyphira-ml-models/fraud-detection/v3/model.pkl
```

Created by

```
j.chen@cyphira.io
```

---

## Step 4 – Triton Model Configuration

```bash
curl \
http://10.10.45.15:8000/v2/models/fraud_detector/config
```

Output

```json
{
 "platform":"pytorch_libtorch",
 "inputs":[
  {
   "name":"transaction_features",
   "datatype":"FP32",
   "shape":[1,47]
  }
 ],
 "max_batch_size":64
}
```

This reveals the exact format expected for inference requests.

---

## Step 5 – Enumerate Qdrant

```bash
curl \
http://10.10.45.18:6333/collections/internal-kb-embeddings
```

Output

```json
{
 "vectors":{
   "size":384,
   "distance":"Cosine"
 },
 "points_count":127843
}
```

Payload schema

- document_title
- department
- sensitivity_level
- last_updated

These fields reveal the structure of indexed organizational documents.

---

## Step 6 – Enumerate Jupyter

```bash
curl \
http://10.10.45.20:8888/api/contents
```

Discovered notebooks

- fraud_model_training.ipynb
- rag_pipeline_debug.ipynb
- data_exploration.ipynb

The most recently modified notebook contained the MLflow service account password:

```
Cyphira-MLfl0w-2024!
```

This demonstrates why unsecured Jupyter notebooks are considered one of the highest-risk AI services.

---

# Commands Used

```bash
curl -X POST http://10.10.45.12:5000/api/2.0/mlflow/experiments/search \
-H "Content-Type: application/json" -d '{}'

curl http://10.10.45.12:5000/api/2.0/mlflow/registered-models/list

curl http://10.10.45.12:5000/api/2.0/mlflow/model-versions/search

curl http://10.10.45.15:8000/v2/models/fraud_detector/config

curl http://10.10.45.18:6333/collections/internal-kb-embeddings

curl http://10.10.45.20:8888/api/contents
```

---

---

# Task 5 – Mapping the AI Attack Surface

## Overview

So far, we have:

- Identified AI services on the network.
- Fingerprinted the framework running behind each service.
- Enumerated valuable metadata from those services.

The final step is connecting all of those findings together.

Finding an exposed MLflow server is useful.

Understanding how that MLflow server connects to Jupyter notebooks, model registries, object storage, vector databases, and inference servers is what creates a complete **AI attack surface map**.

---

# Understanding the AI Attack Surface

Traditional web applications usually expose only a handful of services.

Example:

- Web Server
- Database
- SSH
- Reverse Proxy

Modern AI deployments are much more interconnected.

Example communication flow:

```
Jupyter Notebook
        │
        ▼
 MLflow Tracking
        │
        ▼
 Model Registry
        │
        ▼
Inference Server
        │
        ▼
Vector Database
        │
        ▼
Prometheus Metrics
```

Every service continuously exchanges information with the others.

If one component becomes exposed, attackers may gain access to the entire AI environment.

---

# How AI Expands the Attack Surface

Unlike traditional applications, AI infrastructure contains many interconnected services.

Examples include:

- Model Serving Platforms
- Experiment Tracking Servers
- Model Registries
- Vector Databases
- Notebook Servers
- Object Storage
- Monitoring Services

These services often communicate without strong internal security controls.

Common problems include:

- Services listening on `0.0.0.0`
- Missing mutual TLS (mTLS)
- Overly permissive firewall rules
- Excessive trust between internal services

Compromising one service can expose the rest of the infrastructure.

---

# Common Platform Misconfigurations

Many AI platforms have configuration issues that attackers actively search for.

---

## MLflow

Earlier versions of MLflow shipped without authentication enabled.

Important issues discussed in the room include:

- Default authentication credentials
- Directory traversal vulnerabilities
- Remote Code Execution (RCE)

These issues made publicly exposed MLflow servers attractive reconnaissance targets.

---

## Kubeflow

Common issues include:

- No OIDC authentication
- Public Kubernetes LoadBalancer exposure
- Direct access to Jupyter notebooks

If exposed, attackers may gain access to Kubernetes service accounts with elevated permissions.

---

## TorchServe

Management API

```
Port 8081
```

Supports dynamic model loading.

If accessible, attackers could instruct TorchServe to download malicious `.mar` model archives from external servers.

Because initialization code executes during model loading, this may lead to Remote Code Execution.

---

## SageMaker Notebooks

When configured with:

```
DirectInternetAccess = Enabled
```

notebooks become reachable from the public Internet.

This significantly increases the attack surface.

---

# Why Model Registries Matter

Model registries are one of the highest-value reconnaissance targets.

They store much more than model files.

Typical information includes:

- Model names
- Version history
- Deployment stages
- Creation timestamps
- Training run IDs
- Artifact storage locations
- Contributor identities

Example

```
MLflow Registry
      │
      ▼
Model Version
      │
      ▼
Artifact URI
      │
      ▼
S3 Storage
```

An exposed registry effectively maps an organization's complete AI portfolio.

---

# Supply Chain Reconnaissance

Modern AI systems rely heavily on external resources.

Attackers search for exposed dependencies and credentials.

Examples include:

- Hugging Face API Tokens
- GitHub repositories
- `.env` files
- CI/CD logs
- Kubernetes Secrets

---

## Dependency Confusion

AI projects often contain internal Python packages.

Example

```
company-data-utils
```

If this package is not published publicly, an attacker can register it on PyPI.

Training pipelines that automatically install dependencies may unknowingly execute malicious code.

---

## Model Download Sources

Configuration files often reveal where models originate.

Common sources include:

- Hugging Face Hub
- PyTorch Hub

Compromising upstream model repositories or leaked Hugging Face tokens could poison the entire ML supply chain.

---

# MITRE ATLAS

MITRE ATLAS is the AI equivalent of the MITRE ATT&CK framework.

It focuses specifically on attacks targeting Machine Learning systems.

According to the room:

- 15 Tactics
- 66 Techniques
- 46 Sub-techniques

---

## ATLAS Mapping

| Activity | ATLAS Technique |
|-----------|----------------|
| Scanning AI services | AML.T0006 – Active Scanning |
| Discovering ML artifacts | AML.T0007 – Discover ML Artifacts |
| Supply chain reconnaissance | AML.T0010 – ML Supply Chain Compromise |
| Discovering AI model families | AML.T0014 – Discover ML Model Family |
| Overall Reconnaissance | AML.TA0002 – Reconnaissance |

Using ATLAS identifiers provides a standardized way to document AI security findings.

---

# Case Study – ShadowRay Campaign

The ShadowRay campaign demonstrates how reconnaissance alone can lead to full infrastructure compromise.

Attack chain

```
Internet
      │
      ▼
Shodan Search
      │
      ▼
Exposed Ray Dashboard
      │
      ▼
Job Submission API
      │
      ▼
System Enumeration
      │
      ▼
Credential Theft
      │
      ▼
Cloud Access
      │
      ▼
GPU Hijacking
      │
      ▼
Cryptomining
```

---

## Initial Access

Attackers searched Shodan for publicly exposed Ray dashboards.

Over **230,000** exposed instances were discovered.

---

## Reconnaissance

Once inside the dashboard, attackers gathered information by reading files such as:

```
/etc/passwd
```

They also collected environment variables using commands like:

```
printenv
```

This revealed cloud credentials and IAM tokens.

---

## Lateral Movement

Using stolen credentials, attackers moved throughout the victim's cloud environment.

---

## Resource Hijacking

The attackers deployed cryptocurrency miners.

To remain undetected, they:

- Limited CPU usage
- Disguised processes as Linux kernel workers

---

## ShadowRay 2.0

Later versions became more advanced.

New capabilities included:

- AI-generated malware payloads
- Persistence through cron jobs
- Persistence using systemd services
- GitLab and GitHub payload hosting
- Sockstress attacks
- Botnet functionality

---

# Why This Case Study Matters

Everything used in ShadowRay began with reconnaissance.

The attack followed the same steps practiced in this room:

1. Discover exposed AI services.
2. Fingerprint the framework.
3. Enumerate available information.
4. Exploit weak configurations.
5. Expand access through trusted relationships.

Reconnaissance alone provided enough intelligence to compromise an entire AI environment.

---

# Practical Exercise

The Cyphira Threat Mapper combined all findings from the previous tasks and mapped them to MITRE ATLAS techniques.

---

## Question 1

Finding

- Hugging Face Token discovered inside a Jupyter Notebook.
- MLflow referenced external Hugging Face models.

Correct Mapping

```
AML.T0010
```

**Technique:** ML Supply Chain Compromise

---

## Question 2

Activities performed

- Nmap scanning
- curl enumeration
- MLflow metadata extraction

These all belong to the same ATLAS tactic.

Correct Answer

```
AML.TA0002
```

**Tactic:** Reconnaissance

---

# Commands Used

```bash
nmap

curl

grpcurl
```

---

---

# Task 6 – Structured Reconnaissance Methodology and Detection

## Overview

Throughout this room we learned how to:

- Discover AI infrastructure
- Fingerprint AI services
- Enumerate exposed metadata
- Map the AI attack surface

This task combines all of those techniques into a structured **5-phase AI reconnaissance methodology** that can be reused during security assessments.

It also switches perspectives and explains how defenders can detect these reconnaissance activities through logs and SIEM alerts.

---

# The 5-Phase AI Reconnaissance Methodology

The methodology can be applied during any AI infrastructure assessment.

```
Passive Reconnaissance
        │
        ▼
Active Scanning
        │
        ▼
API Fingerprinting
        │
        ▼
Metadata Extraction
        │
        ▼
Supply Chain Review
```

---

# Phase 1 – Passive Reconnaissance

Before interacting with the target, gather as much publicly available information as possible.

## Search Engines

Useful services:

- Shodan
- Censys
- FOFA

Common searches

```text
port:5000 "MLflow"

port:8888 title:"Home Page - Select or create a notebook"

http.title:"Ray Dashboard"
```

---

## Search GitHub

Look for leaked credentials using GitHub dorks.

Examples

```text
filename:.env MLFLOW_TRACKING_URI

filename:.env HF_TOKEN

filename:config.json model_name
```

These often reveal:

- MLflow connection strings
- Hugging Face tokens
- API keys
- Configuration files

---

## Research Public Sources

Other useful information sources include:

- arXiv papers
- Engineering blogs
- DockerHub
- GitHub Container Registry
- Job postings

Job advertisements can reveal technologies such as:

- Kubeflow
- MLflow
- Triton
- SageMaker

This phase maps to:

```
AML.T0000
```

**Search for Victim's Publicly Available Research Materials**

---

# Phase 2 – Active Scanning

After gathering passive intelligence, scan for AI-specific services.

Example command

```bash
nmap -p 5000,6333,8000,8001,8002,8080,8265,8500,8501,8888,9000,11434,19530 \
-sV \
--script=http-title,http-headers <target>
```

Important ports

| Service | Port |
|----------|------|
| MLflow | 5000 |
| Triton | 8000–8002 |
| Ray | 8265 |
| TensorFlow Serving | 8500–8501 |
| Jupyter | 8888 |
| MinIO | 9000 |
| Ollama | 11434 |
| Milvus | 19530 |

---

## gRPC Enumeration

Nmap often labels gRPC services as generic TCP services.

Use:

```bash
grpcurl
```

Example

```bash
grpcurl -plaintext target:8001 list
```

---

## Metrics Endpoints

Always check:

```
/metrics
```

These endpoints often reveal:

- Model names
- GPU utilization
- Request counts
- Deployment topology

---

# Phase 3 – API Fingerprinting

Once services are discovered, identify the framework behind them.

Useful directory brute-force tools

- ffuf
- feroxbuster

Useful AI-specific endpoints

```text
/v1/models
/v2/models
/v2/health/ready
/api/2.0/mlflow/experiments/list
/api/2.0/mlflow/registered-models/list
/v1/schema
/v1/meta
/api/kernels
/api/contents
/openapi.json
/docs
/graphql
/metrics
/api/tags
/api/show
/collections
/healthz
/ping
```

For every endpoint that responds successfully:

- Check HTTP headers.
- Examine JSON responses.
- Trigger controlled errors.
- Identify the framework.

---

# Phase 4 – Metadata Extraction

After identifying services, enumerate exposed information.

## MLflow

Extract:

- Experiments
- Registered models
- Model versions
- Artifact URIs
- User IDs
- Training runs

---

## Triton / TensorFlow Serving

Retrieve:

- Tensor names
- Input shapes
- Output shapes
- Data types
- Framework information

---

## Vector Databases

Collect:

- Collection names
- Embedding dimensions
- Distance metrics
- Schema information

---

## Jupyter

Inspect:

- Running kernels
- Notebook contents
- Credentials
- API tokens

---

# Phase 5 – Supply Chain Review

Review every external dependency used by the AI environment.

Examples include:

- Hugging Face
- MinIO
- Amazon S3
- Google Cloud Storage
- Internal Python packages

Review:

- requirements.txt
- Pipfile
- Container images
- Notebook cells
- Build logs

Look for:

- Public buckets
- Leaked API keys
- Dependency confusion opportunities
- Model download sources

---

# Tool Reference

| Tool | Purpose | Phase |
|------|---------|-------|
| Shodan / Censys / FOFA | Internet-wide reconnaissance | Phase 1 |
| GitHub Dorks | Search leaked credentials | Phase 1 |
| Nmap | Port scanning | Phase 2 |
| grpcurl | gRPC enumeration | Phase 2 |
| ffuf / feroxbuster | Endpoint discovery | Phase 2–3 |
| curl | Manual API probing | Phase 3–4 |
| MLOKit | MLflow enumeration | Phase 4 |
| Nuclei | Detect AI misconfigurations | Phase 2–3 |
| Agrus Scanner | Shadow AI detection | Phase 2 |

---

# Detection from the Defender's Perspective

Every reconnaissance activity leaves evidence inside logs.

Understanding these patterns helps defenders identify attackers early.

---

## Model Enumeration

Indicator

```
Repeated GET requests

/v2/models
```

Behavior

Multiple requests from one IP within a short period.

---

## Scripted MLflow Access

Requests

```
/registered-models/list

/model-versions/search
```

without a valid MLflow UI session.

This behavior closely matches **MLOKit**.

---

## Prometheus Scraping

Unexpected requests to

```
/metrics
```

from IP addresses outside the monitoring infrastructure indicate reconnaissance.

---

## AI-Aware Port Scanning

Scanning ports such as

```
5000
8000
8001
8080
8265
8888
```

in sequence strongly suggests AI-focused reconnaissance.

---

## Path Traversal Attempts

Indicators

```
../

%2e%2e%2f
```

inside MLflow artifact requests may indicate attempts to exploit path traversal vulnerabilities.

---

## Jupyter Enumeration

Requests to

```
/api/kernels

/api/contents
```

without authentication often indicate automated reconnaissance.

---

# Quick Wins to Reduce the Attack Surface

Several simple configuration changes significantly reduce reconnaissance opportunities.

### Enable MLflow Authentication

Protect the tracking server with:

- Username
- Password
- Reverse proxy authentication

---

### Secure Jupyter

Avoid using

```
--allow-root

--ip=0.0.0.0
```

Require authentication and avoid exposing notebooks publicly.

---

### Restrict AI Ports

Block internet access to ports such as:

- 5000
- 8000–8002
- 8080
- 8265
- 8500–8501
- 8888
- 9000

unless absolutely necessary.

---

### Disable Triton Model Control

Use

```bash
--model-control-mode=none
```

to prevent unauthorized model loading.

---

### Protect Metrics Endpoints

Restrict

```
/metrics
```

to trusted monitoring systems only.

---

### Secure Hugging Face Tokens

- Rotate tokens regularly.
- Use fine-grained permissions.
- Avoid storing tokens inside notebooks or repositories.

---

### Reduce Information Leakage

Disable:

- Debug headers
- Verbose errors
- Stack traces

before exposing services externally.

---

### Secure Artifact Storage

Review:

- MinIO policies
- S3 bucket permissions

Ensure model artifacts are not publicly accessible.

---

# Case Study – Hugging Face Spaces Breach (2024)

In June 2024, attackers gained unauthorized access to Hugging Face Spaces and obtained authentication secrets stored by developers.

Compromised secrets included:

- Hugging Face tokens
- Private model access
- Dataset credentials

The incident demonstrated why leaked credentials are dangerous.

The recommended mitigations included:

- Token rotation
- Fine-grained access control
- Avoid storing secrets inside hosted applications

---

# Practical Exercise

The final exercise placed us in the role of a SOC analyst.

Objectives:

- Review SIEM alerts.
- Identify reconnaissance phases.
- Distinguish legitimate traffic from attacker activity.
- Recommend defensive improvements.

---

## Question 1

A SIEM detected requests to:

```
/api/2.0/mlflow/registered-models/list
```

without a valid MLflow UI session.

This behavior matches:

```
MLOKit
```

---

## Question 2

The most effective mitigation for preventing unauthorized access to an MLflow server is:

```
Enable MLflow authentication
```

---

# Commands Used

```bash
nmap

grpcurl

curl

ffuf

feroxbuster
```

---

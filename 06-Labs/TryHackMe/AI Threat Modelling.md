# AI Threat Modelling --- Detailed Walkthrough Notes

**Study date:** 7 November 2026\
**Platform:** TryHackMe\
**Topic:** AI Threat Modelling\
**Coverage:** Introduction, AI data supply chain, STRIDE-AI, MITRE
ATLAS, OWASP LLM Top 10, and conclusion

------------------------------------------------------------------------

## 1. Why AI Threat Modelling Matters

Artificial intelligence is already part of enterprise operations.
Examples include:

-   Language models handling customer support tickets.
-   Recommendation engines suggesting products.
-   Fraud detection systems making real-time decisions.

These deployments introduce attack surfaces that traditional security
teams may not be accustomed to assessing.

Traditional threat modelling frameworks such as **STRIDE** remain
useful, but AI systems introduce additional assets, behaviours, and
failure modes:

-   Training data can be poisoned.
-   Model weights can be stolen or replaced.
-   Prompts can be injected.
-   Models may produce different outputs for the same or similar inputs
    because their behaviour is non-deterministic.
-   AI systems may retrieve external information or use tools to take
    actions.

The important point is not to discard traditional threat modelling. It
is to adapt it to the assets and behaviour of AI systems.

## 2. The AI Data Supply Chain

AI systems have a data supply chain in addition to the software supply
chain familiar from traditional applications.

A software supply chain includes items such as packages, libraries,
dependencies, and container images. AI systems inherit those risks and
add a separate chain involving the data used to build and operate
models.

### The five stages

`<list marker="number" gap={2}>`{=html} `<list-item>`{=html} **Stage 1
--- Data Collection**

    Training data can come from web scraping, purchased datasets, internal databases, user-generated content, and third-party providers.

    An attacker who can contribute to or influence one of these sources may be able to introduce malicious or misleading data.

`</list-item>`{=html} `<list-item>`{=html} **Stage 2 --- Cleaning and
Labelling**

    Raw data is preprocessed, filtered, and labelled. This may involve external annotation teams, automated labelling tools, or labels inferred from outcomes such as chargebacks or investigation results.

    If labels are compromised or incorrect, the model can learn incorrect associations. A mislabelled dataset may not look corrupted; it may simply teach the model the wrong thing.

`</list-item>`{=html} `<list-item>`{=html} **Stage 3 --- Model
Training**

    The model learns patterns from the prepared data. Poison that survives collection and cleaning can become embedded in the model's **weights**.

    Unlike a compromised library that may be replaced or patched, a poisoned model may require retraining from clean data, which can be expensive and time-consuming.

`</list-item>`{=html} `<list-item>`{=html} **Stage 4 --- Validation and
Packaging**

    The trained model is evaluated, versioned, and stored in a model registry before deployment.

    If the registry is compromised, an attacker may replace a validated model with a backdoored one. Standard validation may not detect the backdoor if the trigger inputs are absent from the validation dataset.

`</list-item>`{=html} `<list-item>`{=html} **Stage 5 --- Inference**

    The model serves predictions in production. LLM applications may retrieve additional context at query time from vector databases or document stores. This retrieval process creates another place where malicious content may be introduced.

`</list-item>`{=html} `</list>`{=html}

### Why the AI supply chain is difficult to secure

The lesson highlights **time** as an important difference.

A compromised software package may be detected and reverted quickly.
Poisoned training data may have delayed effects. The problem may only
become visible after training, validation, deployment, and weeks or
months of production use.

### MegaCorp example: gradual fraud-model poisoning

MegaCorp retrains its fraud detection model monthly using new
transaction data.

An attacker who can inject crafted transactions into the training
pipeline over several months may gradually shift the model's decision
boundaries. Eventually, certain fraudulent patterns may no longer be
detected.

**Defender's lesson:** Protect every stage of the data supply chain, not
only the production model endpoint.

------------------------------------------------------------------------

## 3. STRIDE Refresher

STRIDE is a traditional threat modelling framework introduced by
Microsoft in the late 1990s. It gives defenders six categories for
thinking systematically about threats.

  -------------------------------------------------------------------------
  Letter            Threat category   Security property   Traditional
                                                          meaning
  ----------------- ----------------- ------------------- -----------------
  S                 Spoofing          Authenticity        Pretending to be
                                                          someone or
                                                          something else

  T                 Tampering         Integrity           Modifying data or
                                                          code without
                                                          authorisation

  R                 Repudiation       Non-repudiability   Denying that an
                                                          action was
                                                          performed

  I                 Information       Confidentiality     Exposing
                    Disclosure                            information to
                                                          unauthorised
                                                          parties

  D                 Denial of Service Availability        Making a system
                                                          or resource
                                                          unavailable

  E                 Elevation of      Authorisation       Gaining
                    Privilege                             capabilities
                                                          beyond what is
                                                          permitted
  -------------------------------------------------------------------------

In traditional threat modelling, the system is decomposed into
components and each component is examined through these six categories.

For AI systems, the categories are still useful, but the threats look
different.

## 4. Adapting STRIDE for AI Systems --- STRIDE-AI

### 4.1 S --- Spoofing: Data Source Impersonation

**Traditional meaning:** An attacker forges credentials or otherwise
pretends to be a legitimate user or service.

**Primary AI manifestation --- Data source impersonation**

In a Retrieval-Augmented Generation (RAG) architecture, the model
retrieves context from sources such as vector databases, document
stores, and web content. The model may treat retrieved context as
trustworthy.

If an attacker injects fabricated content into those sources, they can
spoof the knowledge the model relies on. The model may then generate
confident responses based on attacker-controlled information.

Other AI-related spoofing threats include:

-   **Model impersonation:** deploying a look-alike API endpoint that
    mimics a legitimate AI service.
-   **Adversarial identity attacks:** crafting inputs that fool AI-based
    identity verification, such as facial recognition or voice
    authentication.

**MegaCorp example:** An attacker injects fabricated policy documents
into the internal knowledge base used by a customer-facing chatbot. The
chatbot begins serving incorrect policy information to customers.

**Defensive question:** Can we verify the origin and integrity of the
sources that the model retrieves?

### 4.2 T --- Tampering: Data Poisoning

**Traditional meaning:** Modifying data in transit or at rest, such as
changing database records, API responses, or configuration files.

**Primary AI manifestation --- Data poisoning**

An attacker injects malicious data into the training pipeline, causing
the model to learn incorrect patterns.

The effect may be delayed: the poison is embedded during training and
becomes visible only during inference.

Two forms described in the lesson:

-   **Targeted poisoning:** attempts to cause specific
    misclassifications or behaviours.
-   **Untargeted poisoning:** degrades the model's overall performance.

Other AI-related tampering threats include:

-   **Model manipulation:** directly modifying model weights or
    replacing a model in the registry with a backdoored version.
-   **Prompt injection:** altering instructions or context received by
    the model. Its STRIDE classification depends on context: it maps to
    Tampering when the attacker changes model input, but may map to
    Elevation of Privilege when the goal is to bypass guardrails.
-   **Feature manipulation:** changing input features so the model makes
    decisions based on tampered data.

**MegaCorp example:** An attacker submits crafted transactions over
several billing cycles. The monthly retraining process gradually shifts
the fraud model's decision boundaries until a particular fraudulent
pattern is no longer flagged.

**MITRE ATLAS references in the lesson:** - Data Poisoning ---
`AML.T0020` - Backdoor ML Model --- `AML.T0018`

### 4.3 R --- Repudiation: Unexplainable Model Decisions

**Traditional meaning:** A user performs an action and later denies it
because the system lacks adequate logs or audit trails.

**Primary AI manifestation --- Lack of decision audit trails**

AI systems may make consequential decisions, such as approving loans,
flagging transactions, or denying claims.

If the organisation does not log enough information, it may be unable to
reproduce or explain why a model made a particular decision.

Useful records may include:

-   Model inputs and outputs.
-   Model version.
-   Relevant feature values.
-   Retrieval context for RAG systems.
-   Relevant prompt and conversation context.
-   Configuration that affected the response, such as temperature.

Other AI-related repudiation threats include:

-   **Prompt and context volatility:** the full context behind an LLM
    output may not be captured.
-   **Model version ambiguity:** without deployment records, an output
    cannot be confidently attributed to a particular model version or
    state.

**MegaCorp example:** A regulator asks why the fraud detection system
approved a suspicious transaction three weeks earlier. The team cannot
identify the model version, input features, or decision threshold used
at the time.

**Defensive question:** Could we reconstruct the context and model
version behind an important AI decision?

### 4.4 I --- Information Disclosure: Model Extraction

**Traditional meaning:** Sensitive information is exposed through
breaches, insecure APIs, verbose errors, or weak access controls.

**Primary AI manifestation --- Model extraction (model stealing)**

An attacker systematically queries a model's API and uses the
input-output pairs to reconstruct a functionally equivalent copy.

The attacker may not need access to the model's internal weights. A
public-facing endpoint and enough carefully selected queries may be
sufficient.

The stolen model can represent significant intellectual property loss
and may be probed offline for weaknesses.

Other AI-related information disclosure threats include:

-   **Training data extraction:** queries cause a model to reveal
    memorised training data, potentially including personal or
    proprietary information.
-   **System prompt leakage:** prompt extraction reveals internal
    instructions, guardrails, or business logic.
-   **Embedding inversion:** attempting to reconstruct source
    information from embedding vectors stored in a vector database.

**MegaCorp example:** A competitor queries the recommendation engine API
with thousands of product-user combinations and collects confidence
scores. Over time, it builds a shadow model that imitates MegaCorp's
recommendation logic without accessing the original model weights.

**MITRE ATLAS references in the lesson:** - Extract ML Model ---
`AML.T0024` - Infer Training Data Membership --- `AML.T0025`

### 4.5 D --- Denial of Service: Inference Cost Exploitation

**Traditional meaning:** Flooding a service with traffic to exhaust
resources and make it unavailable.

**Primary AI manifestation --- Inference cost exploitation (denial of
wallet)**

AI inference can be much more expensive than traditional API calls. In
cloud deployments billed per token or query, an attacker may cause
serious financial damage without taking the service offline.

Examples include: - Large volumes of expensive queries. - Very long
prompts. - Requests designed to produce maximum-length responses.

Other AI-related denial of service threats include:

-   **GPU resource exhaustion:** complex or high-volume queries saturate
    compute capacity and delay or drop legitimate requests.
-   **Sponge examples:** adversarial inputs designed to maximise
    computational resources consumed during inference.
-   **Training pipeline disruption:** injecting large amounts of junk
    data to delay or corrupt retraining.

**MegaCorp example:** A competitor floods the chatbot API with thousands
of crafted prompts designed to trigger maximum-length responses. The
chatbot remains online, but the monthly inference bill rises from
`$15,000` to `$180,000` --- a 12-fold increase.

The system is technically available, but the attack drains the
organisation's budget.

**OWASP reference in the lesson:** `LLM10:2025 — Unbounded Consumption`.

### 4.6 E --- Elevation of Privilege: Jailbreaking and Excessive Agency

**Traditional meaning:** An attacker gains capabilities beyond those
intended, such as an ordinary user gaining administrator access or a
service account performing unauthorised actions.

**Primary AI manifestation --- Jailbreaking / guardrail bypass**

An attacker crafts prompts that cause an LLM to ignore safety
guidelines, content policies, or behavioural restrictions.

Conceptually, the attacker is escalating their capabilities within the
model: they may gain access to behaviour the model was instructed to
restrict, even though they have not gained operating-system
administrator privileges.

Other AI-related elevation of privilege threats include:

-   **Excessive agency:** the AI system has more tool permissions than
    are appropriate for its role.
-   **Tool use exploitation:** manipulating an agentic AI into using web
    browsing, file writing, or API tools for unintended purposes.
-   **Cross-plugin escalation:** compromising one plugin's input to
    influence the model's behaviour with another, more privileged
    plugin.

**MegaCorp example:** An attacker jailbreaks the customer chatbot. The
chatbot has database query tools for order-status lookups, but those
tools are not sufficiently scoped. The attacker manipulates the chatbot
into issuing queries against a customer PII table and extracting
personal information.

**OWASP reference in the lesson:** `LLM06:2025 — Excessive Agency`.

### 4.7 What STRIDE still misses

Even after adaptation, some AI risks do not fit neatly into a single
STRIDE category.

-   **Adversarial examples:** inputs designed to cause misclassification
    may span Tampering, Spoofing, and Elevation of Privilege, depending
    on context.
-   **Model bias and fairness:** these are security-adjacent concerns
    with regulatory and compliance implications, but they do not fit
    traditional STRIDE categories cleanly.
-   **Emergent behaviours:** large models may exhibit capabilities or
    behaviours that were not explicitly trained for or anticipated.
    Traditional threat categories may not describe these risks
    adequately.

These gaps explain why AI threat modelling benefits from additional
frameworks such as MITRE ATLAS and OWASP LLM Top 10.

### 4.8 STRIDE-AI consolidated mapping

  -----------------------------------------------------------------------
  STRIDE category   Primary AI        Other AI threats  MegaCorp example
                    manifestation                       
  ----------------- ----------------- ----------------- -----------------
  Spoofing          Data source       Model             Fake policy
                    impersonation /   impersonation,    documents
                    RAG injection     adversarial       injected into
                                      identity attacks  chatbot knowledge
                                                        base

  Tampering         Data poisoning    Model             Crafted
                                      manipulation,     transactions
                                      prompt injection, shift fraud
                                      feature tampering model's decision
                                                        boundaries

  Repudiation       Lack of decision  Context           Cannot explain
                    audit trails      volatility, model why fraud model
                                      version ambiguity approved a
                                                        suspicious
                                                        transaction

  Information       Model extraction  Training data     Competitor
  Disclosure        / stealing        extraction,       reconstructs
                                      prompt leakage,   recommendation
                                      embedding         engine through
                                      inversion         API queries

  Denial of Service Inference cost    GPU exhaustion,   Expensive chatbot
                    exploitation /    sponge examples,  prompts cause
                    denial of wallet  pipeline          inference bill to
                                      disruption        rise 12x

  Elevation of      Jailbreaking /    Excessive agency, Jailbroken
  Privilege         guardrail bypass  tool              chatbot uses
                                      exploitation,     database tools to
                                      cross-plugin      query customer
                                      escalation        PII
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 5. MITRE ATLAS --- The AI Threat Technique Catalogue

### 5.1 What is MITRE ATLAS?

**ATLAS** stands for **Adversarial Threat Landscape for
Artificial-Intelligence Systems**.

It is a knowledge base of adversary tactics and techniques targeting AI
and machine-learning systems. The lesson describes it as the AI-focused
counterpart to MITRE ATT&CK.

If ATT&CK helps defenders map adversary behaviour against traditional
infrastructure, ATLAS provides a structured vocabulary for adversarial
activity against AI systems.

The lesson gives the following approximate counts as of the room's
design in early 2026:

-   16 tactics
-   155 techniques
-   35 mitigations
-   52 real-world case studies

These counts are time-sensitive and may change. The lesson recommends
checking the official ATLAS site for current counts.

### 5.2 How ATLAS is structured

  -----------------------------------------------------------------------
  Component               What it answers         Example from the lesson
  ----------------------- ----------------------- -----------------------
  Tactic                  Why the adversary is    ML Attack Staging
                          acting / the goal       (`AML.TA0012`)

  Technique               How the adversary       Data Poisoning
                          achieves the goal       (`AML.T0020`)

  Sub-technique           A more specific variant Craft Adversarial Data
                          of a technique          (`AML.T0043.004`)

  Mitigation              What defensive          Input validation, data
                          countermeasure can      provenance tracking
                          reduce the risk         
  -----------------------------------------------------------------------

Tactics form the columns of the ATLAS matrix, with techniques organised
under them. During threat modelling, identify the attacker's objective
and then examine the techniques that could achieve it against the
system.

### 5.3 Five ATLAS techniques highlighted in the lesson

**1. Data Poisoning --- `AML.T0020`**

Injecting malicious data into training pipelines to corrupt model
behaviour. Effects may be delayed and persist until the model is
retrained using clean data.

-   STRIDE mapping in the lesson: Tampering.

**2. Model Extraction --- `AML.T0024`**

Systematically querying a model API to reconstruct a functional copy.
The attacker may need only access to the public endpoint and enough
queries, rather than internal model access.

-   STRIDE mapping: Information Disclosure.

**3. Evade ML Model --- `AML.T0015`**

Crafting adversarial data that prevents a model from correctly
identifying input content. It may be used to evade malware detection,
bypass content filters, or cause downstream misclassification.

-   STRIDE mapping depends on context and can span Tampering, Spoofing,
    and Elevation of Privilege.

**4. LLM Prompt Injection --- `AML.T0051`**

Manipulating an LLM's behaviour by inserting instructions through direct
user input or through content the model processes.

-   **Direct prompt injection:** malicious instructions are entered by
    the user through the chat interface.
-   **Indirect prompt injection:** malicious instructions are embedded
    in documents or other content the model retrieves or processes, such
    as a RAG pipeline.

For MegaCorp, the lesson identifies indirect injection through the RAG
knowledge base as the primary vector.

-   STRIDE mapping in the lesson: Tampering, while context can affect
    classification.

**5. Backdoor ML Model --- `AML.T0018`**

Embedding hidden triggers in a model during training. The model behaves
normally for ordinary inputs but acts maliciously when a specific
trigger pattern appears.

The lesson compares this to a logic bomb embedded inside a neural
network.

### 5.4 Using ATLAS during threat modelling

The lesson describes a three-step workflow:

1.  **Start with STRIDE:** examine each AI component through the six
    threat categories to identify what could go wrong.
2.  **Enrich with ATLAS:** find the corresponding ATLAS technique to
    understand how the attack could be performed, including documented
    methods and case studies.
3.  **Apply mitigations:** use the technique's defensive guidance to
    identify countermeasures.

STRIDE provides the threat category; ATLAS adds technical detail and a
shared vocabulary.

### 5.5 MegaCorp example: turning a general concern into a finding

During STRIDE analysis, the team identifies a Tampering risk in
MegaCorp's fraud model training pipeline.

They look up **Data Poisoning (`AML.T0020`)** in ATLAS. The lesson
explains that poisoning can be targeted or untargeted, and that an
attacker needs access to a training data source.

Mitigations highlighted in the example include:

-   Data provenance tracking.
-   Anomaly detection on training inputs.
-   Monitoring model performance for drift.

The result is more actionable than simply recording "tampering risk
exists." The finding now has a named technique, an attack explanation,
and defensive measures.

### 5.6 Real-world case studies mentioned

**ShadowRay --- `AML.CS0023`**

The lesson describes attackers exploiting vulnerabilities in Ray, a
framework for distributed AI workloads, to compromise AI training
infrastructure. It illustrates that AI supply chain attacks can affect
production environments.

**Morris II Worm --- `AML.CS0024`**

The lesson describes a research demonstration of a self-replicating
prompt-injection worm that could spread between AI agents through
RAG-based email systems. The injected content could enter model context
without direct user interaction, extract personal information, and
propagate to other agents.

ATLAS case studies connect abstract techniques to concrete examples of
AI-related attacks.

------------------------------------------------------------------------

## 6. OWASP Top 10 for LLM Applications (2025)

### 6.1 What is the OWASP LLM Top 10?

The **OWASP Top 10 for LLM Applications** is a community-driven list of
major security risks specific to large language model deployments. The
lesson identifies it as a project of the OWASP GenAI Security Project.

It serves as a practical way to connect risks to the components of an
LLM architecture.

The goal is not simply to memorise ten risk names. It is to look at an
architecture and identify which components are exposed to which risks.

### 6.2 The 2025 list and component mapping

  -------------------------------------------------------------------------
  ID                Risk              Meaning             Components
                                                          identified in the
                                                          lesson
  ----------------- ----------------- ------------------- -----------------
  LLM01             Prompt Injection  Crafted direct or   Inference
                                      indirect input      endpoint, vector
                                      manipulates model   database / RAG
                                      behaviour           pipeline, any
                                                          component feeding
                                                          text to the model

  LLM02             Sensitive         Model reveals PII,  Inference
                    Information       credentials, or     endpoint,
                    Disclosure        proprietary data    training
                                                          pipeline, system
                                                          prompt

  LLM03             Supply Chain      Compromised models, Training
                                      training data,      pipeline, model
                                      plugins, or         registry,
                                      dependencies        plugin/tool
                                                          integrations

  LLM04             Data and Model    Corrupted training  Training
                    Poisoning         data or model       pipeline, model
                                      weights alter       registry, feature
                                      behaviour           store

  LLM05             Improper Output   Model output is not Web frontend, API
                    Handling          validated before    gateway, systems
                                      downstream use      consuming model
                                                          responses

  LLM06             Excessive Agency  Model has too many  Inference
                                      permissions, tools, endpoint, tool
                                      or autonomy         integrations, API
                                                          gateway, agentic
                                                          orchestration
                                                          layer

  LLM07             System Prompt     Internal prompts    Inference
                    Leakage           containing          endpoint, system
                                      sensitive logic or  prompt
                                      credentials are     configuration
                                      exposed             

  LLM08             Vector and        Weaknesses in RAG,  Vector database,
                    Embedding         vector databases,   RAG pipeline,
                    Weaknesses        or embeddings       embedding
                                                          generation

  LLM09             Misinformation    Model produces      Inference
                                      credible-sounding   endpoint, vector
                                      but false content   database,
                                                          user-facing
                                                          output channels

  LLM10             Unbounded         Uncontrolled        Inference
                    Consumption       resource usage      endpoint, API
                                      causes denial of    gateway, training
                                      service or          pipeline
                                      financial           
                                      exploitation        
  -------------------------------------------------------------------------

### 6.3 How to read the component mapping

The table works in two directions.

**Risk → Component**

Question: "Where does prompt injection live?"

The lesson points to the inference endpoint and RAG pipeline, because
direct user input and retrieved content can both influence model
behaviour.

**Component → Risk**

Question: "We are deploying a vector database for RAG. What risks should
we assess?"

The vector database appears under:

-   LLM01 --- indirect prompt injection through retrieved content.
-   LLM08 --- vector and embedding weaknesses.
-   LLM09 --- misinformation from stale or incorrect source documents.

This second direction helps scope an assessment whenever a new AI
component is introduced.

### 6.4 Component risk profiles for MegaCorp

#### LLM Inference Endpoint

The lesson says the inference endpoint appears in seven of the ten OWASP
entries:

-   LLM01 --- Prompt Injection
-   LLM02 --- Sensitive Information Disclosure
-   LLM05 --- Improper Output Handling
-   LLM06 --- Excessive Agency
-   LLM07 --- System Prompt Leakage
-   LLM09 --- Misinformation
-   LLM10 --- Unbounded Consumption

This is the component with the highest risk concentration in the
lesson's mapping and needs comprehensive hardening.

#### Vector Database / RAG Pipeline

Appears in three entries:

-   LLM01 --- indirect prompt injection through retrieved content.
-   LLM08 --- vector and embedding weaknesses.
-   LLM09 --- misinformation from stale or incorrect source documents.

The lesson highlights input validation for indexed content, access
controls on the vector store, and freshness monitoring for source
documents.

#### Training Pipeline

Appears in three entries:

-   LLM02 --- sensitive data entering training.
-   LLM03 --- third-party datasets, compromised base models, and
    poisoned fine-tuning data.
-   LLM04 --- data and model poisoning.

LLM03 also applies to plugin and tool integrations through compromised
dependencies, but the training pipeline is where third-party models and
datasets enter the system in the lesson's example.

------------------------------------------------------------------------

## 7. Connecting STRIDE, ATLAS, and OWASP

These frameworks are complementary layers rather than competing choices.

  -----------------------------------------------------------------------
  Layer                   What it does            Main question
  ----------------------- ----------------------- -----------------------
  STRIDE-AI               Categorises threats by  What could go wrong?
                          type                    

  MITRE ATLAS             Documents specific      How could an attacker
                          adversary techniques    do it?

  OWASP LLM Top 10        Maps risks to           Where does the risk
                          components and helps    live?
                          scope the assessment    
  -----------------------------------------------------------------------

A useful way to remember the relationship:

-   **STRIDE = threat category**
-   **ATLAS = attack technique**
-   **OWASP = LLM risk and affected component**

### Repeatable workflow

1.  Identify the AI assets and architecture components.
2.  Map how data flows through collection, cleaning, training,
    packaging, and inference.
3.  Walk each component through the six STRIDE categories, adapted for
    AI.
4.  Use ATLAS to identify specific techniques and relevant mitigations.
5.  Use OWASP LLM Top 10 to map risks to the components that need
    assessment.
6.  Produce a prioritised threat assessment.

The lesson describes this workflow as reusable whenever an organisation
deploys a new AI system, updates a model, or introduces agentic
capabilities.

------------------------------------------------------------------------

## 8. Quick Reference --- Important Terms

  -----------------------------------------------------------------------
  Term                                Meaning
  ----------------------------------- -----------------------------------
  AI data supply chain                The stages through which data is
                                      collected, cleaned, labelled, used
                                      for training, packaged, and
                                      consumed

  Model weights                       Learned parameters that encode
                                      patterns acquired during model
                                      training

  Data poisoning                      Introducing malicious or misleading
                                      data into a training process

  Backdoor model                      A model that behaves normally
                                      unless a particular trigger pattern
                                      is present

  Model registry                      A location where trained and
                                      versioned models are stored for
                                      deployment

  Inference                           Using a trained model to produce a
                                      prediction or response

  RAG                                 Retrieval-Augmented Generation;
                                      retrieving external context and
                                      supplying it to an LLM

  Vector database                     Stores vector representations used
                                      in similarity-based retrieval

  Prompt injection                    Manipulating model behaviour
                                      through malicious instructions in
                                      user input or processed content

  Direct prompt injection             Malicious instructions supplied
                                      directly by a user

  Indirect prompt injection           Malicious instructions embedded in
                                      content the model retrieves or
                                      processes

  Model extraction                    Reconstructing a model by
                                      systematically querying its
                                      endpoint

  Model drift                         A change in model performance or
                                      behaviour over time

  Jailbreaking                        Prompting a model to bypass its
                                      intended restrictions or guardrails

  Excessive agency                    Giving an AI system more
                                      permissions or autonomy than it
                                      needs

  Denial of wallet                    Causing excessive AI usage costs
                                      without necessarily making the
                                      service unavailable

  Adversarial example                 Input crafted to cause a model to
                                      make an incorrect prediction

  MITRE ATLAS                         Knowledge base of adversary tactics
                                      and techniques targeting AI/ML
                                      systems

  OWASP LLM Top 10                    List of major LLM application
                                      security risks, mapped to
                                      components in the lesson
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 9. Quick Revision Questions

**1. Why do AI systems need adapted threat modelling?**\
They introduce assets and failure modes such as training data, model
weights, prompt injection, non-deterministic outputs, and retrieval
pipelines that traditional threat models may not fully describe.

**2. What are the five AI data supply chain stages?**\
Data Collection; Cleaning and Labelling; Model Training; Validation and
Packaging; Inference.

**3. Why can data poisoning be difficult to detect?**\
Its effects may be embedded during training and only become visible
later in production.

**4. What does STRIDE stand for?**\
Spoofing, Tampering, Repudiation, Information Disclosure, Denial of
Service, and Elevation of Privilege.

**5. What is the primary AI manifestation of Spoofing in the lesson?**\
Data source impersonation, especially injecting attacker-controlled
content into RAG sources.

**6. What is data poisoning mapped to in STRIDE-AI?**\
Tampering.

**7. Why is audit logging important for AI decisions?**\
Without inputs, outputs, model versions, and relevant context, it may be
difficult to reproduce or explain a past decision.

**8. What is model extraction?**\
Systematically querying a model endpoint and using its outputs to
reconstruct a functionally similar model.

**9. What is denial of wallet?**\
Abusing expensive inference usage to cause financial damage even if the
service remains online.

**10. What is excessive agency?**\
Giving an AI system more tool permissions or autonomy than is
appropriate for its role.

**11. What is the difference between direct and indirect prompt
injection?**\
Direct injection comes from user input; indirect injection is embedded
in content the model retrieves or processes.

**12. What is MITRE ATLAS?**\
A knowledge base of adversary tactics and techniques targeting AI and
machine-learning systems.

**13. What is the ATLAS technique ID for Data Poisoning in the
lesson?**\
`AML.T0020`.

**14. What is the ATLAS technique ID for Model Extraction in the
lesson?**\
`AML.T0024`.

**15. What does OWASP LLM Top 10 help defenders identify?**\
Which LLM-specific risks affect which components of an AI architecture.

**16. Which OWASP risk covers prompt injection?**\
LLM01.

**17. Which OWASP risk covers excessive agency?**\
LLM06.

**18. Which OWASP risk covers unbounded consumption?**\
LLM10.

**19. What are the three complementary framework layers?**\
STRIDE-AI categorises threats, ATLAS describes techniques, and OWASP
maps risks to components.

**20. Why is the workflow repeatable?**\
It can be applied whenever an organisation deploys a new AI system,
updates a model, or adds agentic capabilities.

------------------------------------------------------------------------

## 10. My Key Takeaways

Today I learned that AI systems are not simply traditional applications
with a model added to them. They introduce new assets, a separate data
supply chain, and failure modes that require security teams to adapt
their threat modelling approach.

I learned how the AI data supply chain moves through collection,
cleaning and labelling, training, validation and packaging, and
inference. Every stage can be attacked. Data poisoning is particularly
difficult because malicious influence may remain hidden until the model
is deployed and used.

I also learned how to adapt STRIDE for AI. Spoofing can involve false
data sources in RAG systems; Tampering can involve poisoned training
data; Repudiation can involve missing records of model decisions;
Information Disclosure can involve model extraction; Denial of Service
can become denial of wallet; and Elevation of Privilege can involve
jailbreaking and excessive tool permissions.

MITRE ATLAS adds specific AI attack techniques and mitigations. OWASP
LLM Top 10 helps map risks to the components where they occur. Together,
the three approaches make an AI threat assessment more structured and
actionable.

**Main lesson:** STRIDE tells me what type of threat to consider, MITRE
ATLAS helps me understand how an attacker may carry it out, and OWASP
LLM Top 10 helps me identify where the risk exists in the architecture.

------------------------------------------------------------------------

## 11. Study Checklist

-   [ ] Explain why AI systems need adapted threat modelling.
-   [ ] Name the five stages of the AI data supply chain.
-   [ ] Explain how data poisoning can affect a model.
-   [ ] Recall all six STRIDE categories and their AI manifestations.
-   [ ] Explain why AI decision audit trails matter.
-   [ ] Distinguish model extraction from training data extraction.
-   [ ] Explain denial of wallet and excessive agency.
-   [ ] Distinguish direct from indirect prompt injection.
-   [ ] Explain the hierarchy of MITRE ATLAS.
-   [ ] Recall the five ATLAS techniques highlighted in the lesson.
-   [ ] Explain the purpose of the OWASP LLM Top 10.
-   [ ] Map the OWASP risks to the inference endpoint, RAG/vector
    database, and training pipeline.
-   [ ] Explain how STRIDE, ATLAS, and OWASP work together.

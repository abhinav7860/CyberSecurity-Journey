# The Building Blocks of AI
**Platform:** TryHackMe  
**Date:** July 23, 2026

---
## Introduction

Artificial Intelligence (AI) is the field of computer science that focuses on building systems capable of performing tasks that normally require human intelligence. These tasks include learning, reasoning, problem-solving, understanding language, recognizing images, and making decisions.

Artificial Intelligence has existed since the 1950s, but major advancements occurred after the development of Machine Learning and Deep Learning.

---

# AI Agent Platform

In this TryHackMe room, some tasks use an AI Agent instead of a Linux machine or terminal.

Unlike a normal chatbot, each AI agent has:

- A specific role
- Defined behaviours
- Goals
- Information it protects

Depending on the challenge, you may cooperate with the AI or attempt to bypass its restrictions.

### Important Notes

- Interact naturally.
- Prompt wording matters.
- Some agents intentionally resist your requests.
- Practice using the sandbox before beginning challenges.

---

# Artificial Intelligence (AI)

Artificial Intelligence refers to computer systems capable of performing tasks that usually require human intelligence.

Examples include:

- Voice assistants
- Self-driving cars
- Image recognition
- Chatbots
- Recommendation systems

---

# Machine Learning (ML)

Machine Learning is a subset of Artificial Intelligence.

Instead of being explicitly programmed with rules, ML systems learn patterns from data.

### Example

Traditional Programming

```
Rules + Data
        ↓
    Answer
```

Machine Learning

```
Data + Answers
       ↓
     Model
       ↓
New Data
       ↓
Prediction
```

ML improves automatically as it sees more data.

---

# ML Lifecycle

(Your complete ML Lifecycle section)

---

# Overfitting

Overfitting occurs when a model memorizes its training data instead of learning general patterns.

As a result:

- Performs well on training data.
- Performs poorly on new data.

Example:

A student memorizes previous exam papers but fails when the questions change.

---

# Machine Learning Algorithms

Algorithms are mathematical methods that learn patterns from data.

A trained algorithm becomes an ML Model.

Every ML algorithm follows three steps:

1. Make Prediction
2. Calculate Error
3. Improve Model

---

# Types of Machine Learning

## 1. Supervised Learning

Uses labelled data.

Examples:

- Spam detection
- House price prediction
- Disease prediction

Advantages

- Accurate
- Easy to evaluate

Disadvantages

- Requires labelled datasets

---

## 2. Unsupervised Learning

Uses unlabelled data.

Finds hidden patterns.

Examples

- Customer segmentation
- Network anomaly detection
- Recommendation systems

---

## 3. Semi-Supervised Learning

Uses:

- Small labelled dataset
- Large unlabelled dataset

Useful when labelling data is expensive.

---

## 4. Reinforcement Learning

An AI Agent learns by interacting with an environment.

```
Action
   ↓
Reward / Penalty
   ↓
Learn
```

Examples

- Chess AI
- Robotics
- Self-driving cars

---

# Neural Networks

Neural Networks are inspired by the human brain.

They consist of:

- Input Layer
- Hidden Layers
- Output Layer

Each connection has a weight that determines its importance.

### Example

Digit Recognition

```
Image
   ↓
Input Layer
   ↓
Hidden Layers
   ↓
Output Layer

Prediction:
0 1 2 3 4 5 6 7 8 9
```

Hidden layers learn:

- Edges
- Curves
- Shapes
- Numbers

---

# Deep Learning (DL)

Deep Learning is a type of Machine Learning that uses Neural Networks with multiple hidden layers.

Characteristics

- Learns automatically
- Works with huge datasets
- Excellent for images
- Excellent for speech
- Excellent for NLP

Examples

- Face Unlock
- ChatGPT
- Self-driving cars

---

# Machine Learning vs Deep Learning

| Machine Learning | Deep Learning |
|-----------------|---------------|
| Needs feature engineering | Learns features automatically |
| Smaller datasets | Huge datasets |
| Faster training | Slower training |
| Less computing power | Requires GPUs |

---

# Large Language Models (LLMs)

LLMs are Deep Learning models designed to understand and generate text.

Examples

- ChatGPT
- Llama
- DeepSeek
- Gemini

LLMs predict one word at a time until a complete response is generated.

---

# Parameters

Parameters are internal numerical values that store what the model has learned.

Think of them as the AI's "memory."

GPT models contain billions of parameters.

More parameters generally allow the model to capture more complex language patterns.

---

# Pre-training

Before becoming useful, an LLM is trained on enormous amounts of text.

During training:

```
Sentence
      ↓
Remove Last Word
      ↓
Predict Missing Word
      ↓
Compare Answer
      ↓
Adjust Parameters
      ↓
Repeat Billions of Times
```

---

# Backpropagation

Backpropagation is the learning algorithm used to reduce prediction errors.

It works by:

1. Making a prediction
2. Calculating the error
3. Adjusting weights
4. Improving future predictions

---

# Transformers

Transformers are neural network architectures introduced in Google's paper:

**Attention Is All You Need (2017)**

They process entire sentences simultaneously instead of word by word.

This greatly improved language understanding.

---

# Attention Mechanism

Attention allows a model to determine which words are most important.

Example:

"The bank approved the loan because it was financially stable."

The model correctly understands:

```
"It"
   ↓
Bank
```

instead of

```
"It"
   ↓
Loan
```

---

# GPUs

Large AI models require enormous computational power.

GPUs can process thousands of calculations simultaneously, making modern Deep Learning possible.

Without GPUs, today's LLMs would take years to train.

---

# RLHF

Reinforcement Learning from Human Feedback.

After pre-training:

Humans review responses.

```
Response
    ↓
Human Feedback
    ↓
Adjust Model
    ↓
Better Responses
```

This makes chatbots more useful and safer.

---

# Generative AI

Generative AI creates new content instead of simply analysing data.

It can generate:

- Text
- Images
- Audio
- Video
- Code

Examples

- ChatGPT
- DeepSeek
- Llama

---


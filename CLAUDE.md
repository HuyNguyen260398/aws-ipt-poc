# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Hybrid ML + Agentic AI** proof-of-concept for ITP (Primary Immune Thrombocytopenia) bleeding risk prediction, built on AWS. The system combines classical ML models (Random Forest, XGBoost, LightGBM, Logistic Regression) with an Agentic AI layer using Amazon Bedrock for Vietnamese-language clinical decision support.

**Context**: Supporting a master's thesis by Trần Xuân Nhiên (2025–2027) at BV Truyền máu Huyết học. The ML core satisfies academic requirements; the agentic layer provides novel contribution.

The detailed architecture is in `plans/ITP_Plan_v0.0.2.md` (current). Legacy plan files are in `plans/` for reference.

## Architecture

Four-layer AWS architecture:

```
Layer 4: API Gateway + Cognito → React Web App (Vietnamese) → Bedrock Guardrails
Layer 3: Bedrock Agent "IDA" (supervisor) → Data Processing Agent (Lambda) + Prediction Agent (Lambda→SageMaker) + Explanation Agent (RAG+Bedrock)
Layer 2: SageMaker (training, spot) → SageMaker Serverless Inference → SageMaker Clarify (SHAP)
Layer 1: S3 (data lake) → Glue (ETL) → DynamoDB (feature store + feedback) → Aurora Serverless v2 pgvector (RAG vector store)
```

**Key design decisions (v0.0.2):**
- Foundation model: Claude 3 Haiku via Bedrock (multilingual Vietnamese support, cost-effective); intelligent routing to Nova Micro for simple queries
- RAG source: ASH 2019 / ISTH guidelines + Vietnamese clinical protocols, stored in **Aurora Serverless v2 (pgvector)** — replaces OpenSearch Serverless to eliminate $350/month cost floor
- Vector store upgrade path: Aurora pgvector → OpenSearch Serverless only if RAG quality is insufficient
- Prediction input: 10 clinical features (see Section 6 of the plan)
- Output: bleeding risk probability (0–1) + SHAP attribution + Vietnamese explanation
- ML serving: SageMaker Serverless Inference (pay per request) — upgrade to always-on endpoint only if UAT latency is a problem
- Prompt caching enabled on system prompt + guideline context (up to 90% cost reduction)
- Web hosting: S3 + CloudFront (replaces Amplify)

## Implementation Phases (9-Month Plan)

- **Phase 1** (Months 1–2): AWS setup + data engineering + EDA
- **Phase 2** (Months 3–4): ML model training, Bayesian tuning, SHAP analysis
- **Phase 3** (Months 5–6): Bedrock Agents orchestration + RAG pipeline (self-correcting RAG)
- **Phase 4** (Month 7): React frontend + API Gateway + Cognito
- **Phase 5** (Months 8–9): UAT with clinicians + A/B testing + LLM-as-a-judge RAG evaluation

## Tech Stack

- **Python 3.11+** — all Lambda functions, SageMaker jobs, data processing
- **React.js** — frontend with Vietnamese i18n, hosted on S3 + CloudFront
- **AWS services**: S3, Glue, DynamoDB, Aurora Serverless v2 (pgvector), SageMaker, Bedrock, Lambda, API Gateway, Cognito, CloudFront, CloudWatch
- **ML libraries**: Scikit-learn, XGBoost, LightGBM (SageMaker built-in or custom containers)
- **Cost profile**: Option B cost-optimized (~$65–155/month); see plan Section 10 for Option A vs. B breakdown

## Expected Directory Structure (not yet created)

```
infrastructure/     # Terraform or CDK for AWS resources
src/
  lambda/           # Data processing, prediction, and explanation agent handlers
  ml/               # SageMaker training scripts (train.py per algorithm)
  frontend/         # React app (Vietnamese UI)
  agents/           # Bedrock agent definitions and prompt templates
data/
  raw/              # Local copies of anonymised sample data (never real PHI)
  processed/        # Feature-engineered outputs
docs/               # Architecture diagrams, API specs
```

## Compliance Constraints

- All patient data must be de-identified before entering the system
- HIPAA BAA with AWS required before using HIPAA-eligible services
- Bedrock Guardrails must filter PHI and restrict LLM scope to ITP/hematology
- Lambda functions must not log patient data
- IAM: least-privilege roles per layer (data role, ML role, app role)

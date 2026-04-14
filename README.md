<div align="center">

# 🩸 AWS ITP Bleeding Prediction POC

### Hybrid Machine Learning + Agentic AI for Clinical Decision Support

A proof-of-concept system on AWS for predicting bleeding risk in adult patients with **Primary Immune Thrombocytopenia (ITP)**, combining classical ML with an Agentic AI explanation layer in Vietnamese.

---

![Status](https://img.shields.io/badge/status-planning-yellow)
![License](https://img.shields.io/badge/license-MIT-green)
![Phase](https://img.shields.io/badge/phase-1%20of%203-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-blue?logo=python&logoColor=white)

**Topics**

![Healthcare](https://img.shields.io/badge/topic-healthcare-e63946)
![Hematology](https://img.shields.io/badge/topic-hematology-c1121f)
![Clinical Decision Support](https://img.shields.io/badge/topic-CDSS-780000)
![Machine Learning](https://img.shields.io/badge/topic-machine%20learning-4361ee)
![Agentic AI](https://img.shields.io/badge/topic-agentic%20AI-7209b7)
![Explainable AI](https://img.shields.io/badge/topic-XAI-3a0ca3)
![RAG](https://img.shields.io/badge/topic-RAG-f77f00)

**Cloud & Infrastructure**

![AWS](https://img.shields.io/badge/AWS-232F3E?logo=amazonaws&logoColor=white)
![Amazon SageMaker](https://img.shields.io/badge/SageMaker-FF9900?logo=amazon-sagemaker&logoColor=white)
![Amazon Bedrock](https://img.shields.io/badge/Bedrock-222222?logo=amazon&logoColor=white)
![AWS Lambda](https://img.shields.io/badge/Lambda-FF9900?logo=awslambda&logoColor=white)
![Amazon S3](https://img.shields.io/badge/S3-569A31?logo=amazons3&logoColor=white)
![DynamoDB](https://img.shields.io/badge/DynamoDB-4053D6?logo=amazondynamodb&logoColor=white)
![API Gateway](https://img.shields.io/badge/API%20Gateway-FF4F8B?logo=amazonapigateway&logoColor=white)
![Cognito](https://img.shields.io/badge/Cognito-DD344C?logo=amazoncognito&logoColor=white)
![OpenSearch](https://img.shields.io/badge/OpenSearch-005EB8?logo=opensearch&logoColor=white)
![CloudFront](https://img.shields.io/badge/CloudFront-8C4FFF?logo=amazoncloudfront&logoColor=white)

**ML & Frontend**

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikitlearn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-337AB7)
![LightGBM](https://img.shields.io/badge/LightGBM-00A0DC)
![SHAP](https://img.shields.io/badge/SHAP-orange)
![Claude](https://img.shields.io/badge/Claude%203%20Haiku-D97757?logo=anthropic&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB)

</div>

---

## 📖 Overview

Primary ITP is an autoimmune disorder where bleeding risk becomes difficult to predict once platelet counts exceed 10 × 10⁹/L. This project builds a clinical decision-support tool that combines:

- 🧠 **Classical ML core** — Random Forest, XGBoost, LightGBM, and Logistic Regression trained on hospital ITP data, producing AUC comparisons and SHAP analysis.
- 🤖 **Agentic AI wrapper** — Amazon Bedrock agents (supervisor + sub-agents) producing natural-language, guideline-backed explanations in Vietnamese.

The hybrid design keeps the statistically rigorous ML model at the center (for thesis validation) while layering an LLM-based explanation interface on top for clinical usability.

## 👥 Project Context

### 🎯 Research Objectives

1. Describe clinical characteristics, laboratory findings, and bleeding status of adult ITP patients at BV TMHH
2. Compare predictive performance (AUC, sensitivity, specificity) of RF, XGBoost, LightGBM, and LR models; identify feature importance
3. Deliver an online application that helps clinicians rapidly assess bleeding risk

## 🏗️ Architecture

Four-layer AWS design:

| Layer | Components |
|-------|-----------|
| **4. Application** | API Gateway + Cognito, React (Vietnamese), Bedrock Guardrails |
| **3. Agentic AI** | Bedrock Agent `IDA` (supervisor) orchestrating Data Processing, Prediction, and Explanation sub-agents |
| **2. ML Serving** | SageMaker Studio (training), SageMaker Endpoint (inference), SageMaker Clarify (SHAP) |
| **1. Data** | S3 (data lake), AWS Glue (ETL), DynamoDB (feature store), OpenSearch Serverless (RAG vectors) |

Full details — including agent prompts, input features, cost estimates, and references — are in [`ITP_Bleeding_Prediction_Research_Plan.md`](./ITP_Bleeding_Prediction_Research_Plan.md).

## 🧪 Tech Stack

| Category | Technologies |
|----------|-------------|
| **Language** | Python 3.11+, TypeScript |
| **ML** | scikit-learn, XGBoost, LightGBM, SHAP |
| **LLM / Agents** | Amazon Bedrock, Claude 3 Haiku, Bedrock Agents, Bedrock Knowledge Base, Bedrock Guardrails |
| **Data** | Amazon S3, AWS Glue, DynamoDB, OpenSearch Serverless |
| **Serving** | SageMaker Endpoint, SageMaker Clarify, AWS Lambda |
| **Application** | React.js, API Gateway, Amazon Cognito, AWS Amplify, CloudFront |
| **Observability** | Amazon CloudWatch |

## 🩺 Clinical Inputs (10 Features)

Infection · uncontrolled diabetes · age · ITP type · cardiovascular disease · low lymphocyte count · skin/mucosa bleeding · initial platelet count · current platelet count <20 × 10⁹/L · disease duration.

**Outcome**: Hemorrhage ≥ Grade 2 (WHO scale), binary.

## 🗓️ Implementation Phases

| Phase | Timeline | Deliverable |
|-------|----------|-------------|
| **1. Data & ML Core** | Months 1–2 | Trained models, AUC comparison, SHAP analysis |
| **2. Agentic AI Layer** | Months 3–4 | Bedrock agent pipeline with RAG explanations |
| **3. Application & UAT** | Months 5–6 | Production React app, clinician testing at BV TMHH |

## 🚦 Status

> 🟡 **Planning phase** — the detailed technical blueprint is checked in; implementation code is added during Phase 1.

## 🔒 Security & Compliance

- ✅ All AWS services selected are HIPAA-eligible (BAA required)
- ✅ Patient data is de-identified before entering the system
- ✅ SSE-S3 at rest, TLS 1.2+ in transit, VPC isolation for compute
- ✅ Cognito MFA for clinician authentication
- ✅ Bedrock Guardrails enforce PHI filtering and scope restriction (risk assessment only — not treatment prescription)

## 📚 References

- **An et al. (2023)** — *Life-threatening bleeding prediction model for ITP based on personalized ML*, Science Bulletin 68:2106–2114
- **Dhiman et al. (2026)** — *An Agentic AI system for disease diagnosis with explanations*, Informatics and Health 3:32–40
- **Shen et al. (2025)** — *Prediction of moderate-to-severe bleeding risk in pediatric ITP using ML*, Eur J Pediatr 184:283

Full reference list in the research plan.

## 📄 License

Released under the [MIT License](./LICENSE).

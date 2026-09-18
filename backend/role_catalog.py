"""
Zavran AI — 200+ Professional Role Catalog
Defines over 200 distinct, structured professional roles categorized across 22 industry verticals.
Each role provides name, category, description, common skills, and typical seniority levels.
"""

from typing import Dict, Any, List, Optional
import re

ROLE_CATALOG: List[Dict[str, Any]] = [
    # =========================================================================
    # 1. AI & MACHINE LEARNING (15 roles)
    # =========================================================================
    {
        "name": "AI Engineer",
        "category": "AI & Machine Learning",
        "description": "Designs, implements, and deploys production-grade AI applications and LLM agentic pipelines.",
        "common_skills": ["Python", "LLMs", "RAG", "LangChain/LangGraph", "Vector Databases", "Prompt Engineering", "FastAPI"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Staff", "Principal"]
    },
    {
        "name": "Machine Learning Engineer",
        "category": "AI & Machine Learning",
        "description": "Builds, optimizes, and productionalizes machine learning models, inference servers, and training pipelines.",
        "common_skills": ["PyTorch", "TensorFlow", "Scikit-Learn", "Model Optimization", "Feature Engineering", "Python", "MLflow"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Staff"]
    },
    {
        "name": "MLOps Engineer",
        "category": "AI & Machine Learning",
        "description": "Manages continuous deployment, monitoring, drift detection, and automated retraining for ML systems.",
        "common_skills": ["Kubeflow", "MLflow", "Docker", "Kubernetes", "CI/CD", "Prometheus", "Model Registry", "Python"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Computer Vision Engineer",
        "category": "AI & Machine Learning",
        "description": "Develops algorithms for visual perception, object detection, segmentation, and video analytics.",
        "common_skills": ["OpenCV", "PyTorch", "YOLO", "CNNs", "Image Processing", "TensorRT", "C++", "Python"],
        "seniority_levels": ["Mid-Level", "Senior", "Staff"]
    },
    {
        "name": "NLP Specialist",
        "category": "AI & Machine Learning",
        "description": "Builds natural language processing pipelines, tokenizers, named entity recognition, and translation systems.",
        "common_skills": ["Transformers", "Hugging Face", "Spacy", "NLTK", "BERT", "Tokenization", "Python"],
        "seniority_levels": ["Mid-Level", "Senior", "Staff"]
    },
    {
        "name": "LLM Solutions Architect",
        "category": "AI & Machine Learning",
        "description": "Architects enterprise-scale generative AI workflows, guardrails, context caching, and fine-tuning pipelines.",
        "common_skills": ["RAG Architecture", "LoRA/QLoRA", "Quantization", "vLLM", "Context Windows", "System Design", "Cloud Infrastructure"],
        "seniority_levels": ["Senior", "Staff", "Principal"]
    },
    {
        "name": "Deep Learning Research Engineer",
        "category": "AI & Machine Learning",
        "description": "Implements novel neural network architectures, loss functions, and optimization techniques from scientific papers.",
        "common_skills": ["PyTorch", "JAX", "CUDA", "Distributed Training", "Mathematical Modeling", "Research Prototyping"],
        "seniority_levels": ["Senior", "Staff", "Principal"]
    },
    {
        "name": "Prompt Engineer & AI Evaluator",
        "category": "AI & Machine Learning",
        "description": "Crafts high-precision system prompts, few-shot patterns, benchmark evaluation suites, and red-teaming tests.",
        "common_skills": ["Prompt Design", "LLM Evals", "RAG Triad", "Red Teaming", "Few-Shot Learning", "Python", "JSON Schema"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior"]
    },
    {
        "name": "Robotics AI Engineer",
        "category": "AI & Machine Learning",
        "description": "Develops spatial AI, reinforcement learning, trajectory planning, and SLAM for autonomous robotic systems.",
        "common_skills": ["ROS/ROS2", "Reinforcement Learning", "C++", "Python", "SLAM", "Kalman Filters", "Gazebo"],
        "seniority_levels": ["Mid-Level", "Senior", "Staff"]
    },
    {
        "name": "Speech & Audio AI Engineer",
        "category": "AI & Machine Learning",
        "description": "Builds speech recognition (STT), voice cloning, text-to-speech (TTS), and real-time audio streaming models.",
        "common_skills": ["Whisper", "VITS/Bark", "Audio DSP", "PyTorch", "WebRTC", "Mel-Spectrograms", "Python"],
        "seniority_levels": ["Mid-Level", "Senior", "Staff"]
    },
    {
        "name": "AI Safety & Alignment Engineer",
        "category": "AI & Machine Learning",
        "description": "Implements RLHF, DPO, constitutional AI, toxic content classifiers, and safety guardrails for generative models.",
        "common_skills": ["RLHF", "DPO", "Safety Benchmarks", "Toxicity Classifiers", "Model Red-Teaming", "PyTorch"],
        "seniority_levels": ["Senior", "Staff", "Principal"]
    },
    {
        "name": "Autonomous Systems Engineer",
        "category": "AI & Machine Learning",
        "description": "Designs perception, sensor fusion, and decision-making modules for self-driving vehicles and drones.",
        "common_skills": ["Sensor Fusion", "LiDAR/Radar Processing", "C++", "Safety Critical Systems", "Kalman Filters", "CUDA"],
        "seniority_levels": ["Senior", "Staff", "Principal"]
    },
    {
        "name": "Conversational AI Developer",
        "category": "AI & Machine Learning",
        "description": "Constructs intelligent conversational chatbots, multi-turn dialogue state trackers, and voice agents.",
        "common_skills": ["Dialogue Management", "Rasa", "WebSocket Streaming", "Intent Recognition", "TTS/STT Integration", "Node.js/Python"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior"]
    },
    {
        "name": "Edge AI Engineer",
        "category": "AI & Machine Learning",
        "description": "Optimizes neural network models for embedded devices, microcontrollers, and edge hardware accelerators.",
        "common_skills": ["TensorFlow Lite", "ONNX Runtime", "CoreML", "Quantization", "ARM Cortex", "C++", "Embedded Linux"],
        "seniority_levels": ["Mid-Level", "Senior", "Staff"]
    },
    {
        "name": "AI Product Specialist",
        "category": "AI & Machine Learning",
        "description": "Bridges AI technical capability with domain product requirements, user experience, and model governance.",
        "common_skills": ["LLM Capabilities", "Model Governance", "User Journey Mapping", "Feasibility Assessment", "Data Strategy"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead"]
    },

    # =========================================================================
    # 2. SOFTWARE ENGINEERING (18 roles)
    # =========================================================================
    {
        "name": "Full Stack Engineer",
        "category": "Software Engineering",
        "description": "Builds end-to-end web applications across modern frontend frameworks and scalable backend services.",
        "common_skills": ["TypeScript", "React/Next.js", "Node.js", "Python/Go", "PostgreSQL", "REST/GraphQL", "Docker"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead", "Staff"]
    },
    {
        "name": "Backend Developer",
        "category": "Software Engineering",
        "description": "Designs high-performance server-side APIs, database schemas, caching strategies, and event-driven architectures.",
        "common_skills": ["Python/Java/Go", "FastAPI/Spring Boot", "PostgreSQL", "Redis", "Kafka", "Microservices", "Docker"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Staff", "Principal"]
    },
    {
        "name": "Frontend Developer",
        "category": "Software Engineering",
        "description": "Crafts responsive, performant, and accessible user interfaces with modern client-side architectures.",
        "common_skills": ["JavaScript/TypeScript", "React/Vue/Angular", "HTML5/CSS3", "TailwindCSS", "State Management", "Web Performance"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Distributed Systems Engineer",
        "category": "Software Engineering",
        "description": "Architects fault-tolerant, horizontally scalable consensus protocols, replication systems, and storage engines.",
        "common_skills": ["Go/Rust/C++", "Raft/Paxos", "Distributed Caching", "gRPC", "CAP Theorem", "High Concurrency"],
        "seniority_levels": ["Senior", "Staff", "Principal"]
    },
    {
        "name": "iOS Developer",
        "category": "Software Engineering",
        "description": "Develops native mobile applications for Apple iOS, iPadOS, and watchOS ecosystems.",
        "common_skills": ["Swift", "SwiftUI", "UIKit", "Combine", "CoreData", "App Store Guidelines", "Memory Management"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Android Developer",
        "category": "Software Engineering",
        "description": "Builds native Android applications with reactive architectures and Android Jetpack libraries.",
        "common_skills": ["Kotlin", "Jetpack Compose", "Coroutines/Flow", "Room Database", "Retrofit", "Material 3", "Gradle"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Flutter / React Native Developer",
        "category": "Software Engineering",
        "description": "Develops cross-platform mobile apps for iOS and Android with high code reuse and native bridge optimization.",
        "common_skills": ["Dart/Flutter", "React Native", "TypeScript", "Native Modules", "Mobile CI/CD", "State Management"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior"]
    },
    {
        "name": "Systems Programmer",
        "category": "Software Engineering",
        "description": "Writes low-level kernel modules, OS services, network drivers, and memory-safe system utilities.",
        "common_skills": ["C", "Rust", "C++", "Linux Internals", "POSIX APIs", "Memory Safety", "GDB/Valgrind"],
        "seniority_levels": ["Mid-Level", "Senior", "Staff"]
    },
    {
        "name": "Embedded Software Engineer",
        "category": "Software Engineering",
        "description": "Programs microcontrollers, RTOS firmware, hardware interfaces, and IoT connected devices.",
        "common_skills": ["Embedded C/C++", "FreeRTOS", "I2C/SPI/UART", "ARM Architecture", "Oscilloscopes", "Hardware Debugging"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Staff"]
    },
    {
        "name": "API & Integration Engineer",
        "category": "Software Engineering",
        "description": "Designs unified enterprise API gateways, webhooks, third-party connector pipelines, and protocol adapters.",
        "common_skills": ["OpenAPI/Swagger", "REST/gRPC/GraphQL", "OAuth2", "Rate Limiting", "Enterprise Integration", "Postman"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Compiler & Language Engineer",
        "category": "Software Engineering",
        "description": "Constructs programming language interpreters, LLVM backends, AST parsers, and JIT optimization passes.",
        "common_skills": ["LLVM", "C++", "Rust", "Grammars (BNF)", "Type Systems", "Code Generation", "Optimization Passes"],
        "seniority_levels": ["Senior", "Staff", "Principal"]
    },
    {
        "name": "Graphics & Game Engine Developer",
        "category": "Software Engineering",
        "description": "Implements rendering pipelines, shader programs, physics simulations, and custom game engine systems.",
        "common_skills": ["C++", "Vulkan/DirectX/OpenGL", "HLSL/GLSL", "Linear Algebra", "Unreal Engine/Unity", "Spatial Data Structures"],
        "seniority_levels": ["Mid-Level", "Senior", "Staff"]
    },
    {
        "name": "Firmware Engineer",
        "category": "Software Engineering",
        "description": "Writes bare-metal bootloaders, device drivers, and board support packages (BSP) for consumer electronics.",
        "common_skills": ["Bare-Metal C", "Bootloaders", "Hardware Schematics", "JTAG/SWD", "Flash Memory", "Low Power Modes"],
        "seniority_levels": ["Mid-Level", "Senior", "Staff"]
    },
    {
        "name": "Microservices Architect",
        "category": "Software Engineering",
        "description": "Designs domain-driven distributed service boundaries, event sourcing, transactional outboxes, and resilience.",
        "common_skills": ["Domain Driven Design", "Event Sourcing", "Saga Pattern", "Kafka/RabbitMQ", "Service Mesh", "Kubernetes"],
        "seniority_levels": ["Senior", "Staff", "Principal"]
    },
    {
        "name": "Desktop Application Developer",
        "category": "Software Engineering",
        "description": "Builds high-performance native and cross-platform desktop applications (Electron, Tauri, Qt, .NET).",
        "common_skills": ["C# / .NET", "C++ / Qt", "Tauri/Rust", "Electron/TypeScript", "Native OS APIs", "Packaging/Installers"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "WebAssembly (WASM) Engineer",
        "category": "Software Engineering",
        "description": "Compiles high-performance codebases to browser runtimes with WebAssembly, SIMD, and shared memory.",
        "common_skills": ["Rust", "C++", "Emscripten", "WebAssembly APIs", "Web Workers", "SharedArrayBuffer", "Browser Profiling"],
        "seniority_levels": ["Senior", "Staff"]
    },
    {
        "name": "Legacy Migration Engineer",
        "category": "Software Engineering",
        "description": "Modernizes legacy monolithic systems (COBOL, Mainframe, Java 6/7) to modern cloud-native architectures.",
        "common_skills": ["Strangler Fig Pattern", "Refactoring", "Java/C#", "Database Migration", "Automated Testing", "Cloud Modernization"],
        "seniority_levels": ["Senior", "Staff", "Principal"]
    },
    {
        "name": "Engineering Manager",
        "category": "Software Engineering",
        "description": "Leads software engineering squads, drives architectural standards, mentors engineers, and manages delivery.",
        "common_skills": ["Technical Leadership", "People Management", "Agile Execution", "Hiring & Mentoring", "Sprint Planning", "System Design"],
        "seniority_levels": ["Manager", "Senior Manager", "Director"]
    },

    # =========================================================================
    # 3. DATA & ANALYTICS (12 roles)
    # =========================================================================
    {
        "name": "Data Scientist",
        "category": "Data & Analytics",
        "description": "Applies statistical modeling, exploratory data analysis, and predictive modeling to solve business problems.",
        "common_skills": ["Python", "SQL", "Pandas/NumPy", "Statistical Analysis", "A/B Testing", "Machine Learning", "Data Visualization"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead", "Principal"]
    },
    {
        "name": "Data Engineer",
        "category": "Data & Analytics",
        "description": "Builds resilient ETL/ELT pipelines, data lakes, streaming architectures, and distributed warehouse schemas.",
        "common_skills": ["SQL", "Python/Scala", "Apache Spark", "Airflow/dbt", "Snowflake/BigQuery", "Kafka", "Data Modeling"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Staff", "Principal"]
    },
    {
        "name": "Analytics Engineer",
        "category": "Data & Analytics",
        "description": "Transforms raw warehouse data into clean, tested, documented, and reusable dimensional data models.",
        "common_skills": ["dbt", "SQL", "Snowflake/BigQuery", "Data Modeling", "Git", "Looker/Tableau", "Data Testing"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Business Intelligence (BI) Developer",
        "category": "Data & Analytics",
        "description": "Designs enterprise reporting dashboards, DAX measures, OLAP cubes, and executive KPI trackers.",
        "common_skills": ["Power BI", "Tableau", "SQL", "DAX/M", "Data Warehousing", "KPI Dashboarding", "ETL Integration"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Data Architect",
        "category": "Data & Analytics",
        "description": "Defines enterprise data governance, master data management, schema architecture, and lakehouse strategy.",
        "common_skills": ["Enterprise Data Architecture", "Data Mesh", "Medallion Architecture", "Data Governance", "Delta Lake/Iceberg"],
        "seniority_levels": ["Senior", "Staff", "Principal"]
    },
    {
        "name": "Big Data Engineer",
        "category": "Data & Analytics",
        "description": "Processes petabyte-scale batch and streaming data across distributed clusters and cloud pipelines.",
        "common_skills": ["Apache Spark", "Hadoop/Hive", "Kafka Streams", "Flink", "Scala/Java", "AWS EMR/Databricks"],
        "seniority_levels": ["Mid-Level", "Senior", "Staff"]
    },
    {
        "name": "Quantitative Analyst (Quant)",
        "category": "Data & Analytics",
        "description": "Develops mathematical pricing models, algorithmic trading strategies, and risk quantification formulas.",
        "common_skills": ["Stochastic Calculus", "Python/C++", "Time Series Forecasting", "Financial Mathematics", "Monte Carlo Simulations"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead", "Principal"]
    },
    {
        "name": "Marketing Data Analyst",
        "category": "Data & Analytics",
        "description": "Analyzes customer attribution, multi-touch funnels, campaign ROI, and customer lifetime value (LTV).",
        "common_skills": ["SQL", "Google Analytics 4", "Cohort Analysis", "Attribution Modeling", "Python/R", "Tableau"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior"]
    },
    {
        "name": "Data Governance & Quality Lead",
        "category": "Data & Analytics",
        "description": "Establishes data lineage, data cataloging, quality SLAs, GDPR/CCPA compliance, and stewardship programs.",
        "common_skills": ["Collibra/Alation", "Great Expectations", "Data Lineage", "Data Cataloging", "Compliance Standards", "SQL"],
        "seniority_levels": ["Senior", "Lead", "Director"]
    },
    {
        "name": "Spatial / GIS Data Analyst",
        "category": "Data & Analytics",
        "description": "Processes geospatial datasets, satellite imagery, coordinate systems, and spatial indexing.",
        "common_skills": ["ArcGIS/QGIS", "PostGIS", "GeoPandas", "Spatial Indexing (H3/S2)", "Remote Sensing", "SQL"],
        "seniority_levels": ["Mid-Level", "Senior"]
    },
    {
        "name": "Clinical Data Analyst",
        "category": "Data & Analytics",
        "description": "Analyzes electronic health records (EHR), clinical trial protocols, CDISC standards, and biometric data.",
        "common_skills": ["SAS/R", "CDISC / SDTM", "HIPAA Compliance", "Clinical Biostatistics", "SQL", "Medical Coding"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Operations Data Analyst",
        "category": "Data & Analytics",
        "description": "Optimizes internal business processes, inventory forecasting, capacity planning, and operational SLAs.",
        "common_skills": ["SQL", "Excel / VBA", "Python", "Process Mining", "Root Cause Analysis", "Power BI"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior"]
    },

    # =========================================================================
    # 4. CLOUD & DEVOPS (12 roles)
    # =========================================================================
    {
        "name": "DevOps Engineer",
        "category": "Cloud & DevOps",
        "description": "Implements automated CI/CD pipelines, Infrastructure as Code, container orchestration, and developer tooling.",
        "common_skills": ["Terraform", "Docker", "Kubernetes", "GitHub Actions/GitLab CI", "AWS/GCP/Azure", "Linux/Bash", "Python"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead", "Staff"]
    },
    {
        "name": "Site Reliability Engineer (SRE)",
        "category": "Cloud & DevOps",
        "description": "Ensures uptime, latency SLAs, chaos engineering, incident management, and automated failover for production.",
        "common_skills": ["SLIs/SLOs/Error Budgets", "Prometheus/Grafana", "Distributed Tracing (OpenTelemetry)", "Incident Response", "Chaos Engineering", "Python/Go"],
        "seniority_levels": ["Mid-Level", "Senior", "Staff", "Principal"]
    },
    {
        "name": "Cloud Solutions Architect (AWS/GCP/Azure)",
        "category": "Cloud & DevOps",
        "description": "Architects multi-region, resilient, cost-efficient cloud infrastructures across IaaS, PaaS, and serverless.",
        "common_skills": ["Cloud Architecture", "Well-Architected Framework", "VPC/Networking", "IAM Security", "Terraform", "FinOps"],
        "seniority_levels": ["Senior", "Staff", "Principal"]
    },
    {
        "name": "Platform Engineer",
        "category": "Cloud & DevOps",
        "description": "Constructs internal developer platforms (IDP), self-service provisioning portals, and service templates.",
        "common_skills": ["Backstage", "Kubernetes Operators", "Helm", "Crossplane/Terraform", "Developer Tooling", "Go/Python"],
        "seniority_levels": ["Mid-Level", "Senior", "Staff"]
    },
    {
        "name": "Kubernetes & Container Specialist",
        "category": "Cloud & DevOps",
        "description": "Manages enterprise Kubernetes clusters, ingress controllers, CNI networking, service meshes, and GitOps.",
        "common_skills": ["Kubernetes Admin (CKA)", "Istio/Linkerd", "ArgoCD/Flux", "Cilium/Calico", "Helm", "Container Security"],
        "seniority_levels": ["Senior", "Staff"]
    },
    {
        "name": "FinOps / Cloud Cost Optimization Engineer",
        "category": "Cloud & DevOps",
        "description": "Monitors cloud expenditures, rightsizes infrastructure, purchases savings plans/reserved instances, and cuts waste.",
        "common_skills": ["Cloud FinOps", "AWS Cost Explorer/CUR", "Rightsizing", "Tagging Governance", "Kubecost", "Spot Instances"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Infrastructure as Code (IaC) Specialist",
        "category": "Cloud & DevOps",
        "description": "Authors modular, immutable infrastructure definitions using Terraform, OpenTofu, Pulumi, and Ansible.",
        "common_skills": ["Terraform/OpenTofu", "Pulumi", "Ansible", "Terragrunt", "Policy as Code (OPA)", "GitOps"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Cloud Database Administrator (DBA)",
        "category": "Cloud & DevOps",
        "description": "Administers cloud managed databases (RDS, Aurora, Cloud Spanner), clustering, query tuning, and disaster recovery.",
        "common_skills": ["PostgreSQL/MySQL Tuning", "Aurora/Spanner", "Replication & Sharding", "Backup & PITR", "Connection Pooling (PgBouncer)"],
        "seniority_levels": ["Mid-Level", "Senior", "Staff"]
    },
    {
        "name": "Release & Build Engineer",
        "category": "Cloud & DevOps",
        "description": "Automates multi-platform build pipelines, artifact repositories, binary signing, and release governance.",
        "common_skills": ["Bazel/Gradle", "Artifact Registries", "Code Signing", "Semantic Versioning", "Automated Release Notes", "CI/CD"],
        "seniority_levels": ["Mid-Level", "Senior"]
    },
    {
        "name": "Network & Cloud Connectivity Engineer",
        "category": "Cloud & DevOps",
        "description": "Designs hybrid-cloud network topologies, Direct Connect/ExpressRoute, VPN tunnels, BGP routing, and SD-WAN.",
        "common_skills": ["BGP / Routing Protocols", "Direct Connect / ExpressRoute", "Transit Gateway", "WireGuard / IPsec", "Wireshark", "DNS/BGP"],
        "seniority_levels": ["Mid-Level", "Senior", "Staff"]
    },
    {
        "name": "Serverless & Event-Driven Architect",
        "category": "Cloud & DevOps",
        "description": "Architects serverless applications with AWS Lambda, EventBridge, Step Functions, SQS, and DynamoDB.",
        "common_skills": ["AWS Lambda / Cloud Functions", "EventBridge / SNS / SQS", "DynamoDB Modeling", "Cold Start Optimization", "Serverless Framework"],
        "seniority_levels": ["Senior", "Staff"]
    },
    {
        "name": "Cloud Operations Manager",
        "category": "Cloud & DevOps",
        "description": "Supervises 24/7 cloud NOC teams, on-call schedules, operational readiness reviews, and infrastructure lifecycle.",
        "common_skills": ["Operations Management", "PagerDuty / Opsgenie", "ITIL / Incident Lifecycle", "Vendor Management", "SLA Enforcement"],
        "seniority_levels": ["Manager", "Senior Manager", "Director"]
    },

    # =========================================================================
    # 5. CYBERSECURITY (12 roles)
    # =========================================================================
    {
        "name": "Application Security (AppSec) Engineer",
        "category": "Cybersecurity",
        "description": "Embeds SAST/DAST tooling into CI/CD, conducts code security reviews, and remediates OWASP Top 10 flaws.",
        "common_skills": ["OWASP Top 10", "SAST / DAST / SCA", "Threat Modeling (STRIDE)", "Code Security Review", "Burp Suite", "Secure SDLC"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Staff"]
    },
    {
        "name": "Security Operations Center (SOC) Analyst",
        "category": "Cybersecurity",
        "description": "Monitors SIEM telemetry, investigates security alerts, triages malware incidents, and performs threat hunting.",
        "common_skills": ["SIEM (Splunk/Sentinel)", "EDR / XDR", "Incident Triage", "Log Analysis", "MITRE ATT&CK", "Network Forensics"],
        "seniority_levels": ["Tier 1", "Tier 2", "Tier 3", "SOC Lead"]
    },
    {
        "name": "Penetration Tester & Ethical Hacker",
        "category": "Cybersecurity",
        "description": "Performs authorized offensive security assessments across web apps, APIs, networks, and cloud perimeters.",
        "common_skills": ["Burp Suite Pro", "Metasploit", "Network Exploitation", "Privilege Escalation", "Active Directory Attacks", "OSCP/CEH"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Cloud Security Architect",
        "category": "Cybersecurity",
        "description": "Defines Zero Trust architectures, Cloud Security Posture Management (CSPM), and IAM least-privilege governance.",
        "common_skills": ["Zero Trust Architecture", "CSPM / CIEM", "Cloud IAM Policies", "AWS GuardDuty / Security Hub", "KMS / Encryption"],
        "seniority_levels": ["Senior", "Staff", "Principal"]
    },
    {
        "name": "Identity & Access Management (IAM) Engineer",
        "category": "Cybersecurity",
        "description": "Builds enterprise SSO, OAuth2/OIDC, SAML, SCIM provisioning, privileged access management (PAM), and MFA.",
        "common_skills": ["OAuth2 / OIDC", "SAML 2.0", "Okta / Entra ID", "PAM (CyberArk)", "SCIM Provisioning", "Role-Based Access Control"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Cryptographic Engineer",
        "category": "Cybersecurity",
        "description": "Implements public-key infrastructure, post-quantum algorithms, zero-knowledge proofs, and secure hardware enclaves.",
        "common_skills": ["PKI / TLS", "ZK-SNARKs / Zero Knowledge", "Elliptic Curve Crypto", "HSM Integration", "Rust / C", "Quantum Resistance"],
        "seniority_levels": ["Senior", "Staff", "Principal"]
    },
    {
        "name": "Incident Response & Digital Forensics Lead",
        "category": "Cybersecurity",
        "description": "Coordinates live containment during ransomware/data breaches, forensic memory acquisition, and post-mortems.",
        "common_skills": ["Digital Forensics (EnCase/Volatility)", "Memory Dump Analysis", "Ransomware Containment", "Chain of Custody", "Crisis Communication"],
        "seniority_levels": ["Senior", "Lead", "Director"]
    },
    {
        "name": "DevSecOps Engineer",
        "category": "Cybersecurity",
        "description": "Automates container scanning, secret detection, policy-as-code, and compliance guardrails in pipeline execution.",
        "common_skills": ["Trivy / Snyk", "GitGuardian", "OPA / Gatekeeper", "HashiCorp Vault", "CI/CD Security", "Terraform Security"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Threat Intelligence Analyst",
        "category": "Cybersecurity",
        "description": "Tracks Advanced Persistent Threat (APT) groups, malware indicators of compromise (IOCs), and dark web activities.",
        "common_skills": ["Threat Feeds (STIX/TAXII)", "APT Attribution", "YARA Rules", "OSINT", "Malware Disassembly Basics"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Security Compliance & GRC Lead",
        "category": "Cybersecurity",
        "description": "Oversees SOC 2, ISO 27001, HIPAA, FedRAMP, and PCI-DSS certification audits and internal risk registries.",
        "common_skills": ["SOC 2 Type II", "ISO 27001", "Risk Assessment Frameworks", "Vendor Risk Management", "Vanta/Drata", "Audit Prep"],
        "seniority_levels": ["Senior", "Lead", "Director"]
    },
    {
        "name": "Vulnerability Management Engineer",
        "category": "Cybersecurity",
        "description": "Manages automated vulnerability scanners, CVSS risk scoring, patch prioritization, and asset discovery.",
        "common_skills": ["Qualys / Tenable Nessus", "CVSS v3/v4 Scoring", "Patch Management Workflows", "Asset Inventory", "Risk Prioritization"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior"]
    },
    {
        "name": "Chief Information Security Officer (CISO)",
        "category": "Cybersecurity",
        "description": "Sets enterprise security vision, board risk reporting, security budget allocation, and cybersecurity posture.",
        "common_skills": ["Executive Risk Management", "Board Reporting", "Security Governance", "Cyber Insurance", "Crisis Leadership"],
        "seniority_levels": ["Executive (VP / CISO)"]
    },

    # =========================================================================
    # 6. QA & TESTING (8 roles)
    # =========================================================================
    {
        "name": "Software Development Engineer in Test (SDET)",
        "category": "QA & Testing",
        "description": "Develops programmatic test automation frameworks, mocking engines, and integration testing pipelines.",
        "common_skills": ["Playwright/Cypress", "Selenium", "TypeScript/Python/Java", "API Testing (RestAssured)", "CI/CD Test Runner", "Docker"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead", "Staff"]
    },
    {
        "name": "QA Automation Engineer",
        "category": "QA & Testing",
        "description": "Creates end-to-end regression suites, UI test scripts, cross-browser validation, and test reporting dashboards.",
        "common_skills": ["Playwright", "Cypress", "Page Object Model", "Appium", "Allure Reporting", "JavaScript/Python"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Performance & Load Test Engineer",
        "category": "QA & Testing",
        "description": "Simulates high-concurrency traffic spikes, stress scenarios, bottleneck profiling, and endurance benchmarks.",
        "common_skills": ["k6", "JMeter", "Gatling", "Distributed Load Testing", "APM Profiling", "Network Latency Simulation"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Mobile QA Engineer",
        "category": "QA & Testing",
        "description": "Conducts automated and manual testing on real iOS and Android physical devices, emulators, and device farms.",
        "common_skills": ["Appium", "XCUITest / Espresso", "BrowserStack / SauceLabs", "Mobile Gestures", "Crashlytics", "Network Throttling"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior"]
    },
    {
        "name": "Manual & Exploratory QA Tester",
        "category": "QA & Testing",
        "description": "Executes user scenario exploratory testing, edge-case discovery, accessibility checks, and bug report authoring.",
        "common_skills": ["Test Plan Authoring", "Exploratory Testing", "Jira / TestRail", "Regression Verification", "Accessibility Testing (WCAG)"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior"]
    },
    {
        "name": "Security QA / Penetration QA Engineer",
        "category": "QA & Testing",
        "description": "Integrates automated dynamic security testing (DAST), fuzz testing, and authorization boundary validation.",
        "common_skills": ["ZAP Proxy", "Fuzz Testing", "BOLA/BFLA API Checks", "Input Validation Testing", "OWASP ASVS"],
        "seniority_levels": ["Mid-Level", "Senior"]
    },
    {
        "name": "Data Quality & ETL QA Engineer",
        "category": "QA & Testing",
        "description": "Validates data transformation rules, reconciliation scripts, schema migrations, and statistical data tests.",
        "common_skills": ["SQL Testing", "Great Expectations", "Data Reconciliation", "Schema Validation", "Python Data Checks"],
        "seniority_levels": ["Mid-Level", "Senior"]
    },
    {
        "name": "QA Manager / Director",
        "category": "QA & Testing",
        "description": "Leads organizational quality engineering strategy, test metrics (coverage, defect escape rate), and team governance.",
        "common_skills": ["Quality Strategy", "Defect Metrics & SLAs", "Resource Allocation", "Test Automation ROI", "Leadership"],
        "seniority_levels": ["Manager", "Director"]
    },

    # =========================================================================
    # 7. PRODUCT MANAGEMENT (10 roles)
    # =========================================================================
    {
        "name": "Technical Product Manager (TPM)",
        "category": "Product Management",
        "description": "Drives API platforms, developer tools, infrastructure services, and high-complexity technical roadmaps.",
        "common_skills": ["API Specifications", "System Architecture Understanding", "Developer Experience", "PRD Authoring", "Agile Roadmapping"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead", "Principal", "Director"]
    },
    {
        "name": "AI Product Manager",
        "category": "Product Management",
        "description": "Guides generative AI features, model evaluation thresholds, prompt testing, and AI ethics frameworks.",
        "common_skills": ["LLM Economics", "Model Evaluation (Evals)", "Prompt/Agent Workflows", "AI UX Patterns", "Data Flywheels"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead", "Director"]
    },
    {
        "name": "Growth Product Manager",
        "category": "Product Management",
        "description": "Focuses on user acquisition, onboarding conversion, monetization loops, referral mechanisms, and A/B testing.",
        "common_skills": ["A/B Experimentation", "Funnel Optimization", "PLG (Product-Led Growth)", "Cohort Retention", "Analytics (Amplitude/Mixpanel)"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Enterprise B2B Product Manager",
        "category": "Product Management",
        "description": "Develops enterprise features: RBAC, audit logging, multi-tenancy, custom workflows, and SSO.",
        "common_skills": ["Enterprise Requirements", "RBAC/SSO", "B2B Buyer Personas", "Feature Flagging", "Customer Advisory Boards"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead", "Director"]
    },
    {
        "name": "Consumer (B2C) Product Manager",
        "category": "Product Management",
        "description": "Designs high-engagement mobile/web consumer applications, habit loops, notification systems, and viral mechanics.",
        "common_skills": ["Consumer Psychology", "Mobile UX", "User Empathy", "Viral Loops", "Rapid Prototyping", "Analytics"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Platform Product Manager",
        "category": "Product Management",
        "description": "Manages core platform services, internal APIs, billing engines, and shared capabilities across squads.",
        "common_skills": ["Platform Strategy", "Internal Stakeholder Management", "Microservice Dependency Roadmaps", "SLA Governance"],
        "seniority_levels": ["Senior", "Lead", "Director"]
    },
    {
        "name": "Fintech Product Manager",
        "category": "Product Management",
        "description": "Oversees payment gateways, ledger systems, fraud mitigation, KYC/AML flows, and banking integrations.",
        "common_skills": ["Payment Gateways (Stripe)", "Double-Entry Ledgers", "Regulatory Compliance", "Fraud Prevention", "Transaction Latency"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead", "Director"]
    },
    {
        "name": "Healthcare Product Manager",
        "category": "Product Management",
        "description": "Directs digital health applications, telemedicine, EHR integrations (HL7/FHIR), and HIPAA-compliant patient portals.",
        "common_skills": ["HIPAA Compliance", "HL7 / FHIR Standards", "Clinical Workflows", "Patient Privacy", "Medical Device Regs (FDA)"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "E-Commerce Product Manager",
        "category": "Product Management",
        "description": "Optimizes search relevance, checkout flows, recommendation carousels, inventory management, and cart conversion.",
        "common_skills": ["Cart & Checkout Optimization", "Search & Discovery (Algolia)", "Recommendation Algorithms", "Order Management"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Chief Product Officer (CPO) / VP Product",
        "category": "Product Management",
        "description": "Shapes overall product vision, portfolio strategy, cross-functional team alignment, and executive board roadmap.",
        "common_skills": ["Product Strategy", "Executive Leadership", "Market Positioning", "Organizational Design", "M&A Evaluation"],
        "seniority_levels": ["Executive (VP / CPO)"]
    },

    # =========================================================================
    # 8. PROJECT & AGILE MANAGEMENT (8 roles)
    # =========================================================================
    {
        "name": "Technical Program Manager (TPM)",
        "category": "Project Management",
        "description": "Drives cross-team engineering execution, cross-service dependencies, launch milestones, and risk mitigation.",
        "common_skills": ["Cross-Functional Alignment", "Dependency Mapping", "Milestone Tracking", "Risk Registers", "Technical Architecture"],
        "seniority_levels": ["Mid-Level", "Senior", "Staff", "Principal", "Director"]
    },
    {
        "name": "Scrum Master",
        "category": "Project Management",
        "description": "Facilitates sprint ceremonies, removes blockers, tracks team velocity, and fosters continuous agile improvement.",
        "common_skills": ["Scrum Framework (CSM/PSM)", "Sprint Ceremonies", "Burndown Charts", "Impediment Removal", "Retrospectives"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Agile Coach",
        "category": "Project Management",
        "description": "Trains organizations on Lean/Agile methodologies, SAFe frameworks, Kanban transformations, and team psychology.",
        "common_skills": ["SAFe / LeSS Frameworks", "Agile Transformation", "Executive Coaching", "Kanban Workflows", "Value Stream Mapping"],
        "seniority_levels": ["Senior", "Lead", "Principal"]
    },
    {
        "name": "IT Project Manager",
        "category": "Project Management",
        "description": "Manages enterprise software rollouts, infrastructure upgrades, vendor contracts, and budget allocations.",
        "common_skills": ["PMP / Prince2", "Budget Tracking", "Vendor Management", "Gantt Charts (MS Project)", "Change Management"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Delivery Manager",
        "category": "Project Management",
        "description": "Ensures client software projects are shipped on schedule, within scope, with high engineering quality.",
        "common_skills": ["Client Communication", "Scope Management", "Resource Planning", "Quality Governance", "Billing/Invoicing"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead", "Director"]
    },
    {
        "name": "Operations Project Manager",
        "category": "Project Management",
        "description": "Coordinates internal operational initiatives, process optimizations, facility expansions, and tool migrations.",
        "common_skills": ["Process Optimization", "Stakeholder Communication", "Asana/ClickUp/Jira", "Change Implementation"],
        "seniority_levels": ["Mid-Level", "Senior"]
    },
    {
        "name": "Software Release Manager",
        "category": "Project Management",
        "description": "Coordinates production deployment gates, compliance sign-offs, customer release notes, and rollback plans.",
        "common_skills": ["Release Governance", "Deployment Gates", "Change Advisory Board (CAB)", "Rollback Strategy", "Incident Readiness"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "PMO Director",
        "category": "Project Management",
        "description": "Standardizes project governance, portfolio reporting, resource allocation, and strategic prioritization across the company.",
        "common_skills": ["PMO Governance", "Portfolio Prioritization", "Executive Dashboards", "Resource Capacity Modeling", "Strategic Planning"],
        "seniority_levels": ["Director", "VP"]
    },

    # =========================================================================
    # 9. UI/UX & DESIGN (10 roles)
    # =========================================================================
    {
        "name": "Product Designer (UI/UX)",
        "category": "UI/UX & Design",
        "description": "Designs intuitive user journeys, wireframes, high-fidelity prototypes, and component-based user interfaces.",
        "common_skills": ["Figma", "Design Systems", "Wireframing & Prototyping", "User Centered Design", "Interaction Design", "Usability Testing"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead", "Principal"]
    },
    {
        "name": "UX Researcher",
        "category": "UI/UX & Design",
        "description": "Conducts generative user interviews, usability benchmarking, card sorting, heuristic evaluations, and persona modeling.",
        "common_skills": ["User Interviews", "Usability Testing", "Heuristic Evaluation", "Survey Design", "Affinity Mapping", "Persona Creation"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Design Systems Lead",
        "category": "UI/UX & Design",
        "description": "Creates scalable tokenized design systems, accessible UI kits, component guidelines, and developer handoff specs.",
        "common_skills": ["Design Tokens", "Figma Auto-Layout & Variables", "Accessibility (WCAG AA/AAA)", "Component Architecture", "Storybook Sync"],
        "seniority_levels": ["Senior", "Lead", "Staff"]
    },
    {
        "name": "UX Writer & Content Designer",
        "category": "UI/UX & Design",
        "description": "Crafts microcopy, error messages, onboarding narratives, empty states, and voice-and-tone brand guides.",
        "common_skills": ["Microcopy", "Information Architecture", "Content Strategy", "Voice & Tone", "User Journey Flow", "A/B Copy Testing"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior"]
    },
    {
        "name": "Motion & Interaction Designer",
        "category": "UI/UX & Design",
        "description": "Designs micro-interactions, page transitions, interactive animations, and responsive physical feedback.",
        "common_skills": ["After Effects / Lottie", "Framer", "Protopie", "CSS Keyframes", "Spatial Physics", "Micro-Interactions"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Visual / Brand Designer",
        "category": "UI/UX & Design",
        "description": "Develops brand identities, iconography, marketing collateral, vector illustrations, and style guides.",
        "common_skills": ["Adobe Illustrator / Photoshop", "Typography", "Color Theory", "Vector Art", "Brand Guidelines", "Visual Hierarchy"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "3D & Spatial UI Designer (AR/VR)",
        "category": "UI/UX & Design",
        "description": "Designs spatial user interfaces, 3D assets, gaze/hand gesture controls, and immersive XR experiences.",
        "common_skills": ["Blender / Cinema 4D", "Unity Spatial UI", "VisionOS / Meta Quest Guidelines", "Spatial Layouts", "3D Shading"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Accessibility (a11y) Specialist",
        "category": "UI/UX & Design",
        "description": "Audits applications for screen reader compatibility, keyboard navigation, color contrast, and WCAG standards.",
        "common_skills": ["WCAG 2.1/2.2", "Screen Readers (NVDA/VoiceOver)", "ARIA Attributes", "Color Contrast Auditing", "Assistive Tech"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Design Technologist / UI Prototyper",
        "category": "UI/UX & Design",
        "description": "Bridges design and engineering by building interactive code prototypes in React, HTML/CSS, and WebGL.",
        "common_skills": ["React/TypeScript", "CSS/Tailwind", "Canvas/Three.js", "Figma Plugins", "Rapid Prototyping"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Head of Design / VP Design",
        "category": "UI/UX & Design",
        "description": "Directs overall design vision, builds design culture, oversees brand and product cohesion, and manages design org.",
        "common_skills": ["Design Leadership", "Executive Presentation", "Design Operations (DesignOps)", "Critique Facilitation", "Strategy"],
        "seniority_levels": ["Executive (Head / VP)"]
    },

    # =========================================================================
    # 10. FINANCE & ACCOUNTING (10 roles)
    # =========================================================================
    {
        "name": "Financial Analyst (FP&A)",
        "category": "Finance & Accounting",
        "description": "Builds financial forecasting models, budget variance reports, cash flow projections, and operating plans.",
        "common_skills": ["Financial Modeling", "Excel / Sheets Power User", "Variance Analysis", "Three-Statement Modeling", "Power BI / Tableau", "Budgeting"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Manager", "Director"]
    },
    {
        "name": "Corporate Accountant",
        "category": "Finance & Accounting",
        "description": "Manages general ledger journal entries, month-end close, account reconciliations, and GAAP financial statements.",
        "common_skills": ["US GAAP / IFRS", "General Ledger", "Month-End Close", "QuickBooks / NetSuite", "Accrual Accounting", "Audit Support"],
        "seniority_levels": ["Junior", "Staff Accountant", "Senior Accountant", "Accounting Manager"]
    },
    {
        "name": "Investment Banking Analyst",
        "category": "Finance & Accounting",
        "description": "Executes discounted cash flow (DCF) valuations, LBO models, pitch decks, and M&A transaction due diligence.",
        "common_skills": ["DCF Modeling", "LBO Analysis", "Comparable Company Analysis (Comps)", "PitchBook / Capital IQ", "Deal Structuring"],
        "seniority_levels": ["Analyst", "Associate", "Vice President", "Managing Director"]
    },
    {
        "name": "Treasury & Cash Management Specialist",
        "category": "Finance & Accounting",
        "description": "Manages corporate liquidity, FX hedging, bank relationships, debt covenant compliance, and cash sweeps.",
        "common_skills": ["Liquidity Management", "FX Hedging", "Cash Flow Forecasting", "Bank Relationship Management", "Debt Covenants"],
        "seniority_levels": ["Mid-Level", "Senior", "Manager"]
    },
    {
        "name": "Tax Accountant & Strategist",
        "category": "Finance & Accounting",
        "description": "Prepares federal, state, and international corporate tax returns, R&D credits, and tax optimization strategies.",
        "common_skills": ["Corporate Tax Filing (Form 1120)", "State & Local Tax (SALT)", "R&D Tax Credits", "Transfer Pricing", "CPA"],
        "seniority_levels": ["Staff", "Senior", "Tax Manager", "Tax Director"]
    },
    {
        "name": "Internal Auditor & Forensic Accountant",
        "category": "Finance & Accounting",
        "description": "Evaluates internal controls (SOX 404), tests fraud prevention mechanisms, and investigates financial discrepancies.",
        "common_skills": ["SOX 404 Compliance", "Internal Controls Testing", "Forensic Auditing", "Risk Registers", "Audit Reporting"],
        "seniority_levels": ["Staff Auditor", "Senior Auditor", "Audit Manager"]
    },
    {
        "name": "Credit Risk Analyst",
        "category": "Finance & Accounting",
        "description": "Assesses borrower creditworthiness, default probability models, counterparty limits, and debt restructuring.",
        "common_skills": ["Credit Scoring Models", "Default Probability", "Financial Statement Analysis", "Risk Rating Frameworks", "Underwriting"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior"]
    },
    {
        "name": "Payroll & Benefits Accountant",
        "category": "Finance & Accounting",
        "description": "Administers multi-state and global payroll runs, tax withholdings, 401(k) deductions, and equity compensation (RSUs/options).",
        "common_skills": ["ADP / Gusto / Rippling", "Payroll Tax Compliance", "Equity Stock Option Accounting", "Multi-State Withholding", "Benefits Reconciliation"],
        "seniority_levels": ["Specialist", "Senior Specialist", "Manager"]
    },
    {
        "name": "Financial Controller",
        "category": "Finance & Accounting",
        "description": "Oversees the entire accounting department, external audits, financial governance, and regulatory reporting.",
        "common_skills": ["Financial Leadership", "External Audit Oversight", "NetSuite / SAP ERP", "Revenue Recognition (ASC 606)", "Internal Controls"],
        "seniority_levels": ["Assistant Controller", "Controller", "VP Finance"]
    },
    {
        "name": "Chief Financial Officer (CFO)",
        "category": "Finance & Accounting",
        "description": "Leads enterprise capital allocation, investor relations, fundraising rounds, IPO readiness, and financial strategy.",
        "common_skills": ["Capital Allocation", "Fundraising / IR", "Strategic M&A", "Board Reporting", "Executive Finance"],
        "seniority_levels": ["Executive (CFO)"]
    },

    # =========================================================================
    # 11. HR & RECRUITING (10 roles)
    # =========================================================================
    {
        "name": "Technical Recruiter",
        "category": "HR & Recruiting",
        "description": "Sources, screens, and closes software engineering, AI, and technical leadership candidates.",
        "common_skills": ["Boolean Search", "Technical Screening", "LinkedIn Recruiter", "Offer Negotiation", "ATS (Greenhouse/Lever)", "Candidate Experience"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead", "Manager"]
    },
    {
        "name": "HR Business Partner (HRBP)",
        "category": "HR & Recruiting",
        "description": "Aligns business unit objectives with people strategy, talent planning, performance management, and organizational design.",
        "common_skills": ["Strategic People Consulting", "Performance Management", "Employee Relations", "Organizational Design", "Conflict Resolution"],
        "seniority_levels": ["Mid-Level", "Senior", "Principal", "Director"]
    },
    {
        "name": "People Operations (PeopleOps) Specialist",
        "category": "HR & Recruiting",
        "description": "Manages employee onboarding/offboarding, HRIS systems, compliance policies, leaves of absence, and employee records.",
        "common_skills": ["HRIS (BambooHR/Workday)", "Onboarding Workflows", "Employment Law Basics", "Policy Documentation", "People Analytics"],
        "seniority_levels": ["Coordinator", "Specialist", "Manager"]
    },
    {
        "name": "Talent Sourcing Specialist",
        "category": "HR & Recruiting",
        "description": "Identifies passive executive and niche technical talent across GitHub, LinkedIn, research papers, and networks.",
        "common_skills": ["Passive Candidate Sourcing", "Talent Mapping", "Cold Outreach Sequences", "GitHub/StackOverflow Sourcing", "Pipeline Building"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior"]
    },
    {
        "name": "Compensation & Benefits (Total Rewards) Analyst",
        "category": "HR & Recruiting",
        "description": "Designs salary bands, market benchmark surveys, equity option plans, executive perks, and healthcare benefits.",
        "common_skills": ["Salary Banding", "Market Benchmarking (Radford/Option Impact)", "Equity Compensation Models", "Benefits Administration"],
        "seniority_levels": ["Analyst", "Senior Analyst", "Manager", "Director"]
    },
    {
        "name": "Learning & Development (L&D) Manager",
        "category": "HR & Recruiting",
        "description": "Creates employee skill development workshops, manager training programs, leadership tracks, and LMS curriculum.",
        "common_skills": ["Instructional Design", "LMS Administration", "Leadership Development", "Training Delivery", "Skill Assessment"],
        "seniority_levels": ["Specialist", "Manager", "Director"]
    },
    {
        "name": "Employee Relations Specialist",
        "category": "HR & Recruiting",
        "description": "Investigates workplace grievances, disciplinary proceedings, severance agreements, and ensures labor standard compliance.",
        "common_skills": ["Workplace Investigations", "Mediation", "Labor Law Compliance (EEOC/FMLA)", "Exit Interviews", "Documentation"],
        "seniority_levels": ["Specialist", "Senior Specialist", "Manager"]
    },
    {
        "name": "Diversity, Equity & Inclusion (DEI) Lead",
        "category": "HR & Recruiting",
        "description": "Drives inclusive hiring strategies, employee resource groups (ERGs), mentorship initiatives, and demographic reporting.",
        "common_skills": ["Inclusive Hiring Standards", "ERG Facilitation", "DEI Metrics & Reporting", "Unconscious Bias Training"],
        "seniority_levels": ["Lead", "Manager", "Director"]
    },
    {
        "name": "Employer Branding Specialist",
        "category": "HR & Recruiting",
        "description": "Showcases engineering culture, careers pages, Glassdoor/LinkedIn brand presence, and recruitment marketing campaigns.",
        "common_skills": ["Recruitment Marketing", "Content Creation", "Careers Site Optimization", "Glassdoor/LinkedIn Management", "Talent Events"],
        "seniority_levels": ["Specialist", "Senior Specialist", "Manager"]
    },
    {
        "name": "Chief People Officer (CPO) / VP HR",
        "category": "HR & Recruiting",
        "description": "Leads organizational culture, executive succession planning, global hiring strategy, and executive committee people goals.",
        "common_skills": ["Executive People Strategy", "Organizational Scaling", "Board Compensation Committee", "Culture Building"],
        "seniority_levels": ["Executive (VP / CPO)"]
    },

    # =========================================================================
    # 12. SALES & REVENUE (10 roles)
    # =========================================================================
    {
        "name": "Enterprise Account Executive (AE)",
        "category": "Sales",
        "description": "Manages complex multi-stakeholder enterprise sales cycles, contract negotiations, and multi-million dollar quotas.",
        "common_skills": ["MEDDPICC / MEDDIC", "Enterprise Discovery", "Contract Negotiation", "Executive Presentation (C-Level)", "Salesforce CRM", "Quota Attainment"],
        "seniority_levels": ["Mid-Market AE", "Senior Enterprise AE", "Strategic AE", "Director of Sales"]
    },
    {
        "name": "Sales Engineer / Solutions Consultant",
        "category": "Sales",
        "description": "Partners with Account Executives to deliver technical product demos, architecture validation, and Proof of Concepts (POC).",
        "common_skills": ["Technical Demos", "POC Management", "Architecture Mapping", "Objection Handling", "RFP Authoring", "API Demos"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead", "Director"]
    },
    {
        "name": "Sales Development Representative (SDR)",
        "category": "Sales",
        "description": "Conducts outbound prospecting, cold calling, email sequencing, lead qualification (BANT), and pipeline generation.",
        "common_skills": ["Cold Calling", "Email Sequences (Outreach/SalesLoft)", "BANT Qualification", "LinkedIn Prospecting", "CRM Hygiene"],
        "seniority_levels": ["SDR", "Senior SDR", "Team Lead", "SDR Manager"]
    },
    {
        "name": "Account Manager (Renewals & Upsell)",
        "category": "Sales",
        "description": "Owns existing client relationships, annual contract renewals, expansion opportunities, and net revenue retention (NRR).",
        "common_skills": ["Contract Renewals", "Upselling & Cross-selling", "Customer Relationship Management", "Quarterly Business Reviews (QBRs)"],
        "seniority_levels": ["Mid-Level", "Senior", "Director"]
    },
    {
        "name": "Sales Operations (SalesOps) Analyst",
        "category": "Sales",
        "description": "Optimizes sales tech stack, commission plan calculations, quota allocation, pipeline reporting, and territory mapping.",
        "common_skills": ["Salesforce Administration", "Commission Modeling", "Pipeline Analytics", "Territory Planning", "Sales Process Optimization"],
        "seniority_levels": ["Analyst", "Senior Analyst", "Manager", "Director"]
    },
    {
        "name": "Partnerships & Channel Sales Manager",
        "category": "Sales",
        "description": "Builds reseller networks, system integrator (SI) alliances, co-selling agreements, and channel revenue channels.",
        "common_skills": ["Channel Partner Strategy", "Co-Selling Agreements", "System Integrators (Accenture/Deloitte)", "Joint Business Planning"],
        "seniority_levels": ["Manager", "Senior Manager", "Director"]
    },
    {
        "name": "Inbound Lead Specialist",
        "category": "Sales",
        "description": "Rapidly qualifies incoming trial signups, demo requests, chat leads, and assigns high-intent accounts to sales reps.",
        "common_skills": ["Speed-to-Lead Workflows", "Lead Scoring", "Demo Triage", "HubSpot / Marketo", "Customer Qualification"],
        "seniority_levels": ["Specialist", "Senior Specialist"]
    },
    {
        "name": "Sales Enablement Manager",
        "category": "Sales",
        "description": "Equips sales reps with battlecards, objection handling guides, pitch coaching, and product certification tracks.",
        "common_skills": ["Sales Curriculum Design", "Battlecards / Competitive Intelligence", "Pitch Coaching (Gong/Chorus)", "LMS for Sales"],
        "seniority_levels": ["Manager", "Senior Manager", "Director"]
    },
    {
        "name": "Pre-Sales Architect",
        "category": "Sales",
        "description": "Authors complex enterprise technical proposals, security responses, and custom cloud topology blueprints for deals.",
        "common_skills": ["Security Questionnaire Completion", "Cloud Architecture Sizing", "Custom Solution Blueprinting", "RFP Authoring"],
        "seniority_levels": ["Senior", "Principal", "Director"]
    },
    {
        "name": "Chief Revenue Officer (CRO) / VP Sales",
        "category": "Sales",
        "description": "Owns overall ARR growth, sales compensation plans, board revenue projections, and global sales team leadership.",
        "common_skills": ["Revenue Strategy", "Quota Modeling", "Executive Board Reporting", "Sales Org Scaling", "GTM Leadership"],
        "seniority_levels": ["Executive (VP / CRO)"]
    },

    # =========================================================================
    # 13. MARKETING & GROWTH (10 roles)
    # =========================================================================
    {
        "name": "Product Marketing Manager (PMM)",
        "category": "Marketing",
        "description": "Drives product launches, positioning & messaging, competitive intelligence, customer personas, and sales enablement.",
        "common_skills": ["Product Positioning & Messaging", "Go-To-Market (GTM) Launches", "Competitive Battlecards", "Customer Case Studies", "Market Research"],
        "seniority_levels": ["Associate PMM", "PMM", "Senior PMM", "Lead PMM", "Director of Product Marketing"]
    },
    {
        "name": "Growth Marketing Manager",
        "category": "Marketing",
        "description": "Runs paid customer acquisition channels (Google, LinkedIn, Meta), conversion rate optimization (CRO), and CAC/LTV payback.",
        "common_skills": ["Paid Ads (SEM/PPC)", "Conversion Rate Optimization (CRO)", "CAC / LTV Economics", "Attribution Modeling", "Landing Page Testing"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead", "Director"]
    },
    {
        "name": "Technical Content Strategist",
        "category": "Marketing",
        "description": "Writes deep technical tutorials, architecture breakdown blogs, whitepapers, and developer documentation guides.",
        "common_skills": ["Technical Writing", "Code Walkthroughs", "Whitepaper Authoring", "SEO for Developers", "Developer Advocacy"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "SEO & Organic Search Specialist",
        "category": "Marketing",
        "description": "Audits technical site architecture, keyword clusters, backlink building, search intent matching, and Core Web Vitals.",
        "common_skills": ["Technical SEO", "Ahrefs / Semrush", "Keyword Research", "Schema Markup", "Core Web Vitals", "Link Building"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Marketing Operations (MOPs) Manager",
        "category": "Marketing",
        "description": "Manages marketing automation platforms (HubSpot/Marketo), lead lifecycle routing, attribution, and email deliverability.",
        "common_skills": ["HubSpot / Marketo", "Lead Lifecycle Routing", "Email Deliverability (DKIM/SPF)", "Attribution Tooling", "Zapier/Make"],
        "seniority_levels": ["Specialist", "Manager", "Director"]
    },
    {
        "name": "Social Media & Community Lead",
        "category": "Marketing",
        "description": "Builds company brand presence across Twitter/X, LinkedIn, Discord, Reddit, and organizes community AMA events.",
        "common_skills": ["Social Media Strategy", "Discord/Slack Community Building", "Content Scheduling", "Community Moderation", "Brand Tone"],
        "seniority_levels": ["Specialist", "Lead", "Manager"]
    },
    {
        "name": "Developer Relations (DevRel) / Advocate",
        "category": "Marketing",
        "description": "Engages developer ecosystems through open-source repos, hackathons, conference keynotes, sample SDKs, and tutorials.",
        "common_skills": ["Public Speaking", "Open Source Maintenance", "SDK Sample Apps", "Hackathon Organization", "Developer Empathy"],
        "seniority_levels": ["Advocate", "Senior Advocate", "Head of DevRel"]
    },
    {
        "name": "Brand & Communications Manager",
        "category": "Marketing",
        "description": "Drives press releases, media relations, crisis PR, executive ghostwriting, and industry award submissions.",
        "common_skills": ["Public Relations (PR)", "Media Pitching", "Crisis Communication", "Press Release Writing", "Executive Ghostwriting"],
        "seniority_levels": ["Manager", "Senior Manager", "Director"]
    },
    {
        "name": "Event & Field Marketing Specialist",
        "category": "Marketing",
        "description": "Plans enterprise trade show booths, VIP executive dinners, sponsor sessions, and regional prospect workshops.",
        "common_skills": ["Event Logistics", "Trade Show Sponsorships", "Booth Design", "Field Prospecting", "Budget Management"],
        "seniority_levels": ["Coordinator", "Specialist", "Manager"]
    },
    {
        "name": "Chief Marketing Officer (CMO) / VP Marketing",
        "category": "Marketing",
        "description": "Sets total brand positioning, marketing budget allocation across channels, demand gen targets, and leadership.",
        "common_skills": ["Marketing Strategy", "Demand Generation", "Brand Governance", "Budget Sizing", "Executive Leadership"],
        "seniority_levels": ["Executive (VP / CMO)"]
    },

    # =========================================================================
    # 14. BUSINESS & OPERATIONS (10 roles)
    # =========================================================================
    {
        "name": "Business Operations (BizOps) Associate",
        "category": "Business & Operations",
        "description": "Analyzes cross-functional operational bottlenecks, evaluates new market entries, and implements strategic initiatives.",
        "common_skills": ["Strategic Analysis", "Excel Modeling", "Cross-Functional Execution", "Root Cause Analysis", "Executive Presentations"],
        "seniority_levels": ["Associate", "Manager", "Senior Manager", "Director"]
    },
    {
        "name": "Business Analyst (IT & Systems)",
        "category": "Business & Operations",
        "description": "Translates business stakeholder needs into detailed technical user stories, acceptance criteria, and process flows.",
        "common_skills": ["User Story Authoring", "Process Flow (BPMN)", "Gap Analysis", "Jira / Confluence", "Stakeholder Interviews"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Strategy & Corporate Development Associate",
        "category": "Business & Operations",
        "description": "Evaluates M&A targets, competitive market dynamics, partnership synergies, and long-term 5-year strategic plans.",
        "common_skills": ["M&A Due Diligence", "Market Sizing (TAM/SAM)", "Financial Valuation", "Competitive Strategy", "Board Decks"],
        "seniority_levels": ["Associate", "Manager", "Director"]
    },
    {
        "name": "Chief of Staff",
        "category": "Business & Operations",
        "description": "Acts as the executive proxy, drives executive team OKRs, leads special strategic projects, and resolves org friction.",
        "common_skills": ["Executive Alignment", "OKR Tracking", "High-Stakes Communication", "Crisis Management", "Organizational Agility"],
        "seniority_levels": ["Manager", "Senior", "Director", "VP Level"]
    },
    {
        "name": "Management Consultant",
        "category": "Business & Operations",
        "description": "Advises enterprise clients on organizational restructuring, digital transformation, cost reduction, and growth strategy.",
        "common_skills": ["Hypothesis-Driven Problem Solving", "Executive Deck Building", "Financial Restructuring", "Change Management"],
        "seniority_levels": ["Analyst", "Associate", "Engagement Manager", "Partner"]
    },
    {
        "name": "Supply Chain & Procurement Specialist",
        "category": "Business & Operations",
        "description": "Negotiates vendor Master Service Agreements (MSAs), manages RFP bidding, vendor performance SLAs, and procurement.",
        "common_skills": ["Vendor Negotiation", "RFP Management", "Cost Reduction", "Contract Terms Review", "ERP Procurement Tools"],
        "seniority_levels": ["Specialist", "Senior Specialist", "Manager"]
    },
    {
        "name": "Facilities & Workplace Operations Manager",
        "category": "Business & Operations",
        "description": "Manages commercial real estate leases, hybrid workplace logistics, office security, and vendor facilities maintenance.",
        "common_skills": ["Real Estate Leases", "Workplace Safety & Compliance", "Vendor Facilities Management", "Space Planning"],
        "seniority_levels": ["Manager", "Director"]
    },
    {
        "name": "Risk & Resilience Manager",
        "category": "Business & Operations",
        "description": "Develops business continuity plans (BCP), disaster recovery playbooks, supply chain redundancy, and risk registers.",
        "common_skills": ["Business Continuity Planning", "Enterprise Risk Management (ERM)", "Disaster Recovery Testing", "Crisis Simulations"],
        "seniority_levels": ["Manager", "Director"]
    },
    {
        "name": "Process Automation & RPA Developer",
        "category": "Business & Operations",
        "description": "Automates repetitive manual business workflows using UiPath, Power Automate, Python scripts, and OCR parsing.",
        "common_skills": ["UiPath / Automation Anywhere", "Power Automate", "Python Scripting", "OCR Document Extraction", "Process Mapping"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior"]
    },
    {
        "name": "Chief Operating Officer (COO) / VP Operations",
        "category": "Business & Operations",
        "description": "Directs company-wide operational efficiency, inter-departmental workflows, budget governance, and scaling execution.",
        "common_skills": ["Operational Scaling", "P&L Management", "Strategic Execution", "Executive Leadership", "Cross-Functional Governance"],
        "seniority_levels": ["Executive (VP / COO)"]
    },

    # =========================================================================
    # 15. CUSTOMER SUCCESS & SUPPORT (8 roles)
    # =========================================================================
    {
        "name": "Customer Success Manager (CSM)",
        "category": "Customer Success",
        "description": "Drives customer retention, adoption milestones, executive QBRs, health score monitoring, and churn prevention.",
        "common_skills": ["Account Health Monitoring", "Quarterly Business Reviews", "Customer Onboarding", "Churn Prevention", "Gainsight/ChurnZero"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead", "Director"]
    },
    {
        "name": "Technical Account Manager (TAM)",
        "category": "Customer Success",
        "description": "Serves as dedicated technical advisor for enterprise clients, reviewing architectures, feature requests, and SLAs.",
        "common_skills": ["Technical Troubleshooting", "Architecture Guidance", "SLA Escalations", "API Debugging", "Client Relationship Management"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead", "Director"]
    },
    {
        "name": "Customer Implementation & Onboarding Specialist",
        "category": "Customer Success",
        "description": "Leads complex technical client onboarding, data migrations, initial configuration, and user training sessions.",
        "common_skills": ["Project Onboarding Plans", "Data Migration Mapping", "User Training Delivery", "System Configuration", "Go-Live Support"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior"]
    },
    {
        "name": "Technical Support Engineer (Tier 2/3)",
        "category": "Customer Success",
        "description": "Investigates deep technical customer bugs, examines server logs, writes reproduction scripts, and interfaces with engineering.",
        "common_skills": ["Log Analysis (Kibana/Datadog)", "SQL Querying", "HTTP/API Debugging", "Bug Reproduction Steps", "Zendesk/Jira"],
        "seniority_levels": ["Tier 1", "Tier 2", "Tier 3", "Support Lead"]
    },
    {
        "name": "Customer Support Representative",
        "category": "Customer Success",
        "description": "Delivers prompt, empathetic first-response customer ticket resolutions via email, live chat, and phone.",
        "common_skills": ["Customer Empathy", "Ticket Resolution (Zendesk/Intercom)", "Troubleshooting Basics", "Help Center Documentation", "First Response Time (FRT)"],
        "seniority_levels": ["Representative", "Senior Representative", "Team Lead"]
    },
    {
        "name": "Knowledge Base & Documentation Lead",
        "category": "Customer Success",
        "description": "Authors searchable customer help centers, video walkthroughs, troubleshooting guides, and FAQ resources.",
        "common_skills": ["Technical Writing", "Help Center Information Architecture", "Video Tutorial Creation", "Loom / Camtasia", "SEO for Help Centers"],
        "seniority_levels": ["Specialist", "Lead"]
    },
    {
        "name": "Voice of Customer (VoC) Analyst",
        "category": "Customer Success",
        "description": "Aggregates Net Promoter Scores (NPS), CSAT ratings, support tickets, and feature requests to guide product roadmaps.",
        "common_skills": ["NPS / CSAT Analysis", "Sentiment Analysis", "Customer Feedback Categorization", "Cross-Department Reporting"],
        "seniority_levels": ["Analyst", "Senior Analyst"]
    },
    {
        "name": "VP of Customer Experience & Success",
        "category": "Customer Success",
        "description": "Owns gross and net revenue retention (GRR/NRR), global support SLAs, customer journey design, and team scaling.",
        "common_skills": ["NRR / GRR Optimization", "Support Org Scaling", "Executive Escalations", "Customer Retention Strategy"],
        "seniority_levels": ["Executive (VP / Head)"]
    },

    # =========================================================================
    # 16. HEALTHCARE & LIFE SCIENCES (10 roles)
    # =========================================================================
    {
        "name": "Bioinformatics Scientist",
        "category": "Healthcare",
        "description": "Analyzes genomic sequencing data (NGS), RNA-seq expression, variant calling, and computational biology pipelines.",
        "common_skills": ["Python / R", "Next-Gen Sequencing (NGS)", "Bioconductor", "Variant Calling (GATK)", "BLAST / Alignment", "FastQ / BAM"],
        "seniority_levels": ["Scientist", "Senior Scientist", "Principal Scientist"]
    },
    {
        "name": "Clinical Research Coordinator",
        "category": "Healthcare",
        "description": "Manages clinical trial participant visits, informed consent forms, protocol adherence, and adverse event logging.",
        "common_skills": ["GCP (Good Clinical Practice)", "IRB Protocols", "Informed Consent", "Patient Recruitment", "Adverse Event Reporting"],
        "seniority_levels": ["Coordinator", "Senior Coordinator", "Manager"]
    },
    {
        "name": "Health Informatics Specialist",
        "category": "Healthcare",
        "description": "Optimizes electronic health records (Epic/Cerner), clinical decision support systems, and medical data standards.",
        "common_skills": ["Epic / Cerner Systems", "HL7 / FHIR", "SNOMED / ICD-10", "Clinical Workflows", "Health Data Security"],
        "seniority_levels": ["Specialist", "Senior Specialist", "Manager"]
    },
    {
        "name": "Medical Device Regulatory Affairs Specialist",
        "category": "Healthcare",
        "description": "Authors FDA 510(k), PMA, CE mark submissions, design history files (DHF), and ISO 13485 quality standards.",
        "common_skills": ["FDA 510(k) Submissions", "ISO 13485", "Design History Files (DHF)", "Medical Device Regulations", "Risk Management (ISO 14971)"],
        "seniority_levels": ["Specialist", "Senior Specialist", "Manager", "Director"]
    },
    {
        "name": "Biostatistician",
        "category": "Healthcare",
        "description": "Calculates sample sizes, clinical trial statistical analysis plans (SAP), survival curves, and regulatory FDA summaries.",
        "common_skills": ["SAS / R", "Kaplan-Meier Survival Analysis", "Statistical Analysis Plans (SAP)", "Hypothesis Testing", "FDA Submission Prep"],
        "seniority_levels": ["Biostatistician", "Senior Biostatistician", "Principal"]
    },
    {
        "name": "Computational Chemist / Molecular Modeler",
        "category": "Healthcare",
        "description": "Conducts molecular dynamics simulations, ligand-protein docking, structure-activity relationships (QSAR), and drug discovery.",
        "common_skills": ["Molecular Docking (AutoDock/Schrodinger)", "PyMOL", "Molecular Dynamics (GROMACS)", "QSAR Modeling", "Python / RDKit"],
        "seniority_levels": ["Scientist", "Senior Scientist", "Director"]
    },
    {
        "name": "Medical Science Liaison (MSL)",
        "category": "Healthcare",
        "description": "Engages Key Opinion Leaders (KOLs), explains clinical trial evidence to physicians, and supports scientific publications.",
        "common_skills": ["Scientific Presentation", "KOL Relationship Management", "Clinical Trial Data Translation", "Therapeutic Area Expertise"],
        "seniority_levels": ["MSL", "Senior MSL", "Director"]
    },
    {
        "name": "Healthcare Compliance Officer",
        "category": "Healthcare",
        "description": "Enforces HIPAA privacy rules, Anti-Kickback Statute, Stark Law, fraud waste & abuse (FWA) audits, and ethics hotlines.",
        "common_skills": ["HIPAA Enforcement", "Anti-Kickback Statute", "FWA Audits", "Healthcare Ethics", "Policy Enforcement"],
        "seniority_levels": ["Officer", "Senior Officer", "Director"]
    },
    {
        "name": "Pharmacovigilance & Drug Safety Specialist",
        "category": "Healthcare",
        "description": "Monitors adverse drug reactions (ADRs), MedDRA coding, Periodic Safety Update Reports (PSUR), and FDA FAERS.",
        "common_skills": ["MedDRA Coding", "Individual Case Safety Reports (ICSR)", "FDA FAERS / EudraVigilance", "Signal Detection", "PSUR Authoring"],
        "seniority_levels": ["Specialist", "Senior Specialist", "Manager"]
    },
    {
        "name": "Digital Health Solutions Architect",
        "category": "Healthcare",
        "description": "Architects HIPAA-compliant cloud telemedicine platforms, remote patient monitoring devices, and secure API gateways.",
        "common_skills": ["HIPAA Cloud Architecture", "FHIR APIs", "Remote Patient Monitoring (IoT)", "EHR Interoperability", "Data Encryption"],
        "seniority_levels": ["Senior", "Staff", "Principal"]
    },

    # =========================================================================
    # 17. SUPPLY CHAIN & LOGISTICS (8 roles)
    # =========================================================================
    {
        "name": "Supply Chain Planner & Analyst",
        "category": "Supply Chain & Logistics",
        "description": "Forecasts customer demand, plans safety stock buffers, monitors lead times, and conducts S&OP consensus planning.",
        "common_skills": ["Demand Forecasting", "Inventory Optimization", "S&OP Planning", "ERP (SAP/Oracle)", "Safety Stock Sizing"],
        "seniority_levels": ["Analyst", "Senior Analyst", "Manager", "Director"]
    },
    {
        "name": "Logistics & Fleet Operations Manager",
        "category": "Supply Chain & Logistics",
        "description": "Manages route optimization, freight forwarding, carrier negotiations, DOT compliance, and last-mile deliveries.",
        "common_skills": ["Transportation Management Systems (TMS)", "Route Optimization", "Freight Rate Negotiation", "DOT Regulations", "Last-Mile Delivery"],
        "seniority_levels": ["Manager", "Senior Manager", "Director"]
    },
    {
        "name": "Warehouse Operations Manager",
        "category": "Supply Chain & Logistics",
        "description": "Directs fulfillment center picking/packing throughput, Warehouse Management Systems (WMS), and OSHA safety standards.",
        "common_skills": ["WMS (Manhattan/Blue Yonder)", "Slotting Optimization", "Order Picking Productivity", "OSHA Safety", "Labor Planning"],
        "seniority_levels": ["Supervisor", "Manager", "Director"]
    },
    {
        "name": "Procurement & Strategic Sourcing Lead",
        "category": "Supply Chain & Logistics",
        "description": "Identifies global manufacturing suppliers, audits supplier quality, negotiates vendor contracts, and mitigates tariffs.",
        "common_skills": ["Strategic Sourcing", "Supplier Quality Audits", "Contract Negotiation", "Tariff & Customs Knowledge", "Spend Analytics"],
        "seniority_levels": ["Specialist", "Senior Specialist", "Manager", "Director"]
    },
    {
        "name": "Customs & International Trade Compliance Officer",
        "category": "Supply Chain & Logistics",
        "description": "Manages Harmonized Tariff Schedules (HTS codes), import/export declarations, duty drawbacks, and Incoterms.",
        "common_skills": ["HTS Tariff Classification", "Incoterms 2020", "Export Control Regulations (ITAR/EAR)", "Customs Brokerage", "Duty Optimization"],
        "seniority_levels": ["Officer", "Senior Officer", "Manager"]
    },
    {
        "name": "Inventory Control Specialist",
        "category": "Supply Chain & Logistics",
        "description": "Performs cycle counts, investigates inventory shrink discrepancies, tracks SKU velocity, and manages replenishment triggers.",
        "common_skills": ["Cycle Counting", "Shrink Investigation", "ABC SKU Analysis", "Reorder Point Calculations", "Barcode / RFID Scanning"],
        "seniority_levels": ["Specialist", "Senior Specialist", "Manager"]
    },
    {
        "name": "Reverse Logistics & Returns Specialist",
        "category": "Supply Chain & Logistics",
        "description": "Optimizes return merchandise authorizations (RMA), refurbishment grading, warranty verification, and secondary resale.",
        "common_skills": ["RMA Processing", "Refurbishment Grading", "Warranty Verification", "Circular Economy Sourcing", "Cost Recovery"],
        "seniority_levels": ["Specialist", "Manager"]
    },
    {
        "name": "VP of Global Supply Chain",
        "category": "Supply Chain & Logistics",
        "description": "Oversees worldwide supply chain resilience, global factory networks, supplier dual-sourcing, and executive logistics strategy.",
        "common_skills": ["Global Supply Chain Strategy", "Network Design", "Resilience & Dual Sourcing", "Executive Leadership"],
        "seniority_levels": ["Executive (VP / SVP)"]
    },

    # =========================================================================
    # 18. LEGAL & COMPLIANCE (8 roles)
    # =========================================================================
    {
        "name": "Corporate Counsel (Commercial & Contracts)",
        "category": "Legal & Compliance",
        "description": "Drafts and negotiates Master Services Agreements (MSAs), Statements of Work (SOWs), SLAs, and vendor contracts.",
        "common_skills": ["Contract Drafting & Negotiation", "Commercial Law", "IP Indemnification Clauses", "Limitation of Liability", "SaaS Licensing"],
        "seniority_levels": ["Associate Counsel", "Corporate Counsel", "Senior Corporate Counsel", "General Counsel"]
    },
    {
        "name": "Data Privacy Counsel & DPO",
        "category": "Legal & Compliance",
        "description": "Advises on GDPR, CCPA/CPRA, data transfer agreements (SCCs), privacy by design, and subject access requests (DSAR).",
        "common_skills": ["GDPR / CCPA / CPRA", "Data Processing Agreements (DPAs)", "Cross-Border Data Transfers", "Privacy Impact Assessments (PIA)", "DSAR Workflows"],
        "seniority_levels": ["Counsel", "Senior Counsel", "Data Protection Officer (DPO)"]
    },
    {
        "name": "Intellectual Property (IP) & Patent Attorney",
        "category": "Legal & Compliance",
        "description": "Prosecutes software and hardware patent applications, files trademark registrations, and conducts freedom-to-operate reviews.",
        "common_skills": ["Patent Prosecution (USPTO)", "Prior Art Searches", "Freedom to Operate (FTO)", "Trademark Filings", "Trade Secret Protection"],
        "seniority_levels": ["Associate", "Senior Associate", "Partner / IP Lead"]
    },
    {
        "name": "Compliance & Ethics Manager",
        "category": "Legal & Compliance",
        "description": "Manages anti-bribery (FCPA), code of conduct trainings, whistleblower investigations, and regulatory audit responses.",
        "common_skills": ["FCPA Compliance", "Whistleblower Hotline Management", "Compliance Training", "Regulatory Reporting", "Internal Investigations"],
        "seniority_levels": ["Manager", "Senior Manager", "Director"]
    },
    {
        "name": "Paralegal (Corporate & Transactions)",
        "category": "Legal & Compliance",
        "description": "Assists with board consent resolutions, cap table maintenance, signature packet coordination, and corporate filings.",
        "common_skills": ["Carta / Cap Table Management", "Corporate Minutes & Resolutions", "Filing State Registrations", "Due Diligence Data Rooms", "DocuSign"],
        "seniority_levels": ["Paralegal", "Senior Paralegal", "Lead Paralegal"]
    },
    {
        "name": "Employment & Labor Law Counsel",
        "category": "Legal & Compliance",
        "description": "Advises on employment contracts, non-compete agreements, workplace discrimination claims, and worker classification.",
        "common_skills": ["FLSA & Wage Hour Laws", "Severance Agreements", "Worker Classification (1099 vs W2)", "Employment Dispute Resolution"],
        "seniority_levels": ["Counsel", "Senior Counsel", "Director"]
    },
    {
        "name": "Fintech & Financial Regulatory Attorney",
        "category": "Legal & Compliance",
        "description": "Guides money transmission licenses (MTL), SEC crypto guidelines, Dodd-Frank, and anti-money laundering (BSA/AML) rules.",
        "common_skills": ["Money Transmitter Licenses (MTL)", "BSA / AML Compliance", "SEC Regulations", "Consumer Financial Protection (CFPB)", "Fintech Licensing"],
        "seniority_levels": ["Senior Counsel", "Partner", "Chief Compliance Officer"]
    },
    {
        "name": "General Counsel (GC) / Chief Legal Officer",
        "category": "Legal & Compliance",
        "description": "Leads enterprise legal strategy, manages external law firms, handles litigation risk, and advises the Board of Directors.",
        "common_skills": ["Executive Legal Strategy", "Litigation Oversight", "Board Governance", "M&A Legal Structuring", "Crisis Legal Management"],
        "seniority_levels": ["Executive (General Counsel)"]
    },

    # =========================================================================
    # 19. MANUFACTURING & HARDWARE (8 roles)
    # =========================================================================
    {
        "name": "Hardware Design Engineer (PCB / Electronics)",
        "category": "Manufacturing",
        "description": "Designs high-speed PCB schematics, component selection, signal integrity simulations, and hardware prototypes.",
        "common_skills": ["Altium Designer / KiCad", "High-Speed Layout", "Signal & Power Integrity", "Oscilloscopes & Logic Analyzers", "DFM (Design for Manufacturing)"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Staff", "Principal"]
    },
    {
        "name": "Mechanical Engineer (Product Enclosure & CAD)",
        "category": "Manufacturing",
        "description": "Designs injection-molded plastic enclosures, thermal heatsinks, structural chassis, and CNC machined parts.",
        "common_skills": ["SolidWorks / Fusion 360", "Injection Molding Design", "Thermal Simulation (CFD)", "GD&T (Tolerancing)", "Rapid 3D Prototyping"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "FPGA & ASIC Verification Engineer",
        "category": "Manufacturing",
        "description": "Writes SystemVerilog/UVM testbenches, timing closure constraints, synthesis scripts, and RTL digital logic.",
        "common_skills": ["SystemVerilog / UVM", "VHDL / Verilog", "Vivado / Quartus", "Timing Closure", "RTL Design", "Digital Logic"],
        "seniority_levels": ["Mid-Level", "Senior", "Staff", "Principal"]
    },
    {
        "name": "Manufacturing Quality Engineer",
        "category": "Manufacturing",
        "description": "Implements Statistical Process Control (SPC), Six Sigma methodologies, Root Cause Corrective Action (RCCA), and PPAP.",
        "common_skills": ["Six Sigma (Green/Black Belt)", "Statistical Process Control (SPC)", "PPAP / FMEA", "RCCA (8D Problem Solving)", "CMM Metrology"],
        "seniority_levels": ["Engineer", "Senior Engineer", "Quality Manager"]
    },
    {
        "name": "Industrial & Process Engineer",
        "category": "Manufacturing",
        "description": "Optimizes assembly line balance, takt time, ergonomic workstations, lean manufacturing flows, and factory layouts.",
        "common_skills": ["Lean Manufacturing (5S/Kaizen)", "Takt Time / Line Balancing", "Value Stream Mapping", "Factory Layout Design", "Time Studies"],
        "seniority_levels": ["Engineer", "Senior Engineer", "Lead"]
    },
    {
        "name": "Test & Measurement Hardware Engineer",
        "category": "Manufacturing",
        "description": "Builds automated factory test fixtures, bed-of-nails testers, LabVIEW test suites, and calibration benches.",
        "common_skills": ["LabVIEW / TestStand", "Automated Test Equipment (ATE)", "Bed-of-Nails Fixtures", "Python for Hardware Control", "GPIB / VISA Protocols"],
        "seniority_levels": ["Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Supply Quality & Supplier Development Engineer",
        "category": "Manufacturing",
        "description": "Audits tier-1 contract manufacturers, validates tooling qualification, resolves yield drops, and drives supplier compliance.",
        "common_skills": ["Supplier Audits", "Yield Improvement", "Tooling Validation", "First Article Inspection (FAI)", "Vendor Management"],
        "seniority_levels": ["Senior Engineer", "Lead", "Manager"]
    },
    {
        "name": "VP of Hardware Engineering & Operations",
        "category": "Manufacturing",
        "description": "Directs hardware roadmap from concept to mass production (NPI to ramp), CM relationships, and hardware org.",
        "common_skills": ["NPI Lifecycle", "Contract Manufacturer (Foxconn/Jabil)", "Hardware Product Strategy", "Executive Leadership"],
        "seniority_levels": ["Executive (VP / Head)"]
    },

    # =========================================================================
    # 20. RESEARCH & SCIENCE (8 roles)
    # =========================================================================
    {
        "name": "Applied AI Research Scientist",
        "category": "Research",
        "description": "Conducts original foundational research in model architectures, multimodality, reasoning algorithms, and publishes papers.",
        "common_skills": ["PyTorch / JAX", "Theoretical Machine Learning", "Academic Publishing (NeurIPS/ICLR)", "Novel Architecture Design", "Distributed Supercomputing"],
        "seniority_levels": ["Research Scientist", "Senior Research Scientist", "Principal Scientist"]
    },
    {
        "name": "Quantum Computing Researcher",
        "category": "Research",
        "description": "Develops quantum algorithms (Qiskit/Cirq), error mitigation techniques, variational quantum eigensolvers, and circuit gates.",
        "common_skills": ["Qiskit / Cirq", "Quantum Circuit Design", "Quantum Error Correction", "Linear Algebra", "Physics / Quantum Information"],
        "seniority_levels": ["Researcher", "Senior Researcher", "Principal"]
    },
    {
        "name": "Computational Physicist & Simulation Scientist",
        "category": "Research",
        "description": "Solves complex differential equations, Monte Carlo particle models, fluid dynamics, and high-performance physics solvers.",
        "common_skills": ["C++ / Fortran / Python", "MPI / OpenMP Parallelization", "Partial Differential Equations", "Mesh Generation", "HPC Clusters"],
        "seniority_levels": ["Scientist", "Senior Scientist", "Staff"]
    },
    {
        "name": "Materials Science Engineer",
        "category": "Research",
        "description": "Synthesizes advanced polymers, semiconductor thin films, battery cathode materials, and conducts SEM/XRD analysis.",
        "common_skills": ["SEM / TEM / XRD Analysis", "Material Synthesis", "Polymer Chemistry", "Spectroscopy", "Material Characterization"],
        "seniority_levels": ["Engineer", "Senior Engineer", "Principal"]
    },
    {
        "name": "Operations Research Scientist",
        "category": "Research",
        "description": "Formulates mixed-integer linear programs (MILP), combinatorial vehicle routing, dynamic pricing, and solver algorithms.",
        "common_skills": ["MILP / Linear Programming", "Gurobi / CPLEX / OR-Tools", "Combinatorial Optimization", "Dynamic Programming", "Python / C++"],
        "seniority_levels": ["Scientist", "Senior Scientist", "Principal"]
    },
    {
        "name": "Genomics & Molecular Biology Researcher",
        "category": "Research",
        "description": "Conducts wet-lab CRISPR gene editing, qPCR assays, cellular assays, and analyzes genetic sequencing data.",
        "common_skills": ["CRISPR / Cas9 Workflows", "qPCR / Western Blot", "Cell Culture", "Assay Development", "Genetic Data Interpretation"],
        "seniority_levels": ["Researcher", "Senior Researcher", "Principal"]
    },
    {
        "name": "Research Operations & Lab Manager",
        "category": "Research",
        "description": "Maintains laboratory equipment calibrations, chemical inventories, biosafety protocols (BSL-2), and research grant budgets.",
        "common_skills": ["Biosafety Protocols (BSL)", "Lab Equipment Maintenance", "Chemical Safety (OSHA)", "Grant Budget Tracking", "Lab Inventory"],
        "seniority_levels": ["Manager", "Director"]
    },
    {
        "name": "Director of R&D / Chief Scientist",
        "category": "Research",
        "description": "Shapes enterprise research vision, patent portfolio generation, academic university partnerships, and technology transfer.",
        "common_skills": ["R&D Strategy", "Technology Commercialization", "Academic Partnerships", "Executive Leadership", "Grant Leadership"],
        "seniority_levels": ["Executive (Chief Scientist / VP R&D)"]
    },

    # =========================================================================
    # 21. EDUCATION & TRAINING (8 roles)
    # =========================================================================
    {
        "name": "Instructional Designer",
        "category": "Education",
        "description": "Designs curriculum blueprints, ADDIE instructional frameworks, interactive e-learning modules, and assessments.",
        "common_skills": ["ADDIE Model", "Articulate 360 / Storyline", "Curriculum Design", "Assessment Rubrics", "Adult Learning Theory"],
        "seniority_levels": ["Junior", "Mid-Level", "Senior", "Lead"]
    },
    {
        "name": "Technical Trainer / Bootcamp Instructor",
        "category": "Education",
        "description": "Delivers intensive live coding lectures, workshops, technical labs, code reviews, and student project mentorship.",
        "common_skills": ["Live Coding Instruction", "Curriculum Delivery", "Code Review Feedback", "Technical Mentorship", "Student Motivation"],
        "seniority_levels": ["Instructor", "Senior Instructor", "Lead Instructor"]
    },
    {
        "name": "Educational Technology (EdTech) Specialist",
        "category": "Education",
        "description": "Implements Learning Management Systems (Canvas/Moodle/Blackboard), LTI integrations, SCORM packages, and student analytics.",
        "common_skills": ["LMS (Canvas/Moodle)", "LTI / SCORM Standards", "Student Engagement Analytics", "EdTech Integration", "Web Accessibility"],
        "seniority_levels": ["Specialist", "Senior Specialist", "Manager"]
    },
    {
        "name": "Corporate Training & Enablement Lead",
        "category": "Education",
        "description": "Builds employee leadership cohorts, compliance training tracks, soft-skill workshops, and evaluates training ROI.",
        "common_skills": ["Kirkpatrick Evaluation Model", "Workshop Facilitation", "Executive Coaching", "Training ROI Metrics", "Presentation Skills"],
        "seniority_levels": ["Lead", "Manager", "Director"]
    },
    {
        "name": "Curriculum Development Specialist",
        "category": "Education",
        "description": "Authors subject matter syllabi, textbook modules, lab exercises, and aligns content to educational accreditation standards.",
        "common_skills": ["Syllabus Authoring", "Bloom's Taxonomy", "Accreditation Alignment", "Subject Matter Research", "Rubric Development"],
        "seniority_levels": ["Specialist", "Senior Specialist"]
    },
    {
        "name": "Academic Program Director",
        "category": "Education",
        "description": "Oversees university department degree programs, faculty hiring, student graduation metrics, and institutional accreditation.",
        "common_skills": ["Academic Governance", "Faculty Leadership", "Accreditation Audits", "Student Retention", "Budget Oversight"],
        "seniority_levels": ["Director", "Dean"]
    },
    {
        "name": "Assessment & Psychometrician Specialist",
        "category": "Education",
        "description": "Develops standardized test items, performs Item Response Theory (IRT) statistics, test reliability, and validity studies.",
        "common_skills": ["Item Response Theory (IRT)", "Test Reliability & Validity", "Psychometric Modeling", "Standard Setting (Angoff)", "R / SPSS"],
        "seniority_levels": ["Specialist", "Senior Specialist", "Lead"]
    },
    {
        "name": "Online Learning Program Manager",
        "category": "Education",
        "description": "Manages asynchronous online degree and certification programs, student advising, platform uptime, and graduation rates.",
        "common_skills": ["Cohort Management", "Online Student Support", "Program Operations", "Digital Marketing Coordination", "Retention Tracking"],
        "seniority_levels": ["Manager", "Director"]
    },

    # =========================================================================
    # 22. OTHER PROFESSIONAL ROLES (15 roles)
    # =========================================================================
    {
        "name": "Enterprise Risk Management (ERM) Director",
        "category": "Other Professional Roles",
        "description": "Directs enterprise-wide risk frameworks, catastrophic loss models, geopolitical exposure, and risk mitigation.",
        "common_skills": ["Enterprise Risk Frameworks", "COSO / ISO 31000", "Risk Appetite Statements", "Scenario Stress Testing", "Board Reporting"],
        "seniority_levels": ["Director", "VP"]
    },
    {
        "name": "Sustainability & ESG Specialist",
        "category": "Other Professional Roles",
        "description": "Calculates Scope 1/2/3 carbon footprint emissions, writes ESG annual disclosure reports, and guides circular initiatives.",
        "common_skills": ["GHG Protocol (Scope 1/2/3)", "GRI / SASB / TCFD Reporting", "Carbon Accounting", "Lifecycle Assessment (LCA)", "ESG Audits"],
        "seniority_levels": ["Specialist", "Senior Specialist", "Manager"]
    },
    {
        "name": "Solutions Architect",
        "category": "Other Professional Roles",
        "description": "Bridges enterprise business requirements with scalable end-to-end technical system blueprints and partner integrations.",
        "common_skills": ["System Blueprinting", "Enterprise Integration Patterns", "Cloud / On-Prem Topologies", "Stakeholder Alignment", "Cost Sizing"],
        "seniority_levels": ["Senior", "Staff", "Principal"]
    },
    {
        "name": "Digital Transformation Consultant",
        "category": "Other Professional Roles",
        "description": "Guides legacy enterprise leadership through cloud migrations, paperless automation, and modern data practices.",
        "common_skills": ["Digital Strategy", "Executive Stakeholder Management", "Technology Roadmap Design", "Change Management (Prosci)"],
        "seniority_levels": ["Consultant", "Senior Consultant", "Managing Director"]
    },
    {
        "name": "Business Continuity & Disaster Recovery Lead",
        "category": "Other Professional Roles",
        "description": "Formulates RTO/RPO targets, business impact analyses (BIA), tabletop exercises, and multi-site emergency failovers.",
        "common_skills": ["RTO / RPO Target Sizing", "Business Impact Analysis (BIA)", "Tabletop Disaster Simulations", "Emergency Communication Protocols"],
        "seniority_levels": ["Lead", "Manager", "Director"]
    },
    {
        "name": "Procurement Category Manager (IT & Software)",
        "category": "Other Professional Roles",
        "description": "Manages enterprise SaaS software contracts, cloud spend agreements, software asset management (SAM), and renewal cycles.",
        "common_skills": ["SaaS Contract Negotiation", "Software Asset Management", "Vendor Benchmarking", "Enterprise Licensing (Microsoft/AWS/Salesforce)"],
        "seniority_levels": ["Manager", "Senior Manager", "Director"]
    },
    {
        "name": "Customer Experience (CX) Strategist",
        "category": "Other Professional Roles",
        "description": "Maps holistic end-to-end omnichannel customer journeys, friction reduction, customer effort scores (CES), and retention.",
        "common_skills": ["Customer Journey Mapping", "Omnichannel Experience Design", "Customer Effort Score (CES)", "Friction Point Analysis"],
        "seniority_levels": ["Strategist", "Senior Strategist", "Director"]
    },
    {
        "name": "Knowledge Management Lead",
        "category": "Other Professional Roles",
        "description": "Structures organizational wikis (Confluence/Notion), taxonomy tagging, internal searchability, and institutional knowledge preservation.",
        "common_skills": ["Knowledge Architecture", "Taxonomy & Metadata Tagging", "Internal Wiki Governance", "Search Relevancy", "Content Lifecycle"],
        "seniority_levels": ["Lead", "Manager"]
    },
    {
        "name": "Mergers & Acquisitions (M&A) Integration Manager",
        "category": "Other Professional Roles",
        "description": "Coordinates Day-1 IT cutovers, cultural onboarding, technology consolidation, and post-merger synergy realization.",
        "common_skills": ["Post-Merger Integration (PMI)", "Day-1 Cutover Planning", "Synergy Realization Tracking", "System Consolidation", "Cross-Org Communication"],
        "seniority_levels": ["Manager", "Senior Manager", "Director"]
    },
    {
        "name": "Real Estate & Workplace Strategy Director",
        "category": "Other Professional Roles",
        "description": "Oversees global commercial lease portfolios, hybrid work space utilization data, site selections, and office design.",
        "common_skills": ["Commercial Lease Portfolio Strategy", "Space Utilization Analytics", "Site Selection Modeling", "Workplace Construction Management"],
        "seniority_levels": ["Director", "VP"]
    },
    {
        "name": "Public Sector & Government Relations Manager",
        "category": "Other Professional Roles",
        "description": "Monitors legislative tech policy, manages public sector RFP bids (GSA Schedule), and engages regulatory bodies.",
        "common_skills": ["Government RFP / GSA Schedule", "Tech Policy Analysis", "Regulatory Agency Engagement", "Public Sector Contracting"],
        "seniority_levels": ["Manager", "Director"]
    },
    {
        "name": "Energy & Power Systems Engineer",
        "category": "Other Professional Roles",
        "description": "Designs data center power distribution units (PDU), backup generator systems, battery energy storage (BESS), and microgrids.",
        "common_skills": ["Power Systems Analysis", "BESS Storage", "Data Center PUE Optimization", "High Voltage Switchgear", "Grid Interconnection"],
        "seniority_levels": ["Engineer", "Senior Engineer", "Lead"]
    },
    {
        "name": "Acoustics & Audio Hardware Engineer",
        "category": "Other Professional Roles",
        "description": "Optimizes speaker acoustic enclosures, microphone arrays, beamforming DSP, and Total Harmonic Distortion (THD).",
        "common_skills": ["Acoustic Simulation (COMSOL)", "Anechoic Chamber Testing", "Beamforming Microphone Arrays", "Audio DSP", "THD Measurement"],
        "seniority_levels": ["Engineer", "Senior Engineer", "Staff"]
    },
    {
        "name": "Reliability & Safety Engineer (Aerospace & Automotive)",
        "category": "Other Professional Roles",
        "description": "Performs fault tree analyses (FTA), failure mode and effects analysis (FMEA), MTBF calculations, and ISO 26262 functional safety.",
        "common_skills": ["ISO 26262 Functional Safety (ASIL)", "Fault Tree Analysis (FTA)", "DFMEA / PFMEA", "MTBF / Reliability Calculations", "DO-178C"],
        "seniority_levels": ["Senior Engineer", "Staff", "Principal"]
    },
    {
        "name": "Franchise & Field Operations Director",
        "category": "Other Professional Roles",
        "description": "Oversees distributed regional operating units, brand standard audit consistency, franchisee P&L coaching, and unit economics.",
        "common_skills": ["Franchise Agreement Compliance", "Brand Standard Audits", "Unit Economics Coaching", "Regional Field Team Leadership"],
        "seniority_levels": ["Director", "VP"]
    }
]

# Quick index mapping for fast lookups
_NAME_TO_ROLE: Dict[str, Dict[str, Any]] = {
    role["name"].lower(): role for role in ROLE_CATALOG
}

def get_all_roles() -> List[Dict[str, Any]]:
    """Returns all 200+ distinct professional roles in the catalog."""
    return ROLE_CATALOG

def get_total_role_count() -> int:
    """Returns the total number of distinct roles."""
    return len(ROLE_CATALOG)

def get_categories() -> List[str]:
    """Returns a sorted list of unique category names."""
    categories = sorted(list({r["category"] for r in ROLE_CATALOG}))
    return categories

def get_roles_by_category(category: str) -> List[Dict[str, Any]]:
    """Returns all roles matching the specified category."""
    cat_lower = category.strip().lower()
    return [r for r in ROLE_CATALOG if r["category"].lower() == cat_lower]

def get_role_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Finds a role by exact or case-insensitive name match."""
    if not name:
        return None
    cleaned = name.strip().lower()
    if cleaned in _NAME_TO_ROLE:
        return _NAME_TO_ROLE[cleaned]
    # Partial fallback match
    for key, role in _NAME_TO_ROLE.items():
        if cleaned in key or key in cleaned:
            return role
    return None

def search_roles(query: str, limit: int = 25) -> List[Dict[str, Any]]:
    """
    Searches roles by matching query text against role name, category, description, and common skills.
    """
    if not query:
        return ROLE_CATALOG[:limit]
    
    q = query.strip().lower()
    results = []
    
    # Exact name matches first
    for role in ROLE_CATALOG:
        if q == role["name"].lower():
            results.append((0, role))
        elif role["name"].lower().startswith(q):
            results.append((1, role))
        elif q in role["name"].lower():
            results.append((2, role))
        elif q in role["category"].lower():
            results.append((3, role))
        elif any(q in s.lower() for s in role.get("common_skills", [])):
            results.append((4, role))
        elif q in role.get("description", "").lower():
            results.append((5, role))
            
    results.sort(key=lambda x: x[0])
    return [item[1] for item in results[:limit]]

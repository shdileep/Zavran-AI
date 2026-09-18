import re

text = """DILEEP SAI GALLA 6300668400 dileepgalla200056@gmail.com LinkedIn GitHub Portfolio SUMMARY Full stack AI Engineer with experience building enterprise AI products, intelligent automation platforms, and scalable backend systems. Delivered production applications spanning semantic search, business process automation, autonomous workflows, and developer tooling from architecture to deployment. TECHNICAL SKILLS Languages Python, SQL, Java AI / ML LangChain, LangGraph, RAG, VectorDB, PyTorch, Hugging Face, Agentic AI ML Frameworks scikit-learn, Pandas, NumPy, Sentence Transformers, FAISS, Transformers Backend / APIs Spring Boot, Node.js, FastAPI, REST, GraphQL DevOps / Tools AWS (EC2, S3), Docker, Postman, CI/CD, Git Frontend React.js, Next.js, Vue.js, Tailwind CSS, State Management WORK EXPERIENCE RenoCred July 2026 – Present Backend Developer Intern Remote • Tuned a weighted 8-factor recommendation model over embeddings for explainability, validated against 133 Credit cards. • Developed Taqdeer, a financial co-pilot combining deterministic rules with Gemini-powered conversational advisory. • Structured a resilient three-tier AI fallback flow spanning cloud models, proxy, and local intent handlers automatically. • Streamlined transaction ingestion through SMS parsing across 6+ Indian banking formats, enabling expense tracking. • Hardened data protection with PostgreSQL Row-Level Security and Clerk JWT authentication, keeping SMS client-side. Easehawk Technologies Pvt. Ltd. May 2026 – Aug 2026 AI/ML Architect & Full Stack Engineer Intern Remote • Sharpened a lead classification engine across 6 macro-sectors and 20+ B2B roles, achieving 94% classification accuracy. • Delivered a multilingual retrieval pipeline with robust hybrid search, shrinking Arabic content hallucinations by 75%. • Architected Moxsend, a production B2B AI outreach platform, by developing the orchestration layer for multi-agent execution, API integrations, and request validation pipelines. • Engineered Moxreply with a 15-state workflow enabling real-time parallel signal extraction and systematic validation. • Slashed LLM API costs by 90% through cohort-based orchestration using reusable HTML templates and merge tags. • Simplified MoxQuote proposal creation through responsive interfaces, paring manual quotation efforts down by 40%. • Improved frontend usability with 20+ reusable UI components, streamlining interactions and cutting dev time by 30%. Externsclub Pvt. Ltd Sep 2023 – Nov 2023 AI/ML Intern Bengaluru, Karnataka • Refined LoRA/QLoRA fine-tuning for Llama 3, Qwen, and Mistral, halving training time, with 35% fewer hallucinations. • Redesigned FAISS pipelines with top-k ranking, metadata filtering, and re-ranking, lifting retrieval precision by 28%. • Crafted ResumeAI using T5-based text generation, inference optimization, and response caching, reducing response time from 4.2s to 1.8s. • Administered evaluation checks across resume workflows, trimming relevance/consistency errors 22% through refinement. • Resolved runtime bottlenecks through embedding optimization and token management, reducing execution time by 40%. PROJECTS Satvora AI – Autonomous Meeting Agent Sep 2025 – Present • Built a 10-agent LangGraph scheduling engine with state-based routing for intelligent autonomous meeting coordination. • Orchestrated voice communication using WebSockets, WebRTC VAD, Whisper STT, and streaming TTS for scheduling. • Leveraged GPT-5, Sarvam Saarika v2, and Smallest.ai Waves Lightning v3.1 for multilingual conversational intelligence. • Shipped a Manifest V3 Chrome Extension and Android app for calendar synchronization and automated reminders. • Implemented a Qdrant memory layer to fetch preferences in 40ms, personalizing slot recommendations across sessions. Shubh AI Studio – Agentic Code Synthesis IDE & Self-Correcting Execution May 2026 – Present • Devised a scalable multi-agent engine that synthesizes, tests, and deploys production-ready applications automatically. • Coordinated a self-correcting, multi-language code pipeline achieving 88% first-pass success through repair cycles. • Optimized a local embedding search system, cutting code-context lookup time to under 10ms without external API calls. • Tracked failure cases across test runs to refine prompts, retrieval, and response handling before shipping changes. • Benchmarked coding models including Qwen2.5-Coder, Gemini, Mistral to optimize routing and cut response time 32%. EDUCATION Vellore Institute of Technology Aug 2021 – May 2026 Integrated M.Tech — Software Engineering | CGPA: 7.87/10 Chennai, India ACHIEVEMENTS & ACTIVITIES • Core Member, Linux Club VIT Chennai — conducted workshops on automation and Linux systems for 50+ peers. • Patent: System and Method for Optimizing Garbage Collection Operations. [Application Number: 202641010900] • Hackathon Recognition: Secured 9th place among 200 participants in CodeMania’26, a CTF competition, and 6th place among 141 teams at PASSWORD’24, a 3-day hackathon featuring point-capture and Linux-warfare."""

section_patterns = [
    ('Summary', r'\b(SUMMARY|PROFESSIONAL SUMMARY|EXECUTIVE SUMMARY|OBJECTIVE|PROFILE)\b'),
    ('Technical Skills', r'\b(TECHNICAL SKILLS|SKILLS & COMPETENCIES|SKILLS|CORE COMPETENCIES|TECH STACK)\b'),
    ('Work Experience', r'\b(WORK EXPERIENCE|PROFESSIONAL EXPERIENCE|EXPERIENCE|EMPLOYMENT HISTORY|CAREER HISTORY)\b'),
    ('Key Projects', r'\b(PROJECTS|KEY PROJECTS|TECHNICAL PROJECTS|PERSONAL PROJECTS)\b'),
    ('Education', r'\b(EDUCATION|ACADEMIC BACKGROUND|ACADEMIC HISTORY|QUALIFICATIONS)\b'),
    ('Achievements & Activities', r'\b(ACHIEVEMENTS & ACTIVITIES|ACHIEVEMENTS|ACTIVITIES|CERTIFICATIONS & HONORS|CERTIFICATIONS|PUBLICATIONS|PATENTS|AWARDS|HONORS)\b'),
    ('Languages', r'\b(LANGUAGES|SPOKEN LANGUAGES)\b'),
]

# Header info before first section
matches = []
for label, pat in section_patterns:
    m = re.search(pat, text, re.IGNORECASE)
    if m:
        matches.append((m.start(), m.end(), m.group(0), label))

matches.sort(key=lambda x: x[0])

# Header text
header_text = text[:matches[0][0]] if matches else ''
print("Header text:", header_text)

# Email
email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
email = email_match.group(0) if email_match else ''
print("Email:", email)

# Phone
phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\b\d{10}\b', text)
phone = phone_match.group(0) if phone_match else ''
print("Phone:", phone)

# Name: words before phone/email or first few capitalized words
name_cand = re.sub(r'(\d{10}|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|LinkedIn|GitHub|Portfolio|https?://\S+)', '', header_text)
name = ' '.join(name_cand.split()[:4])
print("Name:", name)

# Sections
sections = []
for i in range(len(matches)):
    start_pos = matches[i][1]
    end_pos = matches[i+1][0] if i+1 < len(matches) else len(text)
    content = text[start_pos:end_pos].strip()
    sections.append({
        'title': matches[i][3],
        'content': content
    })

print(f"\nExtracted {len(sections)} sections successfully:")
for s in sections:
    print(f"\n=== [{s['title']}] ===")
    print(s['content'][:150] + "...")

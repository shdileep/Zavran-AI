import re

text = """DILEEP SAI GALLA 6300668400 dileepgalla200056@gmail.com LinkedIn GitHub Portfolio SUMMARY Full stack AI Engineer with experience building enterprise AI products, intelligent automation platforms, and scalable backend systems. Delivered production applications spanning semantic search, business process automation, autonomous workflows, and developer tooling from architecture to deployment. TECHNICAL SKILLS Languages Python, SQL, Java AI / ML LangChain, LangGraph, RAG, VectorDB, PyTorch, Hugging Face, Agentic AI ML Frameworks scikit-learn, Pandas, NumPy, Sentence Transformers, FAISS, Transformers Backend / APIs Spring Boot, Node.js, FastAPI, REST, GraphQL DevOps / Tools AWS (EC2, S3), Docker, Postman, CI/CD, Git Frontend React.js, Next.js, Vue.js, Tailwind CSS, State Management WORK EXPERIENCE RenoCred July 2026 – Present Backend Developer Intern Remote • Tuned a weighted 8-factor recommendation model over embeddings for explainability, validated against 133 Credit cards. • Developed Taqdeer, a financial co-pilot combining deterministic rules with Gemini-powered conversational advisory. • Structured a resilient three-tier AI fallback flow spanning cloud models, proxy, and local intent handlers automatically. • Streamlined transaction ingestion through SMS parsing across 6+ Indian banking formats, enabling expense tracking. • Hardened data protection with PostgreSQL Row-Level Security and Clerk JWT authentication, keeping SMS client-side. Easehawk Technologies Pvt. Ltd. May 2026 – Aug 2026 AI/ML Architect & Full Stack Engineer Intern Remote • Sharpened a lead classification engine across 6 macro-sectors and 20+ B2B roles, achieving 94% classification accuracy. • Delivered a multilingual retrieval pipeline with robust hybrid search, shrinking Arabic content hallucinations by 75%. • Architected Moxsend, a production B2B AI outreach platform, by developing the orchestration layer for multi-agent execution, API integrations, and request validation pipelines. • Engineered Moxreply with a 15-state workflow enabling real-time parallel signal extraction and systematic validation. • Slashed LLM API costs by 90% through cohort-based orchestration using reusable HTML templates and merge tags. • Simplified MoxQuote proposal creation through responsive interfaces, paring manual quotation efforts down by 40%. • Improved frontend usability with 20+ reusable UI components, streamlining interactions and cutting dev time by 30%. Externsclub Pvt. Ltd Sep 2023 – Nov 2023 AI/ML Intern Bengaluru, Karnataka • Refined LoRA/QLoRA fine-tuning for Llama 3, Qwen, and Mistral, halving training time, with 35% fewer hallucinations. • Redesigned FAISS pipelines with top-k ranking, metadata filtering, and re-ranking, lifting retrieval precision by 28%. • Crafted ResumeAI using T5-based text generation, inference optimization, and response caching, reducing response time from 4.2s to 1.8s. • Administered evaluation checks across resume workflows, trimming relevance/consistency errors 22% through refinement. • Resolved runtime bottlenecks through embedding optimization and token management, reducing execution time by 40%. PROJECTS Satvora AI – Autonomous Meeting Agent Sep 2025 – Present • Built a 10-agent LangGraph scheduling engine with state-based routing for intelligent autonomous meeting coordination. • Orchestrated voice communication using WebSockets, WebRTC VAD, Whisper STT, and streaming TTS for scheduling. • Leveraged GPT-5, Sarvam Saarika v2, and Smallest.ai Waves Lightning v3.1 for multilingual conversational intelligence. • Shipped a Manifest V3 Chrome Extension and Android app for calendar synchronization and automated reminders. • Implemented a Qdrant memory layer to fetch preferences in 40ms, personalizing slot recommendations across sessions. Shubh AI Studio – Agentic Code Synthesis IDE & Self-Correcting Execution May 2026 – Present • Devised a scalable multi-agent engine that synthesizes, tests, and deploys production-ready applications automatically. • Coordinated a self-correcting, multi-language code pipeline achieving 88% first-pass success through repair cycles. • Optimized a local embedding search system, cutting code-context lookup time to under 10ms without external API calls. • Tracked failure cases across test runs to refine prompts, retrieval, and response handling before shipping changes. • Benchmarked coding models including Qwen2.5-Coder, Gemini, Mistral to optimize routing and cut response time 32%. EDUCATION Vellore Institute of Technology Aug 2021 – May 2026 Integrated M.Tech — Software Engineering | CGPA: 7.87/10 Chennai, India ACHIEVEMENTS & ACTIVITIES • Core Member, Linux Club VIT Chennai — conducted workshops on automation and Linux systems for 50+ peers. • Patent: System and Method for Optimizing Garbage Collection Operations. [Application Number: 202641010900] • Hackathon Recognition: Secured 9th place among 200 participants in CodeMania’26, a CTF competition, and 6th place among 141 teams at PASSWORD’24, a 3-day hackathon featuring point-capture and Linux-warfare."""

def segment_experience_items(content):
    date_regex = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}\s*(?:–|-|to)\s*(?:Present|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}))'
    date_matches = list(re.finditer(date_regex, content, re.IGNORECASE))
    
    if not date_matches:
        return [{'title': 'Experience', 'bullets': [b.strip() for b in content.split('•') if b.strip()]}]
        
    items = []
    for i, dm in enumerate(date_matches):
        date_str = dm.group(0)
        date_start = dm.start()
        date_end = dm.end()
        
        # Look backwards from date_start up to 100 chars or to previous sentence end (e.g. '.', '\n', or bullet)
        if i == 0:
            prefix_text = content[:date_start].strip()
        else:
            prev_end = date_matches[i-1].end()
            between = content[prev_end:date_start]
            # Find the last sentence end (after the last bullet point)
            # Find last '.' in between
            dot_pos = between.rfind('.')
            if dot_pos != -1:
                prefix_text = between[dot_pos+1:].strip()
            else:
                prefix_text = between.strip()
                
        # Clean company name
        company_name = re.sub(r'^[•\s\n]+', '', prefix_text).strip()
        
        # Look forward for role & location (text between date_end and first bullet '•')
        if i + 1 < len(date_matches):
            next_start = date_matches[i+1].start()
            between_text = content[date_end:next_start]
            # Find the last period before next company name
            # The bullet section goes until the last period
            dot_pos = between_text.rfind('.')
            if dot_pos != -1:
                body_block = between_text[:dot_pos+1]
            else:
                body_block = between_text
        else:
            body_block = content[date_end:]
            
        first_bullet_idx = body_block.find('•')
        if first_bullet_idx != -1:
            role_loc = body_block[:first_bullet_idx].strip()
            bullets_raw = body_block[first_bullet_idx:]
        else:
            role_loc = ''
            bullets_raw = body_block
            
        bullets = [b.strip() for b in bullets_raw.split('•') if b.strip()]
        items.append({
            'company': company_name,
            'period': date_str,
            'role_location': role_loc,
            'bullets': bullets
        })
    return items

def segment_project_items(content):
    date_regex = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}\s*(?:–|-|to)\s*(?:Present|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}))'
    date_matches = list(re.finditer(date_regex, content, re.IGNORECASE))
    
    if not date_matches:
        return [{'title': 'Projects', 'bullets': [b.strip() for b in content.split('•') if b.strip()]}]
        
    items = []
    for i, dm in enumerate(date_matches):
        date_str = dm.group(0)
        date_start = dm.start()
        date_end = dm.end()
        
        if i == 0:
            prefix_text = content[:date_start].strip()
        else:
            prev_end = date_matches[i-1].end()
            between = content[prev_end:date_start]
            dot_pos = between.rfind('.')
            if dot_pos != -1:
                prefix_text = between[dot_pos+1:].strip()
            else:
                prefix_text = between.strip()
                
        project_title = re.sub(r'^[•\s\n]+', '', prefix_text).strip()
        
        if i + 1 < len(date_matches):
            next_start = date_matches[i+1].start()
            between_text = content[date_end:next_start]
            dot_pos = between_text.rfind('.')
            if dot_pos != -1:
                body_block = between_text[:dot_pos+1]
            else:
                body_block = between_text
        else:
            body_block = content[date_end:]
            
        first_bullet_idx = body_block.find('•')
        if first_bullet_idx != -1:
            tagline = body_block[:first_bullet_idx].strip()
            bullets_raw = body_block[first_bullet_idx:]
        else:
            tagline = ''
            bullets_raw = body_block
            
        bullets = [b.strip() for b in bullets_raw.split('•') if b.strip()]
        items.append({
            'title': project_title,
            'period': date_str,
            'tagline': tagline,
            'bullets': bullets
        })
    return items

exp_text = text[text.find('WORK EXPERIENCE')+15:text.find('PROJECTS')].strip()
exp_items = segment_experience_items(exp_text)
print("=== EXPERIENCES EXTRACTED: ===")
for it in exp_items:
    print(f"\nCompany: '{it['company']}'")
    print(f"Period: '{it['period']}' | Role/Loc: '{it['role_location']}'")
    print(f"Bullets ({len(it['bullets'])}):")
    for b in it['bullets'][:2]:
        print(f"  • {b[:70]}...")

proj_text = text[text.find('PROJECTS')+8:text.find('EDUCATION')].strip()
proj_items = segment_project_items(proj_text)
print("\n=== PROJECTS EXTRACTED: ===")
for it in proj_items:
    print(f"\nProject Title: '{it['title']}'")
    print(f"Period: '{it['period']}'")
    print(f"Bullets ({len(it['bullets'])}):")
    for b in it['bullets'][:2]:
        print(f"  • {b[:70]}...")

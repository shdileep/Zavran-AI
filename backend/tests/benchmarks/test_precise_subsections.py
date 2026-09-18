import re

text = """DILEEP SAI GALLA 6300668400 dileepgalla200056@gmail.com LinkedIn GitHub Portfolio SUMMARY Full stack AI Engineer with experience building enterprise AI products, intelligent automation platforms, and scalable backend systems. Delivered production applications spanning semantic search, business process automation, autonomous workflows, and developer tooling from architecture to deployment. TECHNICAL SKILLS Languages Python, SQL, Java AI / ML LangChain, LangGraph, RAG, VectorDB, PyTorch, Hugging Face, Agentic AI ML Frameworks scikit-learn, Pandas, NumPy, Sentence Transformers, FAISS, Transformers Backend / APIs Spring Boot, Node.js, FastAPI, REST, GraphQL DevOps / Tools AWS (EC2, S3), Docker, Postman, CI/CD, Git Frontend React.js, Next.js, Vue.js, Tailwind CSS, State Management WORK EXPERIENCE RenoCred July 2026 – Present Backend Developer Intern Remote • Tuned a weighted 8-factor recommendation model over embeddings for explainability, validated against 133 Credit cards. • Developed Taqdeer, a financial co-pilot combining deterministic rules with Gemini-powered conversational advisory. • Structured a resilient three-tier AI fallback flow spanning cloud models, proxy, and local intent handlers automatically. • Streamlined transaction ingestion through SMS parsing across 6+ Indian banking formats, enabling expense tracking. • Hardened data protection with PostgreSQL Row-Level Security and Clerk JWT authentication, keeping SMS client-side. Easehawk Technologies Pvt. Ltd. May 2026 – Aug 2026 AI/ML Architect & Full Stack Engineer Intern Remote • Sharpened a lead classification engine across 6 macro-sectors and 20+ B2B roles, achieving 94% classification accuracy. • Delivered a multilingual retrieval pipeline with robust hybrid search, shrinking Arabic content hallucinations by 75%. • Architected Moxsend, a production B2B AI outreach platform, by developing the orchestration layer for multi-agent execution, API integrations, and request validation pipelines. • Engineered Moxreply with a 15-state workflow enabling real-time parallel signal extraction and systematic validation. • Slashed LLM API costs by 90% through cohort-based orchestration using reusable HTML templates and merge tags. • Simplified MoxQuote proposal creation through responsive interfaces, paring manual quotation efforts down by 40%. • Improved frontend usability with 20+ reusable UI components, streamlining interactions and cutting dev time by 30%. Externsclub Pvt. Ltd Sep 2023 – Nov 2023 AI/ML Intern Bengaluru, Karnataka • Refined LoRA/QLoRA fine-tuning for Llama 3, Qwen, and Mistral, halving training time, with 35% fewer hallucinations. • Redesigned FAISS pipelines with top-k ranking, metadata filtering, and re-ranking, lifting retrieval precision by 28%. • Crafted ResumeAI using T5-based text generation, inference optimization, and response caching, reducing response time from 4.2s to 1.8s. • Administered evaluation checks across resume workflows, trimming relevance/consistency errors 22% through refinement. • Resolved runtime bottlenecks through embedding optimization and token management, reducing execution time by 40%. PROJECTS Satvora AI – Autonomous Meeting Agent Sep 2025 – Present • Built a 10-agent LangGraph scheduling engine with state-based routing for intelligent autonomous meeting coordination. • Orchestrated voice communication using WebSockets, WebRTC VAD, Whisper STT, and streaming TTS for scheduling. • Leveraged GPT-5, Sarvam Saarika v2, and Smallest.ai Waves Lightning v3.1 for multilingual conversational intelligence. • Shipped a Manifest V3 Chrome Extension and Android app for calendar synchronization and automated reminders. • Implemented a Qdrant memory layer to fetch preferences in 40ms, personalizing slot recommendations across sessions. Shubh AI Studio – Agentic Code Synthesis IDE & Self-Correcting Execution May 2026 – Present • Devised a scalable multi-agent engine that synthesizes, tests, and deploys production-ready applications automatically. • Coordinated a self-correcting, multi-language code pipeline achieving 88% first-pass success through repair cycles. • Optimized a local embedding search system, cutting code-context lookup time to under 10ms without external API calls. • Tracked failure cases across test runs to refine prompts, retrieval, and response handling before shipping changes. • Benchmarked coding models including Qwen2.5-Coder, Gemini, Mistral to optimize routing and cut response time 32%. EDUCATION Vellore Institute of Technology Aug 2021 – May 2026 Integrated M.Tech — Software Engineering | CGPA: 7.87/10 Chennai, India ACHIEVEMENTS & ACTIVITIES • Core Member, Linux Club VIT Chennai — conducted workshops on automation and Linux systems for 50+ peers. • Patent: System and Method for Optimizing Garbage Collection Operations. [Application Number: 202641010900] • Hackathon Recognition: Secured 9th place among 200 participants in CodeMania’26, a CTF competition, and 6th place among 141 teams at PASSWORD’24, a 3-day hackathon featuring point-capture and Linux-warfare."""

def parse_experience_entries(exp_raw):
    # Regex to find dates: Month YYYY – Present or Month YYYY – Month YYYY
    date_regex = re.compile(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}\s*(?:–|-|to)\s*(?:Present|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}))', re.IGNORECASE)
    
    date_matches = list(date_regex.finditer(exp_raw))
    if not date_matches:
        return [{'company': 'Work Experience', 'period': '', 'role': '', 'bullets': [b.strip() for b in exp_raw.split('•') if b.strip()]}]
    
    entries = []
    for idx, dm in enumerate(date_matches):
        period = dm.group(0)
        d_start, d_end = dm.span()
        
        # Get company name: look backward from d_start up to preceding bullet point or start
        if idx == 0:
            comp_text = exp_raw[:d_start].strip()
        else:
            prev_d_end = date_matches[idx-1].end()
            between = exp_raw[prev_d_end:d_start]
            # Find the last bullet in between
            last_b_idx = between.rfind('•')
            if last_b_idx != -1:
                # The text of the last bullet ends at a period before the next company name
                bullet_body = between[last_b_idx:]
                # Look for company name after the sentence ending (e.g. '. ')
                m_comp = re.search(r'\.\s+([A-Z][A-Za-z0-9\s.,&\'\-]+)$', bullet_body)
                if m_comp:
                    comp_text = m_comp.group(1).strip()
                else:
                    comp_text = between[last_b_idx+1:].strip()
            else:
                comp_text = between.strip()
                
        # Clean company text
        comp_text = re.sub(r'^[•\s\n]+', '', comp_text).strip()
        
        # Get content between this date and next date
        if idx + 1 < len(date_matches):
            next_d_start = date_matches[idx+1].start()
            content_block = exp_raw[d_end:next_d_start]
            # Cut off the company name of the next entry if it exists at the end
            last_b = content_block.rfind('•')
            if last_b != -1:
                m_next_comp = re.search(r'\.\s+([A-Z][A-Za-z0-9\s.,&\'\-]+)$', content_block[last_b:])
                if m_next_comp:
                    content_block = content_block[:last_b + m_next_comp.start() + 1]
        else:
            content_block = exp_raw[d_end:]
            
        # Role & Location is before first bullet
        first_b = content_block.find('•')
        if first_b != -1:
            role_text = content_block[:first_b].strip()
            bullets_part = content_block[first_b:]
        else:
            role_text = ''
            bullets_part = content_block
            
        bullets = [b.strip() for b in bullets_part.split('•') if b.strip()]
        
        entries.append({
            'company': comp_text,
            'role': role_text,
            'period': period,
            'bullets': bullets
        })
        
    return entries

def parse_project_entries(proj_raw):
    date_regex = re.compile(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}\s*(?:–|-|to)\s*(?:Present|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}))', re.IGNORECASE)
    date_matches = list(date_regex.finditer(proj_raw))
    
    if not date_matches:
        return [{'title': 'Project', 'period': '', 'bullets': [b.strip() for b in proj_raw.split('•') if b.strip()]}]
        
    entries = []
    for idx, dm in enumerate(date_matches):
        period = dm.group(0)
        d_start, d_end = dm.span()
        
        if idx == 0:
            title_text = proj_raw[:d_start].strip()
        else:
            prev_d_end = date_matches[idx-1].end()
            between = proj_raw[prev_d_end:d_start]
            last_b_idx = between.rfind('•')
            if last_b_idx != -1:
                bullet_body = between[last_b_idx:]
                m_title = re.search(r'\.\s+([A-Z][A-Za-z0-9\s.,&\'\-–—]+)$', bullet_body)
                if m_title:
                    title_text = m_title.group(1).strip()
                else:
                    title_text = between[last_b_idx+1:].strip()
            else:
                title_text = between.strip()
                
        title_text = re.sub(r'^[•\s\n]+', '', title_text).strip()
        
        if idx + 1 < len(date_matches):
            next_d_start = date_matches[idx+1].start()
            content_block = proj_raw[d_end:next_d_start]
            last_b = content_block.rfind('•')
            if last_b != -1:
                m_next_title = re.search(r'\.\s+([A-Z][A-Za-z0-9\s.,&\'\-–—]+)$', content_block[last_b:])
                if m_next_title:
                    content_block = content_block[:last_b + m_next_title.start() + 1]
        else:
            content_block = proj_raw[d_end:]
            
        first_b = content_block.find('•')
        if first_b != -1:
            bullets_part = content_block[first_b:]
        else:
            bullets_part = content_block
            
        bullets = [b.strip() for b in bullets_part.split('•') if b.strip()]
        
        entries.append({
            'title': title_text,
            'period': period,
            'bullets': bullets
        })
    return entries

exp_text = text[text.find('WORK EXPERIENCE')+15:text.find('PROJECTS')].strip()
exp_entries = parse_experience_entries(exp_text)

print("=== PARSED WORK EXPERIENCES ===")
for e in exp_entries:
    print(f"\n[Company]: {e['company']}")
    print(f"[Role & Loc]: {e['role']} | [Period]: {e['period']}")
    print(f"[Bullets ({len(e['bullets'])})]:")
    for b in e['bullets'][:2]:
        print(f"  • {b[:75]}...")

proj_text = text[text.find('PROJECTS')+8:text.find('EDUCATION')].strip()
proj_entries = parse_project_entries(proj_text)

print("\n=== PARSED PROJECTS ===")
for p in proj_entries:
    print(f"\n[Project Title]: {p['title']}")
    print(f"[Period]: {p['period']}")
    print(f"[Bullets ({len(p['bullets'])})]:")
    for b in p['bullets'][:2]:
        print(f"  • {b[:75]}...")

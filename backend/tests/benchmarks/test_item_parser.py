import re

text = """DILEEP SAI GALLA 6300668400 dileepgalla200056@gmail.com LinkedIn GitHub Portfolio SUMMARY Full stack AI Engineer with experience building enterprise AI products, intelligent automation platforms, and scalable backend systems. Delivered production applications spanning semantic search, business process automation, autonomous workflows, and developer tooling from architecture to deployment. TECHNICAL SKILLS Languages Python, SQL, Java AI / ML LangChain, LangGraph, RAG, VectorDB, PyTorch, Hugging Face, Agentic AI ML Frameworks scikit-learn, Pandas, NumPy, Sentence Transformers, FAISS, Transformers Backend / APIs Spring Boot, Node.js, FastAPI, REST, GraphQL DevOps / Tools AWS (EC2, S3), Docker, Postman, CI/CD, Git Frontend React.js, Next.js, Vue.js, Tailwind CSS, State Management WORK EXPERIENCE RenoCred July 2026 – Present Backend Developer Intern Remote • Tuned a weighted 8-factor recommendation model over embeddings for explainability, validated against 133 Credit cards. • Developed Taqdeer, a financial co-pilot combining deterministic rules with Gemini-powered conversational advisory. • Structured a resilient three-tier AI fallback flow spanning cloud models, proxy, and local intent handlers automatically. • Streamlined transaction ingestion through SMS parsing across 6+ Indian banking formats, enabling expense tracking. • Hardened data protection with PostgreSQL Row-Level Security and Clerk JWT authentication, keeping SMS client-side. Easehawk Technologies Pvt. Ltd. May 2026 – Aug 2026 AI/ML Architect & Full Stack Engineer Intern Remote • Sharpened a lead classification engine across 6 macro-sectors and 20+ B2B roles, achieving 94% classification accuracy. • Delivered a multilingual retrieval pipeline with robust hybrid search, shrinking Arabic content hallucinations by 75%. • Architected Moxsend, a production B2B AI outreach platform, by developing the orchestration layer for multi-agent execution, API integrations, and request validation pipelines. • Engineered Moxreply with a 15-state workflow enabling real-time parallel signal extraction and systematic validation. • Slashed LLM API costs by 90% through cohort-based orchestration using reusable HTML templates and merge tags. • Simplified MoxQuote proposal creation through responsive interfaces, paring manual quotation efforts down by 40%. • Improved frontend usability with 20+ reusable UI components, streamlining interactions and cutting dev time by 30%. Externsclub Pvt. Ltd Sep 2023 – Nov 2023 AI/ML Intern Bengaluru, Karnataka • Refined LoRA/QLoRA fine-tuning for Llama 3, Qwen, and Mistral, halving training time, with 35% fewer hallucinations. • Redesigned FAISS pipelines with top-k ranking, metadata filtering, and re-ranking, lifting retrieval precision by 28%. • Crafted ResumeAI using T5-based text generation, inference optimization, and response caching, reducing response time from 4.2s to 1.8s. • Administered evaluation checks across resume workflows, trimming relevance/consistency errors 22% through refinement. • Resolved runtime bottlenecks through embedding optimization and token management, reducing execution time by 40%. PROJECTS Satvora AI – Autonomous Meeting Agent Sep 2025 – Present • Built a 10-agent LangGraph scheduling engine with state-based routing for intelligent autonomous meeting coordination. • Orchestrated voice communication using WebSockets, WebRTC VAD, Whisper STT, and streaming TTS for scheduling. • Leveraged GPT-5, Sarvam Saarika v2, and Smallest.ai Waves Lightning v3.1 for multilingual conversational intelligence. • Shipped a Manifest V3 Chrome Extension and Android app for calendar synchronization and automated reminders. • Implemented a Qdrant memory layer to fetch preferences in 40ms, personalizing slot recommendations across sessions. Shubh AI Studio – Agentic Code Synthesis IDE & Self-Correcting Execution May 2026 – Present • Devised a scalable multi-agent engine that synthesizes, tests, and deploys production-ready applications automatically. • Coordinated a self-correcting, multi-language code pipeline achieving 88% first-pass success through repair cycles. • Optimized a local embedding search system, cutting code-context lookup time to under 10ms without external API calls. • Tracked failure cases across test runs to refine prompts, retrieval, and response handling before shipping changes. • Benchmarked coding models including Qwen2.5-Coder, Gemini, Mistral to optimize routing and cut response time 32%. EDUCATION Vellore Institute of Technology Aug 2021 – May 2026 Integrated M.Tech — Software Engineering | CGPA: 7.87/10 Chennai, India ACHIEVEMENTS & ACTIVITIES • Core Member, Linux Club VIT Chennai — conducted workshops on automation and Linux systems for 50+ peers. • Patent: System and Method for Optimizing Garbage Collection Operations. [Application Number: 202641010900] • Hackathon Recognition: Secured 9th place among 200 participants in CodeMania’26, a CTF competition, and 6th place among 141 teams at PASSWORD’24, a 3-day hackathon featuring point-capture and Linux-warfare."""

def parse_work_experience(content):
    # Split by company entries. A company header is a line/phrase followed by a date range like (July 2026 – Present, May 2026 – Aug 2026, etc.)
    # Pattern to find date ranges: (Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]* \d{4} (?:–|-|to) (?:Present|\w+ \d{4})
    date_regex = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}\s*(?:–|-|to)\s*(?:Present|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}))'
    
    # We can segment by finding where company blocks start
    # Let's split content into blocks before each company header
    items = []
    # Find all date occurrences
    date_matches = list(re.finditer(date_regex, content, re.IGNORECASE))
    
    if not date_matches:
        # Fallback split by double newlines or bullets
        return [{'title': 'Experience', 'bullets': [b.strip() for b in content.split('•') if b.strip()]}]
    
    for i, dm in enumerate(date_matches):
        date_str = dm.group(0)
        date_start = dm.start()
        date_end = dm.end()
        
        # Find where this entry header started (either from previous entry end or start of content)
        if i == 0:
            entry_header_start = 0
        else:
            # Look at previous entry's bullets end
            # The company name is between the last bullet of previous entry and this date
            prev_block_end = date_matches[i-1].end()
            # Find the last bullet before date_start
            last_bullet_match = list(re.finditer(r'•\s*[^•]+', content[prev_block_end:date_start]))
            if last_bullet_match:
                entry_header_start = prev_block_end + last_bullet_match[-1].end()
            else:
                entry_header_start = prev_block_end
        
        company_raw = content[entry_header_start:date_start].strip()
        # Clean company raw from trailing/leading bullets
        company_raw = re.sub(r'^[•\s]+', '', company_raw)
        
        # Role & Location are often right after the date before the first bullet
        # Next block ends at either next entry header or end of content
        if i + 1 < len(date_matches):
            next_date_start = date_matches[i+1].start()
            # Find last bullet before next_date_start
            bullets_text = content[date_end:next_date_start]
            # The next company name is after the last bullet in bullets_text
            last_bullet = list(re.finditer(r'•\s*[^•]+', bullets_text))
            if last_bullet:
                bullets_block = bullets_text[:last_bullet[-1].end()]
            else:
                bullets_block = bullets_text
        else:
            bullets_block = content[date_end:]
        
        # Extract role/location from beginning of bullets_block before first bullet '•'
        first_bullet_idx = bullets_block.find('•')
        if first_bullet_idx != -1:
            role_loc = bullets_block[:first_bullet_idx].strip()
            bullets_raw = bullets_block[first_bullet_idx:]
        else:
            role_loc = ''
            bullets_raw = bullets_block
            
        bullets = [b.strip() for b in bullets_raw.split('•') if b.strip()]
        
        items.append({
            'company': company_raw,
            'period': date_str,
            'role_location': role_loc,
            'bullets': bullets
        })
        
    return items

def parse_projects(content):
    date_regex = r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}\s*(?:–|-|to)\s*(?:Present|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|July|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{4}))'
    date_matches = list(re.finditer(date_regex, content, re.IGNORECASE))
    
    if not date_matches:
        # Fallback: split by project headers like "Satvora AI", "Shubh AI Studio"
        return [{'title': 'Project', 'bullets': [b.strip() for b in content.split('•') if b.strip()]}]
        
    items = []
    for i, dm in enumerate(date_matches):
        date_str = dm.group(0)
        date_start = dm.start()
        date_end = dm.end()
        
        if i == 0:
            header_start = 0
        else:
            prev_date_end = date_matches[i-1].end()
            bullets_between = list(re.finditer(r'•\s*[^•]+', content[prev_date_end:date_start]))
            if bullets_between:
                header_start = prev_date_end + bullets_between[-1].end()
            else:
                header_start = prev_date_end
                
        proj_title = content[header_start:date_start].strip().replace('•', '').strip()
        
        if i + 1 < len(date_matches):
            next_date_start = date_matches[i+1].start()
            between_text = content[date_end:next_date_start]
            last_bullet = list(re.finditer(r'•\s*[^•]+', between_text))
            if last_bullet:
                bullets_block = between_text[:last_bullet[-1].end()]
            else:
                bullets_block = between_text
        else:
            bullets_block = content[date_end:]
            
        bullets = [b.strip() for b in bullets_block.split('•') if b.strip()]
        items.append({
            'title': proj_title,
            'period': date_str,
            'bullets': bullets
        })
    return items

# Test extraction from user resume
exp_text = text[text.find('WORK EXPERIENCE')+15:text.find('PROJECTS')].strip()
print("Work Experience Items:")
exp_items = parse_work_experience(exp_text)
for idx, it in enumerate(exp_items, 1):
    print(f"\n--- Company {idx}: {it['company']} ({it['period']}) [{it['role_location']}] ---")
    for b in it['bullets'][:2]:
        print(f"  • {b[:80]}...")

proj_text = text[text.find('PROJECTS')+8:text.find('EDUCATION')].strip()
print("\nProjects Items:")
proj_items = parse_projects(proj_text)
for idx, it in enumerate(proj_items, 1):
    print(f"\n--- Project {idx}: {it['title']} ({it['period']}) ---")
    for b in it['bullets'][:2]:
        print(f"  • {b[:80]}...")

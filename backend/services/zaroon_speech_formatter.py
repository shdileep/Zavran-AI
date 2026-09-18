import re
from typing import Set

class ZaroonSpeechFormatter:
    """
    Speech preprocessor for Zaroon AI Technical Recruiter.
    Converts raw text/prompts into natural, speech-optimized utterances for Smallest AI Waves TTS.
    
    Principles:
    1. Preserves exact technical terminology (FastAPI, LangGraph, PostgreSQL, FAISS, etc.).
    2. Strips markdown clutter (*, #, `, -, _) that disrupts TTS prosody.
    3. Normalizes punctuation for natural conversational rhythm and natural pauses.
    4. Never hallucinates or alters the technical meaning of the interviewer's question.
    """

    # Canonical Technical Terms to preserve with exact casing & pronunciation
    PROTECTED_TERMS = {
        "FastAPI", "LangGraph", "LangChain", "PostgreSQL", "pgvector",
        "Redis", "Docker", "Kubernetes", "AWS", "EC2", "S3",
        "RAG", "LLM", "API", "REST", "GraphQL", "WebSocket", "WebSockets",
        "Python", "TypeScript", "JavaScript", "React", "Next.js",
        "PyTorch", "Hugging Face", "HuggingFace", "FAISS", "Qdrant",
        "Chroma", "Milvus", "Pinecone", "gRPC", "Kafka", "RabbitMQ",
        "Celery", "Temporal", "BullMQ", "Ollama", "Llama", "Mistral",
        "Gemma", "Qwen", "DeepSeek", "Claude", "GPT-4o", "GPT-5",
        "CI/CD", "SQL", "NoSQL", "JSON", "YAML", "JWT", "OAuth",
        "SSE", "HNSW", "BM25", "TF-IDF", "LoRA", "QLoRA", "TTFT",
        "STT", "TTS", "VAD", "WebRTC", "Supabase", "Clerk"
    }

    _TERM_MAP = {term.lower(): term for term in PROTECTED_TERMS}

    @classmethod
    def clean_markdown(cls, text: str) -> str:
        """Removes markdown syntax and formatting symbols that sound unnatural in TTS."""
        if not text:
            return ""
        
        # Strip code blocks
        text = re.sub(r'```[\s\S]*?```', ' ', text)
        
        # Strip inline code ticks
        text = re.sub(r'`([^`]+)`', r'\1', text)
        
        # Strip Markdown bold/italic: **text**, *text*, __text__, _text_
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'__([^_]+)__', r'\1', text)
        text = re.sub(r'_([^_]+)_', r'\1', text)
        
        # Strip markdown headers: # Header -> Header
        text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)
        
        # Strip bullet points and list markers at line start
        text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
        text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
        
        # Strip HTML tags
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # Strip emojis / special symbols
        text = re.sub(r'[^\w\s\.,\?!\'\"\-/:;@#\$%\(\)]', ' ', text)
        
        return text

    @classmethod
    def preserve_technical_terms(cls, text: str) -> str:
        """Ensures protected technical terms maintain standard technical casing."""
        words = text.split()
        preserved_words = []
        for word in words:
            match = re.match(r'^([\(\[\'\"\{]*)(.*?)([\)\]\'\"\}\.,\?!;:]*)$', word)
            if match:
                prefix, core, suffix = match.groups()
                core_lower = core.lower()
                if core_lower in cls._TERM_MAP:
                    preserved_words.append(f"{prefix}{cls._TERM_MAP[core_lower]}{suffix}")
                else:
                    preserved_words.append(word)
            else:
                preserved_words.append(word)
        return " ".join(preserved_words)

    @classmethod
    def format_pauses_and_rhythm(cls, text: str) -> str:
        """
        Replaces awkward formatting with natural conversational punctuation.
        Ensures pauses are natural, not robotic or stretched.
        """
        # Normalize multiple dots / ellipses
        text = re.sub(r'\.{2,}', '.', text)
        
        # Normalize multiple exclamation/question marks
        text = re.sub(r'\?{2,}', '?', text)
        text = re.sub(r'!{2,}', '!', text)
        
        # Remove consecutive commas
        text = re.sub(r',{2,}', ',', text)
        
        # Ensure single space after punctuation
        text = re.sub(r'([\.?!,;:])([^\s\d])', r'\1 \2', text)
        
        # Collapse multiple whitespace into clean single spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    @classmethod
    def format_for_speech(cls, text: str) -> str:
        """
        Master pipeline: Formats interviewer text into clean, human-like dialogue for Zaroon TTS.
        """
        if not text or not text.strip():
            return ""

        cleaned = cls.clean_markdown(text)
        with_terms = cls.preserve_technical_terms(cleaned)
        rhythmic = cls.format_pauses_and_rhythm(with_terms)

        # Ensure trailing punctuation if missing
        if rhythmic and rhythmic[-1] not in '.?!':
            rhythmic += '.'

        return rhythmic

zaroon_speech_formatter = ZaroonSpeechFormatter()

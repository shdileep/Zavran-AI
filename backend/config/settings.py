import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"

def load_env_file(env_path: Path = ENV_FILE):
    """Simple parser to load .env variables into os.environ if python-dotenv is not installed."""
    if not env_path.exists():
        return
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip().strip("'\"")
            if key and key not in os.environ:
                os.environ[key] = val

# Auto load upon import
load_env_file()

class Settings:
    # Anthropic / Claude
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Groq
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # Google AI Studio / Gemini
    GOOGLE_AI_STUDIO_API_KEY: str = os.getenv("GOOGLE_AI_STUDIO_API_KEY", "")
    
    # Kimi / Moonshot AI
    KIMI_API_KEY: str = os.getenv("KIMI_API_KEY", "")
    KIMI_BASE_URL: str = os.getenv("KIMI_BASE_URL", "https://api.moonshot.cn/v1")
    KIMI_MODEL: str = os.getenv("KIMI_MODEL", "moonshot-v1-32k")
    
    # Cloudflare & R2 Storage
    CLOUDFLARE_ACCOUNT_ID: str = os.getenv("CLOUDFLARE_ACCOUNT_ID", "")
    CLOUDFLARE_API_TOKEN: str = os.getenv("CLOUDFLARE_API_TOKEN", "")
    CLOUDFLARE_R2_ACCESS_KEY_ID: str = os.getenv("CLOUDFLARE_R2_ACCESS_KEY_ID", "")
    CLOUDFLARE_R2_SECRET_ACCESS_KEY: str = os.getenv("CLOUDFLARE_R2_SECRET_ACCESS_KEY", "")
    CLOUDFLARE_R2_ENDPOINT: str = os.getenv("CLOUDFLARE_R2_ENDPOINT", "")
    
    # AssemblyAI
    ASSEMBLYAI_API_KEY: str = os.getenv("ASSEMBLYAI_API_KEY", "")
    
    # Sarvam AI
    SARVAM_API_KEY: str = os.getenv("SARVAM_API_KEY", "")
    
    # Bolna AI
    BOLNA_API_KEY: str = os.getenv("BOLNA_API_KEY", "")

    # Smallest AI (Exclusive Zaroon Voice Cloning & Engine)
    SMALLEST_API_KEY: str = os.getenv("SMALLEST_API_KEY", "")
    ZAROON_VOICE_ID: str = os.getenv("ZAROON_VOICE_ID", "")
    ZAROON_TTS_MODEL: str = os.getenv("ZAROON_TTS_MODEL", "lightning_v3.1")
    ZAROON_TTS_LANGUAGE: str = os.getenv("ZAROON_TTS_LANGUAGE", "en")
    ZAROON_TTS_SPEED: float = float(os.getenv("ZAROON_TTS_SPEED", "1.0"))
    ZAROON_TTS_SAMPLE_RATE: int = int(os.getenv("ZAROON_TTS_SAMPLE_RATE", "24000"))
    ZAROON_TTS_FORMAT: str = os.getenv("ZAROON_TTS_FORMAT", "wav")

    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL") or os.getenv("NEXT_PUBLIC_SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY") or os.getenv("NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY") or os.getenv("SUPABASE_PUBLISHABLE_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    SUPABASE_DB_URL: str = os.getenv("SUPABASE_DB_URL", "")

    # Hugging Face
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY") or os.getenv("HF_TOKEN", "")
    HF_TOKEN: str = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_API_KEY", "")
    HF_MODEL_TINYLLAMA: str = os.getenv("HF_MODEL_TINYLLAMA", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    HF_MODEL_LLAMA: str = os.getenv("HF_MODEL_LLAMA", "meta-llama/Meta-Llama-3.1-8B-Instruct")
    HF_MODEL_GEMMA: str = os.getenv("HF_MODEL_GEMMA", "google/gemma-2-9b-it")
    HF_MODEL_QWEN: str = os.getenv("HF_MODEL_QWEN", "Qwen/Qwen2.5-7B-Instruct")
    HF_MODEL_QWEN_CODER: str = os.getenv("HF_MODEL_QWEN_CODER", "Qwen/Qwen2.5-Coder-7B-Instruct")
    HF_MODEL_MISTRAL: str = os.getenv("HF_MODEL_MISTRAL", "mistralai/Mistral-7B-Instruct-v0.3")
    HF_MODEL_PHI: str = os.getenv("HF_MODEL_PHI", "microsoft/Phi-3.5-mini-instruct")
    HF_MODEL_DEEPSEEK: str = os.getenv("HF_MODEL_DEEPSEEK", "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")
    HF_MODEL_EMBEDDING: str = os.getenv("HF_MODEL_EMBEDDING", "sentence-transformers/all-MiniLM-L6-v2")

    # Ollama
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL_TINYLLAMA: str = os.getenv("OLLAMA_MODEL_TINYLLAMA", "tinyllama")
    OLLAMA_MODEL_LLAMA: str = os.getenv("OLLAMA_MODEL_LLAMA", "llama3.2")
    OLLAMA_MODEL_GEMMA: str = os.getenv("OLLAMA_MODEL_GEMMA", "gemma2")
    OLLAMA_MODEL_QWEN: str = os.getenv("OLLAMA_MODEL_QWEN", "qwen2.5")
    OLLAMA_MODEL_QWEN_CODER: str = os.getenv("OLLAMA_MODEL_QWEN_CODER", "qwen2.5-coder")
    OLLAMA_MODEL_MISTRAL: str = os.getenv("OLLAMA_MODEL_MISTRAL", "mistral")
    OLLAMA_MODEL_PHI: str = os.getenv("OLLAMA_MODEL_PHI", "phi3.5")
    OLLAMA_MODEL_DEEPSEEK: str = os.getenv("OLLAMA_MODEL_DEEPSEEK", "deepseek-r1")
    OLLAMA_MODEL_EMBEDDING: str = os.getenv("OLLAMA_MODEL_EMBEDDING", "nomic-embed-text")

    # Clerk Authentication
    CLERK_PUBLISHABLE_KEY: str = os.getenv("CLERK_PUBLISHABLE_KEY") or os.getenv("NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY", "")
    CLERK_SECRET_KEY: str = os.getenv("CLERK_SECRET_KEY", "")
    CLERK_WEBHOOK_SECRET: str = os.getenv("CLERK_WEBHOOK_SECRET", "")
    CLERK_SIGN_IN_URL: str = os.getenv("NEXT_PUBLIC_CLERK_SIGN_IN_URL", "/sign-in")
    CLERK_SIGN_UP_URL: str = os.getenv("NEXT_PUBLIC_CLERK_SIGN_UP_URL", "/sign-up")

    # Interview System Configuration
    INTERVIEW_LLM_PROVIDER: str = os.getenv("INTERVIEW_LLM_PROVIDER", "openai")
    STT_PROVIDER: str = os.getenv("STT_PROVIDER", "assemblyai")
    TTS_PROVIDER: str = os.getenv("TTS_PROVIDER", "bolna")
    VISION_PROVIDER: str = os.getenv("VISION_PROVIDER", "browser")
    STORAGE_PROVIDER: str = os.getenv("STORAGE_PROVIDER", "supabase")
    
    # Interview Rules & Integrity Limits
    MAX_VIOLATIONS: int = int(os.getenv("MAX_VIOLATIONS", "15"))
    MAX_CAMERA_OFF_VIOLATIONS: int = int(os.getenv("MAX_CAMERA_OFF_VIOLATIONS", "4"))
    INTERVIEW_DURATION_MINUTES: int = int(os.getenv("INTERVIEW_DURATION_MINUTES", "30"))
    LIGHTING_MIN_LUX: int = int(os.getenv("LIGHTING_MIN_LUX", "45"))
    LIGHTING_MAX_LUX: int = int(os.getenv("LIGHTING_MAX_LUX", "230"))
    VIOLATION_CONFIRMATION_SECONDS: float = float(os.getenv("VIOLATION_CONFIRMATION_SECONDS", "1.5"))
    VIOLATION_DEBOUNCE_SECONDS: float = float(os.getenv("VIOLATION_DEBOUNCE_SECONDS", "2.5"))

    # Email Delivery Configuration
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY", "")
    SENDGRID_API_KEY: str = os.getenv("SENDGRID_API_KEY", "")
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM_EMAIL: str = os.getenv("SMTP_FROM_EMAIL", "support.zarvanai@gmail.com")
    APP_BASE_URL: str = os.getenv("APP_BASE_URL", "http://localhost:8000")
    ZAVRAN_LOGO_PATH: Path = BASE_DIR / "zevaro.png"

    # Configurable LLM Models
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    GOOGLE_MODEL: str = os.getenv("GOOGLE_MODEL", "gemini-1.5-flash")


settings = Settings()

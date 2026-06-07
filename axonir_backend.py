"""
🛸 AXONIR PRO - Backend FastAPI
100% Free AI IDE for Programming
Spark > Apex > Vórtex
Powered by Groq (FREE!)
"""

import os
import json
import asyncio
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import hashlib

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import uvicorn

# ═══════════════════════════════════════════════════════════════════════════
# MODELS & CONFIG
# ═══════════════════════════════════════════════════════════════════════════

class CodeRequest(BaseModel):
    code: str
    model: str  # spark, apex, vortex

class ChatRequest(BaseModel):
    question: str
    model: str
    context: Optional[str] = None

class CodeAnalysisRequest(BaseModel):
    code: str

class ChatResponse(BaseModel):
    success: bool
    response: str
    model: str
    timestamp: str
    tokens_used: int

class CodeResponse(BaseModel):
    success: bool
    output: str
    error: str
    execution_time: float
    model: str

# ═══════════════════════════════════════════════════════════════════════════
# GROQ API CONFIG
# ═══════════════════════════════════════════════════════════════════════════

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

MODELS_CONFIG = {
    "spark": {
        "groq_model": "mixtral-8x7b-32768",
        "name": "🔌 Spark",
        "system_prompt": """Você é um assistente de programação básico focado em ensinar conceitos fundamentais.
- Respostas diretas e didáticas
- Explique passo a passo
- Use exemplos simples
- Foco em aprendizado para iniciantes""",
        "temperature": 0.7,
        "max_tokens": 1024
    },
    "apex": {
        "groq_model": "llama-3.1-70b-versatile",
        "name": "⚡ Apex",
        "system_prompt": """Você é um desenvolvedor sênior assistente em programação.
- Análise profissional de código
- Design patterns e best practices
- Otimizações e performance
- Resolva problemas complexos com eficiência""",
        "temperature": 0.5,
        "max_tokens": 2048
    },
    "vortex": {
        "groq_model": "llama-3.1-405b-reasoning",
        "name": "🌀 Vórtex",
        "system_prompt": """Você é um EXPERT SUPREMO em desenvolvimento de software - OPUS 3.5 LEVEL.
- Arquitetura de sistemas escaláveis e distribuídos
- Problemas extremamente complexos e edge cases
- Otimizações de nível industrial e production
- Inovação, criatividade e soluções elegantes
- Você SUPERA especialistas humanos e Sonnet
- Análise profunda: segurança, performance, maintainability, escalabilidade
- Código production-ready SEMPRE
- Considere impacto, riscos e consequências de cada decisão""",
        "temperature": 0.3,
        "max_tokens": 4096
    }
}

# ═══════════════════════════════════════════════════════════════════════════
# SAFE CODE EXECUTOR (from axonir.py)
# ═══════════════════════════════════════════════════════════════════════════

import subprocess
import tempfile
import sys
import ast

class SafeCodeExecutor:
    """Executor seguro melhorado"""
    def __init__(self):
        self.allowed_imports = {
            'math', 'random', 're', 'json', 'datetime', 'collections',
            'numpy', 'sympy', 'pandas', 'matplotlib', 'statistics', 'itertools'
        }
        self.timeout = 12

    def validar_codigo(self, codigo: str) -> tuple[bool, str]:
        try:
            tree = ast.parse(codigo)
        except SyntaxError as e:
            return False, f"Erro de sintaxe: {e}"

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split('.')[0] not in self.allowed_imports:
                        return False, f"Import não permitido: {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.split('.')[0] not in self.allowed_imports:
                    return False, f"Import não permitido: {node.module}"
            
            if isinstance(node, ast.Name) and node.id in {'exec', 'eval', 'open', '__import__', 'subprocess', 'os', 'sys'}:
                return False, f"Operação perigosa: {node.id}"

        return True, "OK"

    def executar(self, codigo: str) -> Dict:
        valido, msg = self.validar_codigo(codigo)
        if not valido:
            return {
                "sucesso": False,
                "erro": msg,
                "saida": "",
                "tipo": "validation_error",
                "tempo": 0
            }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(codigo)
            temp_file = f.name

        inicio = time.time()
        try:
            resultado = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            tempo = time.time() - inicio
            return {
                "sucesso": resultado.returncode == 0,
                "saida": resultado.stdout.strip(),
                "erro": resultado.stderr.strip(),
                "tipo": "success" if resultado.returncode == 0 else "error",
                "tempo": tempo
            }
        except subprocess.TimeoutExpired:
            tempo = time.time() - inicio
            return {
                "sucesso": False,
                "erro": f"Timeout após {self.timeout}s",
                "tipo": "timeout",
                "tempo": tempo
            }
        except Exception as e:
            tempo = time.time() - inicio
            return {
                "sucesso": False,
                "erro": str(e),
                "tipo": "system_error",
                "tempo": tempo
            }
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

# ═══════════════════════════════════════════════════════════════════════════
# RATE LIMITING & CACHE
# ═══════════════════════════════════════════════════════════════════════════

class SimpleRateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)

    def is_allowed(self, user_id: str) -> bool:
        now = time.time()
        cutoff = now - self.window_seconds
        
        # Limpar requests antigos
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if req_time > cutoff
        ]
        
        if len(self.requests[user_id]) < self.max_requests:
            self.requests[user_id].append(now)
            return True
        return False

class SimpleCache:
    def __init__(self, ttl_seconds: int = 3600):
        self.cache = {}
        self.ttl = ttl_seconds

    def get(self, key: str) -> Optional[str]:
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None

    def set(self, key: str, value: str):
        self.cache[key] = (value, time.time())

    def make_key(self, model: str, question: str) -> str:
        return hashlib.md5(f"{model}:{question}".encode()).hexdigest()

# ═══════════════════════════════════════════════════════════════════════════
# FASTAPI APP
# ═══════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="🛸 AXONIR PRO",
    description="100% Free AI IDE for Programming",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instances
code_executor = SafeCodeExecutor()
rate_limiter = SimpleRateLimiter(max_requests=100, window_seconds=60)
cache = SimpleCache(ttl_seconds=3600)

# ═══════════════════════════════════════════════════════════════════════════
# TOGETHER AI INTEGRATION
# ═══════════════════════════════════════════════════════════════════════════

async def call_groq_api(model: str, messages: List[Dict], temperature: float, max_tokens: int) -> Dict:
    """Chama API Groq (100% FREE!)"""
    if not GROQ_API_KEY:
        return {
            "success": False,
            "error": "GROQ_API_KEY não configurada",
            "response": ""
        }

    model_config = MODELS_CONFIG[model]
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_config["groq_model"],
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": 0.9
    }

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                GROQ_API_URL,
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                # Groq retorna em formato OpenAI
                if "choices" in data and len(data["choices"]) > 0:
                    return {
                        "success": True,
                        "response": data["choices"][0]["message"]["content"],
                        "tokens": data.get("usage", {}).get("total_tokens", 0)
                    }
                else:
                    return {
                        "success": False,
                        "error": "Formato de resposta inesperado",
                        "response": ""
                    }
            else:
                error_text = response.text
                if response.status_code == 401:
                    error_text = "GROQ_API_KEY inválida ou expirada"
                elif response.status_code == 429:
                    error_text = "Rate limit exceeded - tente novamente em alguns segundos"
                return {
                    "success": False,
                    "error": f"Status {response.status_code}: {error_text}",
                    "response": ""
                }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "response": ""
        }

# ═══════════════════════════════════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════════════════════════════════

@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "🛸 AXONIR PRO Running",
        "version": "1.0.0",
        "models": list(MODELS_CONFIG.keys()),
        "features": ["Code Execution", "AI Chat", "Safe Sandbox", "Rate Limiting", "Caching"]
    }

@app.get("/models")
async def get_models():
    """Lista todos os modelos disponíveis"""
    return {
        model: {
            "name": config["name"],
            "system_prompt": config["system_prompt"][:100] + "...",
            "temperature": config["temperature"],
            "max_tokens": config["max_tokens"]
        }
        for model, config in MODELS_CONFIG.items()
    }

@app.post("/execute")
async def execute_code(request: CodeRequest):
    """Executa código Python de forma segura"""
    
    if not rate_limiter.is_allowed("code_execution"):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    start_time = time.time()
    
    result = code_executor.executar(request.code)
    
    execution_time = time.time() - start_time
    
    return CodeResponse(
        success=result["sucesso"],
        output=result["saida"],
        error=result["erro"],
        execution_time=execution_time,
        model=request.model
    )

@app.post("/chat")
async def chat(request: ChatRequest):
    """Chat com IA via Groq"""
    
    if not rate_limiter.is_allowed(f"chat_{request.model}"):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    # Verificar cache
    cache_key = cache.make_key(request.model, request.question)
    cached = cache.get(cache_key)
    if cached:
        return ChatResponse(
            success=True,
            response=cached,
            model=request.model,
            timestamp=datetime.now().isoformat(),
            tokens_used=0
        )
    
    # Construir mensagens
    model_config = MODELS_CONFIG[request.model]
    
    messages = [
        {
            "role": "system",
            "content": model_config["system_prompt"]
        }
    ]
    
    if request.context:
        messages.append({
            "role": "user",
            "content": f"Aqui está o código para contexto:\n\n```\n{request.context}\n```"
        })
    
    messages.append({
        "role": "user",
        "content": request.question
    })
    
    # Chamar Groq
    result = await call_groq_api(
        request.model,
        messages,
        model_config["temperature"],
        model_config["max_tokens"]
    )
    
    if result["success"]:
        # Cachear resposta
        cache.set(cache_key, result["response"])
        
        return ChatResponse(
            success=True,
            response=result["response"],
            model=request.model,
            timestamp=datetime.now().isoformat(),
            tokens_used=result.get("tokens", 0)
        )
    else:
        raise HTTPException(status_code=500, detail=result["error"])

@app.post("/analyze")
async def analyze_code(request: CodeAnalysisRequest):
    """Análise estática de código"""
    
    if not rate_limiter.is_allowed("code_analysis"):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    lines = request.code.split('\n')
    functions = len([l for l in lines if l.strip().startswith('def ')])
    classes = len([l for l in lines if l.strip().startswith('class ')])
    imports = len([l for l in lines if 'import' in l])
    
    return {
        "success": True,
        "analysis": {
            "lines": len(lines),
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "complexity": "high" if len(lines) > 100 else "medium" if len(lines) > 50 else "low"
        }
    }

@app.get("/stats")
async def get_stats():
    """Estatísticas do sistema"""
    return {
        "status": "operational",
        "cache_size": len(cache.cache),
        "rate_limiter_active": True,
        "safe_execution": True,
        "models_available": len(MODELS_CONFIG)
    }

# ═══════════════════════════════════════════════════════════════════════════
# STARTUP
# ═══════════════════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup_event():
    """Startup checks"""
    print("🛸 AXONIR PRO Backend iniciando...")
    print(f"✅ SafeCodeExecutor carregado")
    print(f"✅ Rate Limiter ativo")
    print(f"✅ Cache inicializado")
    
    if GROQ_API_KEY:
        print(f"✅ Groq API configurada (100% FREE!)")
    else:
        print(f"⚠️  GROQ_API_KEY não encontrada!")
        print(f"   1. Vai em: https://console.groq.com")
        print(f"   2. Pega sua API key")
        print(f"   3. Configure: export GROQ_API_KEY=sua_chave")
    
    print(f"✅ Modelos disponíveis:")
    for model_name, config in MODELS_CONFIG.items():
        print(f"   {config['name']} → {config['groq_model']}")
    
    print("🚀 Server ready!")

if __name__ == "__main__":
    uvicorn.run(
        "axonir_backend:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

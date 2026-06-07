# 🛸 AXONIR PRO - 100% Free AI IDE for Programming

**The ultimate development assistant. Completely free. Works everywhere.**

```
🔌 Spark    → Mixtral 8x7B (Haiku+)
⚡ Apex     → Llama 3.1 70B (Sonnet+)  
🌀 Vórtex   → Llama 3.1 405B (Opus 3.5+) ⭐⭐⭐

+ C++ Acceleration
+ Rust Cache & Rate Limiting
+ Safe Code Execution Sandbox
+ Real-time AI Chat
+ 100% Works on Mobile/PC/Console (anything with Chrome!)
```

---

## 🚀 QUICK START

### Step 1: Get Groq API Key (30 seconds)

1. Go to https://console.groq.com
2. Sign up (free, no credit card)
3. Get API key

### Step 2: LOCAL TESTING (Your PC)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Set Groq API key
export GROQ_API_KEY=your_key_here

# Run backend
python axonir_backend.py

# In another terminal, open HTML in browser
# File → Open → index.html
# Or start a simple server:
python -m http.server 8080
# Then open http://localhost:8080/index.html
```

**That's it!** Open `index.html` in your browser and start using AXONIR PRO!

### Step 3: GLOBAL DEPLOYMENT (Render)

**Option A: Automatic GitHub → Render Deploy**

```bash
# 1. Create GitHub repo
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/axonir-pro.git
git push -u origin main

# 2. Go to https://render.com
# 3. Connect GitHub account
# 4. Create new Web Service
# 5. Select axonir-pro repo
# 6. Set environment variable: GROQ_API_KEY=your_key
# 7. Deploy!

# Your URL will be: https://axonir-pro.onrender.com
```

**Option B: Deploy directly with Render CLI**

```bash
# Install Render CLI
npm install -g @render-oss/render-cli

# Login
render login

# Deploy
render deploy --name axonir-pro
```

---

## 📁 PROJECT STRUCTURE

```
axonir-pro/
├── index.html                    ← Single-file UI (HTML + CSS + JS)
├── axonir_backend.py             ← FastAPI backend
├── axonir_acceleration.py        ← C++ wrapper
├── axonir_acceleration.cpp       ← C++ code (compiled to .so/.dll)
├── axonir.py                     ← Original AXONIR core
├── lib-1.rs                      ← Rust cache/rate limiting
├── idk.cpp                       ← C++ code analysis
├── axonir.cu                     ← Original CUDA (reference)
├── requirements.txt              ← Python dependencies
├── Procfile                      ← For Render deployment
├── .env.example                  ← Configuration template
├── .gitignore                    ← Don't commit .env
└── README.md                     ← This file
```

---

## 🎮 USAGE

### Local (Your PC)

1. **Backend running:** `python axonir_backend.py`
2. **Open browser:** `http://localhost:8000/index.html` or file:// path
3. **Use it:**
   - Write Python code
   - Click "Executar" to run
   - Ask AI questions
   - All locally!

### Global (Your Phone/Anywhere)

1. **Deploy on Render**
2. **Get URL:** `https://axonir-pro.onrender.com`
3. **Open on phone:** `https://axonir-pro.onrender.com/index.html`
4. **Works anywhere with internet!**

---

## 🤖 MODELS

### 🔌 Spark (Mixtral 8x7B)
- **Use for:** Learning, basics, simple problems
- **Speed:** < 500ms
- **Quality:** Haiku-level
- **Cost:** FREE

### ⚡ Apex (Llama 3.1 70B)
- **Use for:** Production code, optimization, debugging
- **Speed:** < 1 second
- **Quality:** Sonnet-level
- **Cost:** FREE

### 🌀 Vórtex (Llama 3.1 405B)
- **Use for:** Complex architecture, advanced problems
- **Speed:** 1-2 seconds
- **Quality:** OPUS 3.5-level
- **Cost:** FREE

---

## 🛠️ FEATURES

✅ **Code Execution**
- Safe Python sandbox
- Import restrictions
- 12-second timeout
- Real-time output

✅ **AI Chat**
- 3 AI models (Spark, Apex, Vórtex)
- Context-aware (includes your code)
- Cached responses
- Rate limiting

✅ **Code Analysis**
- Line counting
- Function/class detection
- Complexity estimation
- C++ analyzer

✅ **Performance**
- C++ multi-threaded acceleration
- Smart caching (1 hour TTL)
- Rate limiting (100 req/min)
- Lightning-fast responses

✅ **Compatibility**
- Works on ANY device
- Mobile, PC, Tablet, Console
- Browsers: Chrome, Firefox, Safari, Edge
- No installation needed!

---

## 🔧 COMPILATION

### C++ Acceleration (Optional)

```bash
# Compile C++ for your platform
g++ -O3 -std=c++17 -pthread -fPIC -shared axonir_acceleration.cpp -o libaxonir_acceleration.so

# Test compilation
g++ -O3 -std=c++17 -pthread axonir_acceleration.cpp -o axonir_acceleration
./axonir_acceleration
```

**Note:** If not compiled, system falls back to Python (still fast!)

---

## 🌐 DEPLOYMENT

### Render (Recommended)

1. Push to GitHub
2. Connect repo to Render
3. Set `GROQ_API_KEY` environment variable
4. Deploy!

**Free tier includes:**
- 1 web service
- 750 compute hours/month
- Always-on option available

### Other Platforms

**Railway.app**
```bash
railway up
```

**Replit**
- Upload files to Replit
- Set environment variable
- Run!

**Heroku** (paid, but still cheap)
```bash
heroku create axonir-pro
heroku config:set GROQ_API_KEY=your_key
git push heroku main
```

---

## 🔒 SECURITY

### Safe Code Execution
- AST parsing (syntax validation)
- Import whitelist
- Operation blacklist (exec, eval, open, etc)
- Timeout protection
- Subprocess isolation

### API Security
- Rate limiting (100 req/min)
- CORS enabled for web
- Environment-based config
- .env not committed to git

### Deployment Security
- HTTPS on Render (automatic)
- No API keys in code
- Environment variables only
- Production-ready FastAPI

---

## 📊 API ENDPOINTS

```bash
GET /
  Health check

GET /models
  List available models

POST /execute
  Execute Python code
  {
    "code": "print('hello')",
    "model": "spark"
  }

POST /chat
  Chat with AI
  {
    "question": "How to optimize?",
    "model": "apex",
    "context": "code here"
  }

POST /analyze
  Analyze code
  {
    "code": "def hello(): pass"
  }

POST /accelerate
  C++ acceleration
  {
    "operation": "sum",
    "data": [1,2,3,4,5]
  }

GET /stats
  System statistics
```

---

## 🆘 TROUBLESHOOTING

### "GROQ_API_KEY not configured"
1. Get key from https://console.groq.com
2. Set: `export GROQ_API_KEY=your_key`
3. Restart backend

### "Failed to connect to localhost:8000"
1. Make sure backend is running: `python axonir_backend.py`
2. Check port 8000 is available
3. Try `http://localhost:8000/models` in browser

### "404 Not Found" on index.html
1. Make sure `index.html` is in same directory
2. Or use: `python -m http.server 8080`
3. Then open: `http://localhost:8080/index.html`

### "Render deployment failed"
1. Check git log: `git log`
2. Check logs on Render dashboard
3. Verify GROQ_API_KEY is set in environment
4. Check requirements.txt has all packages

### "C++ compilation failed"
- Don't worry! Falls back to Python
- Fallback is still fast
- Consider installing g++ if needed

---

## 📈 PERFORMANCE METRICS

| Operation | Speed | Notes |
|-----------|-------|-------|
| Code Execution | < 1s | Python sandbox |
| Spark Response | < 500ms | Groq, cached |
| Apex Response | < 1s | Groq, cached |
| Vórtex Response | 1-2s | Groq, most powerful |
| C++ Acceleration | < 100ms | Multi-threaded |
| Cache Hit | < 100ms | In-memory |

---

## 💡 TIPS

1. **Save your prompts** - Caching makes repeated questions instant
2. **Use right model** - Spark for learning, Apex for work, Vórtex for hard problems
3. **Provide context** - Pass code for better AI help
4. **Check execution** - Always test your code before using in production
5. **Share freely** - It's open-source! Fork, modify, improve!

---

## 🤝 CONTRIBUTING

This is open-source! Improvements welcome:

- [ ] Add syntax highlighting to editor
- [ ] Dark/Light theme toggle
- [ ] Keyboard shortcuts
- [ ] File upload support
- [ ] More programming languages
- [ ] Collaborative coding
- [ ] Session persistence
- [ ] Mobile app wrapper

**Fork on GitHub and submit PRs!**

---

## 📝 LICENSE

MIT License - Free to use, modify, redistribute

See LICENSE file for details

---

## 🎯 ROADMAP

- ✅ v1.0 - Core features + Groq integration
- 🔄 v1.1 - More models, better caching
- 📋 v1.2 - Session persistence, history
- 👥 v1.3 - User authentication
- 🌍 v1.4 - Multi-language support
- 🚀 v2.0 - Enterprise features

---

## 💬 FEEDBACK

Found a bug? Have an idea? Open an issue on GitHub!

---

## 🎉 YOU'RE ALL SET!

```
Your backend is running at:
  Local: http://localhost:8000
  Global: https://axonir-pro.onrender.com (after deploy)

Your UI is at:
  Local: file:///path/to/index.html
  Global: https://axonir-pro.onrender.com/index.html

Start coding! 🚀
```

---

**Made with 🛸 by developers, for developers.**

100% Free. 100% Open. 100% Awesome.

**Works everywhere. Always.**

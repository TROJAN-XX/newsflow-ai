# NewsFlow AI

**AI-powered daily news intelligence platform.**

NewsFlow AI collects news from 20+ global RSS sources, removes duplicates, generates AI summaries using OpenAI, and presents everything through a stunning dark-mode web interface.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Multi-source RSS Collection** | 20+ feeds across 7 categories (world, tech, business, science, health, sports, entertainment) |
| **Smart Deduplication** | URL-based exact dedup + title similarity clustering |
| **AI Summarization** | OpenAI-powered summaries, key points, keywords, and importance scoring |
| **Daily Digest** | AI-generated editorial digest with top stories and category overviews |
| **Premium Dark UI** | Glassmorphism design with gradients, animations, and responsive layout |
| **Search & Filter** | Real-time search by title, keyword, or source with category filtering |
| **Archive Browser** | Browse past editions with calendar navigation |
| **GitHub Actions** | Automated twice-daily pipeline + GitHub Pages deployment |

---

## 🏗️ Architecture

```
newsflow-ai/
├── backend/                    # Python news pipeline
│   ├── collector/
│   │   └── rss.py              # RSS feed collector (20+ sources)
│   ├── ai/
│   │   ├── summarizer.py       # OpenAI article summarizer
│   │   ├── processor.py        # Batch AI processing
│   │   └── digest.py           # Daily digest generator
│   ├── storage/
│   │   └── archive.py          # JSON archive management
│   ├── utils/
│   │   ├── config.py           # Centralized configuration
│   │   └── deduplicate.py      # Deduplication engine
│   └── main.py                 # Pipeline orchestrator
│
├── website/                    # React frontend
│   ├── public/
│   │   └── data/               # Synced archive data
│   └── src/
│       ├── components/         # UI components
│       │   ├── Header.js
│       │   ├── NewsCard.js
│       │   ├── DigestCard.js
│       │   ├── CategoryBar.js
│       │   ├── DateSelector.js
│       │   └── SearchBar.js
│       ├── App.js              # Main application
│       └── index.css           # Design system
│
├── data/                       # Generated archive
│   └── news_archive.json
│
├── .github/workflows/
│   ├── newsflow.yml            # Scheduled pipeline
│   └── deploy.yml              # GitHub Pages deployment
│
├── sync_archive.py             # Archive → website sync
├── requirements.txt            # Python dependencies
└── .env.example                # Environment template
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **OpenAI API Key**

### 1. Clone & Setup

```bash
git clone https://github.com/TROJAN-XX/newsflow-ai.git
cd newsflow-ai

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 3. Run the Pipeline

```bash
python -m backend.main
```

This will:
1. Collect articles from 20+ RSS feeds
2. Remove duplicates
3. Generate AI summaries via OpenAI
4. Create a daily digest
5. Save everything to `data/news_archive.json`

### 4. Start the Website

```bash
# Sync archive to website
python sync_archive.py

# Install frontend dependencies
cd website
npm install

# Start dev server
npm start
```

Open **http://localhost:3000** to view the app.

---

## ⚙️ Configuration

All settings are configured via environment variables (see `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | — | **Required.** Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-5.6-luna` | OpenAI model to use |
| `MAX_ARTICLES_PER_RUN` | `20` | Max articles to AI-process per run |
| `SIMILARITY_THRESHOLD` | `0.82` | Title similarity threshold for clustering |
| `REQUEST_TIMEOUT` | `15` | HTTP request timeout in seconds |
| `MAX_RETRIES` | `2` | Max retries for failed RSS feeds |

---

## 🔄 GitHub Actions

### Automated Pipeline (`newsflow.yml`)

Runs twice daily (06:00 and 18:00 UTC):
- Collects fresh news
- Processes with AI
- Commits updated archive
- Triggers website deployment

**Required secret:** `OPENAI_API_KEY`

### Website Deployment (`deploy.yml`)

Auto-deploys to GitHub Pages when:
- Website files change on `main`
- Pipeline workflow completes
- Manually triggered

---

## 📰 News Sources

| Category | Sources |
|----------|---------|
| World | BBC News, DW, Al Jazeera, Reuters |
| Technology | BBC Tech, TechCrunch, Ars Technica, The Verge |
| Business | BBC Business, CNBC |
| Science | BBC Science, Phys.org, Space.com |
| Health | BBC Health, Medical News Today |
| Sports | BBC Sport, ESPN |
| Entertainment | BBC Entertainment |

---

## 🛠️ Tech Stack

- **Backend:** Python, feedparser, OpenAI SDK
- **Frontend:** React 18, Vanilla CSS
- **AI:** OpenAI GPT (structured JSON output)
- **CI/CD:** GitHub Actions
- **Hosting:** GitHub Pages

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

Built with ❤️ and AI by [TROJAN-XX](https://github.com/TROJAN-XX)

# ArcanaBase 🔮

A modern, production-ready RAG (Retrieval-Augmented Generation) knowledge base with a NotebookLM-inspired interface. Built with FastAPI, React, TypeScript, and powered by sentence transformers and FAISS for fast semantic search.

## ✨ Features

- **📄 Multi-format Document Ingestion**: PDF, TXT, MD files and web URLs
- **🔍 Semantic Search**: Powered by sentence transformers and FAISS vector indexing
- **🤖 AI-Powered Answers**: Optional Google Gemini integration for intelligent responses
- **💻 Modern UI**: Clean, responsive React interface with TypeScript
- **⚡ Fast Backend**: FastAPI with async support and automatic API documentation
- **🐍 Conda Ready**: Easy environment management with conda
- **🔧 Flexible Configuration**: Environment-based configuration with sensible defaults

## 🏗️ Project Structure

```
ArcanaBase/
├── backend/                    # FastAPI backend
│   ├── app.py                 # Main FastAPI application
│   ├── rag.py                 # RAG implementation with vector search
│   ├── ingest.py              # Document ingestion pipeline
│   ├── loader.py              # File format loaders
│   ├── models.py              # Pydantic data models
│   ├── requirements.txt       # pip dependencies
│   ├── environment.yml        # conda environment
│   ├── env.example           # environment configuration template
│   └── storage/              # auto-created data directory
│       ├── index.faiss       # FAISS vector index
│       ├── chunks.jsonl      # document chunks
│       └── sources.json      # source registry
└── frontend/                  # React TypeScript frontend
    ├── src/
    │   ├── App.tsx           # main application
    │   ├── components/       # React components
    │   │   ├── ChatPanel.tsx
    │   │   ├── SourceList.tsx
    │   │   ├── UploadPanel.tsx
    │   │   └── Headers.tsx
    │   ├── lib/
    │   │   └── api.ts        # API client
    │   └── types.ts          # TypeScript definitions
    ├── package.json
    ├── vite.config.ts
    └── tailwind.config.js
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+ (with conda recommended)
- Node.js 18+ and npm
- Git

### Backend Setup

1. **Create and activate conda environment:**
   ```bash
   cd backend
   conda env create -f environment.yml
   conda activate vec
   ```

   *Alternative with pip:*
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` to customize settings:
   ```env
   # Optional: Use Google Gemini for AI responses
   USE_GEMINI=true
   GEMINI_API_KEY=your_api_key_here
   
   # Optional: Customize storage location
   STORAGE_DIR=./storage
   
   # Optional: Use different embedding model
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   ```

3. **Start the backend server:**
   ```bash
   uvicorn app:app --reload --port 8000
   ```

   API documentation will be available at: http://localhost:8000/docs

### Frontend Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

   Frontend will be available at: http://localhost:5173

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `STORAGE_DIR` | `./storage` | Directory for storing FAISS index and chunks |
| `EMBEDDING_MODEL` | `sentence-transformers/all-MiniLM-L6-v2` | Sentence transformer model for embeddings |
| `USE_GEMINI` | `false` | Enable Google Gemini for answer synthesis |
| `GEMINI_API_KEY` | - | Google Gemini API key (required if `USE_GEMINI=true`) |

### Getting a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file as `GEMINI_API_KEY`

## 📡 API Reference

### Core Endpoints

- **GET** `/health` - Health check
- **GET** `/sources` - List all ingested sources
- **POST** `/ingest/file` - Upload and ingest a file
- **POST** `/ingest/url` - Ingest content from a URL
- **POST** `/query` - Query the knowledge base

### Query API Example

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is machine learning?",
    "top_k": 5,
    "llm": "gemini",
    "persona": "teacher"
  }'
```

**Query Parameters:**
- `question` (required): The question to ask
- `top_k` (optional, default: 5): Number of relevant chunks to retrieve
- `llm` (optional): Use "gemini" for AI-powered responses
- `persona` (optional): Response style (e.g., "teacher", "diviner")

## 🛠️ Development

### Backend Development

```bash
# Run with hot reload
uvicorn app:app --reload --port 8000

# Run tests (if you add them)
pytest

# Format code
black .
isort .
```

### Frontend Development

```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npm run type-check
```

### Adding New File Types

To support additional file formats, extend the `SUPPORTED_EXT` dictionary in `ingest.py` and add corresponding loaders in `loader.py`.

## 🐳 Production Deployment

### Using Docker (recommended)

*Docker configuration coming soon...*

### Manual Deployment

1. **Backend:**
   ```bash
   # Install production dependencies
   pip install gunicorn
   
   # Run with gunicorn
   gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

2. **Frontend:**
   ```bash
   # Build for production
   npm run build
   
   # Serve with nginx, apache, or any static file server
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**Import errors with sentence_transformers:**
```bash
# Make sure you're in the correct conda environment
conda activate vec
```

**FAISS installation issues:**
```bash
# Use conda for easier FAISS installation
conda install -c conda-forge faiss-cpu
```

**Frontend build errors:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Permission errors with storage directory:**
```bash
# Make sure the storage directory is writable
chmod 755 backend/storage
```

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the excellent Python web framework
- [Sentence Transformers](https://www.sbert.net/) for semantic embeddings
- [FAISS](https://faiss.ai/) for efficient similarity search
- [React](https://reactjs.org/) and [TypeScript](https://www.typescriptlang.org/) for the frontend
- [Tailwind CSS](https://tailwindcss.com/) for styling

---

**Happy knowledge building! 🚀**
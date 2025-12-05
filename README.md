# 📚 Scientific Article Summarizer

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-green.svg)](https://flask.palletsprojects.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.4.0-red.svg)](https://pytorch.org/)
[![Transformers](https://img.shields.io/badge/🤗_Transformers-4.43.3-yellow.svg)](https://huggingface.co/transformers/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

> An intelligent text summarization system leveraging fine-tuned BART transformers for generating high-quality abstractive summaries of scientific articles.

## 🌟 Overview

This project implements a state-of-the-art **abstractive text summarization** system specifically designed for scientific papers. Built upon the BART (Bidirectional and Auto-Regressive Transformers) architecture, the system is capable of generating coherent, concise summaries that capture the essential information from lengthy academic texts.

### Key Features

- 🤖 **Fine-tuned BART Model**: Leverages `facebook/bart-large` fine-tuned on scientific article datasets
- 🌐 **RESTful API**: Production-ready Flask API with Swagger documentation
- 📄 **Multi-format Support**: Process both plain text and files (PDF, TXT)
- 🔄 **Customizable Summary Length**: Control minimum and maximum summary sizes
- ⭐ **Quality Rating System**: Rate and track summary quality
- 🐳 **Docker Support**: Containerized deployment for easy scaling
- 💾 **Persistent Storage**: SQLite database for managing summaries and metadata

## 🏗️ Architecture

The project consists of two main components:

### 1. Model Training Pipeline (`Model/`)
Fine-tunes the BART transformer model on scientific article datasets, extracting abstract-body pairs from XML-formatted research papers.

### 2. REST API Service (`API/`)
Provides HTTP endpoints for text summarization, file processing, and summary management.
```
┌─────────────────┐
│   User Input    │
│  (Text/File)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Flask API     │
│  (Processing)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  BART Model     │
│ (Summarization) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  SQLite DB      │
│  (Storage)      │
└─────────────────┘
```

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- CUDA-compatible GPU (recommended for model training)
- Docker & Docker Compose (for containerized deployment)

### Installation

#### Option 1: Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/scientific-summarizer.git
cd scientific-summarizer
```

2. **Set up the Model environment**
```bash
cd Model
pip install -r requirements.txt
```

3. **Set up the API environment**
```bash
cd ../API
pip install -r requirements.txt
```

#### Option 2: Docker Deployment
```bash
cd API
docker-compose up -d
```

The API will be available at `http://localhost:5000`

## 🎯 Usage

### Training the Model

1. **Prepare your dataset**
   - Place XML-formatted scientific articles in `Model/article_data/`
   - The XML files should contain `<abstract>` and `<body>` sections

2. **Extract and clean data**
```bash
cd Model
python Cleaning_data_json.py
```

3. **Fine-tune the model**
```bash
python fine_tune.py
```

The training process will:
- Load the pre-trained BART model
- Process your scientific article dataset
- Fine-tune on abstract-body pairs
- Save the model to `./results/model/`
- Generate training logs in `training.log`

### Using the API

#### 1. Process Text

**Endpoint:** `POST /process_text`
```bash
curl -X POST http://localhost:5000/process_text \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Your long scientific text here...",
    "minsize": 50,
    "maxsize": 150
  }'
```

**Response:**
```json
{
  "id": "d290f1ee-6c54-4b01-90e6-d701748f0851"
}
```

#### 2. Process File

**Endpoint:** `POST /process_file`
```bash
curl -X POST http://localhost:5000/process_file \
  -F "file=@article.pdf" \
  -F "minsize=50" \
  -F "maxsize=150"
```

#### 3. Get Summary

**Endpoint:** `GET /get_summary/<id>`
```bash
curl http://localhost:5000/get_summary/d290f1ee-6c54-4b01-90e6-d701748f0851
```

**Response:**
```json
{
  "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
  "original_text": "Original long text...",
  "summarized": "Concise summary...",
  "score": null,
  "minsize": 50,
  "maxsize": 150,
  "created_date": "2024-12-05T10:30:00"
}
```

#### 4. Rate Summary

**Endpoint:** `PUT /rate_summary/<id>`
```bash
curl -X PUT http://localhost:5000/rate_summary/d290f1ee-6c54-4b01-90e6-d701748f0851 \
  -H "Content-Type: application/json" \
  -d '{"score": 8.5}'
```

### API Documentation

Visit `http://localhost:5000/apidocs/` for interactive Swagger documentation.

## 📊 Model Details

### BART Architecture

BART (Bidirectional and Auto-Regressive Transformers) combines:
- **Bidirectional encoding** (like BERT) for understanding context
- **Auto-regressive decoding** (like GPT) for generating text

### Training Configuration
```python
learning_rate = 2e-5
batch_size = 4
epochs = 3
max_input_length = 1024
max_output_length = 150
optimizer = AdamW
```

### Dataset Format

The model expects JSON data with the following structure:
```json
[
  {
    "Abstract": "Brief summary of the paper...",
    "Body": "Full text of the research article..."
  }
]
```

## 📁 Project Structure
```
scientific-summarizer/
├── API/
│   ├── app.py                 # Flask application
│   ├── Dockerfile             # Container configuration
│   ├── docker-compose.yml     # Docker Compose setup
│   ├── requirements.txt       # Python dependencies
│   ├── uploads/               # Uploaded files storage
│   └── instance/              # SQLite database
│
├── Model/
│   ├── fine_tune.py           # Model training script
│   ├── Cleaning_data.py       # CSV data extraction
│   ├── Cleaning_data_json.py  # JSON data extraction
│   ├── requirements.txt       # Python dependencies
│   ├── article_data/          # Raw XML articles
│   ├── results/               # Trained models
│   └── logs/                  # Training logs
│
└── README.md
```

## 🔧 Configuration

### Environment Variables
```bash
# Flask
FLASK_ENV=production
DATABASE_URL=sqlite:///instance/app.db

# Model Training
CUDA_VISIBLE_DEVICES=0  # GPU selection
```

### Database Schema
```sql
CREATE TABLE summary_model (
    id TEXT PRIMARY KEY,
    original_text TEXT NOT NULL,
    is_file BOOLEAN NOT NULL,
    file_path TEXT,
    summarized TEXT,
    score FLOAT,
    created_date DATETIME NOT NULL,
    minsize INTEGER NOT NULL,
    maxsize INTEGER NOT NULL
);
```

## 📈 Performance

The model achieves:
- **ROUGE-L Score**: Competitive with state-of-the-art abstractive summarization
- **Inference Time**: ~2-5 seconds per document (GPU)
- **Quality**: Human-readable, coherent summaries preserving key information

## 🛠️ Development

### Running Tests
```bash
# API tests
cd API
python -m pytest tests/

# Model evaluation
cd Model
python evaluate.py
```

### Code Quality
```bash
# Format code
black .

# Lint
flake8 .

# Type checking
mypy .
```

## 📚 References

1. Lewis et al. (2019). "BART: Denoising Sequence-to-Sequence Pre-training for Natural Language Generation, Translation, and Comprehension"
2. Devlin et al. (2018). "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"
3. Vaswani et al. (2017). "Attention Is All You Need"

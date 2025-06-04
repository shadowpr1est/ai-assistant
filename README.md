# Study Assistant Lab

An AI-powered study assistant that uses OpenAI's API to help you learn from PDF materials. The assistant can answer questions about the uploaded documents using advanced language models.

## Prerequisites

- Python 3.x
- OpenAI API key
- PDF documents you want to study

## Setup

1. Clone this repository:
```bash
git clone <repository-url>
cd study-assistant-lab
```

2. Create a `.env` file in the root directory with your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

3. Install the required packages:
```bash
pip install python-dotenv openai pydantic
```

## Project Structure

```
study-assistant-lab/
├── data/                  # Directory for PDF documents
├── scripts/
│   ├── 00_bootstrap.py   # Initial setup script
│   └── 01_qna_assistant.py # Q&A interaction script
├── .env                  # Environment variables
└── assistant_info.json   # Assistant configuration
```

## Usage

1. Place your PDF document in the `data/` directory.

2. Run the bootstrap script to set up the assistant:
```bash
python scripts/00_bootstrap.py
```
This will:
- Upload your PDF file to OpenAI
- Create a vector store
- Set up an AI assistant
- Save the configuration in `assistant_info.json`

3. Start the Q&A session:
```bash
python scripts/01_qna_assistant.py
```

4. Ask questions about your document! Type 'exit' or 'quit' to end the session.

## Features

- PDF document analysis
- Interactive Q&A session
- Context-aware responses
- Citation of sources when possible
- Clean terminal interface

## Configuration

The `assistant_info.json` file contains important configuration details:
- `assistant_id`: OpenAI assistant identifier
- `vector_store_id`: Vector store for document embeddings
- `file_id`: Uploaded file identifier
- `pdf_path`: Local path to the PDF file

## Troubleshooting

If you encounter issues:
1. Ensure your OpenAI API key is valid and properly set in `.env`
2. Check that the PDF file exists in the specified location
3. Verify that `assistant_info.json` contains valid configuration
4. Make sure all required packages are installed


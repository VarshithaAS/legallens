# LegalLens

LegalLens is a web application that extracts and analyses text from legal documents such as PDF, DOCX, and TXT files. It helps users quickly understand a document by extracting its text, generating summaries, identifying keywords and clauses, and highlighting possible risks.

## Live Demo

**Live Application:** [https://legallens-0xrs.onrender.com/](https://legallens-0xrs.onrender.com/)

**GitHub Repository:** [https://github.com/VarshithaAS/-legallens](https://github.com/VarshithaAS/-legallens)

## Features

- Upload PDF, DOCX, and TXT documents
- Extract text from uploaded documents
- Generate document summaries
- Identify keywords and important clauses
- Highlight possible risks in legal documents
- Generate downloadable reports
- Simple web interface for document analysis

## Technologies Used

- Python
- Flask
- Gunicorn
- HTML, CSS, and JavaScript
- `python-docx`
- PDF text-extraction libraries
- Render for cloud deployment

## Supported File Types

| File Type | Extension |
|---|---|
| PDF document | `.pdf` |
| Microsoft Word document | `.docx` |
| Plain text document | `.txt` |

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/VarshithaAS/-legallens.git
```

### 2. Open the project folder

```bash
cd ./-legallens/legal-document-extractive-summariser-main```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

### 5. Open the local application

Open the local URL displayed in the terminal, commonly:

```text
http://127.0.0.1:5000/
```

## Deployment

This application is deployed as a Python web service on Render.

**Live Application URL:** [https://legallens-0xrs.onrender.com/](https://legallens-0xrs.onrender.com/)

The production server runs using:

```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

## Project Structure

```text
legal-document-extractive-summariser-main/
│
├── app.py
├── requirements.txt
├── render.yaml
├── summarizer/
├── templates/
├── static/
├── uploads/
├── reports/
└── history/
```

## Important Notes

- Use sample, dummy, or redacted documents for testing and demonstrations.
- Do not upload confidential, private, or sensitive legal documents.
- The deployed app uses Render’s Free plan, so it may take up to about a minute to open after inactivity.
- Uploaded files, generated reports, and history may be removed after a restart or redeployment because the free deployment does not use persistent storage.

## Author

VarshithaAS

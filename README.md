# Multi-AI Agent Architecture System for Market Reasearch

This is a Flask-based web application that generates AI and Generative AI use cases for a given company or industry based on its website URL. It also provides insights into potential AI/ML solutions, datasets, and resources.

---

## Features

- Accepts a company URL as input.
- Analyzes the company's industry, market segment, and offerings.
- Proposes actionable AI/ML use cases tailored to the company's focus areas.
- Displays results in a clean and responsive UI.
- Easy to use and deploy locally.

---

## Prerequisites

Before running this application, ensure you have the following installed on your system:

1. **Python 3.8 or later**
2. **pip** (Python package manager)

---

## Installation

Follow the steps below to set up and run the application:

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/ai-use-case-generator.git
```

### 2. Set Up a Virtual Environment

It is recommended to use a virtual environment to avoid dependency conflicts.

```bash
python -m venv venv
source venv/bin/activate       # For Linux/Mac
venv\Scripts\activate          # For Windows
```

### 3. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add the following environment variables:

```plaintext
OPENAI_API_KEY=your_openai_api_key_here
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

---

## Usage

### 1. Start the Flask Application

Run the following command to start the application:

```bash
python app.py
```

### 2. Open in Browser

Visit the application in your browser at:

```
http://127.0.0.1:5000/
```

### 3. Input the Company URL

- Enter the company's website URL in the input field.
- Click **Submit** to generate AI use cases and view the results.

---

import os
from flask import Flask, render_template, request
from crewai import Agent, Task, Crew
from crewai_tools import (
    WebsiteSearchTool,
    ScrapeWebsiteTool
)
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"

# Define Agents
researcher = Agent(
    role="Industry/Company Researcher",
    goal="Analyze the company's industry and segment, identifying key offerings and focus areas.",
    backstory="Research the company's website and industry-specific sources to gather insights.",
    allow_delegation=False,
    verbose=True
)

use_case_generator = Agent(
    role="Market Standards & Use Case Generator",
    goal="Propose AI/ML and Generative AI use cases for the company.",
    backstory="Analyze market trends and propose actionable AI use cases for the company.",
    allow_delegation=False,
    verbose=True
)

resource_collector = Agent(
    role="Resource Asset Collector",
    goal="Curate resources and datasets for proposed AI/ML use cases.",
    backstory="Collect relevant datasets, pre-trained models, and papers for implementation.",
    allow_delegation=False,
    verbose=True
)

proposal_finalizer = Agent(
    role="Proposal Finalizer",
    goal="Deliver a professional proposal with prioritized use cases and supporting resources.",
    backstory="Compile and refine outputs from all agents into a clear, actionable proposal.",
    allow_delegation=False,
    verbose=True
)

# Define Tasks
research_task = Task(
    description="Analyze the company's industry, products, and strategic focus areas.",
    expected_output="Company profile and industry insights document.",
    tools=[WebsiteSearchTool(), ScrapeWebsiteTool()],
    agent=researcher
)

use_case_task = Task(
    description="Propose relevant AI/ML use cases based on industry trends and standards.",
    expected_output="A list of AI/ML use cases for the company.",
    agent=use_case_generator
)

resource_task = Task(
    description="Collect datasets and resources for implementing the proposed use cases.",
    expected_output="A curated list of resources and datasets for the use cases.",
    tools=[WebsiteSearchTool()],
    agent=resource_collector
)

proposal_task = Task(
    description="Compile and prioritize the most impactful AI/ML use cases into a polished proposal.",
    expected_output="A professional proposal document with use cases and references.",
    agent=proposal_finalizer
)

# Crew Definition
crew = Crew(
    agents=[researcher, use_case_generator, resource_collector, proposal_finalizer],
    tasks=[research_task, use_case_task, resource_task, proposal_task],
    verbose=2
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get URL from form input
        company_url = request.form.get('url')

        # Execute multi-agent system
        result = crew.kickoff(inputs={"url": company_url})
    #     result = """

    # Company Profile
    # - Industry: Healthcare and Technology
    # - Market Segment: Healthcare services, insurance, and technology solutions
    # - Key Offerings: Claims management, clinical insights, healthcare data analytics, and customer engagement platforms.
    # - Strategic Focus: Enhancing healthcare operations, improving patient outcomes, and delivering cost-efficient solutions.

    # AI/ML Use Cases
    # 1. Predictive Analytics for Patient Health:
    #    - Use ML to predict patient risks for chronic diseases and provide preventative care recommendations.
    # 2. AI-Powered Claims Processing:
    #    - Automate insurance claims validation and fraud detection using Natural Language Processing (NLP).
    # 3. Personalized Patient Engagement:
    #    - Leverage Generative AI chatbots for real-time patient queries, appointment scheduling, and follow-ups.
    # 4. Healthcare Data Analytics:
    #    - Use LLMs to analyze unstructured clinical notes and generate actionable insights.
    # 5. Clinical Decision Support:
    #    - Develop AI models to recommend treatments based on patient history and clinical data.

    # Resource Collection
    # - Datasets:
    #   - Kaggle: [Healthcare Analytics Dataset](https://www.kaggle.com/)
    #   - HuggingFace: [Clinical BERT Pre-trained Models](https://huggingface.co/)
    # - Pre-trained Models:
    #   - TensorFlow Healthcare Models
    #   - GPT-based clinical summarization tools
    # - Code Repositories:
    #   - GitHub: AI-Powered Claims Processing Repository (link)
    #   - GitHub: Predictive Healthcare Analytics (link)

    # Final Proposal
    # - Top Priority Use Cases:
    #   1. AI-Powered Claims Processing: Automate and enhance accuracy in insurance claims.
    #   2. Predictive Analytics for Patient Health: Prevent diseases through early interventions.
    #   3. Personalized Patient Engagement: Improve patient satisfaction and reduce workload.

    # - Supporting Resources:
    #   - Clinical datasets, GPT-based models for text summarization, and fraud detection algorithms.
    # """
        
        # Render result template
        return render_template('result.html', result=result)

    # Render input form
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

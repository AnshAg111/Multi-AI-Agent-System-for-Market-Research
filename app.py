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
        
        # Render result template
        return render_template('result.html', result=result)

    # Render input form
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

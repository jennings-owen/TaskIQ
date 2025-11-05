# Create an agent and deploy using a FastAPI endpoint. Solve a problem that cannot be used by a single LLM call. 
# full stack app to create a PRD document

# Custom CrewAI Agent: Business Idea to PRD Generator
# This agent takes a simple business idea as input, generates a detailed business plan,
# and ensures it conforms to a PRD template markdown file.

import os
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from langchain_openai import ChatOpenAI
import uvicorn

# Add project root to path for utils import
try:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from utils import load_artifact
except ImportError:
    print("Warning: Could not import utils.load_artifact. Template will be loaded from file.")
    load_artifact = None

# Load environment variables
load_dotenv()

# Verify required environment variables
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found. Please check your .env file.")

# FastAPI app instance
app = FastAPI(title="Business Idea to PRD Generator", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models for API
class BusinessIdeaInput(BaseModel):
    business_idea: str
    product_name: Optional[str] = None
    target_market: Optional[str] = None
    budget_range: Optional[str] = None
    timeline: Optional[str] = None

class PRDOutput(BaseModel):
    success: bool
    prd_document: str
    validation_results: Dict[str, Any]

# PRD Template Loading Function
def get_prd_template() -> str:
    """
    Load the PRD template from file using load_artifact.
    Falls back to direct file reading if load_artifact is not available.
    """
    try:
        if load_artifact:
            # Try to load using the utils load_artifact function
            template_content = load_artifact("templates/prd_template.md", base_dir=os.path.dirname(__file__))
            return template_content
        else:
            # Fallback: load directly from file
            template_path = os.path.join(os.path.dirname(__file__), "templates", "prd_template.md")
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        print(f"Warning: Could not load PRD template: {e}")
        # Return a basic template as fallback
        return ""

# Load PRD template at startup
PRD_TEMPLATE = get_prd_template()

# Custom tools for the agents
@tool
def conduct_market_research(business_idea: str, target_market: str = "") -> str:
    """
    Conducts market research for a given business idea.
    
    Args:
        business_idea: The business idea to research
        target_market: Optional target market specification
        
    Returns:
        Market research findings and analysis
    """
    # In a real implementation, this would call actual market research APIs
    # For now, we'll generate a structured market analysis
    research_findings = f"""
    Market Research Analysis for: {business_idea}
    
    Market Size & Opportunity:
    - Total Addressable Market (TAM): Analysis shows significant opportunity
    - Target Market: {target_market if target_market else 'General consumer market'}
    - Market Growth Rate: Estimated based on industry trends
    
    Competitive Landscape:
    - Direct competitors identified and analyzed
    - Market positioning opportunities available
    - Differentiation factors recommended
    
    Customer Pain Points:
    - Primary pain points validated through market analysis
    - Unmet needs identified in current solutions
    - Willingness to pay indicators positive
    
    Risk Assessment:
    - Market entry barriers assessed
    - Regulatory considerations reviewed
    - Technology feasibility confirmed
    """
    return research_findings

@tool
def generate_business_model(business_idea: str, market_research: str) -> str:
    """
    Generates a comprehensive business model based on the idea and market research.
    
    Args:
        business_idea: The core business idea
        market_research: Market research findings
        
    Returns:
        Detailed business model canvas
    """
    business_model = f"""
    Business Model Canvas for: {business_idea}
    
    Value Propositions:
    - Core value delivered to customers
    - Unique selling propositions
    - Competitive advantages
    
    Customer Segments:
    - Primary customer segments identified
    - Customer personas developed
    - Market segmentation strategy
    
    Revenue Streams:
    - Primary revenue models
    - Pricing strategies
    - Revenue forecasting
    
    Key Resources:
    - Technology requirements
    - Human resources needed
    - Financial resources
    
    Key Activities:
    - Core business activities
    - Value creation processes
    - Operational requirements
    
    Cost Structure:
    - Fixed and variable costs
    - Cost optimization opportunities
    - Break-even analysis
    """
    return business_model

@tool
def validate_prd_structure(prd_content: str) -> Dict[str, Any]:
    """
    Validates that the PRD document follows the required template structure.
    
    Args:
        prd_content: The PRD document content to validate
        
    Returns:
        Validation results with completeness scores and missing sections
    """
    required_sections = [
        "Executive Summary & Vision",
        "Problem Statement & Opportunity", 
        "Target Users & Personas",
        "Success Metrics & Goals",
        "Functional Requirements & User Stories",
        "Non-Functional Requirements",
        "Release Plan & Milestones",
        "Out of Scope & Future Considerations",
        "Appendix & Open Questions"
    ]
    
    validation_results = {
        "total_sections": len(required_sections),
        "found_sections": 0,
        "missing_sections": [],
        "completeness_score": 0.0,
        "validation_passed": False
    }
    
    for section in required_sections:
        if section.lower() in prd_content.lower():
            validation_results["found_sections"] += 1
        else:
            validation_results["missing_sections"].append(section)
    
    validation_results["completeness_score"] = (validation_results["found_sections"] / validation_results["total_sections"]) * 100
    validation_results["validation_passed"] = validation_results["completeness_score"] >= 80.0
    
    return validation_results

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0.3)  # Balanced temperature for detailed content generation

# Define CrewAI Agents
business_analyst = Agent(
    role="Senior Business Analyst",
    goal="Analyze business ideas and conduct comprehensive market research to identify opportunities and validate concepts",
    backstory="""You are a seasoned business analyst with 15+ years of experience in market research,
    competitive analysis, and business strategy. You excel at taking raw business ideas and transforming
    them into well-researched, data-driven insights that form the foundation for successful products.""",
    tools=[conduct_market_research],
    verbose=True,
    llm=llm
)

strategy_consultant = Agent(
    role="Strategic Business Consultant", 
    goal="Develop comprehensive business models and strategic frameworks based on market research",
    backstory="""You are an expert strategic consultant who specializes in business model innovation
    and go-to-market strategies. You have helped dozens of startups and enterprises launch successful
    products by creating robust business models and strategic plans.""",
    tools=[generate_business_model],
    verbose=True,
    llm=llm
)

product_manager = Agent(
    role="Senior Product Manager and Technical Writer",
    goal="Generate complete, detailed PRD documents by filling out templates with comprehensive content based on research and business models",
    backstory="""You are a highly experienced product manager who excels at taking business research and 
    strategic frameworks and transforming them into detailed, actionable Product Requirements Documents. 
    You never provide meta-commentary or explanations about your work - you simply deliver the complete 
    PRD document content. You are known for writing comprehensive, detailed sections that provide real 
    value to development teams and stakeholders. When given a template, you fill every section thoroughly 
    with specific, actionable information.""",
    tools=[validate_prd_structure],
    verbose=True,
    llm=llm
)

# Define Tasks
market_research_task = Task(
    description="""
    Conduct comprehensive market research for the given business idea: {business_idea}
    
    Your analysis should include:
    1. Market size and opportunity assessment
    2. Competitive landscape analysis  
    3. Target customer identification and pain points
    4. Market trends and growth projections
    5. Risk assessment and barriers to entry
    
    Target Market Context: {target_market}
    Budget Considerations: {budget_range}
    Timeline Constraints: {timeline}
    
    Provide actionable insights that will inform business model development.
    """,
    expected_output="Comprehensive market research report with key findings, opportunities, and recommendations",
    agent=business_analyst
)

business_model_task = Task(
    description="""
    Based on the market research findings, develop a comprehensive business model for: {business_idea}
    
    Create a detailed business model that includes:
    1. Value propositions and unique selling points
    2. Customer segments and personas
    3. Revenue streams and pricing strategies
    4. Key resources and activities required
    5. Cost structure and financial projections
    6. Go-to-market strategy
    7. Risk mitigation strategies
    
    Ensure the business model is realistic and aligned with the market research findings.
    """,
    expected_output="Complete business model canvas with detailed strategic framework",
    agent=strategy_consultant,
    context=[market_research_task]
)

prd_creation_task = Task(
    description="""
    You must generate the complete PRD document for: {business_idea}
    
    Use the market research and business model from previous tasks to fill out this EXACT template:
    
    {PRD_TEMPLATE}
    
    CRITICAL INSTRUCTIONS:
    1. Start your response with "# Product Requirements Document: {product_name}"
    2. Replace ALL placeholder text in curly braces with actual detailed content
    3. Fill out every section completely with specific, actionable information
    4. Do NOT include any meta-commentary, validation results, or explanatory text
    5. Do NOT say "The document is complete" or similar phrases
    6. Output ONLY the markdown PRD content, nothing else
    
    The final output must be a complete, standalone PRD document ready for stakeholder review.
    """,
    expected_output="Complete PRD markdown document starting with '# Product Requirements Document:' and containing all filled sections",
    agent=product_manager,
    context=[market_research_task, business_model_task]
)

# Create the Crew
business_to_prd_crew = Crew(
    agents=[business_analyst, strategy_consultant, product_manager],
    tasks=[market_research_task, business_model_task, prd_creation_task],
    process=Process.sequential,
    verbose=True
)

# API Endpoints
@app.get("/")
async def root():
    return {"message": "Business Idea to PRD Generator API", "version": "1.0.0"}

@app.post("/generate-prd", response_model=PRDOutput)
async def generate_prd(input_data: BusinessIdeaInput):
    """
    Generates a comprehensive PRD document from a business idea.
    
    This endpoint uses a multi-agent system to:
    1. Conduct market research on the business idea
    2. Develop a comprehensive business model
    3. Create a detailed PRD document that conforms to enterprise standards
    """
    try:
        # Use provided product_name or generate a default one
        product_name = input_data.product_name if hasattr(input_data, 'product_name') and input_data.product_name else "AI-Powered Solution"
        
        # Prepare inputs for the crew with all required template variables
        crew_inputs = {
            "business_idea": input_data.business_idea,
            "product_name": product_name,
            "target_market": input_data.target_market or "General market",
            "budget_range": input_data.budget_range or "To be determined",
            "timeline": input_data.timeline or "6-12 months",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "PRD_TEMPLATE": PRD_TEMPLATE
        }
        
        # Execute the crew workflow
        result = business_to_prd_crew.kickoff(inputs=crew_inputs)
        
        # Extract the PRD content from the result and clean it
        prd_content = str(result).strip()
        
        # Clean up any potential meta-commentary or validation text
        cleanup_patterns = [
            "Validation Results:",
            "The Product Requirements Document (PRD)",
            "has been successfully created",
            "validation",
            "follows the specified template",
            "ready for stakeholder review",
            "document is complete",
            "Final Output:",
            "The complete PRD document content has been provided above",
            "following the exact structure",
            "incorporating the given"
        ]
        
        for pattern in cleanup_patterns:
            if pattern in prd_content:
                # Split on the pattern and take only the first part (the actual PRD)
                parts = prd_content.split(pattern)
                if len(parts) > 1:
                    prd_content = parts[0].strip()
        
        # Remove any leading/trailing whitespace and ensure proper formatting
        prd_content = prd_content.strip()
        
        # Ensure the content starts with the PRD title
        if not prd_content.startswith("# Product Requirements Document"):
            # Look for the PRD start in the content
            lines = prd_content.split('\n')
            prd_start_idx = -1
            for i, line in enumerate(lines):
                if line.startswith("# Product Requirements Document"):
                    prd_start_idx = i
                    break
            
            if prd_start_idx >= 0:
                prd_content = '\n'.join(lines[prd_start_idx:])
            else:
                # If we still don't have a proper PRD, there might be an issue
                # Let's check if the content contains any substantial text
                if len(prd_content) < 100:
                    raise Exception(f"Generated PRD content is too short or malformed: {prd_content[:200]}")
        
        # Final cleanup - remove any trailing meta-commentary
        lines = prd_content.split('\n')
        cleaned_lines = []
        for line in lines:
            # Stop processing if we hit obvious meta-commentary
            if any(phrase in line.lower() for phrase in ["final output", "complete prd document", "provided above", "following the exact"]):
                break
            cleaned_lines.append(line)
        
        prd_content = '\n'.join(cleaned_lines).strip()
        
        # Validate the PRD structure using the function directly
        validation_results = validate_prd_structure.func(prd_content)
        
        return PRDOutput(
            success=True,
            prd_document=prd_content,
            validation_results=validation_results
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PRD: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/template-info")
async def get_template_info():
    """Returns information about the loaded PRD template."""
    return {
        "template_length": len(PRD_TEMPLATE),
        "template_preview": PRD_TEMPLATE[:200] + "..." if len(PRD_TEMPLATE) > 200 else PRD_TEMPLATE,
        "contains_product_name_placeholder": "{product_name}" in PRD_TEMPLATE,
        "contains_date_placeholder": "{date}" in PRD_TEMPLATE
    }

@app.get("/crew-info")
async def get_crew_info():
    """Returns information about the agent crew and their capabilities."""
    return {
        "crew_composition": {
            "business_analyst": {
                "role": business_analyst.role,
                "goal": business_analyst.goal,
                "tools": ["Market Research Tool"]
            },
            "strategy_consultant": {
                "role": strategy_consultant.role,
                "goal": strategy_consultant.goal,
                "tools": ["Business Model Generator"]
            },
            "product_manager": {
                "role": product_manager.role,
                "goal": product_manager.goal,
                "tools": ["PRD Validator"]
            }
        },
        "workflow": [
            "1. Market Research & Analysis",
            "2. Business Model Development", 
            "3. PRD Document Creation & Validation"
        ]
    }

# Main execution
if __name__ == "__main__":
    print("🚀 Starting Business Idea to PRD Generator API...")
    print("📋 This service uses CrewAI to transform business ideas into comprehensive PRD documents")
    print("🔗 API Documentation available at: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)


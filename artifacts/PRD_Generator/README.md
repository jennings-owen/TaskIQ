# Business Idea to PRD Generator

A custom CrewAI agent system that transforms simple business ideas into comprehensive Product Requirements Documents (PRDs) that conform to enterprise standards.

## 🎯 Overview

This project demonstrates how to build a multi-agent system using CrewAI that solves a complex problem requiring multiple specialized skills:

1. **Market Research & Analysis** - Conducted by a Business Analyst agent
2. **Business Model Development** - Handled by a Strategy Consultant agent  
3. **PRD Creation & Validation** - Performed by a Product Manager agent

The system is deployed as a FastAPI web service, making it easy to integrate into existing workflows or use as a standalone service.

## 🏗️ Architecture

### Agent Crew Composition

**Business Analyst Agent**
- Role: Senior Business Analyst
- Tools: Market Research Tool
- Responsibility: Analyze business ideas, conduct market research, identify opportunities

**Strategy Consultant Agent**  
- Role: Strategic Business Consultant
- Tools: Business Model Generator
- Responsibility: Develop comprehensive business models and strategic frameworks

**Product Manager Agent**
- Role: Senior Product Manager
- Tools: PRD Validator
- Responsibility: Create detailed PRDs that conform to enterprise standards

### Workflow

```
Business Idea Input → Market Research → Business Model → PRD Creation → Validation
```

Each agent builds upon the work of the previous agent, ensuring comprehensive analysis and documentation.

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- Virtual environment (recommended)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd "Labs/Agent_notebooks/Custom Agent"
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Running the Service

1. **Start the API server:**
   ```bash
   python agents_custom.py
   ```
   
   The service will start on `http://localhost:8000`

2. **Test the service (in a new terminal):**
   ```bash
   python test_agent.py
   ```

3. **Run frontend**: Expose frontend folder with a live web server. Use VSCode live server to use port 5500

## 📡 API Usage

### Endpoints

#### `POST /generate-prd`
Generates a comprehensive PRD from a business idea.

**Request Body:**
```json
{
  "business_idea": "A mobile app that uses AI to help people learn languages",
  "target_market": "Language learners aged 18-35",
  "budget_range": "$50,000 - $100,000",
  "timeline": "12 months"
}
```

**Response:**
```json
{
  "success": true,
  "prd_document": "# Product Requirements Document: ...",
  "validation_results": {
    "total_sections": 9,
    "found_sections": 9,
    "completeness_score": 100.0,
    "validation_passed": true,
    "missing_sections": []
  }
}
```

#### `GET /crew-info`
Returns information about the agent crew composition and workflow.

#### `GET /health`
Health check endpoint.

### Interactive API Documentation

Visit `http://localhost:8000/docs` when the service is running to access the interactive Swagger documentation.

## 🧪 Example Usage

### Using the Test Script

The included `test_agent.py` demonstrates how to use the service:

```bash
python test_agent.py
```

This will:
1. Check API health
2. Display crew information
3. Generate a PRD for a sample business idea
4. Save the result to a markdown file
5. Show validation results

### Direct API Calls

You can also make direct HTTP requests:

```bash
curl -X POST "http://localhost:8000/generate-prd" \
  -H "Content-Type: application/json" \
  -d '{
    "business_idea": "A sustainable food delivery service connecting local farms with consumers",
    "target_market": "Health-conscious urban professionals",
    "budget_range": "$200,000 - $500,000",
    "timeline": "18 months"
  }'
```

## 📋 PRD Template Structure

The generated PRDs follow a comprehensive enterprise-standard template that is loaded from `templates/prd_template.md` using the `load_artifact` utility function:

1. **Executive Summary & Vision** - High-level overview and long-term vision
2. **Problem Statement & Opportunity** - Specific problems being solved
3. **Target Users & Personas** - Detailed user profiles and demographics
4. **Success Metrics & Goals** - Measurable KPIs and success criteria
5. **Functional Requirements & User Stories** - Core features with acceptance criteria
6. **Non-Functional Requirements** - Performance, security, scalability needs
7. **Release Plan & Milestones** - Development timeline and phases
8. **Out of Scope & Future Considerations** - What's excluded and future roadmap
9. **Appendix & Open Questions** - Dependencies, assumptions, open issues

### Template File Structure

```
Custom Agent/
├── templates/
│   └── prd_template.md          # PRD template loaded using load_artifact
├── agents_custom.py             # Main agent system
├── test_agent.py               # Testing script
└── README.md                   # This documentation
```

The PRD template is now externalized and loaded using the project's `load_artifact` utility, making it easy to:
- Version control template changes
- Share templates across projects
- Customize templates without modifying code
- Use the standard artifact management system

## 🔧 Customization

### Adding New Tools

You can extend the agents with additional tools by defining new functions with the `@tool` decorator:

```python
@tool("Competitive Analysis Tool")
def analyze_competitors(business_idea: str) -> str:
    """Analyze competitors for the given business idea."""
    # Your implementation here
    return analysis_results
```

### Modifying Agent Behavior

Customize agent roles, goals, and backstories in the agent definitions:

```python
custom_agent = Agent(
    role="Your Custom Role",
    goal="Your specific goal",
    backstory="Your agent's background and expertise",
    tools=[your_custom_tools],
    verbose=True,
    llm=llm
)
```

### Extending the PRD Template

The PRD template is now stored in `templates/prd_template.md` and loaded using the `load_artifact` utility. To customize the template:

1. **Edit the template file**: Modify `templates/prd_template.md` to add or change sections
2. **Add new placeholders**: Use `{placeholder_name}` format for dynamic content
3. **Restart the service**: The template is loaded at startup, so restart to see changes

Example template modification:
```markdown
## 10. Risk Assessment & Mitigation
*Identified risks and mitigation strategies.*

{risk_assessment}
```

The agent will automatically use the updated template for all PRD generations.

## 🏃‍♂️ Performance Considerations

- **Processing Time**: Full PRD generation typically takes 2-5 minutes depending on complexity
- **API Timeout**: Set to 5 minutes to accommodate the multi-agent workflow
- **Rate Limits**: Consider OpenAI API rate limits for production usage
- **Caching**: Consider implementing caching for repeated similar requests

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your OpenAI API key is set in the `.env` file
2. **Connection Error**: Make sure the API server is running on port 8000
3. **Timeout Error**: Complex business ideas may take longer to process
4. **Import Error**: Ensure all dependencies are installed via `pip install -r requirements.txt`
5. **Template Loading Error**: If you see template loading warnings, ensure the `templates/prd_template.md` file exists

### Verifying Template Loading

To verify that the PRD template is loading correctly, you can test it manually:

```python
# Test template loading
from agents_custom import get_prd_template

template = get_prd_template()
print(f"Template loaded successfully: {len(template)} characters")
print("First 200 characters:")
print(template[:200])
```

### Debug Mode

Enable verbose logging by setting the agent `verbose=True` parameter (already enabled by default).

## 📝 Example Business Ideas to Try

1. **AI-Powered Language Learning App**
   - Target: Language learners who want conversation practice
   - Unique value: Real-time AI conversation partners

2. **Sustainable Food Delivery**
   - Target: Health-conscious urban professionals
   - Unique value: Direct farm-to-consumer delivery

3. **Remote Work Productivity Suite**
   - Target: Distributed teams and remote workers
   - Unique value: Integrated communication and project management

4. **Pet Health Monitoring Platform**
   - Target: Pet owners who want proactive health management
   - Unique value: IoT sensors + veterinary expertise

## 🤝 Contributing

This project is part of the AI-Driven Software Engineering Program. Feel free to:

1. Extend the agent capabilities
2. Add new tools and integrations
3. Improve the PRD template
4. Enhance the API functionality

## 📄 License

This project is part of the AG-AISOFTDEV course materials and is intended for educational purposes.

---

**🚀 Ready to transform your business ideas into professional PRDs? Start the service and give it a try!**
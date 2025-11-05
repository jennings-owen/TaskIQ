#!/usr/bin/env python3
"""
Test script for the Business Idea to PRD Generator API
This demonstrates how to use the custom CrewAI agent to transform business ideas into PRDs.
"""

import requests
import json
import time
from typing import Dict, Any

# API Configuration
API_BASE_URL = "http://localhost:8000"

def test_api_health() -> bool:
    """Test if the API is running and healthy."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is healthy and running")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {e}")
        print("💡 Make sure to run 'python agents_custom.py' first to start the API server")
        return False

def get_crew_info() -> Dict[str, Any]:
    """Get information about the agent crew composition."""
    try:
        response = requests.get(f"{API_BASE_URL}/crew-info")
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to get crew info: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting crew info: {e}")
        return {}

def generate_prd(business_idea: str, target_market: str = None, budget_range: str = None, timeline: str = None) -> Dict[str, Any]:
    """Generate a PRD document from a business idea."""
    payload = {
        "business_idea": business_idea,
        "target_market": target_market,
        "budget_range": budget_range,
        "timeline": timeline
    }
    
    # Remove None values
    payload = {k: v for k, v in payload.items() if v is not None}
    
    print(f"🚀 Generating PRD for: {business_idea}")
    print(f"📋 Payload: {json.dumps(payload, indent=2)}")
    print("⏳ This may take a few minutes as the agents collaborate...")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/generate-prd",
            json=payload,
            timeout=300  # 5 minutes timeout for complex processing
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to generate PRD: {response.status_code}")
            print(f"Error details: {response.text}")
            return {}
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error generating PRD: {e}")
        return {}

def save_prd_to_file(prd_content: str, filename: str = "generated_prd.md"):
    """Save the generated PRD to a markdown file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(prd_content)
        print(f"📄 PRD saved to: {filename}")
    except Exception as e:
        print(f"❌ Error saving PRD: {e}")

def print_validation_results(validation_results: Dict[str, Any]):
    """Print PRD validation results in a formatted way."""
    print("\n📊 PRD Validation Results:")
    print(f"   • Total sections required: {validation_results.get('total_sections', 0)}")
    print(f"   • Sections found: {validation_results.get('found_sections', 0)}")
    print(f"   • Completeness score: {validation_results.get('completeness_score', 0):.1f}%")
    print(f"   • Validation passed: {'✅ Yes' if validation_results.get('validation_passed', False) else '❌ No'}")
    
    missing_sections = validation_results.get('missing_sections', [])
    if missing_sections:
        print(f"   • Missing sections: {', '.join(missing_sections)}")

def main():
    """Main test function demonstrating the agent's capabilities."""
    print("🤖 Testing Business Idea to PRD Generator")
    print("=" * 50)
    
    # Test API health
    if not test_api_health():
        return
    
    # Get crew information
    print("\n📋 Agent Crew Information:")
    crew_info = get_crew_info()
    if crew_info:
        for agent_name, agent_info in crew_info.get('crew_composition', {}).items():
            print(f"   • {agent_name}: {agent_info.get('role', 'Unknown role')}")
        
        print(f"\n🔄 Workflow: {' → '.join(crew_info.get('workflow', []))}")
    
    # Test cases
    test_cases = [
        {
            "business_idea": "A mobile app that uses AI to help people learn new languages through real-world conversations with native speakers",
            "target_market": "Language learners aged 18-35 who want practical conversation practice",
            "budget_range": "$50,000 - $100,000",
            "timeline": "12 months"
        },
        {
            "business_idea": "A sustainable food delivery service that connects local organic farms directly with consumers",
            "target_market": "Health-conscious urban professionals and families",
            "budget_range": "$200,000 - $500,000",
            "timeline": "18 months"
        }
    ]
    
    # Run test for the first business idea
    test_case = test_cases[0]  # You can change this to test_cases[1] for the second idea
    
    print(f"\n🧪 Test Case:")
    print(f"   Business Idea: {test_case['business_idea']}")
    print(f"   Target Market: {test_case['target_market']}")
    print(f"   Budget Range: {test_case['budget_range']}")
    print(f"   Timeline: {test_case['timeline']}")
    
    # Generate PRD
    start_time = time.time()
    result = generate_prd(**test_case)
    end_time = time.time()
    
    if result.get('success', False):
        print(f"\n✅ PRD Generated Successfully! (took {end_time - start_time:.1f} seconds)")
        
        # Print validation results
        validation_results = result.get('validation_results', {})
        print_validation_results(validation_results)
        
        # Save PRD to file
        prd_content = result.get('prd_document', '')
        if prd_content:
            filename = f"prd_{int(time.time())}.md"
            save_prd_to_file(prd_content, filename)
            
            # Show a preview of the PRD
            print(f"\n📖 PRD Preview (first 500 characters):")
            print("-" * 50)
            print(prd_content[:500] + "..." if len(prd_content) > 500 else prd_content)
            print("-" * 50)
            
        print(f"\n🎉 Test completed successfully!")
        print(f"💡 You can now review the full PRD in the saved file: {filename}")
        
    else:
        print("❌ PRD generation failed")

if __name__ == "__main__":
    main()
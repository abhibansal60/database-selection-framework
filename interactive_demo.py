#!/usr/bin/env python3
"""
Interactive Demo Simulation
Simulates the CLI experience with realistic responses for your project context
"""

from framework import DatabaseFramework
from questions import QuestionSet
from adr_generator import ADRGenerator
import os

def simulate_interactive_session():
    """Simulate an interactive session with realistic responses"""
    
    print("🎯 DATABASE SELECTION FRAMEWORK - INTERACTIVE SIMULATION")
    print("=" * 80)
    print("Simulating a realistic session for your database selection project...")
    print()
    
    # Initialize components
    framework = DatabaseFramework()
    question_set = QuestionSet()
    adr_generator = ADRGenerator()
    
    # Project context
    project_name = "Database Selection Framework Project"
    print(f"📋 PROJECT: {project_name}")
    print()
    
    # Simulate responses based on your actual project context
    responses = [
        {
            'id': 'schema_evolution',
            'text': 'How predictable is your data structure evolution over the next 2 years?',
            'choice': 'somewhat_predictable',
            'choice_text': 'Somewhat predictable - Some changes expected but within known patterns',
            'rationale': 'Moving from SharePoint, some evolution expected but within reasonable bounds'
        },
        {
            'id': 'query_patterns', 
            'text': 'What are your primary data access patterns and query requirements?',
            'choice': 'mixed_patterns',
            'choice_text': 'Mixed patterns - combination of the above',
            'rationale': 'Custom application will need various access patterns'
        },
        {
            'id': 'team_expertise',
            'text': 'What is your team\'s current database and development expertise?',
            'choice': 'mixed_skills',
            'choice_text': 'Mixed skills across different database technologies',
            'rationale': 'Team has varied background, willing to learn'
        },
        {
            'id': 'consistency_needs',
            'text': 'How critical are ACID transactions and strong consistency for your use case?',
            'choice': 'mostly_consistent',
            'choice_text': 'Important - User data integrity matters but some flexibility acceptable',
            'rationale': 'Data integrity important but not financial/compliance level'
        },
        {
            'id': 'performance_profile',
            'text': 'What is your expected performance and scaling profile?',
            'choice': 'balanced_load',
            'choice_text': 'Balanced read/write load with moderate scaling requirements',
            'rationale': 'Internal application, moderate usage expected'
        }
    ]
    
    # Process each question
    print("📊 CORE ASSESSMENT")
    print("=" * 40)
    
    for i, response in enumerate(responses, 1):
        print(f"\n[Question {i}/{len(responses)}]")
        print("🤔 QUESTION")
        print("-" * 40)
        print(f"{response['text']}")
        print()
        print(f"💭 Your likely response: {response['choice_text']}")
        print(f"💡 Context: {response['rationale']}")
        
        # Add to framework
        framework.add_response(
            response['id'],
            response['text'], 
            response['choice'],
            response['choice_text']
        )
        
        print("✓ Response recorded")
    
    # Add ServiceNow context
    framework.add_context('serviceNow_experience', '6-7 months failed evaluation due to platform rigidity')
    framework.add_context('migration_source', 'SharePoint-based system')
    framework.add_context('customization_priority', 'High - must avoid ServiceNow situation')
    
    print("\n" + "="*80)
    
    # Calculate decision
    decision = framework.calculate_decision()
    
    # Display results
    print("🎯 RECOMMENDATION")
    print("=" * 80)
    
    total_score = decision.mongodb_total_score + decision.postgresql_total_score
    if total_score > 0:
        mongodb_pct = (decision.mongodb_total_score / total_score) * 100
        postgresql_pct = (decision.postgresql_total_score / total_score) * 100
    else:
        mongodb_pct = postgresql_pct = 50
    
    print(f"🏆 Recommendation: **{decision.recommendation.value}**")
    print(f"📊 Confidence: {decision.confidence_level}")
    print()
    print("SCORING BREAKDOWN:")
    print(f"MongoDB:    {decision.mongodb_total_score:.2f} ({mongodb_pct:.1f}%)")
    print(f"PostgreSQL: {decision.postgresql_total_score:.2f} ({postgresql_pct:.1f}%)")
    print()
    
    # Show key factors
    print("🔑 KEY FACTORS ANALYSIS:")
    print("-" * 40)
    sorted_responses = sorted(decision.responses, key=lambda r: r.weight, reverse=True)
    
    for i, response in enumerate(sorted_responses, 1):
        weight_pct = response.weight * 100
        print(f"{i}. {response.question_text}")
        print(f"   Weight: {weight_pct:.0f}% | MongoDB: {response.mongodb_score:.2f} | PostgreSQL: {response.postgresql_score:.2f}")
        print(f"   Your response: {response.response}")
        print(f"   Impact: {response.rationale}")
        print()
    
    # ServiceNow analysis
    print("🛡️ SERVICENOW TRAUMA MITIGATION ANALYSIS:")
    print("-" * 40)
    
    if decision.recommendation.value == 'MongoDB':
        print("✅ MongoDB Advantages for ServiceNow Recovery:")
        print("   • Maximum schema flexibility prevents rigid platform constraints")
        print("   • Document model enables complex business logic without limitations")
        print("   • No vendor warnings about customization maintenance burden")
        print("   • Full control over data evolution and business requirements")
    elif decision.recommendation.value == 'PostgreSQL':
        print("✅ PostgreSQL Advantages for ServiceNow Recovery:")
        print("   • Open source eliminates vendor lock-in concerns")
        print("   • JSON capabilities provide document flexibility when needed")
        print("   • Standard SQL avoids proprietary platform constraints")
        print("   • Mature ecosystem with extensive customization options")
    else:
        print("⚖️ Balanced Analysis - Both Options Address ServiceNow Issues:")
        print("   • Both databases provide full customization freedom")
        print("   • Open source options eliminate vendor lock-in")
        print("   • Either choice avoids ServiceNow's rigidity problems")
        print("   • Recommendation: Technical spikes with both databases")
    
    print()
    
    # Generate ADR
    print("📄 ADR GENERATION:")
    print("-" * 40)
    
    os.makedirs("output", exist_ok=True)
    adr_path = adr_generator.save_adr(decision, project_name, output_dir="output")
    
    print(f"✓ Generated ADR: {adr_path}")
    print()
    print("ADR includes:")
    print("• Complete ServiceNow context and lessons learned")
    print("• Factor-by-factor decision analysis")
    print("• Implementation recommendations and next steps")
    print("• Risk mitigation strategies")
    print("• Team consensus documentation")
    
    # Show next steps
    print("\n🚀 RECOMMENDED NEXT STEPS:")
    print("=" * 40)
    
    if decision.recommendation.value != 'Neutral/Requires Further Analysis':
        print(f"1. 🧪 Create technical spike with {decision.recommendation.value}")
        print(f"2. 👥 Share ADR with team for review and consensus")
        print(f"3. 🏗️ Plan infrastructure and deployment approach")
        print(f"4. 📚 Identify team training needs for {decision.recommendation.value}")
        print(f"5. 🔄 Plan migration strategy from SharePoint")
    else:
        print("1. 🧪 Create parallel technical spikes with both MongoDB and PostgreSQL")
        print("2. 👥 Team evaluation sessions with hands-on experience")
        print("3. 📊 Performance testing with representative data")
        print("4. 🤝 Final team decision meeting with spike results")
        print("5. 📄 Update ADR with final choice and rationale")
    
    print("\n✅ Framework Complete!")
    print(f"📁 Review your ADR: {adr_path}")
    print("🎯 Use this analysis for team discussion and final decision")
    
    return decision

if __name__ == "__main__":
    simulate_interactive_session()
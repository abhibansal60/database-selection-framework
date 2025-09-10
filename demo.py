#!/usr/bin/env python3
"""
Demo script for Database Selection Framework

Demonstrates the framework with sample responses that validate against
ServiceNow pain points and show different recommendation scenarios.
"""

from framework import DatabaseFramework
from questions import QuestionSet  
from adr_generator import ADRGenerator
import os

def demo_mongodb_scenario():
    """Demo scenario that leads to MongoDB recommendation"""
    print("=" * 80)
    print("🟢 DEMO: MongoDB-Favoring Scenario")
    print("=" * 80)
    print("Simulating responses that favor MongoDB due to ServiceNow trauma...")
    print()
    
    framework = DatabaseFramework()
    
    # Add responses that favor MongoDB (flexibility-focused)
    framework.add_response(
        'schema_evolution', 
        'How predictable is your data structure evolution over the next 2 years?',
        'unpredictable',
        'Unpredictable - Frequent schema changes driven by evolving business needs'
    )
    
    framework.add_response(
        'query_patterns',
        'What are your primary data access patterns and query requirements?', 
        'document_retrieval',
        'Document-based retrieval with flexible search across nested structures'
    )
    
    framework.add_response(
        'team_expertise',
        'What is your team\'s current database and development expertise?',
        'javascript_heavy', 
        'JavaScript/Node.js heavy with JSON-first thinking'
    )
    
    framework.add_response(
        'consistency_needs',
        'How critical are ACID transactions and strong consistency for your use case?',
        'eventually_consistent',
        'Eventually consistent - Can handle temporary inconsistencies'  
    )
    
    framework.add_response(
        'performance_profile',
        'What is your expected performance and scaling profile?',
        'write_heavy_scaling',
        'Write-heavy with high-volume data ingestion and horizontal scaling needs'
    )
    
    # Add ServiceNow trauma context
    framework.add_context('serviceNow_experience', 'Platform rigidity led to 6-month failed evaluation')
    framework.add_context('customization_priority', 'Critical - must avoid another ServiceNow situation')
    
    # Calculate decision
    decision = framework.calculate_decision()
    
    # Display results
    print(f"🎯 Recommendation: {decision.recommendation.value}")
    print(f"📊 Confidence: {decision.confidence_level}")
    print(f"   MongoDB Score: {decision.mongodb_total_score:.2f}")
    print(f"   PostgreSQL Score: {decision.postgresql_total_score:.2f}")
    print()
    
    # Show how it addresses ServiceNow pain points
    print("🛡️ ServiceNow Pain Point Mitigation:")
    print("   ✓ Schema flexibility prevents rigid platform constraints")
    print("   ✓ Document model allows complex business logic implementation")
    print("   ✓ No vendor lock-in or maintenance burden warnings")
    print("   ✓ Team controls customization without platform limitations")
    
    return framework, decision

def demo_postgresql_scenario():
    """Demo scenario that leads to PostgreSQL recommendation"""
    print("=" * 80)
    print("🔵 DEMO: PostgreSQL-Favoring Scenario") 
    print("=" * 80)
    print("Simulating responses that favor PostgreSQL (structure-focused)...")
    print()
    
    framework = DatabaseFramework()
    
    # Add responses that favor PostgreSQL (structure/consistency-focused)
    framework.add_response(
        'schema_evolution',
        'How predictable is your data structure evolution over the next 2 years?',
        'highly_predictable',
        'Highly predictable - We have well-defined data models that rarely change'
    )
    
    framework.add_response(
        'query_patterns',
        'What are your primary data access patterns and query requirements?',
        'analytical_reporting', 
        'Analytical reporting with aggregations, grouping, and statistical functions'
    )
    
    framework.add_response(
        'team_expertise',
        'What is your team\'s current database and development expertise?',
        'sql_heavy',
        'Strong SQL and relational database experience'
    )
    
    framework.add_response(
        'consistency_needs',
        'How critical are ACID transactions and strong consistency for your use case?',
        'acid_critical',
        'Critical - Financial transactions, audit trails, or regulatory compliance'
    )
    
    framework.add_response(
        'performance_profile', 
        'What is your expected performance and scaling profile?',
        'read_heavy_analytics',
        'Read-heavy with analytical workloads and complex queries'
    )
    
    # Add context showing PostgreSQL addresses ServiceNow issues differently
    framework.add_context('serviceNow_experience', 'Learned importance of open standards over proprietary platforms')
    framework.add_context('compliance_needs', 'Regulatory requirements demand ACID guarantees')
    
    decision = framework.calculate_decision()
    
    print(f"🎯 Recommendation: {decision.recommendation.value}")
    print(f"📊 Confidence: {decision.confidence_level}")
    print(f"   MongoDB Score: {decision.mongodb_total_score:.2f}")
    print(f"   PostgreSQL Score: {decision.postgresql_total_score:.2f}")
    print()
    
    print("🛡️ ServiceNow Pain Point Mitigation:")
    print("   ✓ Open source prevents vendor lock-in like ServiceNow")
    print("   ✓ PostgreSQL flexibility far exceeds ServiceNow limitations")
    print("   ✓ JSON capabilities provide document flexibility when needed")
    print("   ✓ Standard SQL avoids proprietary platform constraints")
    
    return framework, decision

def demo_neutral_scenario():
    """Demo scenario that results in neutral/requires analysis recommendation"""
    print("=" * 80)
    print("⚪ DEMO: Neutral Scenario")
    print("=" * 80)
    print("Simulating balanced responses that require further analysis...")
    print()
    
    framework = DatabaseFramework()
    
    # Add balanced responses
    framework.add_response(
        'schema_evolution',
        'How predictable is your data structure evolution over the next 2 years?',
        'somewhat_predictable',
        'Somewhat predictable - Some changes expected but within known patterns'
    )
    
    framework.add_response(
        'query_patterns',
        'What are your primary data access patterns and query requirements?',
        'mixed_patterns',
        'Mixed patterns - combination of the above'
    )
    
    framework.add_response(
        'team_expertise',
        'What is your team\'s current database and development expertise?',
        'mixed_skills',
        'Mixed skills across different database technologies'
    )
    
    framework.add_response(
        'consistency_needs',
        'How critical are ACID transactions and strong consistency for your use case?',
        'mostly_consistent',
        'Important - User data integrity matters but some flexibility acceptable'
    )
    
    framework.add_response(
        'performance_profile',
        'What is your expected performance and scaling profile?',
        'balanced_load',
        'Balanced read/write load with moderate scaling requirements'
    )
    
    decision = framework.calculate_decision()
    
    print(f"🎯 Recommendation: {decision.recommendation.value}")
    print(f"📊 Confidence: {decision.confidence_level}")
    print(f"   MongoDB Score: {decision.mongodb_total_score:.2f}")
    print(f"   PostgreSQL Score: {decision.postgresql_total_score:.2f}")
    print()
    
    print("🔍 Neutral Result Guidance:")
    print("   → Both databases viable for this project")
    print("   → Recommend technical spikes with both options")
    print("   → Consider team preferences and infrastructure constraints")
    print("   → ServiceNow experience suggests prioritizing flexibility")
    
    return framework, decision

def demo_adr_generation(framework, decision, scenario_name):
    """Demo ADR generation for a given scenario"""
    print(f"\n📄 ADR Generation Demo - {scenario_name}")
    print("-" * 60)
    
    adr_generator = ADRGenerator()
    
    # Create output directory
    os.makedirs("demo_output", exist_ok=True)
    
    # Generate ADR
    adr_filepath = adr_generator.save_adr(
        decision, 
        f"Demo Project - {scenario_name}",
        output_dir="demo_output",
        filename=f"demo_adr_{scenario_name.lower().replace(' ', '_')}.md"
    )
    
    print(f"✓ Generated ADR: {adr_filepath}")
    
    # Show a snippet of the ADR
    with open(adr_filepath, 'r') as f:
        adr_content = f.read()
    
    # Find and display the decision section
    lines = adr_content.split('\n')
    in_decision = False
    decision_lines = []
    
    for line in lines:
        if line.startswith('## Decision'):
            in_decision = True
            decision_lines.append(line)
        elif in_decision and line.startswith('##'):
            break
        elif in_decision:
            decision_lines.append(line)
    
    if decision_lines:
        print("\nADR Decision Section Preview:")
        print("-" * 40)
        for line in decision_lines[:10]:  # Show first 10 lines
            print(line)
        if len(decision_lines) > 10:
            print("   [... truncated ...]")

def validate_serviceNow_mitigation():
    """Validate how the framework addresses ServiceNow pain points"""
    print("=" * 80)
    print("🛡️ SERVICENOW PAIN POINT VALIDATION")
    print("=" * 80)
    
    pain_points = {
        "Out-of-box Rigidity": [
            "Framework prioritizes schema flexibility (25% weight)",
            "MongoDB option addresses rigid data models", 
            "PostgreSQL JSON features provide flexibility within structure"
        ],
        "Customization Warnings": [
            "Framework emphasizes customization freedom",
            "Both database options provide full control over business logic",
            "No vendor lock-in or platform maintenance burden warnings"
        ],
        "SPM Business Logic Limitations": [
            "Query pattern analysis ensures business logic implementability", 
            "Document model (MongoDB) naturally supports complex business rules",
            "SQL flexibility (PostgreSQL) handles complex business requirements"
        ],
        "Platform Constraints": [
            "Team expertise factor (20% weight) ensures sustainable adoption",
            "Open source options avoid vendor platform limitations",
            "Framework generates clear rationale for team consensus"
        ]
    }
    
    for pain_point, mitigations in pain_points.items():
        print(f"\n🔴 ServiceNow Pain Point: {pain_point}")
        print(f"✅ Framework Mitigation:")
        for mitigation in mitigations:
            print(f"   • {mitigation}")
    
    print(f"\n🎯 Key Framework Strengths for ServiceNow Trauma Recovery:")
    print("   1. Explicitly weights customization freedom and flexibility")
    print("   2. Addresses team expertise to avoid adoption friction")
    print("   3. Generates ADRs that explain WHY database choice avoids ServiceNow issues")
    print("   4. Provides clear rationale for stakeholder confidence")
    print("   5. Framework itself is open and customizable (no vendor lock-in)")

def main():
    """Run all demo scenarios"""
    print("🚀 DATABASE SELECTION FRAMEWORK - COMPREHENSIVE DEMO")
    print("=" * 80)
    print("This demo validates the framework against ServiceNow pain points")
    print("and shows different recommendation scenarios.")
    print()
    
    # Run demo scenarios
    scenarios = [
        ("MongoDB Scenario", demo_mongodb_scenario),
        ("PostgreSQL Scenario", demo_postgresql_scenario), 
        ("Neutral Scenario", demo_neutral_scenario)
    ]
    
    results = []
    
    for name, demo_func in scenarios:
        framework, decision = demo_func()
        results.append((framework, decision, name))
        
        # Generate ADR for each scenario
        demo_adr_generation(framework, decision, name)
        print("\n" + "="*80 + "\n")
    
    # Validate ServiceNow pain point mitigation
    validate_serviceNow_mitigation()
    
    print("\n🎉 DEMO COMPLETE")
    print("=" * 80)
    print("Generated files in demo_output/ directory:")
    print("• demo_adr_mongodb_scenario.md")
    print("• demo_adr_postgresql_scenario.md") 
    print("• demo_adr_neutral_scenario.md")
    print()
    print("To run the interactive framework:")
    print("python cli.py")

if __name__ == "__main__":
    main()
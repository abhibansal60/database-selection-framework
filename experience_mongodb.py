#!/usr/bin/env python3
"""
MongoDB-leaning scenario simulation for full framework experience
"""

from framework import DatabaseFramework
from adr_generator import ADRGenerator
import os

def run_mongodb_experience():
    """Show the experience with responses that clearly favor MongoDB"""
    
    print("🎯 DATABASE SELECTION FRAMEWORK - MongoDB Experience")
    print("=" * 80)
    print("Let's see what happens with ServiceNow trauma-informed responses...")
    print()
    
    framework = DatabaseFramework()
    adr_generator = ADRGenerator()
    
    # ServiceNow trauma responses (flexibility-focused)
    print("📊 RESPONSES (Trauma-informed, Flexibility Priority):")
    print("=" * 60)
    
    responses = [
        {
            'question': 'Schema Evolution',
            'answer': 'Unpredictable - frequent changes driven by evolving business needs',
            'reasoning': '🛡️ ServiceNow was too rigid - need maximum flexibility'
        },
        {
            'question': 'Query Patterns', 
            'answer': 'Document-based retrieval with flexible search',
            'reasoning': '📄 Custom app needs flexible data access patterns'
        },
        {
            'question': 'Team Expertise',
            'answer': 'JavaScript/Node.js heavy with JSON-first thinking',
            'reasoning': '💻 Team comfort with JSON and modern web patterns'
        },
        {
            'question': 'Consistency Needs',
            'answer': 'Eventually consistent - can handle temporary inconsistencies', 
            'reasoning': '⚖️ Performance/flexibility more important than strict ACID'
        },
        {
            'question': 'Performance Profile',
            'answer': 'Write-heavy with high-volume data ingestion',
            'reasoning': '🚀 Expecting growth and need horizontal scaling'
        }
    ]
    
    for r in responses:
        print(f"Q: {r['question']}")
        print(f"A: {r['answer']}")
        print(f"   💡 {r['reasoning']}")
        print()
    
    # Add actual responses to framework
    framework.add_response('schema_evolution', 'Schema Evolution', 'unpredictable', 
                         'Unpredictable - frequent changes driven by evolving business needs')
    framework.add_response('query_patterns', 'Query Patterns', 'document_retrieval',
                         'Document-based retrieval with flexible search across nested structures')
    framework.add_response('team_expertise', 'Team Expertise', 'javascript_heavy',
                         'JavaScript/Node.js heavy with JSON-first thinking')
    framework.add_response('consistency_needs', 'Consistency Needs', 'eventually_consistent',
                         'Eventually consistent - Can handle temporary inconsistencies')
    framework.add_response('performance_profile', 'Performance Profile', 'write_heavy_scaling',
                         'Write-heavy with high-volume data ingestion and horizontal scaling needs')
    
    # Add ServiceNow trauma context
    framework.add_context('serviceNow_trauma', 'Platform rigidity led to 6-month failed evaluation')
    framework.add_context('customization_priority', 'Critical - must avoid another ServiceNow situation')
    
    # Calculate decision
    decision = framework.calculate_decision()
    
    print("🎯 FRAMEWORK RECOMMENDATION:")
    print("=" * 60)
    print(f"🏆 Database: {decision.recommendation.value}")
    print(f"📊 Confidence: {decision.confidence_level}")
    print(f"💯 MongoDB Score: {decision.mongodb_total_score:.2f}")
    print(f"💯 PostgreSQL Score: {decision.postgresql_total_score:.2f}")
    
    percentage = (decision.mongodb_total_score / (decision.mongodb_total_score + decision.postgresql_total_score)) * 100
    print(f"📈 MongoDB Advantage: {percentage:.1f}%")
    print()
    
    print("🛡️ SERVICENOW TRAUMA RECOVERY:")
    print("-" * 40)
    print("✅ Maximum schema flexibility - no rigid platform constraints")
    print("✅ Document model supports complex business logic without limits")
    print("✅ Full customization freedom - no maintenance burden warnings")  
    print("✅ JSON-native development matches team expertise")
    print("✅ Horizontal scaling prevents future bottlenecks")
    print()
    
    # Generate ADR
    print("📄 GENERATING ADR...")
    os.makedirs("output", exist_ok=True)
    adr_path = adr_generator.save_adr(decision, "Your Custom Application", output_dir="output")
    print(f"✓ ADR created: {adr_path}")
    print()
    
    # Show key ADR sections
    with open(adr_path, 'r') as f:
        content = f.read()
    
    # Extract decision section
    lines = content.split('\n')
    in_decision = False
    for line in lines:
        if line.startswith('## Decision'):
            in_decision = True
            print("📋 ADR DECISION EXCERPT:")
            print("-" * 30)
        elif in_decision and line.startswith('## Rationale'):
            break
        
        if in_decision:
            print(line)
    
    print("\n🚀 YOUR NEXT STEPS:")
    print("=" * 40)
    print("1. 🧪 Create MongoDB proof-of-concept with your data models")
    print("2. 👥 Share ADR with team - emphasize ServiceNow trauma recovery")
    print("3. 🏗️ Plan MongoDB infrastructure (Atlas vs self-hosted)")
    print("4. 📚 Team MongoDB training (focus on schema design patterns)")
    print("5. 🔄 Design SharePoint migration strategy")
    print("6. 📊 Set up monitoring and operational procedures")
    print()
    print("🎯 Key Success Factors:")
    print("   • Schema governance despite flexibility")
    print("   • Document design patterns for your use cases")  
    print("   • Team MongoDB operational expertise")
    print("   • Performance monitoring and optimization")
    
    return decision

if __name__ == "__main__":
    run_mongodb_experience()
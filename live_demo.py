#!/usr/bin/env python3
"""
Live Interactive Demo - Shows Realistic Usage
Simulates the complete user experience with your actual project context
"""

import time
import os
from framework import DatabaseFramework
from questions import QuestionSet
from adr_generator import ADRGenerator

def print_slow(text, delay=0.03):
    """Print text with typewriter effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def print_header():
    """Print application header with style"""
    print("\n" + "="*80)
    print_slow("🎯 DATABASE SELECTION FRAMEWORK", 0.05)
    print_slow("   MongoDB vs PostgreSQL Decision Engine", 0.03)
    print("="*80)
    print()
    print_slow("Born from platform rigidity concerns - helping you choose the right database")
    print_slow("with clear reasoning and team consensus capabilities.")
    print()

def simulate_user_input(prompt, response, delay=1.0):
    """Simulate user typing with realistic delay"""
    print_slow(prompt, 0.02)
    time.sleep(delay)
    print_slow(f"👤 {response}", 0.04)
    return response

def run_live_demo():
    """Run a complete live demo with realistic responses"""
    
    print_header()
    
    # Project setup
    print_slow("📋 PROJECT SETUP", 0.04)
    print("-" * 40)
    
    project_name = simulate_user_input(
        "Project name (Enter for 'Custom Application'): ",
        "Database Selection Framework Migration",
        1.0
    )
    
    migration_source = simulate_user_input(
        "\nMigrating from (e.g., SharePoint, previous platform): ",
        "SharePoint (after platform limitations)",
        0.8
    )
    
    team_size = simulate_user_input(
        "Team size: ",
        "5 developers",
        0.6
    )
    
    print()
    print_slow("✓ Project: Database Selection Framework Migration")
    print_slow("✓ Migrating from: SharePoint (after platform limitations)")
    print()
    
    time.sleep(1)
    
    # Initialize framework
    framework = DatabaseFramework()
    question_set = QuestionSet()
    adr_generator = ADRGenerator()
    
    # Add context
    framework.add_context('migration_source', migration_source)
    framework.add_context('team_size', team_size)
    framework.add_context('platform_trauma', 'Platform rigidity led to 6-month failed evaluation')
    
    # Core assessment
    print_slow("📊 CORE ASSESSMENT", 0.04)
    print("="*80)
    print_slow("The framework will ask 5 core questions that drive your database decision.")
    print_slow("Each question is weighted based on impact on the final choice.")
    print()
    time.sleep(2)
    
    # Question responses based on your project context
    questions_and_responses = [
        {
            'question': question_set.get_question('schema_evolution'),
            'response_key': 'somewhat_predictable',
            'user_reasoning': 'Moving from SharePoint, expect some evolution but within patterns'
        },
        {
            'question': question_set.get_question('query_patterns'), 
            'response_key': 'mixed_patterns',
            'user_reasoning': 'Decision framework tool needs various data access patterns'
        },
        {
            'question': question_set.get_question('team_expertise'),
            'response_key': 'mixed_skills',
            'user_reasoning': 'Team has varied background, willing to learn new technologies'
        },
        {
            'question': question_set.get_question('consistency_needs'),
            'response_key': 'mostly_consistent',
            'user_reasoning': 'Decision data integrity matters but some flexibility acceptable'
        },
        {
            'question': question_set.get_question('performance_profile'),
            'response_key': 'balanced_load',
            'user_reasoning': 'Internal tool, moderate usage expected'
        }
    ]
    
    for i, q_data in enumerate(questions_and_responses, 1):
        question = q_data['question']
        response_key = q_data['response_key']
        user_reasoning = q_data['user_reasoning']
        
        weight = framework.weights.get(question.id, 0) * 100
        
        print(f"\n[Question {i}/5] Weight: {weight:.0f}%")
        print("\n" + "="*60)
        print_slow("🤔 QUESTION", 0.04)
        print("-" * 60)
        print_slow(question.text, 0.02)
        
        print(f"\n💡 Why this matters:")
        context_lines = [line.strip() for line in question.context.strip().split('\n') if line.strip() and not line.strip().startswith('"""')]
        for line in context_lines[:2]:  # Show first 2 context lines
            if line:
                print_slow(f"   {line}", 0.015)
        
        print(f"\n📝 Options:")
        for j, option in enumerate(question.options, 1):
            print_slow(f"   {j}. {option.text}", 0.02)
        
        # Find the selected option
        selected_option = next(opt for opt in question.options if opt.key == response_key)
        option_number = next(j for j, opt in enumerate(question.options, 1) if opt.key == response_key)
        
        time.sleep(1.5)
        user_choice = simulate_user_input(
            f"\n👉 Select option (1-{len(question.options)}): ",
            str(option_number),
            0.8
        )
        
        print_slow(f"✓ Selected: {selected_option.text}", 0.03)
        print_slow(f"💭 Your reasoning: {user_reasoning}", 0.025)
        
        # Add to framework
        framework.add_response(
            question_id=question.id,
            question_text=question.text,
            response_key=response_key,
            response_text=selected_option.text
        )
        
        time.sleep(1)
    
    # Follow-up question prompt
    print(f"\n🔍 FOLLOW-UP QUESTIONS")
    print("="*60) 
    print_slow("Based on your responses, we have follow-up questions to refine the recommendation.")
    print_slow("These are optional and help improve accuracy.")
    
    follow_up_choice = simulate_user_input(
        "\nProceed with follow-up questions? (y/n, default=y): ",
        "y",
        0.8
    )
    
    # Add one follow-up for demonstration
    if follow_up_choice.lower() != 'n':
        follow_up_q = question_set.get_question('migration_complexity')
        if follow_up_q:
            print(f"\n[Follow-up 1/1]")
            print("\n" + "="*60)
            print_slow("🔍 FOLLOW-UP QUESTION", 0.04)
            print("-" * 60)
            print_slow(follow_up_q.text, 0.02)
            
            print(f"\n📝 Options:")
            for j, option in enumerate(follow_up_q.options, 1):
                print_slow(f"   {j}. {option.text}", 0.02)
            
            time.sleep(1)
            follow_up_choice = simulate_user_input(
                f"\n👉 Select option (1-{len(follow_up_q.options)}): ",
                "2",  # somewhat_comfortable
                0.8
            )
            
            selected_option = follow_up_q.options[1]  # somewhat_comfortable
            print_slow(f"✓ Selected: {selected_option.text}", 0.03)
            
            # Add follow-up with reduced weight
            framework.weights[follow_up_q.id] = 0.05  # Lower weight for follow-ups
            framework.add_response(
                question_id=follow_up_q.id,
                question_text=follow_up_q.text,
                response_key='somewhat_comfortable',
                response_text=selected_option.text
            )
    
    time.sleep(2)
    
    # Calculate decision
    print_slow("\n🧮 CALCULATING RECOMMENDATION...", 0.05)
    time.sleep(2)
    
    decision = framework.calculate_decision()
    
    # Display results
    print("\n" + "="*80)
    print_slow("🎯 RECOMMENDATION", 0.05)
    print("="*80)
    
    # Main recommendation with style
    if decision.recommendation.value == 'MongoDB':
        print_slow("🟢 RECOMMENDATION: **MongoDB**", 0.04)
    elif decision.recommendation.value == 'PostgreSQL':
        print_slow("🔵 RECOMMENDATION: **PostgreSQL**", 0.04)  
    else:
        print_slow("⚪ RECOMMENDATION: **Neutral - Requires Further Analysis**", 0.04)
    
    print_slow(f"📊 Confidence Level: {decision.confidence_level}", 0.03)
    print()
    
    # Scoring breakdown
    total_score = decision.mongodb_total_score + decision.postgresql_total_score
    if total_score > 0:
        mongodb_pct = (decision.mongodb_total_score / total_score) * 100
        postgresql_pct = (decision.postgresql_total_score / total_score) * 100
    else:
        mongodb_pct = postgresql_pct = 50
    
    print_slow("📈 SCORING BREAKDOWN:", 0.04)
    print_slow(f"   MongoDB:    {decision.mongodb_total_score:.2f} points ({mongodb_pct:.1f}%)", 0.03)  
    print_slow(f"   PostgreSQL: {decision.postgresql_total_score:.2f} points ({postgresql_pct:.1f}%)", 0.03)
    print()
    
    time.sleep(1)
    
    # Top factors
    print_slow("🔑 TOP DECISION FACTORS:", 0.04)
    print("-" * 40)
    sorted_responses = sorted(decision.responses, key=lambda r: r.weight, reverse=True)
    
    for i, response in enumerate(sorted_responses[:3], 1):
        weight_pct = response.weight * 100
        print_slow(f"{i}. {response.question_text}", 0.025)
        print_slow(f"   Weight: {weight_pct:.0f}% | Your answer: {response.response}", 0.02)
        print_slow(f"   Impact: {response.rationale}", 0.02)
        print()
        time.sleep(0.5)
    
    # previous platform recovery message
    print_slow("🛡️ platform rigidity concerns RECOVERY:", 0.04)
    print("-" * 40)
    
    if decision.recommendation.value == 'MongoDB':
        print_slow("✅ MongoDB directly addresses platform limitations:", 0.03)
        print_slow("   • Maximum schema flexibility - no rigid platform constraints", 0.025)
        print_slow("   • Document model enables unlimited business logic customization", 0.025)
        print_slow("   • JSON-native development with full team control", 0.025)
        print_slow("   • Horizontal scaling prevents future bottlenecks", 0.025)
    elif decision.recommendation.value == 'PostgreSQL':
        print_slow("✅ PostgreSQL addresses platform limitations differently:", 0.03)
        print_slow("   • Open source eliminates vendor lock-in concerns", 0.025)
        print_slow("   • JSON capabilities provide document flexibility when needed", 0.025)  
        print_slow("   • Standard SQL avoids proprietary platform constraints", 0.025)
        print_slow("   • Mature ecosystem with extensive customization freedom", 0.025)
    else:
        print_slow("⚖️ Both options address platform rigidity concerns:", 0.03)
        print_slow("   • Either choice provides full customization freedom", 0.025)
        print_slow("   • Open source options eliminate vendor lock-in", 0.025) 
        print_slow("   • Both avoid previous platform's rigidity problems", 0.025)
        print_slow("   • Recommend technical spikes to make final choice", 0.025)
    
    print()
    time.sleep(2)
    
    # Session saving
    save_session = simulate_user_input(
        "💾 Save session for team review? (y/n, default=y): ",
        "y",
        1.0
    )
    
    if save_session.lower() != 'n':
        os.makedirs("sessions", exist_ok=True)
        session_file = f"sessions/live_demo_session.json"
        framework.save_session(session_file)
        print_slow(f"✓ Session saved: {session_file}", 0.03)
        print_slow("📤 Share this file with your team for collaborative review", 0.025)
    
    time.sleep(1)
    
    # ADR generation
    generate_adr = simulate_user_input(
        "\n📄 Generate ADR (Architecture Decision Record)? (y/n, default=y): ",
        "y",
        1.0
    )
    
    if generate_adr.lower() != 'n':
        os.makedirs("output", exist_ok=True)
        adr_path = adr_generator.save_adr(decision, project_name, output_dir="output")
        print_slow(f"✓ ADR generated: {adr_path}", 0.03)
        print()
        print_slow("📋 ADR includes:", 0.03)
        print_slow("   • platform experience lessons context", 0.025)
        print_slow("   • Complete decision rationale", 0.025) 
        print_slow("   • Implementation recommendations", 0.025)
        print_slow("   • Risk assessment and mitigation", 0.025)
        print_slow("   • Team consensus documentation", 0.025)
    
    time.sleep(1)
    
    # Next steps
    print_slow(f"\n🚀 RECOMMENDED NEXT STEPS:", 0.04)
    print("="*60)
    
    if decision.recommendation.value == 'Neutral/Requires Further Analysis':
        steps = [
            "🧪 Create parallel technical spikes with MongoDB and PostgreSQL",
            "👥 Team evaluation sessions with hands-on experience", 
            "📊 Performance testing with representative data",
            "🤝 Final team decision meeting with spike results",
            "📄 Update ADR with final choice and rationale"
        ]
    else:
        db_name = decision.recommendation.value
        steps = [
            f"🧪 Create {db_name} proof-of-concept with your data models",
            f"👥 Share ADR with team - emphasize platform rigidity concerns recovery",
            f"🏗️ Plan {db_name} infrastructure and deployment strategy",
            f"📚 Identify {db_name} training needs for your team",
            f"🔄 Design migration strategy from SharePoint",
            f"📊 Set up monitoring and operational procedures"
        ]
    
    for i, step in enumerate(steps, 1):
        print_slow(f"{i}. {step}", 0.025)
        time.sleep(0.3)
    
    print()
    print_slow("💡 Remember: This framework can be re-run as requirements evolve!", 0.03)
    
    time.sleep(1)
    
    print_slow(f"\n✅ FRAMEWORK COMPLETE!", 0.04)
    print("="*80)
    print_slow("🎯 You now have a clear database recommendation with full rationale", 0.025)
    print_slow("📄 Generated ADR provides team consensus documentation", 0.025)  
    print_slow("💾 Session file enables collaborative team review", 0.025)
    print_slow("🛡️ platform rigidity concerns explicitly addressed throughout", 0.025)
    
    if os.path.exists("output") and any(f.endswith('.md') for f in os.listdir("output")):
        print()
        print_slow("📁 Generated files you can review:", 0.03)
        for file in os.listdir("output"):
            if file.endswith('.md'):
                print_slow(f"   📄 output/{file}", 0.025)
    
    print()
    print_slow("👋 Thanks for using the Database Selection Framework!", 0.03)
    return decision

if __name__ == "__main__":
    run_live_demo()
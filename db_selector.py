#!/usr/bin/env python3
"""
Generic Database Selection Tool

Interactive CLI for database comparison with vendor selection and guided examples.
Supports any combination of databases with comprehensive user guidance.
"""

import argparse
import sys
import os
import json
from typing import List, Dict, Any
from datetime import datetime

# Import our framework components
from database_vendors import database_registry
from generic_questions import guided_questions 
from generic_framework import GenericDatabaseFramework, create_comparison

def print_header():
    """Print application header"""
    print("\n" + "="*80)
    print("🎯 DATABASE SELECTION FRAMEWORK")
    print("   Multi-Vendor Database Comparison Engine")
    print("="*80)
    print("Smart database selection with guided analysis and team consensus")
    print()

def display_database_options():
    """Display available database options"""
    vendors = database_registry.get_all_vendors()
    
    print("📊 AVAILABLE DATABASES")
    print("-" * 40)
    
    categories = {}
    for vendor in vendors.values():
        category = vendor.category.value
        if category not in categories:
            categories[category] = []
        categories[category].append(vendor)
    
    for category, vendor_list in categories.items():
        print(f"\n🗂️  {category.title()} Databases:")
        for vendor in vendor_list:
            print(f"   {vendor.id:12} - {vendor.name}")
            print(f"              {vendor.description}")
        
def get_database_selection() -> List[str]:
    """Interactive database selection"""
    vendors = database_registry.get_all_vendors()
    suggestions = database_registry.get_vendor_comparison_pairs()
    
    print("🔍 DATABASE SELECTION")
    print("-" * 40)
    print("Choose databases to compare (2-5 databases recommended)")
    print()
    
    # Show suggestions
    print("💡 Popular Comparisons:")
    for i, suggestion in enumerate(suggestions[:5], 1):
        names = [vendors[db_id].name for db_id in suggestion if db_id in vendors]
        print(f"   {i}. {' vs '.join(names)}")
    
    print(f"\n📋 Available databases: {', '.join(sorted(vendors.keys()))}")
    print()
    
    while True:
        choice = input("👉 Select option (1-5) or enter database IDs (e.g., 'postgresql mongodb'): ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(suggestions):
            # Use suggestion
            selected_ids = suggestions[int(choice) - 1]
            break
        else:
            # Parse manual input
            selected_ids = [db_id.strip() for db_id in choice.split()]
            
            # Validate all IDs
            invalid_ids = [db_id for db_id in selected_ids if db_id not in vendors]
            if invalid_ids:
                print(f"❌ Unknown databases: {', '.join(invalid_ids)}")
                continue
                
            if len(selected_ids) < 2:
                print("❌ Please select at least 2 databases to compare")
                continue
                
            if len(selected_ids) > 5:
                print("❌ Please select at most 5 databases for manageable comparison")
                continue
                
            break
    
    # Confirm selection
    selected_names = [vendors[db_id].name for db_id in selected_ids]
    print(f"\n✅ Comparing: {' vs '.join(selected_names)}")
    return selected_ids

def display_question_guidance(question, option_examples=None):
    """Display comprehensive question guidance"""
    print("\n" + "="*70)
    print("🤔 QUESTION")
    print("-" * 70)
    print(f"{question.text}")
    
    print(f"\n💡 Why this matters:")
    print(f"   {question.description}")
    
    print(f"\n🧭 How to think about this:")
    print(f"   {question.guidance}")
    
    if question.examples:
        print(f"\n🎯 Example scenarios:")
        for key, example in list(question.examples.items())[:3]:
            print(f"   • {example}")
    
    print(f"\n📝 Your options:")
    for i, option in enumerate(question.options, 1):
        print(f"\n   {i}. {option.text}")
        print(f"      📖 {option.explanation}")
        
        if option.examples:
            print(f"      🏷️  Examples: {option.examples[0]}")
        
        if option.considerations:
            print(f"      🤔 Consider: {option.considerations[0]}")
    
    weight_pct = question.weight * 100
    print(f"\n⚖️  Decision weight: {weight_pct:.0f}%")

def conduct_assessment(framework: GenericDatabaseFramework, project_name: str = "Database Selection"):
    """Conduct interactive assessment"""
    print(f"\n📊 ASSESSMENT: {project_name}")
    print("="*70)
    
    # Get core questions
    core_questions = guided_questions.get_core_questions()
    total_questions = len(core_questions)
    
    print(f"We'll ask {total_questions} core questions to guide your database selection.")
    print("Each question includes examples and guidance to help you think through your answer.")
    print()
    
    for i, question in enumerate(core_questions, 1):
        print(f"\n[Question {i}/{total_questions}]")
        display_question_guidance(question)
        
        # Get user choice
        while True:
            try:
                choice = input(f"\n👉 Select option (1-{len(question.options)}): ").strip()
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(question.options):
                    selected_option = question.options[choice_num - 1]
                    break
                else:
                    print(f"❌ Please enter a number between 1 and {len(question.options)}")
            except (ValueError, KeyboardInterrupt):
                print("❌ Please enter a valid number")
                continue
        
        # Confirm selection and ask for reasoning
        print(f"\n✅ Selected: {selected_option.text}")
        reasoning = input("💭 Optional - Share your reasoning (press Enter to skip): ").strip()
        
        # Add to framework
        framework.add_response(
            question_id=question.id,
            question_text=question.text,
            response_key=selected_option.key,
            response_text=selected_option.text
        )
        
        if reasoning:
            framework.add_context(f"{question.id}_reasoning", reasoning)
        
        print(f"📊 Progress: {i}/{total_questions} complete")
    
    # Ask about follow-up questions
    print(f"\n🔍 FOLLOW-UP QUESTIONS")
    print("="*60)
    print("Based on your responses, we can ask additional questions to refine the recommendation.")
    print("Follow-up questions are optional and help improve accuracy.")
    
    follow_up_choice = input("\nProceed with follow-up questions? (y/n, default=n): ").strip().lower()
    
    if follow_up_choice == 'y':
        # This could be expanded to show relevant follow-ups
        print("📈 Follow-up questions would help refine the analysis further.")
        print("💡 For now, we'll proceed with the core assessment.")
    
    return framework

def display_results(comparison, database_names):
    """Display comparison results"""
    print("\n" + "="*80)
    print("🎯 DATABASE COMPARISON RESULTS")
    print("="*80)
    
    # Main recommendation
    if comparison.recommendation:
        recommended_db = comparison.database_scores[comparison.recommendation]
        print(f"🏆 RECOMMENDATION: {recommended_db.database_name}")
    else:
        print("⚖️  RESULT: Requires Further Analysis")
    
    print(f"📊 Confidence: {comparison.confidence_level.value}")
    print()
    
    # Scoring breakdown
    print("📈 SCORING BREAKDOWN")
    print("-" * 50)
    sorted_scores = sorted(comparison.database_scores.items(), 
                          key=lambda x: x[1].total_score, reverse=True)
    
    for db_id, score in sorted_scores:
        print(f"   {score.database_name:12} {score.total_score:6.2f} points ({score.percentage:5.1f}%)")
    print()
    
    # Top decision factors
    print("🔑 TOP DECISION FACTORS")
    print("-" * 50)
    sorted_responses = sorted(comparison.responses, key=lambda r: r.weight, reverse=True)
    
    for i, response in enumerate(sorted_responses[:3], 1):
        weight_pct = response.weight * 100
        print(f"{i}. {response.question_text}")
        print(f"   Weight: {weight_pct:.0f}% | Your answer: {response.response_text}")
        print(f"   Impact: {response.rationale}")
        print()
    
    # Database strengths summary
    print("💪 DATABASE STRENGTHS SUMMARY")
    print("-" * 50)
    vendors = database_registry.get_all_vendors()
    
    for db_id in comparison.databases:
        if db_id in vendors:
            vendor = vendors[db_id]
            score = comparison.database_scores[db_id]
            print(f"\n📊 {vendor.name} ({score.percentage:.1f}%)")
            for strength in vendor.strengths[:3]:
                print(f"   ✅ {strength}")
    
    # Next steps
    print(f"\n🚀 RECOMMENDED NEXT STEPS")
    print("="*60)
    
    if comparison.recommendation:
        recommended_vendor = vendors[comparison.recommendation]
        print(f"1. 🧪 Create proof-of-concept with {recommended_vendor.name}")
        print(f"2. 👥 Share results with your team for consensus")
        print(f"3. 🏗️  Plan infrastructure and deployment strategy")
        print(f"4. 📚 Identify training needs for {recommended_vendor.name}")
        print(f"5. 📊 Set up monitoring and operational procedures")
    else:
        db_names = [vendors[db_id].name for db_id in comparison.databases[:2]]
        print(f"1. 🧪 Create parallel technical spikes with {' and '.join(db_names)}")
        print(f"2. 👥 Team evaluation sessions with hands-on experience")
        print(f"3. 📊 Performance testing with representative data")
        print(f"4. 🤝 Final team decision meeting with spike results")
        print(f"5. 📄 Update documentation with final choice")
    
    print(f"\n💡 Remember: This framework can be re-run as requirements evolve!")

def save_session_prompt(framework: GenericDatabaseFramework):
    """Prompt to save session"""
    save_choice = input(f"\n💾 Save session for team review? (y/n, default=y): ").strip().lower()
    
    if save_choice != 'n':
        os.makedirs("sessions", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_file = f"sessions/session_{timestamp}.json"
        
        framework.save_session(session_file)
        print(f"✅ Session saved: {session_file}")
        print("📤 Share this file with your team for collaborative review")
        return session_file
    
    return None

def interactive_assessment():
    """Run interactive assessment"""
    print_header()
    
    # Get project context
    project_name = input("Project name (default: 'Database Selection'): ").strip()
    if not project_name:
        project_name = "Database Selection"
    
    # Database selection
    database_ids = get_database_selection()
    
    # Create framework
    framework = create_comparison(database_ids)
    framework.add_context('project_name', project_name)
    framework.add_context('interface', 'cli')
    
    # Conduct assessment  
    framework = conduct_assessment(framework, project_name)
    
    # Calculate results
    comparison = framework.calculate_comparison()
    
    # Display results
    database_names = [database_registry.get_vendor(db_id).name for db_id in database_ids]
    display_results(comparison, database_names)
    
    # Save session
    session_file = save_session_prompt(framework)
    
    print(f"\n✅ ASSESSMENT COMPLETE!")
    print("="*80)
    print("🎯 You now have a data-driven database recommendation")
    print("📊 Results are based on weighted analysis of your specific requirements") 
    print("👥 Use the session file for team collaboration and consensus building")
    print()
    
    return comparison

def load_session(session_file: str):
    """Load and display previous session"""
    if not os.path.exists(session_file):
        print(f"❌ Session file not found: {session_file}")
        return
    
    print_header()
    print(f"📂 LOADING SESSION: {session_file}")
    print("-" * 60)
    
    # Load framework
    framework = GenericDatabaseFramework()
    framework.load_session(session_file)
    
    # Recalculate comparison
    comparison = framework.calculate_comparison()
    
    # Display results
    database_names = [database_registry.get_vendor(db_id).name for db_id in framework.database_ids]
    display_results(comparison, database_names)

def show_help():
    """Show detailed help information"""
    print_header()
    print("📖 HELP & USAGE GUIDE")
    print("="*60)
    
    print("🚀 Quick Start:")
    print("   python3 db_selector.py assess         # Start new assessment")
    print("   python3 db_selector.py load <file>    # Load previous session")
    print()
    
    print("🗂️  Commands:")
    print("   assess     - Interactive database comparison")
    print("   load       - Load previous session")
    print("   databases  - List available databases")
    print("   help       - Show this help")
    print()
    
    print("💡 Tips:")
    print("   • Choose 2-5 databases for comparison")
    print("   • Read question guidance carefully")
    print("   • Save sessions to share with your team")
    print("   • Re-run assessments as requirements change")
    print()
    
    print("🔧 Framework Features:")
    print("   • Multi-vendor database comparison")
    print("   • Guided questions with examples")
    print("   • Weighted scoring system")
    print("   • Team collaboration through session files")
    print("   • Extensible architecture")
    print()

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Generic Database Selection Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 db_selector.py assess                    # Start interactive assessment
  python3 db_selector.py load sessions/my.json    # Load previous session
  python3 db_selector.py databases                # List available databases
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Assessment command
    assess_parser = subparsers.add_parser('assess', help='Start database assessment')
    assess_parser.add_argument('--project', help='Project name')
    
    # Load command
    load_parser = subparsers.add_parser('load', help='Load previous session')
    load_parser.add_argument('session_file', help='Path to session file')
    
    # Databases command
    subparsers.add_parser('databases', help='List available databases')
    
    # Help command
    subparsers.add_parser('help', help='Show detailed help')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'assess' or args.command is None:
            interactive_assessment()
        elif args.command == 'load':
            load_session(args.session_file)
        elif args.command == 'databases':
            print_header()
            display_database_options()
        elif args.command == 'help':
            show_help()
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        print(f"\n\n👋 Database selection interrupted. Your progress has been saved.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("💡 Run with 'help' command for usage information")
        sys.exit(1)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Database Selection Framework - Interactive CLI Application

A production-ready command-line tool for MongoDB vs PostgreSQL selection
with team collaboration and ADR generation capabilities.
"""

import argparse
import sys
import os
import json
from typing import Optional, List, Dict
from datetime import datetime

from framework import DatabaseFramework, DecisionResult, DatabaseChoice
from questions import QuestionSet, Question, QuestionOption
from adr_generator import ADRGenerator

class DatabaseSelector:
    """Main application class for database selection"""
    
    def __init__(self):
        self.framework = DatabaseFramework()
        self.question_set = QuestionSet()
        self.adr_generator = ADRGenerator()
        self.project_name = "Custom Application"
        self.session_name = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
    def print_header(self):
        """Print application header"""
        print("\n" + "="*80)
        print("🎯 DATABASE SELECTION FRAMEWORK")
        print("   MongoDB vs PostgreSQL Decision Engine")
        print("="*80)
        print()
        print("Born from platform rigidity concerns - helping you choose the right database")
        print("with clear reasoning and team consensus capabilities.")
        print()
    
    def print_help(self):
        """Print detailed help information"""
        help_text = """
🔧 USAGE EXAMPLES:
  
  Interactive Assessment:
  python3 database_selector.py assess
  python3 database_selector.py assess --project "My Application"
  
  Load Previous Session:  
  python3 database_selector.py load sessions/my_session.json
  
  Demo Scenarios:
  python3 database_selector.py demo
  python3 database_selector.py demo --scenario mongodb
  python3 database_selector.py demo --scenario postgresql
  python3 database_selector.py demo --scenario neutral
  
  Generate ADR from Session:
  python3 database_selector.py adr sessions/my_session.json
  
📁 FILE STRUCTURE:
  output/          # Generated ADR documents
  sessions/        # Session files for team collaboration
  demo_output/     # Example outputs from demo scenarios
  
🎯 FRAMEWORK FEATURES:
  • 4-5 core questions drive 80% of decision
  • Weighted scoring: Schema(25%) + Queries(25%) + Team(20%) + Consistency(15%) + Performance(15%)  
  • platform rigidity concerns recovery built-in
  • ADR generation for team consensus
  • Session saving for collaboration
  
🛡️ previous platform PAIN POINT MITIGATION:
  • Schema flexibility prioritized (25% weight)
  • Customization freedom emphasized  
  • Open source options only (no vendor lock-in)
  • Team expertise considered (20% weight)
        """
        print(help_text)
    
    def get_project_info(self) -> Dict[str, str]:
        """Get project context information"""
        print("📋 PROJECT SETUP")
        print("-" * 40)
        
        try:
            project_name = input("Project name (Enter for 'Custom Application'): ").strip()
            if project_name:
                self.project_name = project_name
            
            # Optional context
            print("\nOptional context (press Enter to skip):")
            migration_source = input("Migrating from (e.g., SharePoint, previous platform): ").strip()
            team_size = input("Team size: ").strip()
            timeline = input("Project timeline: ").strip()
            
            context = {
                'project_name': self.project_name,
                'migration_source': migration_source,
                'team_size': team_size, 
                'timeline': timeline
            }
            
            # Add to framework
            if migration_source:
                self.framework.add_context('migration_source', migration_source)
            if team_size:
                self.framework.add_context('team_size', team_size)
            if timeline:
                self.framework.add_context('timeline', timeline)
            
            print(f"\n✓ Project: {self.project_name}")
            if migration_source:
                print(f"✓ Migrating from: {migration_source}")
            
            return context
            
        except KeyboardInterrupt:
            print("\n\n❌ Setup cancelled by user")
            sys.exit(0)
    
    def ask_question(self, question: Question) -> str:
        """Ask a single question and get response"""
        print("\n" + "="*60)
        print("🤔 QUESTION")
        print("-" * 60)
        print(f"{question.text}")
        
        if question.context.strip():
            print("\n💡 Why this matters:")
            context_lines = [line.strip() for line in question.context.strip().split('\n') if line.strip()]
            for line in context_lines:
                if line and not line.startswith('"""'):
                    print(f"   {line}")
        
        print(f"\n📝 Options:")
        for i, option in enumerate(question.options, 1):
            print(f"   {i}. {option.text}")
        
        # Get user selection
        while True:
            try:
                choice = input(f"\n👉 Select option (1-{len(question.options)}, or 'q' to quit): ").strip().lower()
                
                if choice == 'q':
                    raise KeyboardInterrupt
                    
                choice_num = int(choice)
                if 1 <= choice_num <= len(question.options):
                    selected_option = question.options[choice_num - 1]
                    print(f"✓ Selected: {selected_option.text}")
                    return selected_option.key
                else:
                    print(f"❌ Please enter a number between 1 and {len(question.options)}")
            except ValueError:
                if choice != 'q':
                    print("❌ Please enter a valid number or 'q' to quit")
            except KeyboardInterrupt:
                print("\n\n❌ Assessment cancelled by user")
                sys.exit(0)
    
    def run_assessment(self) -> DecisionResult:
        """Run the complete assessment"""
        print("📊 CORE ASSESSMENT")
        print("="*80)
        print("The framework will ask 5 core questions that drive your database decision.")
        print("Each question is weighted based on impact on the final choice.")
        print()
        
        # Get project context
        self.get_project_info()
        
        # Add previous platform context marker
        self.framework.add_context('framework_version', 'previous platform-trauma-informed v1.0')
        
        # Core questions
        core_questions = self.question_set.get_core_questions()
        follow_up_queue = []
        
        for i, question in enumerate(core_questions, 1):
            print(f"\n[Question {i}/{len(core_questions)}] Weight: {self.framework.weights.get(question.id, 0)*100:.0f}%")
            response_key = self.ask_question(question)
            
            # Add response to framework
            selected_option = next(opt for opt in question.options if opt.key == response_key)
            self.framework.add_response(
                question_id=question.id,
                question_text=question.text,
                response_key=response_key,
                response_text=selected_option.text
            )
            
            # Queue follow-up questions (limit to avoid overwhelming)
            follow_ups = self.question_set.get_follow_up_questions(response_key, question.id)
            if follow_ups:
                follow_up_queue.extend(follow_ups[:2])  # Max 2 follow-ups per question
        
        # Follow-up questions (optional)
        if follow_up_queue:
            print(f"\n🔍 FOLLOW-UP QUESTIONS")
            print("="*60) 
            print(f"Based on your responses, we have {len(follow_up_queue)} follow-up questions")
            print("to refine the recommendation. These are optional.")
            
            try:
                proceed = input("\nProceed with follow-up questions? (y/n, default=y): ").strip().lower()
                if proceed != 'n':
                    # Limit follow-ups to avoid fatigue
                    for i, question_id in enumerate(follow_up_queue[:3], 1):
                        question = self.question_set.get_question(question_id)
                        if question:
                            print(f"\n[Follow-up {i}/3]")
                            response_key = self.ask_question(question)
                            
                            selected_option = next(opt for opt in question.options if opt.key == response_key)
                            # Lower weight for follow-ups
                            original_weight = self.framework.weights.get(question.id, 0.05)  
                            self.framework.weights[question.id] = original_weight * 0.3
                            
                            self.framework.add_response(
                                question_id=question.id,
                                question_text=question.text,
                                response_key=response_key,
                                response_text=selected_option.text
                            )
            except KeyboardInterrupt:
                print("\n⏭️ Skipping follow-up questions...")
        
        # Calculate decision
        decision = self.framework.calculate_decision()
        return decision
    
    def display_results(self, decision: DecisionResult):
        """Display assessment results"""
        print("\n" + "="*80)
        print("🎯 RECOMMENDATION")
        print("="*80)
        
        # Main recommendation
        if decision.recommendation == DatabaseChoice.MONGODB:
            print("🟢 RECOMMENDATION: **MongoDB**")
        elif decision.recommendation == DatabaseChoice.POSTGRESQL:
            print("🔵 RECOMMENDATION: **PostgreSQL**")  
        else:
            print("⚪ RECOMMENDATION: **Neutral - Requires Further Analysis**")
        
        print(f"📊 Confidence Level: {decision.confidence_level}")
        print()
        
        # Scoring breakdown
        total_score = decision.mongodb_total_score + decision.postgresql_total_score
        if total_score > 0:
            mongodb_pct = (decision.mongodb_total_score / total_score) * 100
            postgresql_pct = (decision.postgresql_total_score / total_score) * 100
        else:
            mongodb_pct = postgresql_pct = 50
        
        print("📈 SCORING BREAKDOWN:")
        print(f"   MongoDB:    {decision.mongodb_total_score:.2f} points ({mongodb_pct:.1f}%)")  
        print(f"   PostgreSQL: {decision.postgresql_total_score:.2f} points ({postgresql_pct:.1f}%)")
        print()
        
        # Top factors
        print("🔑 TOP DECISION FACTORS:")
        print("-" * 40)
        sorted_responses = sorted(decision.responses, key=lambda r: r.weight, reverse=True)
        
        for i, response in enumerate(sorted_responses[:3], 1):
            weight_pct = response.weight * 100
            print(f"{i}. {response.question_text}")
            print(f"   Weight: {weight_pct:.0f}% | Your answer: {response.response}")
            print(f"   Impact: {response.rationale}")
            print()
        
        # previous platform recovery message
        print("🛡️ platform rigidity concerns RECOVERY:")
        print("-" * 40)
        
        if decision.recommendation == DatabaseChoice.MONGODB:
            print("✅ MongoDB directly addresses platform limitations:")
            print("   • Maximum schema flexibility - no rigid platform constraints")
            print("   • Document model enables unlimited business logic customization")
            print("   • JSON-native development with full team control")
            print("   • Horizontal scaling prevents future bottlenecks")
        elif decision.recommendation == DatabaseChoice.POSTGRESQL:
            print("✅ PostgreSQL addresses platform limitations differently:")
            print("   • Open source eliminates vendor lock-in concerns")
            print("   • JSON capabilities provide document flexibility when needed")  
            print("   • Standard SQL avoids proprietary platform constraints")
            print("   • Mature ecosystem with extensive customization freedom")
        else:
            print("⚖️ Both options address platform rigidity concerns:")
            print("   • Either choice provides full customization freedom")
            print("   • Open source options eliminate vendor lock-in") 
            print("   • Both avoid previous platform's rigidity problems")
            print("   • Recommend technical spikes to make final choice")
        
        print()
    
    def save_session_prompt(self) -> bool:
        """Prompt to save session"""
        try:
            save = input("💾 Save session for team review? (y/n, default=y): ").strip().lower()
            if save != 'n':
                os.makedirs("sessions", exist_ok=True)
                session_file = f"sessions/{self.session_name}.json"
                self.framework.save_session(session_file)
                print(f"✓ Session saved: {session_file}")
                print("📤 Share this file with your team for collaborative review")
                return True
            return False
        except KeyboardInterrupt:
            return False
    
    def generate_adr_prompt(self, decision: DecisionResult) -> bool:
        """Prompt to generate ADR"""
        try:
            generate = input("📄 Generate ADR (Architecture Decision Record)? (y/n, default=y): ").strip().lower()
            if generate != 'n':
                os.makedirs("output", exist_ok=True)
                adr_path = self.adr_generator.save_adr(decision, self.project_name, output_dir="output")
                print(f"✓ ADR generated: {adr_path}")
                print()
                print("📋 ADR includes:")
                print("   • platform experience lessons context")
                print("   • Complete decision rationale") 
                print("   • Implementation recommendations")
                print("   • Risk assessment and mitigation")
                print("   • Team consensus documentation")
                return True
            return False
        except KeyboardInterrupt:
            return False
    
    def show_next_steps(self, decision: DecisionResult):
        """Show next steps based on recommendation"""
        print("\n🚀 RECOMMENDED NEXT STEPS:")
        print("="*60)
        
        if decision.recommendation == DatabaseChoice.NEUTRAL:
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
                f"🔄 Design migration strategy from current system",
                f"📊 Set up monitoring and operational procedures"
            ]
        
        for i, step in enumerate(steps, 1):
            print(f"{i}. {step}")
        
        print(f"\n💡 Remember: This framework can be re-run as requirements evolve!")
    
    def load_session(self, filepath: str) -> DecisionResult:
        """Load and display a previous session"""
        try:
            self.framework.load_session(filepath)
            decision = self.framework.calculate_decision()
            
            print(f"📂 Loaded session: {filepath}")
            print(f"🗓️  Created: {decision.timestamp.strftime('%Y-%m-%d %H:%M')}")
            
            self.display_results(decision)
            return decision
            
        except FileNotFoundError:
            print(f"❌ Session file not found: {filepath}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"❌ Invalid session file format: {filepath}")
            sys.exit(1)
    
    def run_demo(self, scenario: str = "all"):
        """Run demo scenarios"""
        print("🎮 DEMO MODE - Database Selection Framework")
        print("="*80)
        
        if scenario == "all":
            print("Running all demo scenarios...")
            os.system("python3 demo.py")
        elif scenario == "mongodb":
            print("Running MongoDB-favoring scenario...")
            os.system("python3 experience_mongodb.py")  
        elif scenario == "postgresql":
            print("Running PostgreSQL-favoring scenario...")
            # Create quick PostgreSQL demo
            from demo import demo_postgresql_scenario
            framework, decision = demo_postgresql_scenario()
            self.display_results(decision)
        elif scenario == "neutral":
            print("Running neutral scenario...")
            from demo import demo_neutral_scenario
            framework, decision = demo_neutral_scenario()  
            self.display_results(decision)
        else:
            print(f"❌ Unknown scenario: {scenario}")
            print("Available scenarios: mongodb, postgresql, neutral, all")

def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(
        description='Database Selection Framework - MongoDB vs PostgreSQL',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python3 database_selector.py assess
  python3 database_selector.py assess --project "My App"
  python3 database_selector.py load sessions/my_session.json
  python3 database_selector.py demo --scenario mongodb
  python3 database_selector.py adr sessions/my_session.json
        '''
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Assessment command
    assess_parser = subparsers.add_parser('assess', help='Run interactive assessment')
    assess_parser.add_argument('--project', '-p', help='Project name')
    
    # Load session command
    load_parser = subparsers.add_parser('load', help='Load previous session')
    load_parser.add_argument('session_file', help='Path to session JSON file')
    
    # Demo command
    demo_parser = subparsers.add_parser('demo', help='Run demo scenarios')
    demo_parser.add_argument('--scenario', choices=['mongodb', 'postgresql', 'neutral', 'all'], 
                           default='all', help='Demo scenario to run')
    
    # ADR generation command
    adr_parser = subparsers.add_parser('adr', help='Generate ADR from session')
    adr_parser.add_argument('session_file', help='Path to session JSON file')
    adr_parser.add_argument('--project', '-p', help='Project name for ADR')
    
    # Help command
    subparsers.add_parser('help', help='Show detailed help')
    
    args = parser.parse_args()
    
    # Initialize application
    app = DatabaseSelector()
    
    try:
        if args.command == 'assess':
            app.print_header()
            if args.project:
                app.project_name = args.project
            
            decision = app.run_assessment()
            app.display_results(decision)
            app.save_session_prompt()
            app.generate_adr_prompt(decision)
            app.show_next_steps(decision)
            
        elif args.command == 'load':
            app.print_header()
            decision = app.load_session(args.session_file)
            
            # Offer to generate ADR
            app.generate_adr_prompt(decision)
            app.show_next_steps(decision)
            
        elif args.command == 'demo':
            app.run_demo(args.scenario)
            
        elif args.command == 'adr':
            app.print_header()
            decision = app.load_session(args.session_file)
            if args.project:
                app.project_name = args.project
            app.generate_adr_prompt(decision)
            
        elif args.command == 'help':
            app.print_header()
            app.print_help()
            
        else:
            app.print_header()
            parser.print_help()
            
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for using Database Selection Framework!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please report this issue for framework improvement.")
        sys.exit(1)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Interactive CLI for Database Selection Framework

Provides a smooth, user-friendly interface for the MongoDB vs PostgreSQL
decision framework with team collaboration features.
"""

import sys
import os
from typing import Dict, List, Optional
import json
from datetime import datetime

from framework import DatabaseFramework, DecisionResult
from questions import QuestionSet, Question, QuestionOption
from adr_generator import ADRGenerator

class InteractiveCLI:
    """Interactive command-line interface for database selection framework"""
    
    def __init__(self):
        self.framework = DatabaseFramework()
        self.question_set = QuestionSet()
        self.adr_generator = ADRGenerator()
        self.session_name = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.project_name = "Custom Application"
        
    def display_welcome(self):
        """Display welcome message and framework overview"""
        print("=" * 80)
        print("🎯 DATABASE SELECTION FRAMEWORK")
        print("   MongoDB vs PostgreSQL Decision Engine")
        print("=" * 80)
        print()
        print("This framework helps you choose between MongoDB and PostgreSQL based on")
        print("your specific requirements, team expertise, and lessons learned from")
        print("platform rigidity issues (like the previous platform experience).")
        print()
        print("The framework will:")
        print("• Ask 4-5 core questions about your project")
        print("• Provide follow-up questions based on your responses")
        print("• Generate a clear recommendation with rationale")
        print("• Create an ADR (Architecture Decision Record) for team consensus")
        print()
    
    def get_project_context(self):
        """Collect basic project information"""
        print("📋 PROJECT CONTEXT")
        print("-" * 40)
        
        project_name = input("Project name (press Enter for 'Custom Application'): ").strip()
        if project_name:
            self.project_name = project_name
            
        print(f"Project: {self.project_name}")
        print()
    
    def display_question(self, question: Question) -> str:
        """Display a question and collect response"""
        print("🤔 QUESTION")
        print("-" * 40)
        print(f"{question.text}")
        
        if question.context.strip():
            print()
            print("💡 Context:")
            # Clean up context formatting
            context_lines = [line.strip() for line in question.context.strip().split('\n') if line.strip()]
            for line in context_lines:
                if line:
                    print(f"   {line}")
        
        print()
        print("Options:")
        for i, option in enumerate(question.options, 1):
            print(f"   {i}. {option.text}")
        
        print()
        
        # Get user selection
        while True:
            try:
                choice = input(f"Select option (1-{len(question.options)}): ").strip()
                choice_num = int(choice)
                if 1 <= choice_num <= len(question.options):
                    selected_option = question.options[choice_num - 1]
                    print(f"✓ Selected: {selected_option.text}")
                    print()
                    return selected_option.key
                else:
                    print(f"❌ Please enter a number between 1 and {len(question.options)}")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def run_core_questions(self):
        """Run through the core questions"""
        print("📊 CORE ASSESSMENT")
        print("=" * 80)
        print("Let's start with the core questions that drive 80% of the database decision.")
        print()
        
        core_questions = self.question_set.get_core_questions()
        follow_up_queue = []
        
        for i, question in enumerate(core_questions, 1):
            print(f"[Question {i}/{len(core_questions)}]")
            response_key = self.display_question(question)
            
            # Add response to framework
            selected_option = next(opt for opt in question.options if opt.key == response_key)
            self.framework.add_response(
                question_id=question.id,
                question_text=question.text,
                response_key=response_key,
                response_text=selected_option.text
            )
            
            # Queue follow-up questions
            follow_ups = self.question_set.get_follow_up_questions(response_key, question.id)
            if follow_ups:
                follow_up_queue.extend(follow_ups)
                print(f"📌 Queued {len(follow_ups)} follow-up question(s) for later")
                print()
        
        return follow_up_queue
    
    def run_follow_up_questions(self, follow_up_queue: List[str]):
        """Run follow-up questions based on core responses"""
        if not follow_up_queue:
            return
        
        print("🔍 FOLLOW-UP QUESTIONS")
        print("=" * 80)
        print("Based on your responses, here are some additional questions to refine the recommendation.")
        print()
        
        # Limit follow-ups to avoid overwhelming the user
        max_follow_ups = min(3, len(follow_up_queue))
        
        for i, question_id in enumerate(follow_up_queue[:max_follow_ups], 1):
            question = self.question_set.get_question(question_id)
            if question:
                print(f"[Follow-up {i}/{max_follow_ups}]")
                response_key = self.display_question(question)
                
                # Add response to framework with lower weight
                selected_option = next(opt for opt in question.options if opt.key == response_key)
                # Follow-up questions get 50% weight of core questions
                original_weight = self.framework.weights.get(question.id, 0.05)
                self.framework.weights[question.id] = original_weight * 0.5
                
                self.framework.add_response(
                    question_id=question.id,
                    question_text=question.text,
                    response_key=response_key,
                    response_text=selected_option.text
                )
    
    def display_results(self, decision_result: DecisionResult):
        """Display the framework results"""
        print("🎯 RECOMMENDATION")
        print("=" * 80)
        
        # Calculate percentages for display
        total_score = decision_result.mongodb_total_score + decision_result.postgresql_total_score
        if total_score > 0:
            mongodb_pct = (decision_result.mongodb_total_score / total_score) * 100
            postgresql_pct = (decision_result.postgresql_total_score / total_score) * 100
        else:
            mongodb_pct = postgresql_pct = 50
        
        print(f"Recommendation: **{decision_result.recommendation.value}**")
        print(f"Confidence: {decision_result.confidence_level}")
        print()
        
        print("📊 SCORING BREAKDOWN")
        print(f"MongoDB:    {decision_result.mongodb_total_score:.2f} ({mongodb_pct:.1f}%)")
        print(f"PostgreSQL: {decision_result.postgresql_total_score:.2f} ({postgresql_pct:.1f}%)")
        print()
        
        # Show key factors
        print("🔑 KEY FACTORS")
        print("-" * 40)
        sorted_responses = sorted(decision_result.responses, key=lambda r: r.weight, reverse=True)
        
        for response in sorted_responses[:3]:  # Show top 3 factors
            weight_pct = response.weight * 100
            print(f"• {response.question_text}")
            print(f"  Weight: {weight_pct:.0f}% | Your response: {response.response}")
            print(f"  Impact: {response.rationale}")
            print()
        
        # previous platform context
        if decision_result.recommendation.value in ['MongoDB', 'PostgreSQL']:
            print("🛡️ platform rigidity concerns MITIGATION")
            print("-" * 40)
            if decision_result.recommendation.value == 'MongoDB':
                print("✓ Maximum schema flexibility - avoid rigid platform constraints")
                print("✓ Full customization freedom - no platform warnings about modifications")
                print("✓ Business logic implementation - no SPM-style limitations")
            else:
                print("✓ Structured flexibility - PostgreSQL offers more freedom than previous platform")
                print("✓ JSON capabilities - document features when needed")
                print("✓ Open source - no vendor lock-in concerns")
            print()
    
    def offer_adr_generation(self, decision_result: DecisionResult):
        """Offer to generate ADR document"""
        print("📄 DECISION DOCUMENTATION")
        print("-" * 40)
        
        generate_adr = input("Generate ADR (Architecture Decision Record)? (y/n): ").lower().startswith('y')
        
        if generate_adr:
            print("Generating ADR...")
            
            # Create output directory
            os.makedirs("output", exist_ok=True)
            
            # Generate and save ADR
            filepath = self.adr_generator.save_adr(
                decision_result, 
                self.project_name,
                output_dir="output"
            )
            
            print(f"✓ ADR generated: {filepath}")
            print()
            print("The ADR includes:")
            print("• Complete decision rationale")
            print("• platform experience lessons context")
            print("• Implementation considerations")
            print("• Team consensus documentation")
            print("• Consequences and trade-offs")
            
        return generate_adr
    
    def save_session(self, decision_result: DecisionResult):
        """Save session for team collaboration"""
        print("💾 SESSION SAVE")
        print("-" * 40)
        
        save_session = input("Save session for team review? (y/n): ").lower().startswith('y')
        
        if save_session:
            os.makedirs("sessions", exist_ok=True)
            session_file = f"sessions/{self.session_name}.json"
            self.framework.save_session(session_file)
            
            print(f"✓ Session saved: {session_file}")
            print("Team members can review and discuss the decision using this session file.")
        
        return save_session
    
    def display_next_steps(self):
        """Display recommended next steps"""
        print("🚀 NEXT STEPS")
        print("=" * 80)
        print("Recommended actions to move forward:")
        print()
        print("1. **Team Review**: Share the ADR with your development team")
        print("2. **Technical Spike**: Create a proof-of-concept with the recommended database")
        print("3. **Infrastructure Planning**: Define hosting and operational requirements")
        print("4. **Training Plan**: Identify any team training needs")
        print("5. **Migration Strategy**: Plan the transition from your current system")
        print()
        print("Remember: This decision can be revisited if requirements change significantly.")
        print("The framework can be re-run as your project evolves.")
    
    def run(self):
        """Run the complete interactive framework"""
        try:
            # Welcome and setup
            self.display_welcome()
            self.get_project_context()
            
            # Run questions
            follow_up_queue = self.run_core_questions()
            self.run_follow_up_questions(follow_up_queue)
            
            # Generate results
            decision_result = self.framework.calculate_decision()
            
            # Display results
            self.display_results(decision_result)
            
            # Generate documentation
            adr_generated = self.offer_adr_generation(decision_result)
            session_saved = self.save_session(decision_result)
            
            # Next steps
            self.display_next_steps()
            
            print("✅ Framework complete! Thank you for using the Database Selection Framework.")
            
        except KeyboardInterrupt:
            print("\n\n❌ Framework interrupted. Your progress has not been saved.")
            sys.exit(1)
        except Exception as e:
            print(f"\n\n❌ An error occurred: {e}")
            print("Please report this issue for framework improvement.")
            sys.exit(1)

def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == '--load-session':
        if len(sys.argv) < 3:
            print("Usage: python cli.py --load-session <session_file.json>")
            sys.exit(1)
        
        # TODO: Implement session loading for team collaboration
        print("Session loading feature coming soon!")
        sys.exit(0)
    
    # Run interactive framework
    cli = InteractiveCLI()
    cli.run()

if __name__ == "__main__":
    main()
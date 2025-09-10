"""
Question definitions and progressive interview logic for database selection framework.

This module contains the structured questions, branching logic, and follow-up 
questions based on the platform limitations and database selection criteria.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class QuestionOption:
    key: str
    text: str
    follow_up_questions: Optional[List[str]] = None

@dataclass
class Question:
    id: str
    text: str
    context: str
    options: List[QuestionOption]
    required: bool = True

class QuestionSet:
    """Progressive interview questions for MongoDB vs PostgreSQL selection"""
    
    def __init__(self):
        self.questions = self._initialize_questions()
        self.follow_up_questions = self._initialize_follow_up_questions()
    
    def _initialize_questions(self) -> Dict[str, Question]:
        """Initialize the core question set"""
        
        return {
            'schema_evolution': Question(
                id='schema_evolution',
                text="How predictable is your data structure evolution over the next 2 years?",
                context="""
                This question addresses the core lesson from previous platform: platform rigidity vs. customization freedom.
                Schema flexibility is crucial for avoiding another 'platform constraints' where business logic 
                requirements can't be implemented due to platform constraints.
                """,
                options=[
                    QuestionOption(
                        key='highly_predictable',
                        text='Highly predictable - We have well-defined data models that rarely change',
                        follow_up_questions=['migration_complexity', 'business_logic_complexity']
                    ),
                    QuestionOption(
                        key='somewhat_predictable',
                        text='Somewhat predictable - Some changes expected but within known patterns',
                        follow_up_questions=['change_frequency', 'team_migration_comfort']
                    ),
                    QuestionOption(
                        key='unpredictable',
                        text='Unpredictable - Frequent schema changes driven by evolving business needs',
                        follow_up_questions=['schema_governance', 'data_validation_needs']
                    ),
                    QuestionOption(
                        key='completely_unknown',
                        text='Completely unknown - This is a greenfield project with undefined requirements',
                        follow_up_questions=['prototyping_needs', 'rapid_iteration_requirements']
                    )
                ]
            ),
            
            'query_patterns': Question(
                id='query_patterns',
                text="What are your primary data access patterns and query requirements?",
                context="""
                Understanding query patterns is essential for performance and development velocity.
                previous platform's limitation with business logic implementation business logic 
                highlights the importance of flexible query capabilities.
                """,
                options=[
                    QuestionOption(
                        key='simple_crud',
                        text='Simple CRUD operations - Basic create, read, update, delete',
                        follow_up_questions=['api_design_preferences', 'orm_requirements']
                    ),
                    QuestionOption(
                        key='complex_joins',
                        text='Complex joins and relational queries across multiple entities',
                        follow_up_questions=['join_complexity', 'query_optimization_needs']
                    ),
                    QuestionOption(
                        key='analytical_reporting',
                        text='Analytical reporting with aggregations, grouping, and statistical functions',
                        follow_up_questions=['reporting_tools', 'data_warehouse_integration']
                    ),
                    QuestionOption(
                        key='document_retrieval',
                        text='Document-based retrieval with flexible search across nested structures',
                        follow_up_questions=['search_requirements', 'indexing_strategy']
                    ),
                    QuestionOption(
                        key='hierarchical_nested',
                        text='Hierarchical or deeply nested data structures',
                        follow_up_questions=['nesting_depth', 'tree_operations']
                    ),
                    QuestionOption(
                        key='mixed_patterns',
                        text='Mixed patterns - combination of the above',
                        follow_up_questions=['pattern_priorities', 'optimization_focus']
                    )
                ]
            ),
            
            'team_expertise': Question(
                id='team_expertise',
                text="What is your team's current database and development expertise?",
                context="""
                Team expertise affects adoption speed, maintenance burden, and long-term success.
                The previous platform experience showed the importance of team comfort with customization
                and maintenance of the chosen technology stack.
                """,
                options=[
                    QuestionOption(
                        key='sql_heavy',
                        text='Strong SQL and relational database experience',
                        follow_up_questions=['postgresql_specific_experience', 'migration_from_sql']
                    ),
                    QuestionOption(
                        key='nosql_heavy',
                        text='Strong NoSQL and document database experience',
                        follow_up_questions=['mongodb_specific_experience', 'operational_expertise']
                    ),
                    QuestionOption(
                        key='javascript_heavy',
                        text='JavaScript/Node.js heavy with JSON-first thinking',
                        follow_up_questions=['backend_language_preferences', 'api_design_patterns']
                    ),
                    QuestionOption(
                        key='mixed_skills',
                        text='Mixed skills across different database technologies',
                        follow_up_questions=['learning_capacity', 'training_resources']
                    ),
                    QuestionOption(
                        key='learning_motivated',
                        text='Limited database expertise but motivated to learn',
                        follow_up_questions=['learning_timeline', 'mentoring_availability']
                    )
                ]
            ),
            
            'consistency_needs': Question(
                id='consistency_needs',
                text="How critical are ACID transactions and strong consistency for your use case?",
                context="""
                Consistency requirements often drive database architecture decisions.
                Understanding the true consistency needs helps avoid over-engineering
                while ensuring data integrity where it matters most.
                """,
                options=[
                    QuestionOption(
                        key='acid_critical',
                        text='Critical - Financial transactions, audit trails, or regulatory compliance',
                        follow_up_questions=['compliance_requirements', 'audit_complexity']
                    ),
                    QuestionOption(
                        key='mostly_consistent',
                        text='Important - User data integrity matters but some flexibility acceptable',
                        follow_up_questions=['conflict_resolution', 'data_recovery_needs']
                    ),
                    QuestionOption(
                        key='eventually_consistent',
                        text='Eventually consistent - Can handle temporary inconsistencies',
                        follow_up_questions=['inconsistency_tolerance', 'conflict_handling']
                    ),
                    QuestionOption(
                        key='flexible',
                        text='Flexible - Performance and availability more important than strict consistency',
                        follow_up_questions=['performance_priorities', 'availability_requirements']
                    )
                ]
            ),
            
            'performance_profile': Question(
                id='performance_profile',
                text="What is your expected performance and scaling profile?",
                context="""
                Performance characteristics help determine the most suitable database architecture.
                Different databases excel in different performance scenarios.
                """,
                options=[
                    QuestionOption(
                        key='read_heavy_analytics',
                        text='Read-heavy with analytical workloads and complex queries',
                        follow_up_questions=['concurrent_users', 'query_response_time']
                    ),
                    QuestionOption(
                        key='write_heavy_scaling',
                        text='Write-heavy with high-volume data ingestion and horizontal scaling needs',
                        follow_up_questions=['write_volume', 'scaling_strategy']
                    ),
                    QuestionOption(
                        key='balanced_load',
                        text='Balanced read/write load with moderate scaling requirements',
                        follow_up_questions=['growth_expectations', 'resource_constraints']
                    ),
                    QuestionOption(
                        key='low_latency_critical',
                        text='Low latency critical for user experience',
                        follow_up_questions=['latency_targets', 'geographic_distribution']
                    ),
                    QuestionOption(
                        key='high_concurrency',
                        text='High concurrency with many simultaneous connections',
                        follow_up_questions=['connection_pooling', 'resource_management']
                    )
                ]
            )
        }
    
    def _initialize_follow_up_questions(self) -> Dict[str, Question]:
        """Initialize follow-up questions based on core responses"""
        
        return {
            # Schema Evolution Follow-ups
            'migration_complexity': Question(
                id='migration_complexity',
                text="How comfortable is your team with database schema migrations?",
                context="Understanding migration comfort helps assess PostgreSQL adoption friction.",
                options=[
                    QuestionOption('very_comfortable', 'Very comfortable with migration tools and processes'),
                    QuestionOption('somewhat_comfortable', 'Some experience, willing to learn'),
                    QuestionOption('uncomfortable', 'Prefer to avoid complex migration processes')
                ],
                required=False
            ),
            
            'schema_governance': Question(
                id='schema_governance',
                text="How will you govern schema changes in a flexible document model?",
                context="MongoDB's flexibility requires governance to prevent data quality issues.",
                options=[
                    QuestionOption('strict_validation', 'Strict validation rules and schema enforcement'),
                    QuestionOption('gradual_evolution', 'Gradual evolution with backward compatibility'),
                    QuestionOption('minimal_governance', 'Minimal governance, trust application logic')
                ],
                required=False
            ),
            
            # Query Pattern Follow-ups
            'join_complexity': Question(
                id='join_complexity',
                text="How complex are your typical join operations?",
                context="Complex joins strongly favor PostgreSQL's relational model.",
                options=[
                    QuestionOption('simple_joins', '2-3 table joins, straightforward relationships'),
                    QuestionOption('moderate_joins', '4-6 table joins with some complexity'),
                    QuestionOption('complex_joins', '7+ table joins with complex business logic')
                ],
                required=False
            ),
            
            # Team Expertise Follow-ups  
            'postgresql_specific_experience': Question(
                id='postgresql_specific_experience',
                text="Does your team have specific PostgreSQL experience?",
                context="PostgreSQL-specific knowledge reduces learning curve and operational risk.",
                options=[
                    QuestionOption('extensive', 'Extensive PostgreSQL experience'),
                    QuestionOption('some', 'Some PostgreSQL experience'),
                    QuestionOption('none', 'No PostgreSQL-specific experience')
                ],
                required=False
            ),
            
            'mongodb_specific_experience': Question(
                id='mongodb_specific_experience', 
                text="Does your team have specific MongoDB operational experience?",
                context="MongoDB operational expertise is crucial for production deployments.",
                options=[
                    QuestionOption('extensive', 'Extensive MongoDB operations experience'),
                    QuestionOption('some', 'Some MongoDB development experience'),
                    QuestionOption('none', 'No MongoDB-specific experience')
                ],
                required=False
            )
        }
    
    def get_question(self, question_id: str) -> Optional[Question]:
        """Get a question by ID from core or follow-up questions"""
        if question_id in self.questions:
            return self.questions[question_id]
        elif question_id in self.follow_up_questions:
            return self.follow_up_questions[question_id]
        return None
    
    def get_core_questions(self) -> List[Question]:
        """Get all core questions in recommended order"""
        order = ['schema_evolution', 'query_patterns', 'team_expertise', 'consistency_needs', 'performance_profile']
        return [self.questions[qid] for qid in order if qid in self.questions]
    
    def get_follow_up_questions(self, core_response_key: str, question_id: str) -> List[str]:
        """Get follow-up question IDs based on a core response"""
        question = self.get_question(question_id)
        if not question:
            return []
        
        for option in question.options:
            if option.key == core_response_key and option.follow_up_questions:
                return option.follow_up_questions
        
        return []
    
    def get_platform_context_questions(self) -> List[Question]:
        """Get questions specifically addressing platform limitations"""
        platform_questions = [
            Question(
                id='customization_freedom',
                text="How important is the ability to implement custom business logic without platform constraints?",
                context="""
                Direct response to previous platform's rigidity. This question assesses the need for
                customization freedom that led to previous platform's rejection.
                """,
                options=[
                    QuestionOption('critical', 'Critical - Must avoid another platform constraints'),
                    QuestionOption('important', 'Important - Some flexibility needed'),
                    QuestionOption('moderate', 'Moderate - Can work within some constraints')
                ]
            ),
            
            Question(
                id='maintenance_burden_concern',
                text="How concerned are you about long-term maintenance and platform lock-in?",
                context="""
                previous platform's maintenance warnings created trauma. This assesses the priority
                placed on avoiding similar maintenance burden situations.
                """,
                options=[
                    QuestionOption('very_concerned', 'Very concerned - Want full control'),
                    QuestionOption('somewhat_concerned', 'Somewhat concerned - Balanced approach'),
                    QuestionOption('not_concerned', 'Not concerned - Trust platform evolution')
                ]
            )
        ]
        
        return platform_questions

if __name__ == "__main__":
    qs = QuestionSet()
    print(f"Loaded {len(qs.questions)} core questions and {len(qs.follow_up_questions)} follow-up questions")
    
    for q in qs.get_core_questions():
        print(f"\n{q.text}")
        for option in q.options:
            print(f"  - {option.text}")
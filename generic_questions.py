#!/usr/bin/env python3
"""
Generic Question System with Guided Examples

Database-agnostic questions with real-time guidance and examples.
Designed to help users think through their answers with practical context.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

@dataclass
class QuestionOption:
    """Individual option for a question"""
    key: str
    text: str
    explanation: str  # Detailed explanation of what this means
    examples: List[str]  # Real-world examples
    considerations: List[str]  # Things to think about

@dataclass 
class GuidedQuestion:
    """A question with comprehensive guidance"""
    id: str
    text: str
    description: str  # Why this question matters
    guidance: str  # How to think about this question
    examples: Dict[str, str]  # Example scenarios by option
    weight: float  # Importance weight (0.0 to 1.0)
    options: List[QuestionOption]
    follow_ups: List[str]  # IDs of potential follow-up questions

class GenericQuestionSet:
    """Database-agnostic question set with guided examples"""
    
    def __init__(self):
        self.questions = {}
        self.weights = {}
        self._initialize_questions()
    
    def _initialize_questions(self):
        """Initialize generic database selection questions"""
        
        # Schema Evolution Question
        schema_options = [
            QuestionOption(
                key='highly_predictable',
                text='Highly predictable - Well-defined models that rarely change',
                explanation='Your data structure is stable with clear, established patterns',
                examples=[
                    'E-commerce product catalog with standard fields',
                    'User management system with fixed user profiles',
                    'Financial system with regulatory compliance requirements'
                ],
                considerations=[
                    'Are you certain requirements won\'t evolve?',
                    'Do you have regulatory constraints limiting changes?',
                    'Is this a mature domain with established patterns?'
                ]
            ),
            QuestionOption(
                key='somewhat_predictable', 
                text='Somewhat predictable - Some changes expected within known patterns',
                explanation='You expect evolution but within understood boundaries',
                examples=[
                    'CRM system that might add new customer fields',
                    'Content management with occasional new content types',
                    'Inventory system that may track new product attributes'
                ],
                considerations=[
                    'What types of changes do you anticipate?',
                    'How frequently do requirements change?',
                    'Can you identify the likely areas of evolution?'
                ]
            ),
            QuestionOption(
                key='unpredictable',
                text='Unpredictable - Frequent changes driven by business needs',
                explanation='Your schema needs to adapt quickly to changing business requirements',
                examples=[
                    'Startup MVP that pivots based on user feedback',
                    'Analytics platform tracking diverse data sources',
                    'IoT system collecting varied sensor data'
                ],
                considerations=[
                    'How quickly do you need to implement changes?',
                    'Is rapid iteration more important than data consistency?',
                    'Do you have dedicated data modeling expertise?'
                ]
            ),
            QuestionOption(
                key='completely_unknown',
                text='Completely unknown - Greenfield project with undefined requirements',
                explanation='You\'re exploring problem space with minimal constraints',
                examples=[
                    'Research project with evolving data collection needs',
                    'New product with unclear feature requirements',
                    'Prototype exploring multiple use cases'
                ],
                considerations=[
                    'Is this truly exploratory or do you have some constraints?',
                    'What\'s your timeline for requirement clarity?',
                    'Do you need maximum flexibility over performance?'
                ]
            )
        ]
        
        self.questions['schema_evolution'] = GuidedQuestion(
            id='schema_evolution',
            text='How predictable is your data structure evolution over the next 2 years?',
            description='Schema flexibility vs. structure trade-offs significantly impact database choice',
            guidance='Think about your product roadmap, team dynamics, and requirement stability. Consider both technical and business factors that drive schema changes.',
            examples={
                'highly_predictable': 'Financial trading system with regulatory constraints',
                'somewhat_predictable': 'E-commerce platform adding seasonal features', 
                'unpredictable': 'Social media platform with frequent feature updates',
                'completely_unknown': 'AI research platform with experimental data models'
            },
            weight=0.25,
            options=schema_options,
            follow_ups=['migration_complexity', 'development_velocity']
        )
        
        # Query Patterns Question
        query_options = [
            QuestionOption(
                key='simple_crud',
                text='Simple CRUD operations - Basic create, read, update, delete',
                explanation='Your application primarily performs straightforward data operations',
                examples=[
                    'User profile management',
                    'Basic content publishing',
                    'Simple inventory tracking'
                ],
                considerations=[
                    'Will you need complex reporting later?',
                    'Are relationships between entities important?',
                    'Do you need advanced search capabilities?'
                ]
            ),
            QuestionOption(
                key='complex_joins',
                text='Complex joins and relational queries across multiple entities',
                explanation='You need sophisticated queries spanning multiple related data entities',
                examples=[
                    'Financial reporting with transaction analysis',
                    'Supply chain management with multi-tier relationships',
                    'Academic systems with student-course-instructor relationships'
                ],
                considerations=[
                    'How many entities typically participate in your queries?',
                    'Do you need referential integrity enforcement?',
                    'Are ad-hoc queries from business users important?'
                ]
            ),
            QuestionOption(
                key='analytical_reporting',
                text='Analytical reporting with aggregations and statistical functions',
                explanation='You need to perform complex analysis and generate insights from data',
                examples=[
                    'Business intelligence dashboards',
                    'Performance monitoring systems',
                    'Sales analytics and forecasting'
                ],
                considerations=[
                    'What\'s your data volume and query complexity?',
                    'Do you need real-time or batch analytics?',
                    'Will you integrate with BI tools?'
                ]
            ),
            QuestionOption(
                key='document_based',
                text='Document-based retrieval with flexible search across nested structures',
                explanation='Your data is naturally hierarchical or you need flexible search capabilities',
                examples=[
                    'Content management systems',
                    'Product catalogs with varied attributes',
                    'Configuration management systems'
                ],
                considerations=[
                    'How deeply nested is your data?',
                    'Do you need full-text search capabilities?',
                    'Is data structure consistency important?'
                ]
            ),
            QuestionOption(
                key='hierarchical_data',
                text='Hierarchical or deeply nested data structures',
                explanation='Your data naturally forms tree-like or complex nested structures',
                examples=[
                    'Organizational charts and reporting structures',
                    'Category/subcategory taxonomies',
                    'Geographic location hierarchies'
                ],
                considerations=[
                    'How deep are your hierarchies?',
                    'Do you need to query across hierarchy levels?',
                    'Is hierarchy structure stable or dynamic?'
                ]
            ),
            QuestionOption(
                key='mixed_patterns',
                text='Mixed patterns - combination of the above',
                explanation='Your application requires multiple different query patterns',
                examples=[
                    'Enterprise applications with diverse features',
                    'Platforms supporting multiple use cases',
                    'Systems with both transactional and analytical needs'
                ],
                considerations=[
                    'Which pattern is most critical to performance?',
                    'Could you separate concerns into different databases?',
                    'What\'s the relative frequency of each pattern?'
                ]
            )
        ]
        
        self.questions['query_patterns'] = GuidedQuestion(
            id='query_patterns',
            text='What are your primary data access patterns and query requirements?',
            description='Query patterns drive performance characteristics and database feature requirements',
            guidance='Consider your application\'s core functionality and how users interact with data. Think about both current needs and likely future requirements.',
            examples={
                'simple_crud': 'User registration and profile management system',
                'complex_joins': 'ERP system with interconnected business processes',
                'analytical_reporting': 'Sales dashboard with drill-down capabilities',
                'document_based': 'CMS with flexible content types and search',
                'hierarchical_data': 'Company directory with organizational structure',
                'mixed_patterns': 'E-commerce platform with products, orders, and analytics'
            },
            weight=0.25,
            options=query_options,
            follow_ups=['performance_requirements', 'data_volume']
        )
        
        # Team Expertise Question
        team_options = [
            QuestionOption(
                key='strong_sql',
                text='Strong SQL and relational database experience',
                explanation='Your team is highly proficient with SQL databases and relational concepts',
                examples=[
                    'Database administrators with years of SQL experience',
                    'Backend developers comfortable with complex joins',
                    'Data analysts who write SQL queries daily'
                ],
                considerations=[
                    'How comfortable is the team with NoSQL concepts?',
                    'Is retraining time a constraint?',
                    'Do you have dedicated database expertise?'
                ]
            ),
            QuestionOption(
                key='strong_nosql',
                text='Strong NoSQL and document database experience',
                explanation='Your team has significant experience with document databases and NoSQL concepts',
                examples=[
                    'Developers with extensive MongoDB or CouchDB experience',
                    'Teams that think in JSON/document structures',
                    'Microservices teams using document stores'
                ],
                considerations=[
                    'How comfortable is the team with SQL and joins?',
                    'Do you have experience with schema design in NoSQL?',
                    'Is the team prepared for eventual consistency models?'
                ]
            ),
            QuestionOption(
                key='javascript_json',
                text='JavaScript/Node.js heavy with JSON-first thinking',
                explanation='Your team primarily works in JavaScript and thinks in JSON data structures',
                examples=[
                    'Full-stack JavaScript teams (MEAN/MERN)',
                    'Frontend-heavy teams building APIs',
                    'Teams with strong React/Vue component experience'
                ],
                considerations=[
                    'How important is end-to-end JavaScript consistency?',
                    'Does the team understand database performance concepts?',
                    'Are you comfortable with JavaScript-based database tools?'
                ]
            ),
            QuestionOption(
                key='mixed_skills',
                text='Mixed skills across different database technologies',
                explanation='Your team has varied experience with different database approaches',
                examples=[
                    'Teams with both frontend and backend specialists',
                    'Full-stack developers with diverse project backgrounds',
                    'Teams transitioning between technology stacks'
                ],
                considerations=[
                    'Which skills are strongest in your team?',
                    'Who will be responsible for database decisions?',
                    'Is knowledge sharing effective in your team?'
                ]
            ),
            QuestionOption(
                key='limited_experience',
                text='Limited database expertise but motivated to learn',
                explanation='Your team is newer to databases but eager to adopt best practices',
                examples=[
                    'Junior developers or bootcamp graduates',
                    'Teams transitioning from different domains',
                    'Startups building their first major application'
                ],
                considerations=[
                    'What\'s your timeline for getting productive?',
                    'Do you have access to mentoring or training?',
                    'Is simplicity more important than advanced features?'
                ]
            )
        ]
        
        self.questions['team_expertise'] = GuidedQuestion(
            id='team_expertise',
            text='What is your team\'s current database and development expertise?',
            description='Team expertise affects adoption speed, maintenance quality, and long-term success',
            guidance='Consider not just current skills but learning capacity, time constraints, and who will maintain the system long-term.',
            examples={
                'strong_sql': 'Enterprise team with dedicated DBAs and SQL-heavy applications',
                'strong_nosql': 'Startup team with microservices and document-oriented thinking',
                'javascript_json': 'Full-stack JavaScript team building modern web applications',
                'mixed_skills': 'Growing team with diverse backgrounds and project experience',
                'limited_experience': 'New team or organization building first major data application'
            },
            weight=0.20,
            options=team_options,
            follow_ups=['learning_timeline', 'maintenance_capacity']
        )
        
        # Consistency Requirements Question
        consistency_options = [
            QuestionOption(
                key='critical_acid',
                text='Critical - Financial transactions, audit trails, or regulatory compliance',
                explanation='Data consistency is absolutely critical with zero tolerance for inconsistency',
                examples=[
                    'Banking and financial transaction systems',
                    'Medical records and patient data',
                    'Legal document management systems'
                ],
                considerations=[
                    'Are you subject to regulatory requirements?',
                    'What are the consequences of data inconsistency?',
                    'Do you need audit trails and compliance features?'
                ]
            ),
            QuestionOption(
                key='important_flexible',
                text='Important - Data integrity matters but some flexibility acceptable',
                explanation='You need reliable data but can handle brief inconsistencies during updates',
                examples=[
                    'E-commerce inventory and order management',
                    'User-generated content platforms',
                    'Project management and collaboration tools'
                ],
                considerations=[
                    'What level of temporary inconsistency is acceptable?',
                    'How quickly do inconsistencies need to be resolved?',
                    'Are there specific data types that require strong consistency?'
                ]
            ),
            QuestionOption(
                key='eventually_consistent',
                text='Eventually consistent - Can handle temporary inconsistencies',
                explanation='You can tolerate short-term inconsistencies if they resolve automatically',
                examples=[
                    'Social media feed generation',
                    'Recommendation systems',
                    'Analytics and reporting dashboards'
                ],
                considerations=[
                    'How do users react to seeing stale data?',
                    'Are there business processes that depend on immediate consistency?',
                    'Can your application logic handle eventual consistency?'
                ]
            ),
            QuestionOption(
                key='performance_priority',
                text='Performance priority - Availability and speed over strict consistency',
                explanation='System performance and availability are more critical than perfect consistency',
                examples=[
                    'High-traffic content delivery systems',
                    'Gaming leaderboards and statistics',
                    'IoT sensor data collection'
                ],
                considerations=[
                    'What\'s the impact of system downtime vs. stale data?',
                    'Can your business logic work with approximations?',
                    'How do you handle conflict resolution?'
                ]
            )
        ]
        
        self.questions['consistency_requirements'] = GuidedQuestion(
            id='consistency_requirements',
            text='How critical are ACID transactions and strong consistency for your use case?',
            description='Consistency requirements fundamentally shape database architecture and performance',
            guidance='Think about your business consequences of inconsistent data vs. system availability. Consider regulatory requirements and user expectations.',
            examples={
                'critical_acid': 'Banking system where transaction integrity is legally required',
                'important_flexible': 'E-commerce site where brief inventory inconsistencies are manageable',
                'eventually_consistent': 'Social network where feed updates can lag slightly',
                'performance_priority': 'Gaming platform where speed trumps perfect accuracy'
            },
            weight=0.15,
            options=consistency_options,
            follow_ups=['transaction_complexity', 'compliance_requirements']
        )
        
        # Performance and Scaling Question
        performance_options = [
            QuestionOption(
                key='read_heavy',
                text='Read-heavy with analytical workloads and complex queries',
                explanation='Your system primarily serves data to users and analytics tools',
                examples=[
                    'Business intelligence and reporting systems',
                    'Content delivery and news platforms',
                    'Product catalog and search systems'
                ],
                considerations=[
                    'What\'s your read-to-write ratio?',
                    'How complex are your typical queries?',
                    'Do you need real-time analytics or is batch processing acceptable?'
                ]
            ),
            QuestionOption(
                key='write_heavy',
                text='Write-heavy with high-volume data ingestion and scaling needs',
                explanation='Your system continuously ingests large volumes of data from various sources',
                examples=[
                    'IoT sensor data collection systems',
                    'Log aggregation and monitoring platforms',
                    'Event streaming and analytics systems'
                ],
                considerations=[
                    'What\'s your peak write volume?',
                    'Do you need to scale writes horizontally?',
                    'Is write durability more important than immediate consistency?'
                ]
            ),
            QuestionOption(
                key='balanced_load',
                text='Balanced read/write load with moderate scaling requirements',
                explanation='Your system has roughly equal read and write operations with predictable growth',
                examples=[
                    'Internal business applications',
                    'Medium-scale web applications',
                    'Project management and collaboration tools'
                ],
                considerations=[
                    'What\'s your expected growth trajectory?',
                    'Are there peak usage periods you need to handle?',
                    'Is vertical or horizontal scaling more important?'
                ]
            ),
            QuestionOption(
                key='low_latency',
                text='Low latency critical for user experience',
                explanation='Response time is crucial for user satisfaction and business success',
                examples=[
                    'Real-time messaging and chat systems',
                    'Gaming and interactive applications',
                    'Financial trading platforms'
                ],
                considerations=[
                    'What response time do users expect?',
                    'Are you willing to trade consistency for speed?',
                    'Do you need geographic distribution?'
                ]
            ),
            QuestionOption(
                key='high_concurrency',
                text='High concurrency with many simultaneous connections',
                explanation='Your system needs to handle large numbers of concurrent users efficiently',
                examples=[
                    'Social media platforms',
                    'Multiplayer gaming systems',
                    'High-traffic e-commerce during peak events'
                ],
                considerations=[
                    'What\'s your peak concurrent user count?',
                    'Do connection spikes happen predictably?',
                    'Is connection pooling and management critical?'
                ]
            )
        ]
        
        self.questions['performance_scaling'] = GuidedQuestion(
            id='performance_scaling',
            text='What is your expected performance and scaling profile?',
            description='Performance characteristics determine optimal database architecture and scaling strategy',
            guidance='Consider your current traffic, growth projections, and user expectations. Think about peak loads, geographic distribution, and budget constraints.',
            examples={
                'read_heavy': 'News website with millions of readers but few content updates',
                'write_heavy': 'IoT platform collecting sensor data from thousands of devices',
                'balanced_load': 'CRM system with equal amounts of data entry and reporting',
                'low_latency': 'Chat application where message delay impacts user experience',
                'high_concurrency': 'Live streaming platform with thousands of simultaneous viewers'
            },
            weight=0.15,
            options=performance_options,
            follow_ups=['geographic_distribution', 'budget_constraints']
        )
        
        # Store weights
        for question in self.questions.values():
            self.weights[question.id] = question.weight
    
    def get_question(self, question_id: str) -> Optional[GuidedQuestion]:
        """Get a specific question by ID"""
        return self.questions.get(question_id)
    
    def get_core_questions(self) -> List[GuidedQuestion]:
        """Get all core questions in order"""
        core_order = [
            'schema_evolution',
            'query_patterns', 
            'team_expertise',
            'consistency_requirements',
            'performance_scaling'
        ]
        return [self.questions[qid] for qid in core_order if qid in self.questions]
    
    def get_follow_up_questions(self, answered_questions: List[str]) -> List[GuidedQuestion]:
        """Get relevant follow-up questions based on answered questions"""
        follow_ups = []
        for q_id in answered_questions:
            if q_id in self.questions:
                question = self.questions[q_id]
                for follow_up_id in question.follow_ups:
                    if follow_up_id in self.questions:
                        follow_ups.append(self.questions[follow_up_id])
        return follow_ups
    
    def get_question_guidance(self, question_id: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get comprehensive guidance for a question"""
        question = self.get_question(question_id)
        if not question:
            return {}
        
        guidance = {
            'question': question,
            'examples_by_option': question.examples,
            'decision_weight': f"{question.weight * 100:.0f}%",
            'related_concepts': []
        }
        
        # Add contextual guidance based on previous answers
        if context:
            guidance['contextual_hints'] = self._get_contextual_hints(question, context)
        
        return guidance
    
    def _get_contextual_hints(self, question: GuidedQuestion, context: Dict[str, Any]) -> List[str]:
        """Generate contextual hints based on previous answers"""
        hints = []
        
        # Example contextual logic
        if question.id == 'team_expertise' and context.get('startup_context'):
            hints.append("As a startup, consider learning curve vs. time-to-market trade-offs")
        
        if question.id == 'consistency_requirements' and context.get('financial_domain'):
            hints.append("Financial applications typically require strong consistency for compliance")
            
        return hints

# Global instance
guided_questions = GenericQuestionSet()
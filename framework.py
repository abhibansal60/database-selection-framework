#!/usr/bin/env python3
"""
Database Selection Framework: MongoDB vs PostgreSQL Decision Engine

A refined decision framework that helps choose between MongoDB and PostgreSQL
with clear reasoning and team consensus capabilities.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum
import json
from datetime import datetime

class DatabaseChoice(Enum):
    MONGODB = "MongoDB"
    POSTGRESQL = "PostgreSQL"
    NEUTRAL = "Neutral/Requires Further Analysis"

@dataclass
class QuestionResponse:
    question_id: str
    question_text: str
    response: str
    weight: float
    mongodb_score: float
    postgresql_score: float
    rationale: str

@dataclass
class DecisionResult:
    recommendation: DatabaseChoice
    confidence_level: str
    mongodb_total_score: float
    postgresql_total_score: float
    responses: List[QuestionResponse]
    additional_context: Dict[str, str]
    timestamp: datetime

class DatabaseFramework:
    """Core decision engine for MongoDB vs PostgreSQL selection"""
    
    def __init__(self):
        self.responses = []
        self.additional_context = {}
        
        # Weight distribution for decision factors
        self.weights = {
            'schema_evolution': 0.25,    # 25% - Schema flexibility needs
            'query_patterns': 0.25,      # 25% - Query complexity and patterns
            'team_expertise': 0.20,      # 20% - Current team knowledge
            'consistency_needs': 0.15,   # 15% - ACID transaction requirements
            'performance_profile': 0.15  # 15% - Performance and scaling needs
        }
    
    def score_response(self, question_id: str, response_key: str) -> Tuple[float, float, str]:
        """Calculate MongoDB and PostgreSQL scores for a given response"""
        
        scoring_matrix = {
            'schema_evolution': {
                'highly_predictable': (0, 2, "Well-defined schema benefits from PostgreSQL's structure and migration tools"),
                'somewhat_predictable': (1, 1, "Mixed requirements can work with either database"),
                'unpredictable': (2, 0, "Frequent schema changes favor MongoDB's flexible document model"),
                'completely_unknown': (2, 0, "Unknown evolution patterns benefit from schema flexibility")
            },
            'query_patterns': {
                'simple_crud': (1, 1, "Basic operations work well with both databases"),
                'complex_joins': (0, 2, "Complex relational queries are PostgreSQL's strength"),
                'analytical_reporting': (0, 2, "SQL analytics and reporting favor PostgreSQL"),
                'document_retrieval': (2, 0, "Document-based access patterns suit MongoDB"),
                'hierarchical_nested': (2, 0, "Nested data structures are natural in MongoDB"),
                'mixed_patterns': (1, 1, "Varied patterns may work with either approach")
            },
            'team_expertise': {
                'sql_heavy': (0, 1, "SQL expertise reduces PostgreSQL learning curve"),
                'nosql_heavy': (1, 0, "NoSQL experience favors MongoDB adoption"),
                'javascript_heavy': (1, 0, "JavaScript familiarity aligns with MongoDB's JSON model"),
                'mixed_skills': (0.5, 0.5, "Balanced skills allow either choice"),
                'learning_motivated': (1, 1, "Team openness to learning supports either technology")
            },
            'consistency_needs': {
                'acid_critical': (0, 2, "Critical consistency requirements demand PostgreSQL's ACID guarantees"),
                'mostly_consistent': (0, 1, "Strong consistency preferences favor PostgreSQL"),
                'eventually_consistent': (1, 0, "Eventual consistency acceptable, MongoDB suitable"),
                'flexible': (1, 0, "Flexible consistency allows MongoDB's performance benefits")
            },
            'performance_profile': {
                'read_heavy_analytics': (0, 1, "Read-heavy analytical workloads suit PostgreSQL"),
                'write_heavy_scaling': (1, 0, "High-volume writes benefit from MongoDB's scaling"),
                'balanced_load': (1, 1, "Balanced workloads work with either database"),
                'low_latency_critical': (1, 0, "Low latency often favors MongoDB's document model"),
                'high_concurrency': (0, 1, "High concurrency benefits from PostgreSQL's maturity")
            }
        }
        
        if question_id in scoring_matrix and response_key in scoring_matrix[question_id]:
            mongodb_score, postgresql_score, rationale = scoring_matrix[question_id][response_key]
            return mongodb_score, postgresql_score, rationale
        
        return 0, 0, "Response not found in scoring matrix"
    
    def add_response(self, question_id: str, question_text: str, response_key: str, response_text: str):
        """Add a response to the framework and calculate scores"""
        weight = self.weights.get(question_id, 0.0)
        mongodb_score, postgresql_score, rationale = self.score_response(question_id, response_key)
        
        response = QuestionResponse(
            question_id=question_id,
            question_text=question_text,
            response=response_text,
            weight=weight,
            mongodb_score=mongodb_score * weight,
            postgresql_score=postgresql_score * weight,
            rationale=rationale
        )
        
        self.responses.append(response)
    
    def add_context(self, key: str, value: str):
        """Add additional context information"""
        self.additional_context[key] = value
    
    def calculate_decision(self) -> DecisionResult:
        """Calculate final recommendation based on all responses"""
        mongodb_total = sum(r.mongodb_score for r in self.responses)
        postgresql_total = sum(r.postgresql_score for r in self.responses)
        
        # Determine recommendation and confidence
        total_possible = sum(self.weights.values()) * 2  # Max score per database
        mongodb_percentage = (mongodb_total / total_possible) * 100
        postgresql_percentage = (postgresql_total / total_possible) * 100
        
        score_difference = abs(mongodb_percentage - postgresql_percentage)
        
        if score_difference < 10:  # Within 10% - neutral
            recommendation = DatabaseChoice.NEUTRAL
            confidence = "Low confidence - requires further analysis"
        elif score_difference < 20:  # 10-20% difference - weak
            recommendation = DatabaseChoice.MONGODB if mongodb_total > postgresql_total else DatabaseChoice.POSTGRESQL
            confidence = "Moderate confidence"
        else:  # >20% difference - strong
            recommendation = DatabaseChoice.MONGODB if mongodb_total > postgresql_total else DatabaseChoice.POSTGRESQL
            confidence = "High confidence"
        
        return DecisionResult(
            recommendation=recommendation,
            confidence_level=confidence,
            mongodb_total_score=mongodb_total,
            postgresql_total_score=postgresql_total,
            responses=self.responses.copy(),
            additional_context=self.additional_context.copy(),
            timestamp=datetime.now()
        )
    
    def save_session(self, filepath: str):
        """Save current session to JSON file for team collaboration"""
        decision = self.calculate_decision()
        
        session_data = {
            'timestamp': decision.timestamp.isoformat(),
            'recommendation': decision.recommendation.value,
            'confidence_level': decision.confidence_level,
            'mongodb_total_score': decision.mongodb_total_score,
            'postgresql_total_score': decision.postgresql_total_score,
            'responses': [
                {
                    'question_id': r.question_id,
                    'question_text': r.question_text,
                    'response': r.response,
                    'weight': r.weight,
                    'mongodb_score': r.mongodb_score,
                    'postgresql_score': r.postgresql_score,
                    'rationale': r.rationale
                } for r in decision.responses
            ],
            'additional_context': decision.additional_context
        }
        
        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=2)
    
    def load_session(self, filepath: str):
        """Load session from JSON file"""
        with open(filepath, 'r') as f:
            session_data = json.load(f)
        
        self.responses = []
        for r_data in session_data['responses']:
            response = QuestionResponse(**r_data)
            self.responses.append(response)
        
        self.additional_context = session_data.get('additional_context', {})

if __name__ == "__main__":
    print("Database Selection Framework - Core Engine")
    print("Use cli.py for interactive questionnaire")
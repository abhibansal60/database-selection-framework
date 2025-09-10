#!/usr/bin/env python3
"""
Generic Database Selection Framework

Multi-vendor database comparison framework with configurable scoring.
Supports any combination of databases with extensible architecture.
"""

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from database_vendors import DatabaseRegistry, DatabaseVendor, database_registry
from generic_questions import GenericQuestionSet, GuidedQuestion, guided_questions

class ConfidenceLevel(Enum):
    HIGH = "High confidence"
    MODERATE = "Moderate confidence" 
    LOW = "Low confidence - requires further analysis"

@dataclass
class DatabaseScore:
    """Score for a specific database"""
    database_id: str
    database_name: str
    total_score: float
    factor_scores: Dict[str, float]  # question_id -> score
    percentage: float

@dataclass
class ComparisonResponse:
    """Response to a comparison question"""
    question_id: str
    question_text: str
    response_key: str
    response_text: str
    weight: float
    scores: Dict[str, float]  # database_id -> score for this response
    rationale: str

@dataclass
class DatabaseComparison:
    """Result of database comparison"""
    timestamp: str
    databases: List[str]  # Database IDs being compared
    recommendation: Optional[str]  # Recommended database ID
    confidence_level: ConfidenceLevel
    database_scores: Dict[str, DatabaseScore]  # database_id -> DatabaseScore
    responses: List[ComparisonResponse]
    additional_context: Dict[str, Any]
    summary: str

class GenericDatabaseFramework:
    """Generic framework for comparing multiple databases"""
    
    def __init__(self, database_ids: List[str] = None):
        """Initialize framework with specific databases to compare"""
        self.database_registry = database_registry
        self.question_set = guided_questions
        
        # Set databases to compare
        if database_ids:
            self.database_ids = database_ids
        else:
            self.database_ids = ['postgresql', 'mongodb']  # Default comparison
        
        # Validate database IDs
        self.databases = {}
        for db_id in self.database_ids:
            vendor = self.database_registry.get_vendor(db_id)
            if vendor:
                self.databases[db_id] = vendor
            else:
                raise ValueError(f"Unknown database vendor: {db_id}")
        
        # Initialize scoring framework
        self.responses = []
        self.additional_context = {}
        
        # Default weights from question set
        self.weights = guided_questions.weights.copy()
    
    def set_databases(self, database_ids: List[str]):
        """Change which databases to compare"""
        self.__init__(database_ids)
    
    def add_response(self, question_id: str, question_text: str, response_key: str, response_text: str):
        """Add a response to the framework"""
        weight = self.weights.get(question_id, 0)
        scores = self._score_response(question_id, response_key)
        rationale = self._generate_rationale(question_id, response_key, scores)
        
        response = ComparisonResponse(
            question_id=question_id,
            question_text=question_text,
            response_key=response_key,
            response_text=response_text,
            weight=weight,
            scores=scores,
            rationale=rationale
        )
        
        self.responses.append(response)
    
    def _score_response(self, question_id: str, response_key: str) -> Dict[str, float]:
        """Score response for each database"""
        scores = {}
        
        # Initialize all databases with 0 score
        for db_id in self.database_ids:
            scores[db_id] = 0.0
        
        # Apply scoring logic based on question and response
        if question_id == 'schema_evolution':
            scores.update(self._score_schema_evolution(response_key))
        elif question_id == 'query_patterns':
            scores.update(self._score_query_patterns(response_key))
        elif question_id == 'team_expertise':
            scores.update(self._score_team_expertise(response_key))
        elif question_id == 'consistency_requirements':
            scores.update(self._score_consistency_requirements(response_key))
        elif question_id == 'performance_scaling':
            scores.update(self._score_performance_scaling(response_key))
        
        return scores
    
    def _score_schema_evolution(self, response_key: str) -> Dict[str, float]:
        """Score schema evolution preferences"""
        scores = {}
        
        for db_id in self.database_ids:
            vendor = self.databases[db_id]
            base_score = 0.0
            
            if response_key == 'highly_predictable':
                # Relational databases excel with predictable schemas
                if vendor.category.value == 'relational':
                    base_score = 0.5
                elif vendor.category.value == 'document':
                    base_score = 0.2
                    
            elif response_key == 'somewhat_predictable':
                # Both approaches can work
                if vendor.category.value == 'relational':
                    base_score = 0.3
                elif vendor.category.value == 'document':
                    base_score = 0.3
                    
            elif response_key in ['unpredictable', 'completely_unknown']:
                # Document databases excel with unpredictable schemas
                if vendor.category.value == 'document':
                    base_score = 0.5
                elif vendor.category.value == 'relational':
                    base_score = 0.1
                    
            scores[db_id] = base_score
            
        return scores
    
    def _score_query_patterns(self, response_key: str) -> Dict[str, float]:
        """Score query pattern preferences"""
        scores = {}
        
        for db_id in self.database_ids:
            vendor = self.databases[db_id]
            base_score = 0.0
            
            if response_key in ['simple_crud', 'balanced_load']:
                # Both database types handle CRUD well
                base_score = 0.25
                
            elif response_key in ['complex_joins', 'analytical_reporting']:
                # Relational databases excel at complex queries
                if vendor.category.value == 'relational':
                    base_score = 0.5
                elif vendor.category.value == 'document':
                    base_score = 0.1
                    
            elif response_key in ['document_based', 'hierarchical_data']:
                # Document databases excel at hierarchical data
                if vendor.category.value == 'document':
                    base_score = 0.5
                elif vendor.category.value == 'relational':
                    base_score = 0.2
                    
            elif response_key == 'mixed_patterns':
                # PostgreSQL with JSON or multi-model approaches
                if db_id == 'postgresql':
                    base_score = 0.3
                elif vendor.category.value == 'multi_model':
                    base_score = 0.4
                else:
                    base_score = 0.2
                    
            scores[db_id] = base_score
            
        return scores
    
    def _score_team_expertise(self, response_key: str) -> Dict[str, float]:
        """Score based on team expertise"""
        scores = {}
        
        for db_id in self.database_ids:
            vendor = self.databases[db_id]
            base_score = 0.0
            
            if response_key == 'strong_sql':
                if vendor.category.value == 'relational':
                    base_score = 0.4
                else:
                    base_score = 0.1
                    
            elif response_key == 'strong_nosql':
                if vendor.category.value in ['document', 'key_value']:
                    base_score = 0.4
                else:
                    base_score = 0.1
                    
            elif response_key == 'javascript_json':
                if vendor.category.value == 'document':
                    base_score = 0.3
                elif db_id == 'postgresql':  # JSON support
                    base_score = 0.2
                else:
                    base_score = 0.1
                    
            elif response_key in ['mixed_skills', 'limited_experience']:
                # Equal footing, slight preference for easier learning curve
                if vendor.learning_curve == 'Low':
                    base_score = 0.2
                elif vendor.learning_curve == 'Medium':
                    base_score = 0.15
                else:
                    base_score = 0.1
                    
            scores[db_id] = base_score
            
        return scores
    
    def _score_consistency_requirements(self, response_key: str) -> Dict[str, float]:
        """Score consistency requirements"""
        scores = {}
        
        for db_id in self.database_ids:
            vendor = self.databases[db_id]
            base_score = 0.0
            
            if response_key == 'critical_acid':
                # Strong ACID requirements favor relational databases
                if vendor.category.value == 'relational':
                    base_score = 0.3
                else:
                    base_score = 0.05
                    
            elif response_key == 'important_flexible':
                # Moderate consistency needs - both can work
                if vendor.category.value == 'relational':
                    base_score = 0.2
                else:
                    base_score = 0.15
                    
            elif response_key in ['eventually_consistent', 'performance_priority']:
                # Flexible consistency favors NoSQL
                if vendor.category.value in ['document', 'key_value']:
                    base_score = 0.2
                elif vendor.category.value == 'relational':
                    base_score = 0.1
                    
            scores[db_id] = base_score
            
        return scores
    
    def _score_performance_scaling(self, response_key: str) -> Dict[str, float]:
        """Score performance and scaling preferences"""
        scores = {}
        
        for db_id in self.database_ids:
            vendor = self.databases[db_id]
            base_score = 0.0
            
            if response_key == 'read_heavy':
                # Read optimization varies by implementation
                if vendor.category.value == 'relational':
                    base_score = 0.2
                elif vendor.category.value == 'document':
                    base_score = 0.15
                    
            elif response_key == 'write_heavy':
                # Write scaling often favors horizontal scaling
                if vendor.scaling_model in ['Horizontal', 'Both']:
                    base_score = 0.25
                else:
                    base_score = 0.1
                    
            elif response_key in ['balanced_load', 'low_latency']:
                # Balanced requirements
                base_score = 0.15
                
            elif response_key == 'high_concurrency':
                # Connection handling varies by database
                if db_id in ['redis', 'mongodb']:
                    base_score = 0.2
                else:
                    base_score = 0.15
                    
            scores[db_id] = base_score
            
        return scores
    
    def _generate_rationale(self, question_id: str, response_key: str, scores: Dict[str, float]) -> str:
        """Generate rationale for scoring decision"""
        # Find highest scoring database(s)
        max_score = max(scores.values()) if scores else 0
        top_databases = [db_id for db_id, score in scores.items() if score == max_score]
        
        if len(top_databases) == 1:
            winner = self.databases[top_databases[0]]
            return f"Preference aligns with {winner.name}'s strengths in this area"
        elif len(top_databases) == len(scores):
            return "Response is neutral across database options"
        else:
            winners = [self.databases[db_id].name for db_id in top_databases]
            return f"Response favors {' and '.join(winners)} for this factor"
    
    def calculate_comparison(self) -> DatabaseComparison:
        """Calculate final database comparison"""
        # Calculate total scores
        database_scores = {}
        for db_id in self.database_ids:
            total_score = 0.0
            factor_scores = {}
            
            for response in self.responses:
                weighted_score = response.scores.get(db_id, 0) * response.weight
                total_score += weighted_score
                factor_scores[response.question_id] = weighted_score
            
            database_scores[db_id] = DatabaseScore(
                database_id=db_id,
                database_name=self.databases[db_id].name,
                total_score=total_score,
                factor_scores=factor_scores,
                percentage=0.0  # Will be calculated below
            )
        
        # Calculate percentages
        total_all_scores = sum(score.total_score for score in database_scores.values())
        if total_all_scores > 0:
            for score in database_scores.values():
                score.percentage = (score.total_score / total_all_scores) * 100
        
        # Determine recommendation and confidence
        recommendation, confidence = self._determine_recommendation(database_scores)
        
        # Generate summary
        summary = self._generate_summary(database_scores, recommendation, confidence)
        
        return DatabaseComparison(
            timestamp=datetime.now().isoformat(),
            databases=self.database_ids,
            recommendation=recommendation,
            confidence_level=confidence,
            database_scores=database_scores,
            responses=self.responses.copy(),
            additional_context=self.additional_context.copy(),
            summary=summary
        )
    
    def _determine_recommendation(self, scores: Dict[str, DatabaseScore]) -> Tuple[Optional[str], ConfidenceLevel]:
        """Determine recommendation and confidence level"""
        if not scores:
            return None, ConfidenceLevel.LOW
        
        # Sort by total score
        sorted_scores = sorted(scores.items(), key=lambda x: x[1].total_score, reverse=True)
        
        if len(sorted_scores) == 1:
            return sorted_scores[0][0], ConfidenceLevel.HIGH
        
        # Calculate score difference between top two
        top_score = sorted_scores[0][1].total_score
        second_score = sorted_scores[1][1].total_score
        
        # Handle case where top score is 0
        if top_score == 0:
            return None, ConfidenceLevel.LOW
        
        score_difference = abs(top_score - second_score) / top_score
        
        # Determine confidence based on score separation
        if score_difference > 0.20:  # >20% difference
            return sorted_scores[0][0], ConfidenceLevel.HIGH
        elif score_difference > 0.10:  # 10-20% difference
            return sorted_scores[0][0], ConfidenceLevel.MODERATE
        else:  # <10% difference
            return None, ConfidenceLevel.LOW  # Too close to call
    
    def _generate_summary(self, scores: Dict[str, DatabaseScore], recommendation: Optional[str], confidence: ConfidenceLevel) -> str:
        """Generate comparison summary"""
        if recommendation:
            winner = self.databases[recommendation]
            return f"Recommended {winner.name} based on {confidence.value.lower()} from weighted analysis"
        else:
            database_names = [self.databases[db_id].name for db_id in self.database_ids]
            return f"Scores are too close between {' and '.join(database_names)} - requires additional analysis"
    
    def add_context(self, key: str, value: Any):
        """Add additional context to the comparison"""
        self.additional_context[key] = value
    
    def save_session(self, filepath: str):
        """Save current session to file"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        session_data = {
            'timestamp': datetime.now().isoformat(),
            'database_ids': self.database_ids,
            'responses': [asdict(response) for response in self.responses],
            'additional_context': self.additional_context,
            'weights': self.weights
        }
        
        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=2)
    
    def load_session(self, filepath: str):
        """Load session from file"""
        with open(filepath, 'r') as f:
            session_data = json.load(f)
        
        # Restore state
        self.database_ids = session_data.get('database_ids', ['postgresql', 'mongodb'])
        self.additional_context = session_data.get('additional_context', {})
        self.weights = session_data.get('weights', guided_questions.weights.copy())
        
        # Rebuild database registry
        self.databases = {}
        for db_id in self.database_ids:
            vendor = self.database_registry.get_vendor(db_id)
            if vendor:
                self.databases[db_id] = vendor
        
        # Restore responses
        self.responses = []
        for response_data in session_data.get('responses', []):
            response = ComparisonResponse(**response_data)
            self.responses.append(response)
    
    def get_available_databases(self) -> Dict[str, DatabaseVendor]:
        """Get all available database vendors"""
        return self.database_registry.get_all_vendors()
    
    def get_comparison_suggestions(self) -> List[List[str]]:
        """Get suggested database comparison pairs"""
        return self.database_registry.get_vendor_comparison_pairs()

# Convenience function for creating framework instances
def create_comparison(database_ids: List[str]) -> GenericDatabaseFramework:
    """Create a new database comparison framework"""
    return GenericDatabaseFramework(database_ids)
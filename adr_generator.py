"""
ADR (Architecture Decision Record) Generator for Database Selection Framework

Generates comprehensive decision documentation based on framework responses,
specifically addressing platform limitations and team consensus needs.
"""

from typing import Dict, List
from framework import DecisionResult, DatabaseChoice
from datetime import datetime
import os

class ADRGenerator:
    """Generate Architecture Decision Records for database selection decisions"""
    
    def __init__(self):
        self.template_sections = {
            'title': self._generate_title,
            'status': self._generate_status,  
            'context': self._generate_context,
            'decision': self._generate_decision,
            'rationale': self._generate_rationale,
            'consequences': self._generate_consequences,
            'implementation': self._generate_implementation_notes,
            'alternatives': self._generate_alternatives_considered
        }
    
    def generate_adr(self, decision_result: DecisionResult, project_name: str = "Custom Application") -> str:
        """Generate complete ADR document"""
        
        sections = []
        
        # Generate each section
        for section_name, generator_func in self.template_sections.items():
            section_content = generator_func(decision_result, project_name)
            sections.append(section_content)
        
        # Combine all sections
        adr_content = "\n\n".join(sections)
        
        return adr_content
    
    def _generate_title(self, decision_result: DecisionResult, project_name: str) -> str:
        """Generate ADR title section"""
        return f"# ADR: Database Selection - {decision_result.recommendation.value} for {project_name}"
    
    def _generate_status(self, decision_result: DecisionResult, project_name: str) -> str:
        """Generate status section"""
        status = "Proposed"  # Default status
        if decision_result.confidence_level == "High confidence":
            status = "Accepted"
        elif decision_result.confidence_level == "Low confidence":
            status = "Under Review"
        
        return f"""## Status

**{status}** - {decision_result.timestamp.strftime('%Y-%m-%d')}

Confidence Level: **{decision_result.confidence_level}**"""
    
    def _generate_context(self, decision_result: DecisionResult, project_name: str) -> str:
        """Generate context section addressing previous platform experience"""
        
        # Extract relevant context from responses
        schema_concerns = self._extract_schema_concerns(decision_result.responses)
        team_context = self._extract_team_context(decision_result.responses)
        
        context = f"""## Context

### Project Background
We are developing a custom application for {project_name}, moving away from our previous SharePoint-based approach after a failed platform evaluation.

### previous platform experience & Lessons Learned
After 6-7 months of platform evaluation, we encountered critical limitations:

- **platform rigidity**: Standard workflows couldn't accommodate our business requirements
- **platform limitations**: platform constrained customizations due to maintenance burden
- **business logic implementation Limitations**: Unable to implement required business logic
- **Platform Constraints**: Fundamental inability to adapt to actual business needs

These experiences have shaped our database selection criteria, emphasizing:
- **Customization Freedom**: Must avoid platform constraints that limit business logic implementation
- **Schema Evolution**: Ability to change data structures without platform limitations  
- **Long-term Maintenance**: Sustainable development approach without vendor lock-in risks
- **Team Control**: Full ownership of technology decisions and implementation approaches

### Technical Requirements Context
{schema_concerns}

### Team Context  
{team_context}

### Decision Scope
This decision specifically addresses **database technology selection** (MongoDB vs PostgreSQL) for the custom application backend. The choice directly impacts our ability to avoid the previous platform rigidity issues while maintaining development velocity and long-term sustainability."""
        
        return context
    
    def _generate_decision(self, decision_result: DecisionResult, project_name: str) -> str:
        """Generate decision section"""
        
        percentage_mongodb = (decision_result.mongodb_total_score / (decision_result.mongodb_total_score + decision_result.postgresql_total_score)) * 100 if (decision_result.mongodb_total_score + decision_result.postgresql_total_score) > 0 else 50
        percentage_postgresql = 100 - percentage_mongodb
        
        decision = f"""## Decision

**We will use {decision_result.recommendation.value} as the primary database for {project_name}.**

### Scoring Summary
- **MongoDB Score**: {decision_result.mongodb_total_score:.2f} ({percentage_mongodb:.1f}%)
- **PostgreSQL Score**: {decision_result.postgresql_total_score:.2f} ({percentage_postgresql:.1f}%)
- **Confidence Level**: {decision_result.confidence_level}"""

        if decision_result.recommendation == DatabaseChoice.NEUTRAL:
            decision += f"""

### Neutral Recommendation Note
The scoring analysis indicates both databases are viable options for this project. This requires additional evaluation focusing on:
- Team consensus and preferences
- Specific technical spike investigations  
- Prototype development with both technologies
- Infrastructure and operational considerations"""
        
        return decision
    
    def _generate_rationale(self, decision_result: DecisionResult, project_name: str) -> str:
        """Generate detailed rationale section"""
        
        rationale = "## Rationale\n\n### Decision Factors Analysis\n"
        
        # Sort responses by weight (most important first)
        sorted_responses = sorted(decision_result.responses, key=lambda r: r.weight, reverse=True)
        
        for response in sorted_responses:
            weight_percentage = (response.weight * 100)
            rationale += f"""
#### {response.question_text} (Weight: {weight_percentage:.0f}%)
- **Response**: {response.response}
- **MongoDB Impact**: {response.mongodb_score:.2f}
- **PostgreSQL Impact**: {response.postgresql_score:.2f}
- **Rationale**: {response.rationale}"""
        
        # Add previous platform-specific analysis
        rationale += self._generate_platform_analysis(decision_result)
        
        return rationale
    
    def _generate_consequences(self, decision_result: DecisionResult, project_name: str) -> str:
        """Generate consequences section"""
        
        if decision_result.recommendation == DatabaseChoice.MONGODB:
            consequences = """## Consequences

### Positive Consequences
- **Schema Flexibility**: Easy adaptation to evolving business requirements without migration complexity
- **Development Velocity**: JSON-native approach aligns with modern web development practices
- **Horizontal Scaling**: Built-in support for distributed scaling as requirements grow
- **platform rigidity concerns Mitigation**: Maximum customization freedom without platform constraints

### Negative Consequences & Mitigations
- **Query Complexity**: Limited support for complex joins
  - *Mitigation*: Design document structure to minimize join requirements
- **ACID Limitations**: Eventual consistency model
  - *Mitigation*: Implement application-level consistency where critical
- **Operational Expertise**: Team may need MongoDB-specific operational knowledge
  - *Mitigation*: Invest in training and potentially managed database services
- **Data Governance**: Flexible schema requires discipline
  - *Mitigation*: Implement schema validation and documentation standards"""
        
        elif decision_result.recommendation == DatabaseChoice.POSTGRESQL:
            consequences = """## Consequences

### Positive Consequences  
- **ACID Guarantees**: Strong consistency and transaction support
- **Query Power**: Complex analytical queries and joins natively supported
- **SQL Familiarity**: Leverages existing team SQL knowledge
- **Ecosystem Maturity**: Rich tooling and extensive community support
- **JSON Support**: Modern PostgreSQL provides document capabilities when needed

### Negative Consequences & Mitigations
- **Schema Rigidity**: Changes require migrations
  - *Mitigation*: Careful initial design and incremental migration strategies
- **Scaling Complexity**: Vertical scaling limitations
  - *Mitigation*: Modern PostgreSQL scaling solutions and read replicas
- **previous platform Similarity Concerns**: Structured approach may feel constraining
  - *Mitigation*: PostgreSQL's flexibility far exceeds previous platform's limitations"""
        
        else:  # Neutral
            consequences = """## Consequences

### Neutral Decision Consequences
Since both databases scored similarly, the consequences depend on the final choice after additional analysis:

#### If MongoDB is chosen:
- Focus on schema design patterns and governance
- Invest in NoSQL operational expertise
- Plan for application-level consistency patterns

#### If PostgreSQL is chosen:  
- Design migration-friendly schema patterns
- Leverage existing SQL knowledge effectively
- Plan for JSON document features where beneficial

### Required Next Steps
- Technical spike with both databases
- Team consensus building through hands-on evaluation
- Infrastructure assessment for operational requirements"""
        
        return consequences
    
    def _generate_implementation_notes(self, decision_result: DecisionResult, project_name: str) -> str:
        """Generate implementation notes section"""
        
        notes = """## Implementation Notes

### Immediate Next Steps"""
        
        if decision_result.recommendation != DatabaseChoice.NEUTRAL:
            database = decision_result.recommendation.value
            notes += f"""
1. **Technology Spike**: Create proof-of-concept with {database} using core data models
2. **Team Onboarding**: Plan training and knowledge transfer for {database}-specific patterns
3. **Infrastructure Planning**: Define hosting, backup, and monitoring strategies
4. **Development Standards**: Establish coding standards and best practices
5. **Migration Strategy**: Plan data migration from current SharePoint system"""
            
            # Add database-specific implementation notes
            if decision_result.recommendation == DatabaseChoice.MONGODB:
                notes += """

### MongoDB-Specific Implementation Considerations
- **Schema Design**: Define document structures and embedding vs. referencing patterns
- **Index Strategy**: Plan indexing for query performance optimization  
- **Connection Management**: Implement connection pooling and error handling
- **Data Validation**: Set up schema validation rules and governance processes
- **Operational Monitoring**: Establish monitoring for performance and resource usage"""
            
            elif decision_result.recommendation == DatabaseChoice.POSTGRESQL:
                notes += """

### PostgreSQL-Specific Implementation Considerations
- **Schema Design**: Define table structures with future evolution in mind
- **Migration Framework**: Set up migration tools and processes (e.g., Alembic, Flyway)
- **Performance Optimization**: Plan indexing strategy and query optimization approaches
- **JSON Usage**: Define patterns for leveraging PostgreSQL's JSON capabilities
- **Connection Pooling**: Implement efficient connection management"""
        
        else:
            notes += """
1. **Parallel Technical Spikes**: Create proof-of-concepts with both MongoDB and PostgreSQL
2. **Team Evaluation**: Have team members work with both technologies
3. **Performance Testing**: Compare performance characteristics for specific use cases
4. **Operational Assessment**: Evaluate hosting, backup, and monitoring for both options
5. **Final Decision Meeting**: Synthesize findings and make final choice"""
        
        # Add team consensus section
        notes += f"""

### Team Consensus & Communication
- **Decision Documentation**: This ADR serves as the formal decision record
- **Stakeholder Communication**: Share rationale with project stakeholders
- **Team Buy-in**: Ensure all team members understand and support the decision
- **Knowledge Sharing**: Plan internal presentations on chosen technology

### Success Metrics
- Development velocity maintained or improved compared to current system
- Schema evolution handled smoothly without previous platform-style constraints
- Team productivity and satisfaction with technology choice
- Successful migration from SharePoint with improved functionality"""
        
        return notes
    
    def _generate_alternatives_considered(self, decision_result: DecisionResult, project_name: str) -> str:
        """Generate alternatives considered section"""
        
        return f"""## Alternatives Considered

### Database Options Evaluated
This decision framework specifically focused on **MongoDB vs PostgreSQL** as the finalist options after broader technology evaluation.

#### MongoDB
- **Strengths**: Schema flexibility, horizontal scaling, JSON-native development
- **Weaknesses**: Limited join support, eventual consistency model
- **Score**: {decision_result.mongodb_total_score:.2f}

#### PostgreSQL  
- **Strengths**: ACID compliance, complex query support, SQL familiarity
- **Weaknesses**: Schema migration complexity, vertical scaling limitations
- **Score**: {decision_result.postgresql_total_score:.2f}

### Previously Rejected Options
- **previous platform**: Rejected after 6-7 months due to platform rigidity and customization limitations
- **SharePoint**: Current system being replaced due to functional limitations
- **Other NoSQL Options**: Not evaluated in detail as MongoDB represents the document database category
- **Other SQL Options**: PostgreSQL selected as representative of modern relational databases

### Why Not Other Databases?
- **MySQL**: PostgreSQL chosen for superior JSON support and advanced features
- **Oracle/SQL Server**: Licensing costs and complexity outweigh benefits for this project  
- **DynamoDB/CosmosDB**: Vendor lock-in concerns after previous platform experience
- **Neo4j/Graph DBs**: Data relationships don't justify graph database complexity

The two-database comparison approach ensures focused evaluation while representing the core architectural decision: document-oriented vs relational data modeling."""
    
    def _extract_schema_concerns(self, responses: List) -> str:
        """Extract schema-related concerns from responses"""
        schema_response = next((r for r in responses if r.question_id == 'schema_evolution'), None)
        if schema_response:
            return f"**Schema Evolution Requirements**: {schema_response.response}"
        return "Schema evolution requirements not specified in evaluation."
    
    def _extract_team_context(self, responses: List) -> str:
        """Extract team context from responses"""
        team_response = next((r for r in responses if r.question_id == 'team_expertise'), None)
        if team_response:
            return f"**Team Expertise**: {team_response.response}"
        return "Team expertise context not specified in evaluation."
    
    def _generate_platform_analysis(self, decision_result: DecisionResult) -> str:
        """Generate previous platform-specific analysis section"""
        
        return """

### previous platform experience Impact Analysis

Our platform evaluation failure directly influenced this database selection:

#### Customization Freedom Priority
The previous platform team's warnings about customization maintenance burden highlighted the importance of technology choices that provide maximum implementation flexibility without platform constraints.

#### Schema Evolution Lessons
previous platform's rigid data model structure prevented implementation of our business logic implementation requirements. This experience prioritizes database technologies that allow business logic evolution without platform limitations.

#### Long-term Maintenance Considerations  
The previous platform maintenance burden warnings emphasized the importance of technology choices where we maintain full control over customization and evolution paths.

This database decision directly addresses these concerns by prioritizing flexibility, customization freedom, and team control over the technology stack."""
    
    def save_adr(self, decision_result: DecisionResult, project_name: str = "Custom Application", 
                 output_dir: str = "./", filename: str = None) -> str:
        """Generate and save ADR to file"""
        
        adr_content = self.generate_adr(decision_result, project_name)
        
        if filename is None:
            timestamp = decision_result.timestamp.strftime('%Y%m%d')
            db_choice = decision_result.recommendation.value.lower().replace(' ', '_').replace('/', '_')
            filename = f"adr_{timestamp}_database_selection_{db_choice}.md"
        
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(adr_content)
        
        return filepath

if __name__ == "__main__":
    print("ADR Generator for Database Selection Framework")
    print("Use with DecisionResult from framework.py")
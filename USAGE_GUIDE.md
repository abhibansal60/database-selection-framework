# Database Selection Framework - Usage Guide

## 🚀 Quick Start Options

### Option 1: Command Line Interface (Recommended)
```bash
# Interactive assessment
python3 database_selector.py assess

# With project name
python3 database_selector.py assess --project "My Application"

# Easy launcher (no arguments needed)
./db-select
```

### Option 2: Web Interface 
```bash
# Start web server
python3 web_ui.py

# Custom port
python3 web_ui.py 8090

# Open browser to: http://localhost:8080
```

## 📋 Command Reference

### 🔍 Assessment Commands
```bash
# Start new assessment
python3 database_selector.py assess
python3 database_selector.py assess --project "My App"

# Load previous session
python3 database_selector.py load sessions/my_session.json

# Generate ADR from session  
python3 database_selector.py adr sessions/my_session.json
python3 database_selector.py adr sessions/my_session.json --project "My App"
```

### 🎮 Demo Commands
```bash
# All demo scenarios
python3 database_selector.py demo

# Specific scenarios
python3 database_selector.py demo --scenario mongodb
python3 database_selector.py demo --scenario postgresql  
python3 database_selector.py demo --scenario neutral
```

### 📖 Help Commands
```bash
# Detailed help
python3 database_selector.py help

# Command help
python3 database_selector.py assess --help
python3 database_selector.py load --help
```

## 🎯 Usage Workflows

### Individual Assessment
1. **Run Assessment**: `python3 database_selector.py assess`
2. **Answer Questions**: 4-5 core questions + optional follow-ups  
3. **Review Results**: Get recommendation with confidence level
4. **Save Session**: For team review and collaboration
5. **Generate ADR**: Architecture Decision Record for documentation

### Team Collaboration  
1. **Individual Sessions**: Each team member runs assessment
2. **Share Sessions**: Exchange session JSON files
3. **Review Together**: Compare results and reasoning
4. **Generate Final ADR**: Document team consensus
5. **Implementation**: Use ADR for next steps

### Demo and Validation
1. **Run Demos**: `python3 database_selector.py demo`
2. **See All Scenarios**: MongoDB-leaning, PostgreSQL-leaning, Neutral
3. **Validate Logic**: Understand how scoring works
4. **Review ADRs**: See example decision documentation

## 📊 Understanding Results

### Confidence Levels
- **High Confidence**: Score difference >20%, clear recommendation
- **Moderate Confidence**: Score difference 10-20%, good recommendation  
- **Low Confidence**: Score difference <10%, neutral/requires analysis

### Scoring Weights
- **Schema Evolution**: 25% (previous platform trauma factor)
- **Query Patterns**: 25% (Business logic requirements)
- **Team Expertise**: 20% (Adoption and maintenance)
- **Consistency Needs**: 15% (ACID vs eventual consistency)
- **Performance Profile**: 15% (Scaling and load patterns)

### Interpretation Guide
```
MongoDB Advantages:
✅ Schema flexibility and evolution
✅ Document-based data models
✅ JSON-native development
✅ Horizontal scaling
✅ Rapid prototyping

PostgreSQL Advantages:  
✅ ACID transactions and consistency
✅ Complex queries and joins
✅ SQL expertise leverage
✅ JSON support when needed
✅ Mature ecosystem and tooling
```

## 🛡️ previous platform Trauma Recovery

The framework explicitly addresses previous platform pain points:

### Platform Rigidity → Schema Flexibility (25% weight)
- Unpredictable schema changes favor MongoDB
- Predictable schemas can use PostgreSQL effectively
- Both avoid vendor platform constraints

### Customization Warnings → Open Source Freedom  
- Both databases provide full customization control
- No vendor warnings about maintenance burden
- Team owns the technology stack completely

### Business Logic Limitations → Query Pattern Analysis
- Framework ensures your business logic can be implemented
- Document model (MongoDB) vs Relational model (PostgreSQL)
- No platform restrictions on complex requirements

### Team Expertise → Sustainable Adoption (20% weight)
- Considers current team skills and learning capacity
- Avoids adoption friction that plagued previous platform
- Builds on existing knowledge where possible

## 📁 File Organization

### Generated Files
```
output/                 # ADR documents from assessments
├── adr_20250910_database_selection_mongodb.md
├── adr_20250910_database_selection_postgresql.md  
└── adr_20250910_database_selection_neutral.md

sessions/               # Session files for team collaboration
├── session_20250910_143022.json
├── team_review.json
└── final_decision.json

demo_output/            # Example outputs from demos
├── demo_adr_mongodb_scenario.md
├── demo_adr_postgresql_scenario.md
└── demo_adr_neutral_scenario.md
```

### Session File Format
```json
{
  "timestamp": "2025-09-10T14:30:22.123456",
  "recommendation": "MongoDB", 
  "confidence_level": "High confidence",
  "mongodb_total_score": 1.5,
  "postgresql_total_score": 0.0,
  "responses": [
    {
      "question_id": "schema_evolution",
      "question_text": "How predictable is your data structure evolution?",
      "response": "Unpredictable - frequent changes driven by business needs",
      "weight": 0.25,
      "mongodb_score": 0.5,
      "postgresql_score": 0.0,
      "rationale": "Frequent schema changes favor MongoDB's flexible document model"
    }
  ],
  "additional_context": {
    "project_name": "My Application",
    "migration_source": "SharePoint"
  }
}
```

## 🔧 Customization

### Adding New Questions
1. Edit `questions.py` in `_initialize_questions()`
2. Add new question with options and follow-ups
3. Update `framework.py` weights dictionary
4. Add scoring matrix in `score_response()` method

### Modifying Weights
```python
# In framework.py, __init__ method
self.weights = {
    'schema_evolution': 0.30,    # Increase schema flexibility weight
    'query_patterns': 0.25,      
    'team_expertise': 0.20,      
    'consistency_needs': 0.15,   
    'performance_profile': 0.10  # Decrease performance weight
}
```

### Custom ADR Templates
1. Edit `adr_generator.py` template methods
2. Modify sections: title, context, decision, rationale, consequences
3. Add organization-specific sections or formatting

## 🚨 Troubleshooting

### Common Issues
```bash
# Permission denied
chmod +x database_selector.py db-select web_ui.py

# Python not found
python3 --version  # Ensure Python 3.7+ installed

# Module import errors
# Framework uses only standard library - no external dependencies needed

# Web UI not accessible
# Check firewall settings, try different port: python3 web_ui.py 8090
```

### Reset and Clean Start
```bash  
# Remove generated files
rm -rf output/ sessions/ demo_output/ __pycache__/

# Clean restart
python3 database_selector.py assess
```

## 📞 Support Scenarios

### "I got a neutral recommendation"
- Both databases are viable for your project  
- Run technical spikes with both options
- Consider team preferences and infrastructure
- previous platform experience suggests prioritizing flexibility

### "Results don't seem right"
- Review your responses in the generated session file
- Re-run assessment with refined answers
- Consider follow-up questions for more precision
- Framework weights can be customized for your organization

### "Team disagrees with recommendation"  
- Share session files for transparent review
- Use ADR as discussion starting point, not final decision
- Framework provides reasoning, team makes final choice
- Consider running individual assessments for comparison

## 🎯 Success Tips

1. **Be Honest About Requirements**: Framework is only as good as your inputs
2. **Consider previous platform Lessons**: Prioritize flexibility and team control
3. **Use Team Input**: Individual assessments + collaborative review
4. **Document Decisions**: ADRs provide rationale for future reference
5. **Stay Flexible**: Recommendations can change as projects evolve

---

**Remember**: This framework helps structure your thinking and provides data-driven recommendations, but your team makes the final decision based on your specific context and constraints.
#!/usr/bin/env python3
"""
Simple Web UI for Database Selection Framework

A lightweight web interface using Python's built-in server
Perfect for team collaboration and non-technical stakeholders
"""

import http.server
import socketserver
import json
import urllib.parse
import os
from datetime import datetime
from framework import DatabaseFramework
from questions import QuestionSet
from adr_generator import ADRGenerator

class DatabaseSelectorHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP request handler for the database selection web UI"""
    
    def __init__(self, *args, **kwargs):
        self.framework = DatabaseFramework()
        self.question_set = QuestionSet()
        self.adr_generator = ADRGenerator()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/index.html':
            self.serve_main_page()
        elif self.path == '/api/questions':
            self.serve_questions()
        elif self.path.startswith('/api/sessions'):
            self.serve_sessions()
        elif self.path.startswith('/output/') or self.path.startswith('/sessions/'):
            # Serve files from output and sessions directories
            super().do_GET()
        else:
            super().do_GET()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/assess':
            self.handle_assessment()
        elif self.path == '/api/generate-adr':
            self.handle_adr_generation()
        else:
            self.send_error(404)
    
    def serve_main_page(self):
        """Serve the main web interface"""
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Database Selection Framework</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6;
            background: #f5f7fa;
        }
        .header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 30px;
        }
        .card { 
            background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .question { background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .options { margin: 15px 0; }
        .option { 
            display: block; margin: 10px 0; padding: 12px; background: white;
            border: 2px solid #e9ecef; border-radius: 6px; cursor: pointer; transition: all 0.2s;
        }
        .option:hover { border-color: #667eea; background: #f8f9ff; }
        .option input { margin-right: 10px; }
        .btn { 
            background: #667eea; color: white; border: none; padding: 12px 24px;
            border-radius: 6px; cursor: pointer; font-size: 16px; margin: 10px 5px 10px 0;
        }
        .btn:hover { background: #5a6fd8; }
        .btn-secondary { background: #6c757d; }
        .btn-secondary:hover { background: #545b62; }
        .results { background: #d4edda; padding: 20px; border-radius: 8px; margin: 20px 0; }
        .mongodb { border-left: 5px solid #47a447; }
        .postgresql { border-left: 5px solid #337ab7; }
        .neutral { border-left: 5px solid #f0ad4e; }
        .progress { width: 100%; background: #e9ecef; border-radius: 4px; margin: 10px 0; }
        .progress-bar { height: 8px; background: #667eea; border-radius: 4px; transition: width 0.3s; }
        .trauma-recovery { background: #fff3cd; padding: 15px; border-radius: 6px; margin: 15px 0; }
        .hidden { display: none; }
        .factor { background: white; padding: 15px; margin: 10px 0; border-radius: 6px; border: 1px solid #dee2e6; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Database Selection Framework</h1>
        <p>MongoDB vs PostgreSQL Decision Engine</p>
        <p><small>Born from platform rigidity concerns - helping you choose with confidence</small></p>
    </div>

    <div id="intro-card" class="card">
        <h2>🚀 Get Started</h2>
        <p>This framework will ask you 4-5 core questions about your project to recommend either MongoDB or PostgreSQL.</p>
        <p><strong>Built-in platform rigidity concerns Recovery:</strong> Explicitly addresses platform rigidity and customization concerns.</p>
        
        <div>
            <label for="project-name">Project Name:</label><br>
            <input type="text" id="project-name" placeholder="My Custom Application" style="width: 100%; padding: 8px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px;">
        </div>
        
        <button class="btn" onclick="startAssessment()">Start Assessment</button>
        <button class="btn btn-secondary" onclick="showDemo()">View Demo</button>
        <button class="btn btn-secondary" onclick="loadSession()">Load Session</button>
    </div>

    <div id="assessment-card" class="card hidden">
        <h2>📊 Assessment</h2>
        <div class="progress">
            <div id="progress-bar" class="progress-bar" style="width: 0%"></div>
        </div>
        <div id="current-question"></div>
        <button class="btn" onclick="nextQuestion()">Next</button>
        <button class="btn btn-secondary" onclick="prevQuestion()">Previous</button>
    </div>

    <div id="results-card" class="card hidden">
        <h2>🎯 Recommendation</h2>
        <div id="recommendation"></div>
        <div id="scoring"></div>
        <div id="factors"></div>
        <div id="trauma-recovery" class="trauma-recovery"></div>
        <button class="btn" onclick="generateADR()">Generate ADR</button>
        <button class="btn btn-secondary" onclick="saveSession()">Save Session</button>
        <button class="btn btn-secondary" onclick="startOver()">Start Over</button>
    </div>

    <script>
        let questions = [];
        let currentQuestionIndex = 0;
        let responses = {};
        let projectName = "Custom Application";

        async function startAssessment() {
            projectName = document.getElementById('project-name').value || 'Custom Application';
            
            // Load questions
            const response = await fetch('/api/questions');
            questions = await response.json();
            
            document.getElementById('intro-card').classList.add('hidden');
            document.getElementById('assessment-card').classList.remove('hidden');
            
            showCurrentQuestion();
        }

        function showCurrentQuestion() {
            if (currentQuestionIndex >= questions.length) {
                submitAssessment();
                return;
            }

            const question = questions[currentQuestionIndex];
            const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
            
            document.getElementById('progress-bar').style.width = progress + '%';
            
            const questionHtml = `
                <div class="question">
                    <h3>${question.text}</h3>
                    <p><em>${question.context}</em></p>
                    <div class="options">
                        ${question.options.map((option, index) => `
                            <label class="option">
                                <input type="radio" name="q${currentQuestionIndex}" value="${option.key}">
                                ${option.text}
                            </label>
                        `).join('')}
                    </div>
                </div>
            `;
            
            document.getElementById('current-question').innerHTML = questionHtml;
        }

        function nextQuestion() {
            const selectedOption = document.querySelector(`input[name="q${currentQuestionIndex}"]:checked`);
            if (!selectedOption) {
                alert('Please select an option before continuing.');
                return;
            }

            responses[questions[currentQuestionIndex].id] = selectedOption.value;
            currentQuestionIndex++;
            showCurrentQuestion();
        }

        function prevQuestion() {
            if (currentQuestionIndex > 0) {
                currentQuestionIndex--;
                showCurrentQuestion();
            }
        }

        async function submitAssessment() {
            const assessmentData = {
                project_name: projectName,
                responses: responses
            };

            const response = await fetch('/api/assess', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(assessmentData)
            });

            const result = await response.json();
            showResults(result);
        }

        function showResults(result) {
            document.getElementById('assessment-card').classList.add('hidden');
            document.getElementById('results-card').classList.remove('hidden');

            const recommendation = result.recommendation;
            const confidence = result.confidence_level;
            
            let recClass = 'neutral';
            if (recommendation === 'MongoDB') recClass = 'mongodb';
            if (recommendation === 'PostgreSQL') recClass = 'postgresql';

            document.getElementById('recommendation').innerHTML = `
                <div class="results ${recClass}">
                    <h3>${recommendation}</h3>
                    <p><strong>Confidence:</strong> ${confidence}</p>
                </div>
            `;

            const mongoScore = result.mongodb_total_score;
            const pgScore = result.postgresql_total_score;
            const total = mongoScore + pgScore;
            const mongoPct = total > 0 ? (mongoScore / total * 100).toFixed(1) : 50;
            const pgPct = total > 0 ? (pgScore / total * 100).toFixed(1) : 50;

            document.getElementById('scoring').innerHTML = `
                <h4>📊 Scoring Breakdown</h4>
                <p>MongoDB: ${mongoScore.toFixed(2)} (${mongoPct}%)</p>
                <p>PostgreSQL: ${pgScore.toFixed(2)} (${pgPct}%)</p>
            `;

            const factorsHtml = result.responses.map((r, i) => `
                <div class="factor">
                    <strong>${r.question_text}</strong><br>
                    <small>Weight: ${(r.weight * 100).toFixed(0)}% | Your response: ${r.response}</small><br>
                    <em>${r.rationale}</em>
                </div>
            `).join('');

            document.getElementById('factors').innerHTML = `<h4>🔑 Decision Factors</h4>${factorsHtml}`;

            // platform rigidity concerns recovery
            let traumaHtml = `<h4>🛡️ platform rigidity concerns Recovery</h4>`;
            if (recommendation === 'MongoDB') {
                traumaHtml += `
                    <p>✅ MongoDB directly addresses platform limitations:</p>
                    <ul>
                        <li>Maximum schema flexibility - no rigid platform constraints</li>
                        <li>Document model enables unlimited business logic customization</li>
                        <li>JSON-native development with full team control</li>
                    </ul>
                `;
            } else if (recommendation === 'PostgreSQL') {
                traumaHtml += `
                    <p>✅ PostgreSQL addresses platform limitations:</p>
                    <ul>
                        <li>Open source eliminates vendor lock-in concerns</li>
                        <li>JSON capabilities provide document flexibility when needed</li>
                        <li>Standard SQL avoids proprietary platform constraints</li>
                    </ul>
                `;
            } else {
                traumaHtml += `<p>⚖️ Both options address platform rigidity concerns - recommend technical spikes</p>`;
            }

            document.getElementById('trauma-recovery').innerHTML = traumaHtml;
        }

        async function generateADR() {
            const response = await fetch('/api/generate-adr', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ project_name: projectName, responses: responses })
            });

            const result = await response.json();
            alert(`ADR generated: ${result.adr_path}`);
            
            // Open ADR in new window
            window.open(result.adr_path, '_blank');
        }

        function saveSession() {
            const sessionData = {
                project_name: projectName,
                responses: responses,
                timestamp: new Date().toISOString()
            };
            
            const blob = new Blob([JSON.stringify(sessionData, null, 2)], {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `session_${new Date().toISOString().split('T')[0]}.json`;
            a.click();
        }

        function startOver() {
            currentQuestionIndex = 0;
            responses = {};
            document.getElementById('results-card').classList.add('hidden');
            document.getElementById('intro-card').classList.remove('hidden');
        }

        function showDemo() {
            alert('Demo: Check the command line for: python3 database_selector.py demo');
        }

        function loadSession() {
            alert('To load a session, use: python3 database_selector.py load session_file.json');
        }
    </script>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def serve_questions(self):
        """Serve questions as JSON"""
        questions = self.question_set.get_core_questions()
        questions_data = []
        
        for q in questions:
            questions_data.append({
                'id': q.id,
                'text': q.text,
                'context': q.context.strip()[:200] + "..." if len(q.context.strip()) > 200 else q.context.strip(),
                'options': [{'key': opt.key, 'text': opt.text} for opt in q.options]
            })
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(questions_data).encode())
    
    def handle_assessment(self):
        """Handle assessment submission"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        framework = DatabaseFramework()
        question_set = QuestionSet()
        
        # Add responses
        for question_id, response_key in data['responses'].items():
            question = question_set.get_question(question_id)
            if question:
                selected_option = next((opt for opt in question.options if opt.key == response_key), None)
                if selected_option:
                    framework.add_response(
                        question_id=question_id,
                        question_text=question.text,
                        response_key=response_key,
                        response_text=selected_option.text
                    )
        
        # Add context
        framework.add_context('project_name', data.get('project_name', 'Web Application'))
        framework.add_context('interface', 'web_ui')
        
        # Calculate decision
        decision = framework.calculate_decision()
        
        # Prepare response
        result = {
            'recommendation': decision.recommendation.value,
            'confidence_level': decision.confidence_level,
            'mongodb_total_score': decision.mongodb_total_score,
            'postgresql_total_score': decision.postgresql_total_score,
            'responses': [
                {
                    'question_text': r.question_text,
                    'response': r.response,
                    'weight': r.weight,
                    'mongodb_score': r.mongodb_score,
                    'postgresql_score': r.postgresql_score,
                    'rationale': r.rationale
                } for r in decision.responses
            ]
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

def find_free_port(start_port=8080, max_attempts=10):
    """Find a free port starting from start_port"""
    import socket
    
    for attempt in range(max_attempts):
        test_port = start_port + attempt
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', test_port))
                return test_port
        except OSError:
            continue
    
    # If no free port found, raise an exception
    raise RuntimeError(f"No free port found in range {start_port}-{start_port + max_attempts - 1}")

def start_web_server(port=8080, auto_find_port=True):
    """Start the web server with automatic port conflict resolution"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    original_port = port
    
    if auto_find_port:
        try:
            # First try the requested port
            with socketserver.TCPServer(("", port), DatabaseSelectorHandler) as test_httpd:
                pass
        except OSError:
            print(f"⚠️  Port {port} is already in use")
            try:
                port = find_free_port(port + 1)
                print(f"🔄 Automatically using port {port} instead")
            except RuntimeError as e:
                print(f"❌ {e}")
                print(f"💡 Try specifying a different port: python3 web_ui.py <port>")
                return
    
    try:
        with socketserver.TCPServer(("", port), DatabaseSelectorHandler) as httpd:
            print(f"\n🌐 Database Selection Framework Web UI")
            print(f"📡 Server running at: http://localhost:{port}")
            if port != original_port:
                print(f"   (Originally requested port {original_port}, but using {port})")
            print(f"🎯 Open your browser and start the assessment!")
            print(f"⏹️  Press Ctrl+C to stop the server")
            print(f"\n💡 Next time, use: python3 web_ui.py {port} (to use this port directly)")
            print()
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print(f"\n👋 Server stopped. Thanks for using Database Selection Framework!")
                
    except OSError as e:
        print(f"❌ Failed to start server on port {port}: {e}")
        print(f"💡 Try a different port: python3 web_ui.py <port>")
        return

if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
            if port < 1024:
                print(f"⚠️  Warning: Port {port} may require administrator privileges")
            elif port > 65535:
                print(f"❌ Invalid port {port}. Port must be between 1-65535")
                sys.exit(1)
        except ValueError:
            print(f"❌ Invalid port '{sys.argv[1]}'. Please provide a valid port number.")
            print(f"💡 Usage: python3 web_ui.py [port]")
            print(f"💡 Example: python3 web_ui.py 8090")
            sys.exit(1)
    else:
        port = 8080
    
    print(f"🚀 Starting Database Selection Framework Web UI...")
    start_web_server(port)
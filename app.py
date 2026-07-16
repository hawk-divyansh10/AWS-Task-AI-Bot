from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In-Memory Database for demonstration
tasks = [
    {"id": 1, "text": "Setup Dockerfile with Alpine image", "priority": "High", "completed": True},
    {"id": 2, "text": "Configure AWS EC2 Security Groups", "priority": "High", "completed": False},
    {"id": 3, "text": "Optimize Flask backend API routing", "priority": "Medium", "completed": False}
]
task_id_counter = 4

@app.route('/')
def index():
    return render_template('index.html')

# API Route: Get all tasks
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# API Route: Create task
@app.route('/api/tasks', methods=['POST'])
def add_task():
    global task_id_counter
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    new_task = {
        "id": task_id_counter,
        "text": data['text'],
        "priority": data.get('priority', 'Medium'),
        "completed": False
    }
    tasks.append(new_task)
    task_id_counter += 1
    return jsonify(new_task), 201

# API Route: Toggle task completion
@app.route('/api/tasks/<int:task_id>', methods=['PATCH'])
def toggle_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

# API Route: Delete task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({"success": True})

# API Route: Rule-based AI Assistant Simulation
@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    data = request.json
    user_message = data.get('message', '').lower()
    
    if "prioritize" in user_message or "schedule" in user_message:
        high_tasks = [t['text'] for t in tasks if t['priority'] == 'High' and not t['completed']]
        if high_tasks:
            reply = f"Focus immediately on High Priority items: {', '.join(high_tasks)}."
        else:
            reply = "All high priority tasks are clear! You can safely pick up medium or low items."
    elif "status" in user_message or "health" in user_message:
        pending = len([t for t in tasks if not t['completed']])
        reply = f"Container: Healthy. You have {pending} pending tasks active on this EC2 node."
    else:
        reply = "I am your CloudTask AI Engine. Type 'prioritize tasks' or check 'system status' for real-time analysis."
        
    return jsonify({"reply": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
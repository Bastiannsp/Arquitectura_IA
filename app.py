from flask import Flask, request, jsonify

app = Flask(__name__)

# Base de datos simulada en memoria
tasks = [
    {"id": 1, "title": "Tarea 1", "description": "Hacer la compra"},
    {"id": 2, "title": "Tarea 2", "description": "Llamar al cliente"}
]
# Contador para simular IDs autoincrementables
task_id_counter = 3

# Health Check (Buena práctica)
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

# GET (Obtener todas las tareas)
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks}), 200

# GET (Obtener una tarea específica)
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        return jsonify(task), 200
    return jsonify({"error": "Tarea no encontrada"}), 404

# POST (Crear una nueva tarea)
@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id_counter
    data = request.json
    
    if not data or "title" not in data:
        return jsonify({"error": "Datos incompletos. Se requiere 'title'."}), 400
    
    new_task = {
        "id": task_id_counter,
        "title": data["title"],
        "description": data.get("description", "") # Descripción es opcional
    }
    
    tasks.append(new_task)
    task_id_counter += 1
    
    return jsonify(new_task), 201

# PUT (Actualizar una tarea existente)
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404
    
    data = request.json
    if not data:
        return jsonify({"error": "No hay datos para actualizar"}), 400

    # Actualiza los campos proporcionados
    task["title"] = data.get("title", task["title"])
    task["description"] = data.get("description", task["description"])
    
    return jsonify(task), 200

# DELETE (Eliminar una tarea)
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t["id"] == task_id), None)
    
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404
        
    tasks = [t for t in tasks if t["id"] != task_id]
    
    return jsonify({"message": "Tarea eliminada correctamente"}), 200

# Se mantiene el 'app.run' para pruebas locales
if __name__ == "__main__":
    # 0.0.0.0 es necesario para que sea accesible desde fuera del contenedor
    app.run(debug=True, host="0.0.0.0", port=5000)
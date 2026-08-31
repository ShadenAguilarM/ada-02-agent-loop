import os
import subprocess


# 1. HERRAMIENTAS

# READ: lee un archivo y devuelve su contenido.
def tool_read(filepath):
    if not os.path.exists(filepath):
        return {"success": False, "content": f"No existe: {filepath}"}

    with open(filepath, "r", encoding="utf-8") as file:
        return {"success": True, "content": file.read()}


# WRITE: escribe contenido en un archivo.
def tool_write(filepath, content):
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)

    return {"success": True, "content": f"Archivo escrito: {filepath}"}

# EDIT: reemplaza una parte específica de un archivo.
def tool_edit(filepath, old_text, new_text):
    if not os.path.exists(filepath):
        return {"success": False, "content": f"No existe: {filepath}"}

    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    if old_text not in content:
        return {"success": False, "content": "No se encontró el texto a editar."}

    content = content.replace(old_text, new_text)
    
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)

    return {"success": True, "content": f"Archivo editado: {filepath}"}

# BASH: ejecuta un comando en la terminal y devuelve su salida.
def tool_bash(command):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    output = (result.stdout + result.stderr).strip()

    return {
        "success": result.returncode == 0,
        "content": output
    }


# 2. EJECUTAR LA HERRAMIENTA ELEGIDA

# Ejecuta la herramienta seleccionada por el agente y devuelve la observación.
def execute_tool(action):
    tool = action["tool"]
    args = action["args"]

    if tool == "READ":
        return tool_read(args["filepath"])

    if tool == "WRITE":
        return tool_write(args["filepath"], args["content"])

    if tool == "EDIT":
        return tool_edit(
            args["filepath"],
            args["old_text"],
            args["new_text"]
        )

    if tool == "BASH":
        return tool_bash(args["command"])

    return {"success": False, "content": "Herramienta desconocida."}


# 3. TAREA Y DECISIÓN

# La tarea es encontrar y corregir un bug en el archivo calculator.py.
def get_task():
    return "Find and fix the bug in the calculator."

# La decisión del agente depende del paso actual en el contexto.
def decide_action(context):
    step = len(context["history"])

    if step == 0:
        return {
            "tool": "READ",
            "args": {"filepath": "calculator.py"}
        }

    if step == 1:
        return {
            "tool": "READ",
            "args": {"filepath": "test_calculator.py"}
        }

    if step == 2:
        return {
            "tool": "BASH",
            "args": {"command": "pytest -q"}
        }

    if step == 3:
        return {
            "tool": "EDIT",
            "args": {
                "filepath": "calculator.py",
                "old_text": "def divide(a, b):\n    return a * b",
                "new_text": "def divide(a, b):\n    return a / b"
            }
        }

    if step == 4:
        return {
            "tool": "BASH",
            "args": {"command": "pytest -q"}
        }


# 4. ACTUALIZAR EL CONTEXTO

# Actualiza el contexto del agente con la acción tomada y la observación recibida.
def update_context(context, action, observation):
    context["history"].append({
        "action": action,
        "observation": observation
    })

    total_steps = len(context["history"])

    # Después de leer los dos archivos, se ejecuta pytest por primera vez.
    if total_steps == 3:
        if observation["success"]:
            context["finished"] = True
            context["result"] = "no_changes"
        return

    # Si la edición no pudo realizarse, se detiene y lo informa.
    if action["tool"] == "EDIT":
        if observation["success"]:
            context["edit_made"] = True
        else:
            context["finished"] = True
            context["result"] = "edit_failed"
        return

    # pytest final: solo hubo corrección si EDIT funcionó y los tests pasaron.
    if total_steps == 5 and action["tool"] == "BASH":
        context["finished"] = True

        if context["edit_made"] and observation["success"]:
            context["result"] = "fixed"
        else:
            context["result"] = "tests_failed"


# 5. LOOP PRINCIPAL

# Ejecuta el loop del agente hasta que se complete la tarea.
def run_agent():

    # Obtiene la tarea a realizar.
    task = get_task() 

    # Inicializa el contexto del agente.
    context = {
        "history": [],
        "finished": False,
        "edit_made": False,
        "result": ""
    }

    print("\n=== MINI-AGENT LOOP ===\n")
    print(f"Tarea: {task}\n")

    # Loop principal del agente: decide acción, ejecuta herramienta, recibe observación y actualiza contexto.
    while not context["finished"]:
        action = decide_action(context) # Decide la acción a tomar según el contexto.

        print("Decisión:")
        print(action) # Muestra la acción decidida por el agente.

        observation = execute_tool(action) # Ejecuta la herramienta y obtiene la observación.

        print("\nObservación:")
        print(observation["content"]) # Muestra la observación obtenida tras ejecutar la herramienta.
        print()

        update_context(context, action, observation) # Actualiza el contexto del agente con la acción y observación.

    # Resultado final del loop del agente.
    print("=== RESULTADO FINAL ===")

    if context["result"] == "fixed":
        print("El bug fue corregido y los tests pasaron.")

    elif context["result"] == "no_changes":
        print("No se realizaron cambios: los tests ya pasaban al iniciar.")

    elif context["result"] == "edit_failed":
        print("No se pudo realizar la edición esperada.")

    else:
        print("La edición se intentó, pero los tests finales fallaron.")

if __name__ == "__main__":
    run_agent()
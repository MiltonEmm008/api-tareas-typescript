#!/usr/bin/env python3
import os
import json
import subprocess
import sys

def create_directory_structure(project_name):
    """Crear la estructura de directorios del proyecto"""
    directories = [
        project_name,
        f"{project_name}/src",
        f"{project_name}/src/db"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Directorio creado: {directory}")

def create_package_json(project_name):
    """Crear el archivo package.json"""
    package_data = {
        "name": project_name,
        "version": "1.0.0",
        "description": f"API minimalista con Express, TypeScript y SQLite - {project_name}",
        "main": "index.js",
        "scripts": {
            "test": "echo \"Error: no test specified\" && exit 1",
            "dev": "ts-node-dev --respawn src/index.ts",
            "build": "tsc",
            "start": "node dist/index.js"
        },
        "keywords": ["express", "typescript", "sqlite", "api"],
        "author": "",
        "license": "ISC",
        "type": "commonjs",
        "dependencies": {
            "better-sqlite3": "^12.2.0",
            "express": "^5.1.0"
        },
        "devDependencies": {
            "@types/better-sqlite3": "^7.6.13",
            "@types/express": "^5.0.3",
            "@types/node": "^24.0.10",
            "ts-node-dev": "^2.0.0",
            "typescript": "^5.8.3"
        }
    }
    
    with open(f"{project_name}/package.json", "w", encoding="utf-8") as f:
        json.dump(package_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ package.json creado")

def create_tsconfig_json(project_name):
    """Crear el archivo tsconfig.json"""
    tsconfig_content = '''{
  "compilerOptions": {
    "target": "ES2020",
    "module": "CommonJS",
    "rootDir": "./src",
    "outDir": "./dist",
    "strict": true,
    "esModuleInterop": true
  }
}'''
    
    with open(f"{project_name}/tsconfig.json", "w", encoding="utf-8") as f:
        f.write(tsconfig_content)
    
    print(f"✓ tsconfig.json creado")

def create_gitignore(project_name):
    """Crear el archivo .gitignore"""
    gitignore_content = """node_modules
dist
*.db
.env
.DS_Store
"""
    
    with open(f"{project_name}/.gitignore", "w", encoding="utf-8") as f:
        f.write(gitignore_content)
    
    print(f"✓ .gitignore creado")

def create_db_file(project_name):
    """Crear el archivo de configuración de base de datos"""
    db_content = '''import Database from "better-sqlite3";
import path from "path";

const db = new Database(path.resolve(__dirname, "tareas.db"));

// Creamos la tabla si no existe
db.exec(`
CREATE TABLE IF NOT EXISTS tareas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    completado INTEGER DEFAULT 0
)`);

export default db;
'''
    
    with open(f"{project_name}/src/db/db.ts", "w", encoding="utf-8") as f:
        f.write(db_content)
    
    print(f"✓ src/db/db.ts creado")

def create_index_file(project_name):
    """Crear el archivo principal index.ts"""
    index_content = '''import express, { Request, Response } from "express";
import db from "./db/db";

const app = express();
const port = 3000;

app.use(express.json());

interface Tarea {
  id: number;
  titulo: string;
  completado: boolean;
}

// Bienvenida
app.get("/", (request: Request, response: Response) => {
  response.json({ mensaje: "Api de tareas funcionando con typescript" });
});

// Obtener todas las tareas
app.get("/tareas", (request: Request, response: Response) => {
  const stmt = db.prepare(`SELECT 
    id,
    titulo,
    CASE completado 
      WHEN 1 THEN 'Completado' 
      ELSE 'Pendiente' 
    END AS estado
  FROM tareas`);
  const tareas = stmt.all();
  response.json(tareas);
});

// Añadir tarea
app.post("/tareas", (request: Request, response: Response) => {
  const { titulo } = request.body;
  const stmt = db.prepare("INSERT INTO tareas (titulo) VALUES (?)");
  const resultado = stmt.run(titulo);
  const nuevaTarea = db
    .prepare("SELECT * FROM tareas WHERE id = ?")
    .get(resultado.lastInsertRowid);
  response.status(201).json(nuevaTarea);
});

// Cambiar completado
app.put("/tareas/:id", (request: Request, response: Response) => {
  const id = Number(request.params.id);
  const tarea = db.prepare("SELECT * FROM tareas WHERE id = ?").get(id) as
    | Tarea
    | undefined;
  if (!tarea) {
    response.status(404).json({ mensaje: "No se encontro la tarea" });
    return;
  }

  const tareaActualizada = db
    .prepare("UPDATE tareas SET completado = ? WHERE id = ?")
    .run(tarea.completado ? 0 : 1, id);
  response.status(200).json(tareaActualizada);
});

// Eliminar tarea
app.delete("/tareas/:id", (request: Request, response: Response) => {
  const id = Number(request.params.id);
  const tarea = db.prepare("SELECT * FROM tareas WHERE id = ?").get(id) as
    | Tarea
    | undefined;

  if (!tarea) {
    response.status(404).json({ mensaje: "No se encontro la tarea" });
    return;
  }

  db.prepare("DELETE FROM tareas WHERE id = ?").run(id);
  response.status(204).send();
});

app.listen(port, () => {
  console.log(`Api de tareas corriendo en http://localhost:${port}`);
});
'''
    
    with open(f"{project_name}/src/index.ts", "w", encoding="utf-8") as f:
        f.write(index_content)
    
    print(f"✓ src/index.ts creado")

def create_readme(project_name):
    """Crear un README.md básico"""
    readme_content = f'''# {project_name}

API minimalista construida con Express, TypeScript y SQLite.

## Instalación

```bash
npm install
```

## Scripts disponibles

- `npm run dev` - Ejecutar en modo desarrollo con hot reload
- `npm run build` - Compilar TypeScript a JavaScript
- `npm start` - Ejecutar la aplicación compilada

## Endpoints

- `GET /` - Mensaje de bienvenida
- `GET /tareas` - Obtener todas las tareas
- `POST /tareas` - Crear una nueva tarea
- `PUT /tareas/:id` - Cambiar estado de completado de una tarea
- `DELETE /tareas/:id` - Eliminar una tarea

## Estructura del proyecto

```
{project_name}/
├── src/
│   ├── db/
│   │   └── db.ts
│   └── index.ts
├── dist/
├── package.json
├── tsconfig.json
└── .gitignore
```
'''
    
    with open(f"{project_name}/README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"README.md creado")

def main():
    """Función principal del script"""
    print("Generador de API Express + TypeScript + SQLite")
    print("=" * 50)
    
    # Solicitar nombre del proyecto
    project_name = input("Ingresa el nombre del proyecto: ").strip()
    
    if not project_name:
        print("El nombre del proyecto no puede estar vacío")
        sys.exit(1)
    
    # Validar que el directorio no exista
    if os.path.exists(project_name):
        print(f"El directorio '{project_name}' ya existe")
        sys.exit(1)
    
    print(f"\nCreando proyecto: {project_name}")
    print("-" * 30)
    
    # Crear estructura del proyecto
    create_directory_structure(project_name)
    create_package_json(project_name)
    create_tsconfig_json(project_name)
    create_gitignore(project_name)
    create_db_file(project_name)
    create_index_file(project_name)
    create_readme(project_name)
    
    print(f"\nProyecto '{project_name}' creado exitosamente!")
    print(f"\nPróximos pasos:")
    print(f"   cd {project_name}")
    print(f"   npm install")
    print(f"   npm run dev")
    print(f"\nLa API estará disponible en: http://localhost:3000")

if __name__ == "__main__":
    main() 
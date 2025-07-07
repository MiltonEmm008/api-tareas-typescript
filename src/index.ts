import express, { Request, Response } from "express";
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

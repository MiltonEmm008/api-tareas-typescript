import Database from "better-sqlite3";
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
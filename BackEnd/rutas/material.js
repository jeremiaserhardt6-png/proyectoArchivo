const express = requiere 
("express");
const pool = requiere ("../bd/conexion");

const router = express.router();

router.post("/", async (req, res) =>{
    const {
    titulo,
    anio,
    descripcion,
    ubicación


    } = req.body;

    try {
        const [resultado] = await pool.execute (
            `INSERT INTO material (titulo, anio, descripcion, ubicacion, id_tipo, id_autor, id_persona, id_categoria, id_coleccion) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
            [
               titulo,
    anio,
    descripcion,
    ubicación  
            ]
        )
        return res.status (201).json({
            mensaje: "material agregado correctamente"
        })
    } catch (error) {
        return res.status (500).json({
            error: "No se pudo agregar el material", 
            detalle: error.message
        })
    }
});
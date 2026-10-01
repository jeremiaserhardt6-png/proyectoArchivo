const express = require("express");
const pool = require("../bd/conexion");

const router = express.Router();

// AGREGAR MATERIAL
router.post("/", async (req, res) => {
    const {
        titulo,
        anio,
        descripcion,
        ubicacion,
        id_tipo,
        id_autor,
        id_persona,
        id_categoria,
        id_coleccion
    } = req.body;

    try {
        const [resultado] = await pool.execute(
            `INSERT INTO material 
            (titulo, anio, descripcion, ubicacion, id_tipo, id_autor, id_persona, id_categoria, id_coleccion) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
            [
                titulo,
                anio,
                descripcion,
                ubicacion,
                id_tipo,
                id_autor,
                id_persona,
                id_categoria,
                id_coleccion
            ]
        );

        return res.status(201).json({
            mensaje: "Material agregado correctamente",
            id: resultado.insertId
        });

    } catch (error) {
        return res.status(500).json({
            error: "No se pudo agregar el material",
            detalle: error.message
        });
    }
});


// LISTAR TODOS LOS MATERIALES
router.get("/", async (req, res) => {
    try {
        const [materiales] = await pool.execute(
            `SELECT * FROM material`
        );

        return res.status(200).json(materiales);

    } catch (error) {
        return res.status(500).json({
            error: "No se pudieron listar los materiales",
            detalle: error.message
        });
    }
});


// EDITAR MATERIAL
router.put("/:id", async (req, res) => {
    const { id } = req.params;

    const {
        titulo,
        anio,
        descripcion,
        ubicacion,
        id_tipo,
        id_autor,
        id_persona,
        id_categoria,
        id_coleccion
    } = req.body;

    try {
        const [resultado] = await pool.execute(
            `UPDATE material 
             SET titulo = ?,
                 anio = ?,
                 descripcion = ?,
                 ubicacion = ?,
                 id_tipo = ?,
                 id_autor = ?,
                 id_persona = ?,
                 id_categoria = ?,
                 id_coleccion = ?
             WHERE id_material = ?`,
            [
                titulo,
                anio,
                descripcion,
                ubicacion,
                id_tipo,
                id_autor,
                id_persona,
                id_categoria,
                id_coleccion,
                id
            ]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: "Material no encontrado"
            });
        }

        return res.status(200).json({
            mensaje: "Material actualizado correctamente"
        });

    } catch (error) {
        return res.status(500).json({
            error: "No se pudo actualizar el material",
            detalle: error.message
        });
    }
});


// ELIMINAR MATERIAL
router.delete("/:id", async (req, res) => {
    const { id } = req.params;

    try {
        const [resultado] = await pool.execute(
            `DELETE FROM material WHERE id_material = ?`,
            [id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: "Material no encontrado"
            });
        }

        return res.status(200).json({
            mensaje: "Material eliminado correctamente"
        });

    } catch (error) {
        return res.status(500).json({
            error: "No se pudo eliminar el material",
            detalle: error.message
        });
    }
});


module.exports = router;


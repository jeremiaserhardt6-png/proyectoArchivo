const express = require("express");
const pool = require("../bd/conexion");

const router = express.Router();


// ============================================================
// CREAR AUTOR
// ============================================================

router.post("/", async (req, res) => {

    const {
        nombre,
        apellido,
        fecha_nacimiento
    } = req.body;

    try {

        const [resultado] = await pool.execute(
            `INSERT INTO autores
            (nombre, apellido, fecha_nacimiento)
            VALUES (?, ?, ?)`,
            [
                nombre,
                apellido,
                fecha_nacimiento
            ]
        );

        return res.status(201).json({
            mensaje: "Autor agregado correctamente",
            id: resultado.insertId
        });

    } catch (error) {

        return res.status(500).json({
            error: "No se pudo agregar el autor",
            detalle: error.message
        });

    }

});


// ============================================================
// LISTAR TODOS LOS AUTORES
// ============================================================

router.get("/", async (req, res) => {

    try {

        const [autores] = await pool.execute(
            `SELECT * FROM autores`
        );

        return res.status(200).json(autores);

    } catch (error) {

        return res.status(500).json({
            error: "No se pudieron listar los autores",
            detalle: error.message
        });

    }

});


// ============================================================
// EDITAR AUTOR
// ============================================================

router.put("/:id", async (req, res) => {

    const { id } = req.params;

    const {
        nombre,
        apellido,
        fecha_nacimiento
    } = req.body;

    try {

        const [resultado] = await pool.execute(
            `UPDATE autores
             SET nombre = ?,
                 apellido = ?,
                 fecha_nacimiento = ?
             WHERE id_autor = ?`,
            [
                nombre,
                apellido,
                fecha_nacimiento,
                id
            ]
        );

        if (resultado.affectedRows === 0) {

            return res.status(404).json({
                error: "Autor no encontrado"
            });

        }

        return res.status(200).json({
            mensaje: "Autor actualizado correctamente"
        });

    } catch (error) {

        return res.status(500).json({
            error: "No se pudo actualizar el autor",
            detalle: error.message
        });

    }

});


// ============================================================
// ELIMINAR AUTOR
// ============================================================

router.delete("/:id", async (req, res) => {

    const { id } = req.params;

    try {

        const [resultado] = await pool.execute(
            `DELETE FROM autores
             WHERE id_autor = ?`,
            [id]
        );

        if (resultado.affectedRows === 0) {

            return res.status(404).json({
                error: "Autor no encontrado"
            });

        }

        return res.status(200).json({
            mensaje: "Autor eliminado correctamente"
        });

    } catch (error) {

        return res.status(500).json({
            error: "No se pudo eliminar el autor",
            detalle: error.message
        });

    }

});


module.exports = router;

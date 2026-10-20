
const express = require("express");
const pool = require("../bd/conexion");

const router = express.Router();

// ============================================================
// AGREGAR PERSONA
// ============================================================

router.post("/", async (req, res) => {
    const { nombre, apellido, telefono } = req.body;

    if (!nombre || !apellido) {
        return res.status(400).json({
            error: "El nombre y el apellido son obligatorios"
        });
    }

    try {
        const [resultado] = await pool.execute(
            `INSERT INTO persona (nombre, apellido, telefono)
             VALUES (?, ?, ?)`,
            [nombre, apellido, telefono || null]
        );

        res.status(201).json({
            mensaje: "Persona agregada correctamente",
            id: resultado.insertId
        });

    } catch (error) {
        res.status(500).json({
            error: "No se pudo agregar la persona",
            detalle: error.message
        });
    }
});

// ============================================================
// LISTAR TODAS LAS PERSONAS
// ============================================================

router.get("/", async (req, res) => {
    try {
        const [personas] = await pool.execute(
            "SELECT * FROM persona ORDER BY id_persona DESC"
        );

        res.json(personas);

    } catch (error) {
        res.status(500).json({
            error: "No se pudieron listar las personas",
            detalle: error.message
        });
    }
});

// ============================================================
// BUSCAR PERSONA POR ID
// ============================================================

router.get("/:id", async (req, res) => {
    const { id } = req.params;

    if (!Number.isInteger(Number(id)) || Number(id) < 1) {
        return res.status(400).json({
            error: "El ID debe ser un número válido"
        });
    }

    try {
        const [personas] = await pool.execute(
            "SELECT * FROM persona WHERE id_persona = ?",
            [id]
        );

        if (personas.length === 0) {
            return res.status(404).json({
                error: "Persona no encontrada"
            });
        }

        res.json(personas[0]);

    } catch (error) {
        res.status(500).json({
            error: "No se pudo buscar la persona",
            detalle: error.message
        });
    }
});

// ============================================================
// EDITAR PERSONA
// ============================================================

router.put("/:id", async (req, res) => {
    const { id } = req.params;
    const { nombre, apellido, telefono } = req.body;

    if (!Number.isInteger(Number(id)) || Number(id) < 1) {
        return res.status(400).json({
            error: "El ID debe ser un número válido"
        });
    }

    if (!nombre || !apellido) {
        return res.status(400).json({
            error: "El nombre y el apellido son obligatorios"
        });
    }

    try {
        const [resultado] = await pool.execute(
            `UPDATE persona
             SET nombre = ?, apellido = ?, telefono = ?
             WHERE id_persona = ?`,
            [nombre, apellido, telefono || null, id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: "Persona no encontrada"
            });
        }

        res.json({
            mensaje: "Persona actualizada correctamente"
        });

    } catch (error) {
        res.status(500).json({
            error: "No se pudo actualizar la persona",
            detalle: error.message
        });
    }
});

// ============================================================
// ELIMINAR PERSONA
// ============================================================

router.delete("/:id", async (req, res) => {
    const { id } = req.params;

    if (!Number.isInteger(Number(id)) || Number(id) < 1) {
        return res.status(400).json({
            error: "El ID debe ser un número válido"
        });
    }

    try {
        const [resultado] = await pool.execute(
            "DELETE FROM persona WHERE id_persona = ?",
            [id]
        );

        if (resultado.affectedRows === 0) {
            return res.status(404).json({
                error: "Persona no encontrada"
            });
        }

        res.json({
            mensaje: "Persona eliminada correctamente"
        });

    } catch (error) {
        res.status(500).json({
            error: "No se pudo eliminar la persona",
            detalle: error.message
        });
    }
});

module.exports = router;

const express = require("express");
const pool = require("../bd/conexion");

const router = express.Router();


// ============================================================
// CREAR USUARIO
// ============================================================

router.post("/", async (req, res) => {

    const {
        nombre_usuario,
        contrasena,
        rol,
        id_persona
    } = req.body;

    try {

        const [resultado] = await pool.execute(
            `INSERT INTO usuario
            (nombre_usuario, contrasena, rol, id_persona)
            VALUES (?, ?, ?, ?)`,
            [
                nombre_usuario,
                contrasena,
                rol,
                id_persona
            ]
        );

        return res.status(201).json({
            mensaje: "Usuario agregado correctamente",
            id: resultado.insertId
        });

    } catch (error) {

        return res.status(500).json({
            error: "No se pudo agregar el usuario",
            detalle: error.message
        });

    }

});


// ============================================================
// LISTAR TODOS LOS USUARIOS
// ============================================================

router.get("/", async (req, res) => {

    try {

        const [usuarios] = await pool.execute(
            `SELECT id_usuario, nombre_usuario, rol, id_persona
             FROM usuario`
        );

        return res.status(200).json(usuarios);

    } catch (error) {

        return res.status(500).json({
            error: "No se pudieron listar los usuarios",
            detalle: error.message
        });

    }

});


// ============================================================
// EDITAR USUARIO
// ============================================================

router.put("/:id", async (req, res) => {

    const { id } = req.params;

    const {
        nombre_usuario,
        contrasena,
        rol,
        id_persona
    } = req.body;

    try {

        const [resultado] = await pool.execute(
            `UPDATE usuario
             SET nombre_usuario = ?,
                 contrasena = ?,
                 rol = ?,
                 id_persona = ?
             WHERE id_usuario = ?`,
            [
                nombre_usuario,
                contrasena,
                rol,
                id_persona,
                id
            ]
        );

        if (resultado.affectedRows === 0) {

            return res.status(404).json({
                error: "Usuario no encontrado"
            });

        }

        return res.status(200).json({
            mensaje: "Usuario actualizado correctamente"
        });

    } catch (error) {

        return res.status(500).json({
            error: "No se pudo actualizar el usuario",
            detalle: error.message
        });

    }

});


// ============================================================
// ELIMINAR USUARIO
// ============================================================

router.delete("/:id", async (req, res) => {

    const { id } = req.params;

    try {

        const [resultado] = await pool.execute(
            `DELETE FROM usuario
             WHERE id_usuario = ?`,
            [id]
        );

        if (resultado.affectedRows === 0) {

            return res.status(404).json({
                error: "Usuario no encontrado"
            });

        }

        return res.status(200).json({
            mensaje: "Usuario eliminado correctamente"
        });

    } catch (error) {

        return res.status(500).json({
            error: "No se pudo eliminar el usuario",
            detalle: error.message
        });

    }

});

module.exports = router;

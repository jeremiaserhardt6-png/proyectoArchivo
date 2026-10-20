const express = require("express");
const pool = require("../bd/conexion");

const router = express.Router();

// LISTAR COLECCIONES
router.get("/", async (req, res) => {
    try {
        const [colecciones] = await pool.execute(
            "SELECT id_coleccion, nombre, descripcion FROM coleccion ORDER BY nombre"
        );

        res.json(colecciones);
    } catch (error) {
        res.status(500).json({
            error: "No se pudieron listar las colecciones",
            detalle: error.message
        });
    }
});

module.exports = router;
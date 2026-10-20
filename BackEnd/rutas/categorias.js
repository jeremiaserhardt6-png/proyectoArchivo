const express = require("express");
const pool = require("../bd/conexion");

const router = express.Router();

// LISTAR CATEGORÍAS
router.get("/", async (req, res) => {
    try {
        const [categorias] = await pool.execute(
            "SELECT id_categoria, nombre, descripcion FROM categoria ORDER BY nombre"
        );

        res.json(categorias);
    } catch (error) {
        res.status(500).json({
            error: "No se pudieron listar las categorías",
            detalle: error.message
        });
    }
});

module.exports = router;
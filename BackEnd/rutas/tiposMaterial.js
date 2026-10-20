const express = require("express");
const pool = require("../bd/conexion");

const router = express.Router();

// LISTAR TIPOS DE MATERIAL
router.get("/", async (req, res) => {
    try {
        const [tipos] = await pool.execute(
            "SELECT id_tipo, nombredeltipo FROM tipodematerial ORDER BY nombredeltipo"
        );

        res.json(tipos);
    } catch (error) {
        res.status(500).json({
            error: "No se pudieron listar los tipos de material",
            detalle: error.message
        });
    }
});

module.exports = router;
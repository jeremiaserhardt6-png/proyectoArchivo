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

});
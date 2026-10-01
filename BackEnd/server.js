const express = require("express");
const pool = require("./bd/conexion")
const routerMateriales = require("./rutas/material")

const app=express();
const PORT =3000;

app.use(express.json());

app.use("/api/materiales", routerMateriales)


async function probarConexion() {
      try {
            await pool.query("select 1");
            console.log("conexion exitosa")
      } catch (error) {
            console.log("Error en la conexion")
            console.log(error.message)
      }
      
}

app.listen(PORT, async () => {
      console.log(`servidor ejecutandose en https://localhost:${PORT}`)
      await probarConexion()
  
})
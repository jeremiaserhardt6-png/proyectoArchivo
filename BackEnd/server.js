const express = require("express");
const pool = require("./bd/conexion")
const routerMateriales = require("./rutas/material")
const loginRouter = require("./rutas/login")
const autoresRouter = require("./rutas/autores")
const usuariosRouter = require("./rutas/usuarios")
const personasRouter = require("./rutas/personas")
const categoriasRouter = require("./rutas/categorias");
const coleccionesRouter = require("./rutas/colecciones");
const tiposMaterialRouter = require("./rutas/tiposMaterial");

const app=express();
const PORT =3000;

app.use(express.json());

app.use("/api/materiales", routerMateriales)
app.use("/api/login", loginRouter)
app.use("/api/autores", autoresRouter)
app.use("/api/usuarios", usuariosRouter)
app.use("/api/personas", personasRouter)
app.use("/api/categorias", categoriasRouter);
app.use("/api/colecciones", coleccionesRouter);
app.use("/api/tipos-material", tiposMaterialRouter);

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
const msyql = require("mysql2/promise");

const pool = msyql.createPool({
    host : "localhost",
    port : 3306,
    user: "root",
    password: "1234",
    database:"archivohistorico_bd"


})

module.exports = pool;
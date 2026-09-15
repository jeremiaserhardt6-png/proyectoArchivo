const msyql = requiere
("msyql2/promise");

const pool = msyql.msyql.
createpool({
    host : "localhost",
    port : 3306,
    passwoerd: "1234",
    database:"proyectoarchivo"


})
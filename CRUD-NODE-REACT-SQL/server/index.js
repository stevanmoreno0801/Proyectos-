const express = require('express');
const cors = require('cors');
// 1. CORRECCIÓN: Importamos directamente 'connection' ya que es el objeto de conexión
const { connection } = require('./db'); 

const app = express();
// Middleware para permitir solicitudes de origen cruzado (CORS)
app.use(cors());
// Middleware para parsear el cuerpo de las solicitudes como JSON
app.use(express.json());

// ====================================================================
// RUTAS PARA PRODUCTOS
// ====================================================================

// RUTA: Obtener todos los productos
// Cambiado de /empleados a /productos para coincidir con el Front-End
app.get('/productos', (req, res) => {
    // CORRECCIÓN: Usar la variable 'connection' en lugar de 'db.db'
    const sql = 'SELECT * FROM productos';
    
    connection.query(sql, (err, results) => {
        if (err) {
            console.error('Error al obtener los datos de productos:', err);
            return res
                .status(500)
                .json({ error: 'Error al obtener los datos de productos' });
        }

        // Si no hay error, devuelve los resultados
        return res.json(results);
    });
});

// RUTA: Crear un nuevo producto
// Cambiado de /empleados a /productos
app.post('/productos', (req, res) => {
    // 2. CAMBIO: Recibimos los nuevos campos de Producto
    const { nombre, descripcion, precio, imagenUrl } = req.body;
    // CAMBIO: Consulta SQL adaptada a la tabla y campos de productos
    const sql = 'INSERT INTO productos (nombre, descripcion, precio, imagenUrl) VALUES (?, ?, ?, ?)';  

    connection.query(sql, [nombre, descripcion, precio, imagenUrl], (err, results) => {
        if (err) {
            console.error('Error al crear el producto:', err);
            return res
                .status(500)
                .json({ error: 'Error al crear el producto' });
        }
        // Devuelve el objeto creado con el ID insertado
        return res.json({
            message: 'Producto creado exitosamente',
            id: results.insertId,
            nombre,
            descripcion,
            precio,
            imagenUrl
        });
    });
});

// RUTA: Actualizar un producto existente por ID
// Cambiado de /empleados/:id a /productos/:id
app.put('/productos/:id', (req, res) => {
    const { id } = req.params;
    // 3. CAMBIO: Recibimos los nuevos campos de Producto
    const { nombre, descripcion, precio, imagenUrl } = req.body;
    // CAMBIO: Consulta SQL adaptada a la tabla y campos de productos
    const sql = 'UPDATE productos SET nombre = ?, descripcion = ?, precio = ?, imagenUrl = ? WHERE id = ?';   

    connection.query(sql, [nombre, descripcion, precio, imagenUrl, id], (err, results) => {
        if (err) {
            console.error('Error al actualizar el producto:', err);
            return res  
                .status(500)
                .json({ error: 'Error al actualizar el producto' });
        }
        // Verifica si se actualizó alguna fila
        if (results.affectedRows === 0) {
            return res.status(404).json({ message: 'Producto no encontrado' });
        }
        return res.json({
            message: 'Producto actualizado exitosamente'});
    });
});

// RUTA: Eliminar un producto por ID
// Cambiado de /empleados/:id a /productos/:id
app.delete('/productos/:id', (req, res) => {
    const { id } = req.params;
    const sql = 'DELETE FROM productos WHERE id = ?';   
    
    connection.query(sql, [id], (err, results) => {
        if (err) {
            console.error('Error al eliminar el producto:', err);
            return res
                .status(500)
                .json({ error: 'Error al eliminar el producto' });
        }           
        // Verifica si se eliminó alguna fila
        if (results.affectedRows === 0) {
            return res.status(404).json({ message: 'Producto no encontrado' });
        }
        return res.json({
            message: 'Producto eliminado exitosamente'});
    });
}); 

const PORT = process.env.PORT || 3001;

app.listen(PORT, () => {
    console.log(`Servidor corriendo en el puerto ${PORT}`);
});
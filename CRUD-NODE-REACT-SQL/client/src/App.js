import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [nombre, setNombre] = useState("");
  const [edad, setEdad] = useState("");
  const [pais, setPais] = useState("");
  const [cargo, setCargo] = useState("");
  const [anios, setAnios] = useState("");

  const [registros, setRegistros] = useState([]);
  const [editId, setEditId] = useState(null);

  // Cargar empleados
  useEffect(() => {
    const cargarEmpleados = async () => {
      try {
        const response = await fetch('http://localhost:3001/empleados');
        const data = await response.json();
        setRegistros(data);
      } catch (error) {
        alert('Error al cargar los empleados');
      }
    };

    cargarEmpleados();
  }, []);

  // Registrar o actualizar
  const registrarDatos = async (e) => {
    e.preventDefault();

    const empleado = { nombre, edad, pais, cargo, anios };

    if (editId !== null) {
      // Actualizar
      try {
        const response = await fetch(`http://localhost:3001/empleados/${editId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(empleado)
        });

        if (response.ok) {
          setRegistros(registros.map((reg) =>
            reg.id === editId ? { id: editId, ...empleado } : reg
          ));

          resetForm();
          alert('Empleado actualizado correctamente');
        } else {
          alert('Error al actualizar el empleado');
        }
      } catch (error) {
        alert('Error de conexión al actualizar');
      }
    } else {
      // Crear nuevo
      try {
        const response = await fetch('http://localhost:3001/empleados', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(empleado)
        });

        const data = await response.json();

        if (response.ok) {
          setRegistros([...registros, data]);
          resetForm();
          alert('Empleado guardado correctamente');
        } else {
          alert('Error al guardar el empleado');
        }
      } catch (error) {
        alert('Error de conexión');
      }
    }
  };

  // Eliminar
  const eliminarRegistro = async (id) => {
    try {
      const response = await fetch(`http://localhost:3001/empleados/${id}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        setRegistros(registros.filter(reg => reg.id !== id));

        if (editId === id) resetForm();

        alert('Empleado eliminado correctamente');
      } else {
        alert('Error al eliminar el empleado');
      }
    } catch (error) {
      alert('Error de conexión al eliminar');
    }
  };

  // Editar
  const editarRegistro = (reg) => {
    setNombre(reg.nombre);
    setEdad(reg.edad);
    setPais(reg.pais);
    setCargo(reg.cargo);
    setAnios(reg.anios);
    setEditId(reg.id);
  };

  // Reset
  const resetForm = () => {
    setNombre("");
    setEdad("");
    setPais("");
    setCargo("");
    setAnios("");
    setEditId(null);
  };

  return (
    <div className="App">
      <form className="datos" onSubmit={registrarDatos}>
        <label> Nombre:
          <input
            type="text"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            required
          />
        </label>

        <label> Edad:
          <input
            type="number"
            value={edad}
            onChange={(e) => setEdad(e.target.value)}
            required
          />
        </label>

        <label> País:
          <input
            type="text"
            value={pais}
            onChange={(e) => setPais(e.target.value)}
            required
          />
        </label>

        <label> Cargo:
          <input
            type="text"
            value={cargo}
            onChange={(e) => setCargo(e.target.value)}
            required
          />
        </label>

        <label> Años:
          <input
            type="number"
            value={anios}
            onChange={(e) => setAnios(e.target.value)}
            required
          />
        </label>

        <button type="submit">
          {editId ? 'Actualizar' : 'Registrar'}
        </button>
      </form>

      {/* Tabla */}
      {registros.length > 0 && (
        <div className="tabla-container">
          <table className="tabla-registros">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Edad</th>
                <th>País</th>
                <th>Cargo</th>
                <th>Años</th>
                <th>Acciones</th>
              </tr>
            </thead>

            <tbody>
              {registros.map((reg) => (
                <tr key={reg.id}>
                  <td>{reg.nombre}</td>
                  <td>{reg.edad}</td>
                  <td>{reg.pais}</td>
                  <td>{reg.cargo}</td>
                  <td>{reg.anios}</td>

                  <td>
                    <button className="btn-editar" onClick={() => editarRegistro(reg)}>
                      Editar
                    </button>
                    <button className="btn-eliminar" onClick={() => eliminarRegistro(reg.id)}>
                      Eliminar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>

          </table>
        </div>
      )}
    </div>
  );
}

export default App;

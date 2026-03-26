package modelo;

// Clase abstracta base para personas
public abstract class Persona {
    private String nombre;
    private String documento;

    public Persona(String nombre, String documento) {
        setNombre(nombre);
        setDocumento(documento);
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        if (nombre != null && nombre.trim().length() >= 2) {
            this.nombre = nombre.trim();
        } else {
            this.nombre = "Sin nombre";
        }
    }

    public String getDocumento() {
        return documento;
    }

    public void setDocumento(String documento) {
        if (documento != null && !documento.trim().isEmpty()) {
            this.documento = documento.trim();
        } else {
            this.documento = "Desconocido";
        }
    }

    // Método abstracto (debe implementarse en las clases hijas)
    public abstract String descripcion();
}


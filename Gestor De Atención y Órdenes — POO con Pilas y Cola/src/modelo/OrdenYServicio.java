package modelo;

import java.util.Date;

// Representa una orden de servicio creada al atender un cliente
public class OrdenYServicio {
    private int id;
    private Cliente cliente;
    private String descripcionProblema;
    private String estado;
    private Date fechaCreacion;

    public OrdenYServicio(int id, Cliente cliente, String descripcionProblema) {
        this.id = id;
        this.cliente = cliente;
        this.descripcionProblema = descripcionProblema;
        this.estado = "ABIERTA";
        this.fechaCreacion = new Date();
    }

    public int getId() {
        return id;
    }

    public Cliente getCliente() {
        return cliente;
    }

    public String getDescripcionProblema() {
        return descripcionProblema;
    }

    public String getEstado() {
        return estado;
    }

    public Date getFechaCreacion() {
        return fechaCreacion;
    }

    @Override
    public String toString() {
        return "Orden #" + id + " | " + cliente.getNombre() +
               " | " + descripcionProblema + " | " + estado;
    }
}

import smtplib
from email.message import EmailMessage

def enviar_aviso_registro(usuario_nuevo, rol_solicitado):
    # QUIÉN ENVÍA: Usaremos este como el "correo del sistema"
    remitente = "stevan.moreno300@gmail.com" 
    
    # QUIÉN RECIBE: El correo donde quieres que te llegue la alerta (tu otro correo)
    destinatario = "stevanmoreno445@gmail.com" 
    
    # LA LLAVE: Aquí debes pegar las 16 letras amarillas que generes en Google
    # (No es tu contraseña normal de inicio de sesión)
    password = "pvclgsxbcwktfszo" 

    msg = EmailMessage()
    msg.set_content(f"Hola,\n\nEl usuario '{usuario_nuevo}' se ha registrado solicitando el rol de '{rol_solicitado}'.\n\nPor favor, ingresa al panel de administración para activarlo.")
    msg['Subject'] = "🔔 Nueva solicitud de acceso - Sistema de Análisis"
    msg['From'] = remitente
    msg['To'] = destinatario

    try:
        # Configuración para Gmail
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(remitente, password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False
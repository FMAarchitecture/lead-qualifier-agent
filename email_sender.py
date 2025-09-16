import smtplib
from email.message import EmailMessage

def send_email(subject: str, body: str, to_email: str):
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    from_email = "laura.bueno@fernandamarques.com.br"
    from_password = "Fma@2025@@"

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    # Texto simples (fallback)
    msg.set_content(body)

    # HTML com estilo leve e quebra de parágrafos
    html_body = body.replace("Here is the summary:", "").strip().replace("\n\n", "</p><p>").replace("\n", "<br>")

    msg.add_alternative(f"""
    <html>
    <body style="font-family: Arial, sans-serif; font-size: 14px;">
        <h3 style="color: #333;">Resumo do lead qualificado</h3>
        <p>{html_body}</p>
    </body>
    </html>
    """, subtype='html')


    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.send_message(msg)
        print("✅ E-mail enviado com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")

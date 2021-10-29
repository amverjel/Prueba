from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, validators


class Formulario_Login(Form):    
    usuario = StringField('Usuario', 
    [
        validators.DataRequired(message='Campo requerido.'),
        validators.Length(min=8, max=25)
    ])
    password = PasswordField('Contraseña', 
    [
        validators.DataRequired(message='Campo requerido.'),
        validators.Length(min=8, max=25)
    ])
    recordar = BooleanField('Recordar contraseña')
    enviar = SubmitField('Iniciar sesión')

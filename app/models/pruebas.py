from app.models import usuario as usuario_model

# Test the function
result = usuario_model.mostrar_usuarios()
for row in result:
    print(row)
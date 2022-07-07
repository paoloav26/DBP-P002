# DBP "Sistema de calificación por categorías" 💾

## Integrantes 🙋‍♂️
- Paolo Armas Vega [paoloav26]
- Juan Sara Junco [juansara]
- Dimael Rivas Chavez [artrivas]
- Matias Avendaño Vargas  [Matias222]

## Descripcion 
Un foro con la capacidad de brindarle al usuario la posibilidad de criticar y puntuar una película, serie, novela, anime, etc y que a su vez estos comentarios puedan ser visualizados por los demás participantes.

## Objetivos principales
-Implementar el foro mencionado anteriormente, con operaciones CRUD.

## Misión
- Conectar mediante el intercambio de reseñas a distintas personas, para asi lograr una mayor intertextualidad en los comentarios. 

## Visión
- Llegar a ser uno de los principales foros en materia de análisis cinematográfico.

## Librerías y Frameworks
### Front-end:
    -Bootstrap
### Back-end:
    -Flask
    -SqlAlchemy
    -Hashlib
    -Sys
### Base de datos:
    -PostgreSQL

## Script principal
- app.py
    -   Host:127.0.0.1:5000   
## Información acerca de los APIs. Requests y Responses  
### login:
Renderiza el template login.html
### login_validator: 
Recibe el diccionario de datos json y valida que la contraseña ingresada sea la correcta, caso contrario muestra un error del tipo 500.
### register_validator: 
Recibe el diccionario de datos json e inserta la data en la bd, corroborando que la contraseña tenga más de 8 caracteres y por lo menos un número, en caso la clave no cumpla con los requirimentos se imprimira un desplegable de advertencia, además si las llaves primarias ya estan ocupadas, muestra un error del tipo 500.
### search_items: 
Recibe el diccionario de datos json, y dado el nombre de la película y categoría, muestra el contenido requerido.
### comentar: 
Recibe el diccionario de datos json e inserta el comentario si es exitoso el status cambia a 200. En caso ya tenga un comentario, se mostrara una advertencia, ya que solo se 
puede tener una reseña y el status sera 409, consecuentemente el usuario tendra la posibilidad de actualizar o eliminar su comentario. Por último si el formulario tiene partes vacias el status sera 400.
### eliminar_comentario:
Elimina el comentario publicado por el usuario logeado.
### actualizar_comentario:
Actualiza el comentario publicado por el usuario logeado, si no hay problemas el status sera de 200, caso contrario 500.

# DBP "Sistema de calificación por categorías" 💾

## Integrantes 🙋‍♂️
- Paolo Armas Vega [paoloav26]
- Juan Sara Junco [juansara]
- Dimael Rivas Chavez [artrivas]
- Matias Avendaño Vargas  [Matias222]

## Descripción 
Un foro con la capacidad de brindarle al usuario la posibilidad de criticar y puntuar una película, serie, novela, anime, etc y que a su vez estos comentarios puedan ser visualizados por los demás participantes.

## Objetivos principales
-Implementar el foro mencionado anteriormente, con operaciones CRUD.
<br />
-Crear una Restful API que permita acceder a toda la información subyacente.

## Misión
- Conectar mediante el intercambio de reseñas a distintas personas, para asi lograr una mayor intertextualidad en los comentarios. 

## Visión
- Llegar a ser uno de los principales foros en materia de análisis cinematográfico.

## Librerías y Frameworks
### Front-end:
    -Vue
    -Bootstrap
### Back-end:
    -Flask
    -SqlAlchemy
    -Hashlib
    -Sys
### Base de datos:
    -PostgreSQL
    -FireBase

## Script principal
- API: __init__.py
    <br />
    -  Host:127.0.0.1:5000   
    <br />
-Frontend: ...
    <br />
    -   Host:127.0.0.1:5000
## Información acerca de los EndPoints.  
### /usuarios (Get)
Retorna un diccionario de datos JSON, con tres características success, usuarios y total_usuarios, si la cantidad de usuarios es 0 retornar un error 404, caso contrario, los valores del diccionario seran los siguientes; True, usuarios (todos los usuarios ordenados por username con su respectiva paginación), len(usuarios); respectivamente.
### /usuarios (Post)
Recibe el diccionario JSON con los datos para la inserción, si alguno de los campos esta vacio retorna un error 422, si el correo o usuario ya existen en la bd retorna un error 500, en caso no suceda nada de lo anterior se encripta la contraseña y se procede al insert, retornando un JSON con las siguientes características success, created, usuarios, total_usuarios; los valores del diccionario seran los siguientes; True, new_usuario (el usuario insertado), usuarios(todos los usuarios ordenados por username con su respectiva paginación), len(usuarios); respectivamente.
### /usuarios/_<username> (Patch)
Si el username no existe retorna un error 404, caso contrario actualiza el correo, contraseña y username del usuario, retornando un diccionario JSON con las siguientes características success, usuario; los valores del diccionario seran los siguientes; True, username; respectivamente. 
### /usuarios/_<username> (Delte)
Si el username no existe retorna un error 404, caso contrario elimina el usuario, retornando un diccionario JSON con las siguientes características success, deleted, usuario, total_usuarios; los valores del diccionario seran los siguientes; True, username, usuarios (todos los usuarios ordenados por username con su respectiva paginación), len(usuarios); respectivamente. 


## Información respecto al testing por Modelo
### Usuarios: 10 Tests
### Items: 2 Tests
### Categoria: 2 tests
### Calificaciones: 16 tests
Cabe destacar que la cantidad de tests no es homogénea debido a que por ejemplo Items y Categorías son modelos que no presentan operaciones de update, inserción o delete, es debido a eso su baja cantidad de pruebas.

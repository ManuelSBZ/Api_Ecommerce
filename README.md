# Api_Ecommerce

El presente repositorio anexa un una base de datos expuesta con una interface api que implementa los metodos GET, POST, PATCH, DELETE.

- Tecnologias principales:
   1. Python 3.7-alpine.
   2. Flask, Flask-Restjsonapi y Flask-Sqlalchemy.
   3. Postgresql 10-alpine.
   4. Gunicorn 20.0.4 .
   4. Docker 19.03.12 .
 
- Patrones de diseño Flask:
  1. Factory.
  2. Blueprint.

- Para explorar la solucion se debe:
    1. Clonar el repositorio.
    2. Abrir simbolo del sistema.
    3. Ubicarse desde la consola en la carpeta que contiene el docker-compose.yaml dentro del proyecto.
    4. Ejecutar " docker-compose up --build ".
    
- Para probar la api se recomienda hacer uso de postman, cliente en el cual se tiene una coleccion de 93 endpoints para las distintas operaciones CRUD. Para acceder a la coleccion
  usar el siguiente url Postman https://www.getpostman.com/collections/2e8302ec380ebc590347 .
 

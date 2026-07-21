# Sistema Mercado (Python)

Sistema de gestión para una tienda/mercado, con backend en **Python (Flask)** y frontend en **HTML/CSS/JS + Bootstrap**. Usa una arquitectura híbrida con **MySQL** como base transaccional y **MongoDB** como base de datos de destino para migración, comentarios y calificaciones de productos.

## Arquitectura

```
Fask.py           # API Flask: expone endpoints y contiene lógica de migración MySQL → MongoDB
cone.py           # Capa de acceso a datos: funciones de consulta/inserción sobre MySQL
conexion1.py       # Script independiente de migración masiva MySQL → MongoDB
index.html         # Página principal (landing) del frontend
pages/             # Vistas HTML del sistema, una por funcionalidad
```

- **Backend transaccional (MySQL):** clientes, productos, sucursales, compras, devoluciones — vía `mysql.connector` y funciones en `cone.py`.
- **Backend documental (MongoDB Atlas):** comentarios y calificaciones de productos, además de una copia migrada de las tablas de MySQL.
- **Frontend:** páginas HTML estáticas con Bootstrap 5, que consumen la API Flask vía `axios`, y usan la API de Google Maps para geolocalización de clientes/sucursales.

## Funcionalidades

- Gestión de **clientes**, **productos**, **sucursales**, **compras** y **devoluciones** (CRUD básico sobre MySQL).
- Cálculo de **sucursales más cercanas** a cada cliente usando la fórmula de Haversine directamente en SQL.
- **Comentarios y calificaciones** de productos, almacenados en MongoDB.
- **Migración de datos** de MySQL a MongoDB, incluyendo relaciones entre tablas (compras → cliente/producto/sucursal, devoluciones → compra/sucursal).
- Mapa interactivo de clientes y sucursales (Google Maps API) en `pages/clientes.html` y `pages/sucursales.html`.

## Páginas del frontend

| Página | Función |
|---|---|
| `index.html` | Landing / página principal |
| `pages/productos.html` | Listado de productos |
| `pages/newproducto.html` | Registro de nuevo producto |
| `pages/clientes.html` | Gestión de clientes + mapa |
| `pages/sucursales.html` | Gestión de sucursales + mapa |
| `pages/sucursales_cercanas.html` | Sucursales más cercanas por cliente |
| `pages/compra.html` | Registro de compras |
| `pages/devoluciones.html` | Registro de devoluciones |
| `pages/calificaciones.html` | Calificación de productos |
| `pages/administracion.html` | Panel de administración |

## Tecnologías

- **Backend:** Python, Flask, Flask-CORS
- **Bases de datos:** MySQL (`mysql-connector-python`), MongoDB (`pymongo`, MongoDB Atlas)
- **Frontend:** HTML5, Bootstrap 5, JavaScript (axios), Google Maps JavaScript API

## Requisitos

```bash
pip install flask flask-cors pymongo mysql-connector-python
```

> El repo no incluye `requirements.txt`; puedes generarlo con `pip freeze > requirements.txt` una vez tengas el entorno funcionando.

## Configuración

Las credenciales de MySQL y MongoDB están **hardcodeadas** en `Fask.py`, `cone.py` y `conexion1.py`:

```python
mysql_config = {
    "host": "localhost",
    "user": "root",
    "password": "...",
    "database": "entrega"
}
mongo_uri = "mongodb+srv://usuario:password@entregafinal.ucptk.mongodb.net/"
```

Necesitas:
1. Una base de datos MySQL llamada `entrega` con las tablas `Clientes`, `Productos`, `Sucursales`, `Compras`, `Devoluciones`.
2. Un clúster de MongoDB Atlas (o local) accesible con la URI configurada.
3. Una API key de Google Maps válida (usada en `pages/clientes.html` y `pages/sucursales.html`).

## Ejecución

```bash
python Fask.py
```

El servidor Flask corre en modo debug por defecto (`app.run(debug=True)`), en `http://localhost:5000`. Luego abre `index.html` (o sírvelo con un servidor estático) para navegar el frontend.

Para migrar datos de MySQL a MongoDB de forma independiente (sin pasar por la API):

```bash
python conexion1.py
```

## Endpoints principales (Flask)

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/obtener_clientes` | Listar clientes |
| GET | `/obtener_productos` | Listar productos (resumen) |
| GET | `/obtener_todos_productos` | Listar productos (detalle completo) |
| GET | `/obtener_sucursales` | Listar sucursales |
| GET | `/obtener_compras` | Listar compras |
| POST | `/insertar_cliente` | Registrar cliente |
| POST | `/insertar_producto` | Registrar producto |
| POST | `/insertar_sucursal` | Registrar sucursal |
| POST | `/insertar_compra` | Registrar compra |
| POST | `/insertar_devolucion` | Registrar devolución |
| GET | `/get_locations` | Ubicaciones de clientes y sucursales (para el mapa) |
| GET | `/sucursales_cercanas` | Sucursales más cercanas por cliente (Haversine) |
| POST | `/migrar` | Migrar datos de MySQL a MongoDB |
| POST | `/comentarios` | Insertar comentario sobre un producto |
| GET | `/comentarios` | Listar todos los comentarios |
| GET | `/comentarios/<productoId>` | Comentarios de un producto específico |
| POST | `/productos` | Registrar calificación de un producto |

## Estado del proyecto

Proyecto académico. Pendiente de mejoras habituales: manejo centralizado de errores, validación de entradas, separación de configuración/credenciales del código, y (opcionalmente) mover la lógica de conexión a un único módulo en vez de duplicarla entre `cone.py`, `conexion1.py` y `Fask.py`.

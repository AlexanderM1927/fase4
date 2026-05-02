# TEST

````
fase4/
├── main.py                        ← App principal (tk.Tk, navegación de frames)
├── utils.py                       ← Logger → logs/app.log
├── demo.py                        ← 14 operaciones de simulación
├── models/
│   ├── entidad.py                 ← Clase abstracta base (ABC)
│   ├── cliente.py                 ← Cliente con encapsulación y propiedades validadas
│   ├── servicio.py                ← Clase abstracta Servicio + SalaReuniones, AlquilerEquipo, Asesoria
│   └── reserva.py                 ← Reserva con ciclo de vida + manejo de excepciones
├── services/
│   ├── gestor_clientes.py
│   ├── gestor_servicios.py
│   └── gestor_reservas.py
├── exceptions/
|
|
|
└── frames/
    ├── LoginFrame.py
    ├── MainFrame.py               ← Notebook con 4 pestañas + botón Demostración
    ├── ClientesFrame.py
    ├── ServiciosFrame.py
    ├── ReservasFrame.py
    └── LogsFrame.py               ← Visor en tiempo real de logs/app.log
````
# Software FJ

## Architecture
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
└── frames/
    ├── LoginFrame.py
    ├── MainFrame.py               ← Notebook con 4 pestañas + botón Demostración
    ├── ClientesFrame.py
    ├── ServiciosFrame.py
    ├── ReservasFrame.py
    └── LogsFrame.py               ← Visor en tiempo real de logs/app.log
````

# Principios OOP implementados:

Abstracción: Entidad (ABC) con obtener_informacion() / validar() abstractos; Servicio abstracto con calcular_costo(), describir(), validar_parametros()
Herencia: SalaReuniones, AlquilerEquipo, Asesoria heredan de Servicio; Cliente y los servicios heredan de Entidad
Polimorfismo: cada servicio sobreescribe calcular_costo(), describir() y validar_parametros() con lógica propia
Encapsulación: Cliente usa propiedades con setters validados (_cedula, _email, etc.)
Sobrecarga simulada: calcular_costo(horas) / calcular_costo(horas, con_iva=True) / calcular_costo(horas, descuento=0.15) / calcular_costo(horas, con_iva=True, descuento=0.10)

# Manejo de excepciones:

try/except — captura de errores de validación en todas las operaciones UI
try/except/else — confirmar() usa else para el bloque exitoso
try/except/finally — cancelar() garantiza registro del intento, operación 12 restaura disponibilidad
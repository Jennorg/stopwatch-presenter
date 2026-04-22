# Stopwatch Presenter

Stopwatch Presenter es una aplicación de cronometraje diseñada para moderadores y presentadores. Desarrollada con Python y PyQt6, ofrece una interfaz de doble ventana para gestionar presentaciones.

## Características Principales

- Sistema de Doble Ventana: Panel de control independiente para el moderador y una vista de presentador limpia y de alto contraste.
- Diseño de Interfaz Moderno: Tema oscuro optimizado para entornos de poca luz y reducción de la fatiga visual.
- Configuración Rápida: Botones de tiempo preestablecidos para una configuración rápida de la sesión.
- Umbrales Visuales: Cambios dinámicos de color (Blanco, Amarillo, Rojo) basados en límites de tiempo de advertencia y críticos personalizables.
- Notificaciones de Audio: Alertas sonoras integradas compatibles con modo offline para eventos de advertencia y finalización de tiempo.
- Enfoque en la Presentación: Optimizado para configuraciones de múltiples monitores con soporte de proyección a pantalla completa.

## Requisitos

- Python 3.10 o superior
- PyQt6
- PyQt6-QtMultimedia

## Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/stopwatch-presenter.git
   cd stopwatch-presenter
   ```

2. Crear y activar un entorno virtual:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Ejecute la aplicación usando:
```bash
python main.py
```

1. Configure el tiempo total y los umbrales de advertencia.
2. Seleccione el monitor de destino para la proyección.
3. Haga clic en "Proyectar e Iniciar" para comenzar la cuenta regresiva.

## Licencia

Este proyecto está bajo la Licencia MIT - vea el archivo LICENSE para más detalles.

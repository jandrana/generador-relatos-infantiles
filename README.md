# Generador de relatos infantiles

Pequeña herramienta CLI que usa la API de Google GenAI para generar relatos infantiles, opcionalmente crear una ilustración y exportar el resultado en PDF. Proyecto creado como solución para ZIEN Ideas en 42Málaga.

## Requisitos
- Python 3.8+
- Acceso a Internet
- Clave de la API de Google GenAI

Paquetes Python (recomendado instalar desde requirements.txt):
- fpdf
- Pillow
- python-dotenv
- google-genai
- pydantic


## Instalación
1. Clona o descarga el repositorio.

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Configuración de la API key
Crea un fichero `.env` en la raíz del proyecto (no subirlo a repositorios públicos). Puedes usar el archivo `.env.template` como guía.

Ejemplo `.env`:
```text
API_KEY=tu_api_key_aqui
```

Asegúrate de que la variable se llama `API_KEY`. El script carga variables con python-dotenv.

## Uso
Ejecuta el script desde la terminal:
```bash
python generator.py
```
Introduce por teclado la petición para el relato cuando se te pregunte (por ejemplo: "blond girl who moves to malaga").

Salidas previstas:
- PDF con el relato en `output/` (nombre generado a partir del título).
- `generation_traces.txt` — trazas de intentos si se usan reintentos.
- `generated_image.png` — si la generación de imagen está activada y funciona.

## Archivos clave
- `generator.py` — script principal.
- `requirements.txt` — dependencias.
- `.env.template` — plantilla para la configuración de la API (si existe).
- `README.md` — documentación.
- `output/` — carpeta destino para PDFs generados.

## Flujo de Trabajo
1. El usuario ejecuta `generator.py` y proporciona una petición para el relato.
2. El script usa Google GenAI para generar el relato basado en la petición.
3. Opcionalmente, genera una imagen ilustrativa.
4. El relato (y la imagen si se genera) se exportan a un PDF en 
`output/`.

## Fases del desarrollo
- [x] Configuración del entorno y dependencias.
- [x] Implementación de generación de relatos con Google GenAI.
- [x] Estructuración del output de la API con Pydantic para validar y generar el relato.
- [x] Manejo de errores y reintentos.
- [x] Generación de trazas al fallar.
- [x] Exportación a PDF.
- [ ] Implementación de generación de imágenes (opcional) (da un error en la API por exceso de uso del modelo)

## Licencia
Proyecto para uso personal/educativo. Ajustar licencia según necesidad.
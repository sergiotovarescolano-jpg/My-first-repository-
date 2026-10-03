# Macro prompt: Jarvis, mi asistente personal

> Copia todo lo que hay debajo de la línea en Claude Code (o en la herramienta con la que vayas a programar).
> Antes, rellena lo que va entre `[CORCHETES]`.

---

Quiero que construyas **Jarvis**, mi asistente personal. Tiene que poder hablar conmigo **fuera del chat**: por Telegram (texto y notas de voz) y por **llamada de teléfono**. Su función principal es decirme cada día qué tenemos que hacer, recordarme pendientes y ayudarme a organizar mi trabajo.

## Quién soy y cómo trabajo
- Nombre: [TU NOMBRE]
- A qué me dedico: [ej. agencia de marketing digital para negocios locales: anuncios en Meta, contenido en vídeo, webs]
- Clientes principales: [LISTA BREVE]
- Zona horaria: Europe/Madrid
- Idioma: español, trato cercano, respuestas cortas y directas.
- Horario: [ej. de lunes a viernes, 9:00–19:00]
- Reglas: nunca gastar dinero, publicar ni enviar nada a terceros sin mi confirmación explícita.

Guarda todo esto en `perfil.md`. Jarvis debe leerlo siempre y puede proponerme cambios cuando aprenda algo nuevo de mí, pero no los guarda hasta que yo diga que sí.

## Funciones (por orden de prioridad)

### 1. Canal de conversación: bot de Telegram
- Le escribo o le mando una nota de voz, y él me contesta en texto (y en voz si se lo pido).
- Las notas de voz se transcriben con Whisper (OpenAI API o `faster-whisper` en local).
- Solo responde a mi `chat_id`; ignora a cualquier otra persona.

### 2. Gestión de tareas
- Tareas con: descripción, cliente, prioridad (alta/media/baja), fecha límite y estado.
- Que entienda lenguaje natural: "recuérdame llamar a Pepe el jueves a las 11" crea la tarea y el recordatorio.
- Comandos rápidos: `/hoy`, `/semana`, `/pendientes`, `/hecho <id>`.
- Guárdalo en SQLite con IDs autoincrementales (no uses `len(lista) + 1`).
- Puedes partir de mi `task_manager (1).py` de este repo.

### 3. Briefing diario (lo más importante)
- Cada día laborable a las [08:30] me manda por Telegram:
  1. Mi agenda de hoy (Google Calendar).
  2. Las tareas que vencen hoy y las atrasadas.
  3. Las 3 prioridades que me recomienda, con una frase de por qué.
  4. Opcional: un resumen de ayer de mis campañas de Meta Ads (gasto, resultados y cualquier anomalía).
- Por la tarde, a las [18:30], un cierre: qué se hizo, qué queda y qué pasa a mañana.

### 4. Llamadas de teléfono
- Jarvis me puede **llamar** a mi número [+34 XXX XXX XXX] con Twilio Voice:
  - Por la mañana, si lo activo, me lee el briefing en voz alta.
  - Para recordatorios urgentes (tareas de prioridad alta a punto de vencer).
- Durante la llamada puedo contestarle con la voz ("vale, pásala a mañana", "márcala como hecha") y él actúa.
- Voz en español natural (ElevenLabs o las voces neuronales de Twilio/Amazon Polly).
- Yo también puedo llamar al número de Twilio y hablar con él.
- Límite de seguridad: como mucho [3] llamadas al día y nunca fuera de mi horario, salvo que lo marque como urgente.

### 5. Memoria
- Guarda un historial de conversaciones y un resumen semanal de lo aprendido (clientes, decisiones, preferencias).
- Cuando le pregunte "¿qué hablamos sobre el cliente X?", que lo busque en su memoria.

## Stack técnico
- **Lenguaje:** Python 3.12.
- **Cerebro:** API de Anthropic con `claude-sonnet-5-5` y *tool use* (las herramientas son: tareas, calendario, memoria, Meta Ads en solo lectura y llamar).
- **Bot:** `python-telegram-bot`.
- **Llamadas:** Twilio Voice + servidor FastAPI para los *webhooks*.
- **Programación de avisos:** APScheduler.
- **Calendario:** Google Calendar API (OAuth).
- **Base de datos:** SQLite.
- **Secretos:** en `.env` (nunca en el código ni en git); incluye un `.env.example`.
- **Despliegue:** algo barato que esté encendido 24/7 (Railway, Fly.io o un VPS pequeño), con instrucciones paso a paso.

## Cómo quiero que lo construyas
1. Hazlo por fases y no pases a la siguiente sin que la anterior funcione:
   - **Fase 1:** bot de Telegram + tareas + `perfil.md`.
   - **Fase 2:** briefing diario + Google Calendar.
   - **Fase 3:** llamadas con Twilio.
   - **Fase 4:** memoria + Meta Ads.
2. Al final de cada fase, explícame en lenguaje sencillo cómo probarlo y qué claves o cuentas necesito crear (Telegram BotFather, Twilio, Google Cloud, Anthropic), con los pasos exactos.
3. Escribe tests para la lógica de tareas y del briefing.
4. Código sencillo y comentado: no soy programador experto.
5. Dime una estimación del coste mensual (APIs + Twilio + servidor).

Empieza por la Fase 1.

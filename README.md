# AI Music Creator Platform

A Django-based AI music generation platform that uses the **Strategy design pattern** to support multiple interchangeable song-generation backends.

---

## Project Structure

```
project_root/
├── app/
│   ├── controllers/          # Request handlers (views)
│   │   └── generation_controller.py
│   ├── models/               # Domain models (one file per entity)
│   │   ├── user.py
│   │   ├── library.py
│   │   ├── song.py           # Song + GenerationStatus enum
│   │   ├── prompt.py         # Prompt + Mood/Occasion/SingerTone enums
│   │   ├── draft.py
│   │   ├── generation.py     # GenerationJob
│   │   ├── share.py          # ShareLink
│   │   ├── playback.py       # PlaybackSession
│   │   └── equalizer.py      # EqualizerPreset
│   ├── routes/               # URL routing
│   │   └── generation_urls.py
│   ├── services/             # Business logic
│   │   └── generation_service.py
│   ├── strategies/           # Strategy Pattern
│   │   ├── base.py           # Abstract interface (SongGeneratorStrategy)
│   │   ├── factory.py        # Centralized strategy selection
│   │   ├── mock_strategy.py  # Offline mock implementation
│   │   ├── suno_strategy.py  # Suno API implementation
│   │   └── exceptions.py     # Custom generation exceptions
│   └── migrations/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── .env                      # Secret config — NOT committed
├── .env.example              # Template showing required variables
├── .gitignore
└── manage.py
```

---

## Setup

### 1. Install dependencies

```bash
pip install django requests python-dotenv
```

### 2. Configure environment

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Edit `.env` and set your values (see sections below for mock vs suno).

### 3. Apply migrations

```bash
python manage.py migrate
```

### 4. Start the server

```bash
python manage.py runserver
```

---

## Running in Mock Mode (offline, no API key needed)

In your `.env` file set:

```
GENERATOR_STRATEGY=mock
```

The mock strategy returns deterministic, pre-defined output immediately — no network access required. This is the default.

**Test it:**

```bash
curl -X POST http://127.0.0.1:8000/api/generation/generate/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Happy Birthday Song",
    "description": "A joyful song for my friend'\''s birthday",
    "occasion": "BIRTHDAY",
    "mood": "HAPPY",
    "singer_tone": "FEMALE",
    "requested_duration": "3:00",
    "user_email": "demo@example.com"
  }'
```

Expected response:

```json
{
  "success": true,
  "task_id": "mock-5052fcbc",
  "song_id": 1,
  "status": "SUCCESS",
  "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
  "message": "Song generation started"
}
```

---

## Running in Suno Mode (live API)

### Where to put the Suno API key

**Never commit your API key.** Add it only to your local `.env` file:

```
GENERATOR_STRATEGY=suno
SUNO_API_KEY=your-actual-key-from-sunoapi-org
```

The `.env` file is listed in `.gitignore` and will never be committed.

**Start generation:**

```bash
curl -X POST http://127.0.0.1:8000/api/generation/generate/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Graduation Anthem",
    "description": "An energetic song celebrating graduation day",
    "occasion": "GRADUATION",
    "mood": "ENERGETIC",
    "singer_tone": "NEUTRAL",
    "requested_duration": "3:30",
    "user_email": "demo@example.com"
  }'
```

The response will contain a `task_id`. Use it to poll for the result:

```bash
curl http://127.0.0.1:8000/api/generation/status/<task_id>/
```

Suno status values: `QUEUED` → `GENERATING` → `SUCCESS` / `FAILED`

---

## Strategy Pattern Design

The generation behavior is fully swappable via the `GENERATOR_STRATEGY` environment variable. The selection is **centralized in one place**: `app/strategies/factory.py`.

```
GenerationRequest
      │
      ▼
SongGeneratorStrategy  (abstract base — app/strategies/base.py)
      │
      ├── MockSongGeneratorStrategy   (app/strategies/mock_strategy.py)
      │       • No external calls
      │       • Deterministic output
      │       • Always returns SUCCESS
      │
      └── SunoSongGeneratorStrategy   (app/strategies/suno_strategy.py)
              • POST /api/v1/generate → returns taskId
              • GET  /api/v1/generate/record-info → polls status

factory.get_generator()  ← reads GENERATOR_STRATEGY setting
```

There are no `if strategy == ...` checks scattered in the codebase — only in `factory.py`.

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| `POST` | `/api/generation/generate/` | Submit a song generation request |
| `GET`  | `/api/generation/status/<task_id>/` | Poll generation status |

### POST `/api/generation/generate/` — Request body

| Field | Type | Required | Values |
|-------|------|----------|--------|
| `title` | string | yes | Song title |
| `description` | string | no | Prompt description |
| `occasion` | string | yes | `BIRTHDAY`, `WEDDING`, `ANNIVERSARY`, `GRADUATION`, `CELEBRATION`, `CUSTOM` |
| `mood` | string | yes | `HAPPY`, `SAD`, `ENERGETIC`, `CALM`, `ROMANTIC`, `INSPIRATIONAL` |
| `singer_tone` | string | yes | `MALE`, `FEMALE`, `NEUTRAL`, `CHILD` |
| `requested_duration` | string | no | e.g. `"3:00"` |
| `user_email` | string | no | Identifies the user (default: `demo@example.com`) |

---

## Domain Model

Entities implemented as Django models:

- **User** — email, display_name, google_id
- **Library** — one-to-one with User; contains Songs
- **Song** — title, audio_file_url, duration, status (GenerationStatus), is_favorite, play_count
- **Prompt** — title, description, occasion, mood, singer_tone, requested_duration
- **Draft** — saved Prompt state; composition of Prompt + Library
- **GenerationJob** — links Song ↔ Prompt, stores task_id and status
- **ShareLink** — unique_token, expires_at, access_count
- **PlaybackSession** — one-to-one with User; current_position, is_playing, volume, looping
- **EqualizerPreset** — bass_level, mid_level, treble_level per User

Enumerations: `GenerationStatus`, `Mood`, `Occasion`, `SingerTone`

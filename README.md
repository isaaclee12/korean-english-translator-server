# Korean-English Translator Server

This is the backend server for the Korean-English Translator application, built with Django and Django REST Framework.

## Setup Instructions

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/korean-english-translator.git
cd korean-english-translator/korean-english-translator-server
```

2. **Create and Activate Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Requirements**
```bash
pip install -r requirements.txt
```

4. **Set Up Environment Variables**
- Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

- Edit `.env` with your configuration:
```
DJANGO_SECRET_KEY=your_secret_key_here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1]
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure and never share them
- Use a different secret key for production environments

5. **Run the Server**
```bash
python manage.py runserver
```

The server will be available at `http://localhost:8000`

## API Documentation

### 1. Translation Endpoint

**Endpoint:** `POST /api/v0/translate/`

**Purpose:** Translate text between English and Korean with additional context and pronunciation

**Request Parameters: (JSON body)**
- `text` (string, required): The text to translate
- `from` (string, required): Source language ("en" or "ko")
- `to` (string, required): Target language ("en" or "ko")

**Response:**
```json
{
    "translation": "Translated text with pronunciation and context"
}
```

**Example Request: (English to Korean)**
```json
{
    "text": "Hello, how are you?",
    "from": "en",
    "to": "ko"
}
```

**Example Response: (English to Korean)**
```json
{
    "translation": "안녕하세요, 어떻게 지내세요? (annyeonghaseyo, eotteohge jinaeseyo?)"
}
```

### 2. Korean Phrase Analysis Endpoint

**Endpoint:** `POST /api/v0/phrase-lookup/`

**Purpose:** Analyze Korean phrases with pronunciation, origin, cultural context, and formality levels

**Request Parameters: (JSON body)**
- `phrase` (string, required): The Korean phrase to analyze

**Response:**
```json
{
    "phrase": "string",
    "pronunciation": "string",
    "origin": "string",
    "example": "string",
    "context": "string",
    "formality": {
        "level": "string",
        "alternatives": ["string"]
    }
}
```

**Example Request: (Korean phrase analysis)**
```json
{
    "phrase": "할아버지께서 어제 비가 오셨다가 그만두시더라고 하셨어요."
}
```

**Example Response: (Korean phrase analysis)**
```json
{
    "phrase": "할아버지께서 어제 비가 오셨다가 그만두시더라고 하셨어요.",
    "pronunciation": "(haraebujikseoh eojeo biga osyeotdaga geumandusyedero hasyeosseoyo)",
    "origin": "mixed (native Korean and Sino-Korean)",
    "example": "Corrected: 할아버지께서 어제 비가 오다가 그쳤다고 하셨어요.",
    "context": "This sentence contains a common grammatical error where honorifics (-시-) are incorrectly applied to non-human subjects (비/rain). In Korean culture, honorifics are only used for people, not natural phenomena.",
    "formality": {
        "level": "high",
        "alternatives": [
            "할아버지가 어제 비가 오다가 그쳤다고 했어.",
            "할아버지께서 어제 비가 오다가 멈췄다고 말씀하셨어요.",
            "할아버지께서 어제 비가 왔다가 그쳤다고 하셨습니다."
        ]
    }
}

# Rasa Chatbot - Pascasarjana ITS

Indonesian language chatbot for ITS (Institut Teknologi Sepuluh Nopember) postgraduate program information.

## Features

- **Indonesian Language Support**: Native Indonesian language processing
- **Intent Recognition**: Handles 32+ intents related to postgraduate admissions
- **Custom Actions**: Dynamic responses for complex queries
- **Fixed Port Configuration**: Consistent port setup for easy deployment

## Quick Start

### Prerequisites

- Python 3.11+
- Virtual environment activated

### Installation

```bash
pip install rasa
```

### Training

```bash
rasa train
```

### Running the Chatbot

#### Option 1: Use Helper Scripts

```powershell
# Start Inspector (port 5006)
.\rinspect.ps1

# Start Action Server (port 5055)
.\start_rasa.ps1
```

#### Option 2: Manual Commands

```bash
# Start Inspector
rasa inspect --port 5006

# Start Action Server
rasa run actions --port 5055

# Interactive Shell
rasa shell
```

## Configuration

### Fixed Ports

- **Rasa Inspector**: Port 5006
- **Action Server**: Port 5055
- **Core Server**: Port 5005

### Pipeline

- WhitespaceTokenizer
- RegexFeaturizer
- KeywordIntentClassifier
- FallbackClassifier (threshold: 0.7)

## Project Structure

```
demo_chatbot/
├── actions/                 # Custom actions
│   ├── __init__.py
│   ├── action.py           # Main action implementations
│   └── db.py              # Database utilities
├── data/                   # Training data
│   ├── nlu.yml            # Intent examples
│   ├── rules.yml          # Conversation rules
│   └── stories.yml        # Conversation stories
├── models/                # Trained models
├── config.yml             # Rasa configuration
├── domain.yml             # Domain definition
├── endpoints.yml          # Endpoint configuration
└── credentials.yml        # Channel credentials
```

## Intents Supported

- Admission requirements (`tanya_syarat_pendaftaran`)
- Available programs (`tanya_prodi_tersedia`)
- Tuition fees (`tanya_biaya_kuliah`)
- Application procedures (`tanya_cara_pendaftaran`)
- And many more...

## Development

### Training New Models

```bash
rasa train
```

### Testing

```bash
rasa test
```

### Interactive Learning

```bash
rasa interactive
```

## Deployment

The chatbot is configured with fixed ports for consistent deployment:

- Use the provided helper scripts for easy startup
- All configurations are documented in `config.yml`

## License

MIT License

# VAPI Voice Configuration Guide

## ElevenLabs Voice Options

Here are popular ElevenLabs voice IDs you can use in your VAPI integration:

### Female Voices
- **Rachel** (Professional, clear): `21m00Tcm4TlvDq8ikWAM`
- **Domi** (Strong, confident): `AZnzlk1XvdvUeBnXmlld`
- **Bella** (Friendly, warm): `EXAVITQu4vr4xnSDxMaL`
- **Elli** (Emotional, expressive): `MF3mGyEYCl7XYWbV9V6O`
- **Grace** (Professional, mature): `oWAxZDx7w5VEj9dCyTzz`

### Male Voices
- **Adam** (Deep, professional): `pNInz6obpgDQGcFmaJgB`
- **Antoni** (Mature, reliable): `ErXwobaYiN019PkySvjV`
- **Arnold** (Strong, authoritative): `VR6AewLTigWG4xSOukaG`
- **Josh** (Young, friendly): `TxGEqnHWrfWFTfGW9XjX`
- **Sam** (Casual, conversational): `yoZ06aMxZJJ28mfd3POQ`

## How to Change Voice

### Method 1: Edit the vapi_integration.py file directly

1. Open `src/vapi_integration.py`
2. Find line ~76: `"voiceId": "21m00Tcm4TlvDq8ikWAM"`
3. Replace with your preferred voice ID

### Method 2: Add voice configuration to environment variables

Add to your `.env` file:
```
VAPI_VOICE_ID=pNInz6obpgDQGcFmaJgB
VAPI_VOICE_PROVIDER=11labs
VAPI_VOICE_STABILITY=0.5
VAPI_VOICE_SIMILARITY_BOOST=0.8
```

### Method 3: Use different voice providers

VAPI supports multiple voice providers:

#### OpenAI Voices
```json
{
    "provider": "openai",
    "voice": "alloy"  // Options: alloy, echo, fable, onyx, nova, shimmer
}
```

#### Azure Voices
```json
{
    "provider": "azure",
    "voice": "en-US-JennyNeural"
}
```

#### PlayHT Voices
```json
{
    "provider": "playht",
    "voice": "jennifer"
}
```

## Voice Settings Explained

- **stability** (0.0-1.0): Lower = more expressive, Higher = more stable
- **similarityBoost** (0.0-1.0): Lower = more creative, Higher = more similar to original
- **provider**: Voice service provider (11labs, openai, azure, playht)
- **voiceId**: Unique identifier for the specific voice

# 🎤 Voice Assistant Management & Multilingual Support Guide

## 1. 🔄 Process for Changing Voice Assistant

### Option A: Quick Voice Change (Recommended) ⚡
**Use this for changing voice while keeping the same assistant and language**

```bash
python scripts/voice_manager.py
```

Choose option **A** to update your current assistant's voice instantly.

**Steps:**
1. Run the voice manager script
2. Select "A. Change voice (update current assistant)"
3. Choose your preferred voice (1-10)
4. The change is applied immediately

**Pros:**
- ✅ Instant change (no phone number update needed)
- ✅ Keeps all conversation history and settings
- ✅ No downtime

**Cons:**
- ❌ Language change requires new assistant

### Option B: Create New Assistant ⚙️
**Use this for language changes or when you want to keep multiple assistants**

```bash
python scripts/voice_manager.py
```

Choose option **B** to create a new assistant with different voice/language.

**Steps:**
1. Run the voice manager script
2. Select "B. Create new assistant with different voice/language"
3. Choose your preferred voice/language (1-10)
4. Choose whether to update your phone number to use the new assistant

**Pros:**
- ✅ Supports different languages
- ✅ Can keep old assistant as backup
- ✅ Fresh start with new assistant

**Cons:**
- ❌ Requires phone number update
- ❌ Loses previous conversation history

### Manual Process (Alternative)

If you prefer to do it manually:

1. **Update .env file** (for new assistants only):
```env
VAPI_VOICE_PROVIDER=11labs
VAPI_VOICE_ID=your_voice_id_here
VAPI_VOICE_STABILITY=0.5
VAPI_VOICE_SIMILARITY_BOOST=0.8
```

2. **Create/Update Assistant**:
```bash
python -c "import sys; sys.path.append('src'); from vapi_integration import VAPIIntegration; # ... create assistant"
```

3. **Update Phone Number** (if using new assistant):
```bash
python scripts/update_phone_assistant.py
```

## 2. 🌍 Multilingual Support (Spanish & Chinese)

### Available Languages & Voices

#### English 🇺🇸
- **Rachel**: Professional, clear female voice
- **Adam**: Deep, professional male voice  
- **Bella**: Friendly, warm female voice
- **Antoni**: Mature, reliable male voice
- **Domi**: Strong, confident female voice
- **OpenAI Alloy/Nova**: Neutral AI voices

#### Spanish 🇪🇸
- **Lupe**: Female Spanish voice
- **Mateo**: Male Spanish voice

#### Chinese 🇨🇳
- **Xiaoxiao**: Female Chinese voice (Azure)

### Setting Up Multilingual Assistant

#### Method 1: Using Voice Manager (Recommended)
```bash
python scripts/voice_manager.py
```

1. Choose option **B** (Create new assistant)
2. Select a non-English voice (8=Spanish Female, 9=Spanish Male, 10=Chinese Female)
3. The system will automatically:
   - Create prompts in the target language
   - Set up proper transcription for the language
   - Configure the appropriate voice

#### Method 2: Manual Configuration

**For Spanish Assistant:**
```python
# Spanish system prompt is automatically generated
# First message: "¡Hola! Soy tu asistente de TechSolutions Pro (Español). ¿Cómo puedo ayudarte hoy?"

# Voice configuration:
{
    "provider": "11labs",
    "voiceId": "KaHKR3ooHlYrg9OLhLFE",  # Lupe (Female)
    "stability": 0.5,
    "similarityBoost": 0.8
}

# Transcriber configuration:
{
    "model": "nova-2",
    "language": "es",
    "provider": "deepgram"
}
```

**For Chinese Assistant:**
```python
# Chinese system prompt is automatically generated
# First message: "您好！我是您的TechSolutions Pro (中文)助理。今天我可以为您做些什么？"

# Voice configuration:
{
    "provider": "azure", 
    "voice": "zh-CN-XiaoxiaoNeural"
}

# Transcriber configuration:
{
    "model": "nova-2",
    "language": "zh", 
    "provider": "deepgram"
}
```

### Language-Specific Features

#### Automatic Language Detection
- The assistant automatically responds in the language it was configured for
- Business information is presented in the appropriate language
- Professional tone maintained across all languages

#### Business Context Translation
The system automatically translates your business guidelines into the target language:

**English Guidelines:**
```
"Always base your answers on the business information provided"
"Be professional, friendly, and helpful"
```

**Spanish Guidelines:**
```
"Siempre basa tus respuestas en la información empresarial proporcionada"
"Sé profesional, amigable y útil"
```

**Chinese Guidelines:**
```
"始终根据提供的商务信息回答"
"保持专业、友好和有帮助的态度"
```

### Testing Your Multilingual Assistant

1. **Create Spanish Assistant:**
```bash
python scripts/voice_manager.py
# Choose B -> Choose 8 or 9 for Spanish
```

2. **Test by calling your number and speaking in Spanish:**
- "¿Cuáles son sus horarios de atención?"
- "¿Qué servicios ofrecen?"
- "¿Cuánto cuesta el desarrollo web?"

3. **Create Chinese Assistant:**
```bash
python scripts/voice_manager.py 
# Choose B -> Choose 10 for Chinese
```

4. **Test by calling and speaking in Chinese:**
- "你们的营业时间是什么时候？"
- "你们提供什么服务？"
- "网站开发需要多少钱？"

## 3. 📋 Quick Reference Commands

### Change Voice Only (Same Language)
```bash
python scripts/voice_manager.py
# Choose A -> Select voice number
```

### Change Voice + Language  
```bash
python scripts/voice_manager.py
# Choose B -> Select voice number -> Update phone number
```

### View Voice Configuration
```bash
python scripts/voice_manager.py
# Choose C -> Select voice number
```

### Check Current Setup
```bash
python -c "import sys; sys.path.append('src'); from vapi_integration import VAPIIntegration; vapi = VAPIIntegration(); print('Phone Numbers:', vapi.get_phone_numbers())"
```

## 4. 🚀 Advanced Configurations

### Custom Voice Settings

**For More Expressive Voice:**
```env
VAPI_VOICE_STABILITY=0.3  # Lower = more expressive
VAPI_VOICE_SIMILARITY_BOOST=0.9  # Higher = closer to original
```

**For More Stable Voice:**
```env
VAPI_VOICE_STABILITY=0.8  # Higher = more stable
VAPI_VOICE_SIMILARITY_BOOST=0.7  # Lower = more creative
```

### Adding New Languages

To add support for other languages:

1. **Find appropriate voice ID** for your language
2. **Add to VOICE_OPTIONS** in `scripts/voice_manager.py`
3. **Create system prompt** in target language
4. **Configure transcriber** with correct language code

### Switching Between Languages

You can have multiple assistants for different languages:

```bash
# English Assistant ID: 8ff1ebe8-9fdf-4e43-b87a-614523d4f63b
# Spanish Assistant ID: [created when needed]  
# Chinese Assistant ID: [created when needed]
```

Switch between them using the phone update script:
```bash
python scripts/update_phone_assistant.py
```

## 5. 🎯 Best Practices

### Voice Selection
- **Customer Service**: Use Rachel (Professional) or Adam (Deep)
- **Friendly Business**: Use Bella (Friendly) or Antoni (Mature)
- **Authoritative**: Use Domi (Strong) or Adam (Deep)

### Language Deployment
- **Single Language**: Use Option A for quick voice changes
- **Multiple Languages**: Create separate assistants for each language
- **Testing**: Always test with native speakers before deployment

### Performance Optimization
- Spanish and Chinese voices may have slight latency due to transcription
- ElevenLabs voices generally provide better quality than OpenAI
- Azure voices work well for Chinese but require proper configuration

Now you have a complete system for managing voices and supporting multiple languages! 🎉

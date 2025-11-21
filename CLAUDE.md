# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**bergsonAndFriends** - Philosophical chatbots for French high school (Terminale) students. Three philosophers (Spinoza, Bergson, Kant) powered by fine-tuned LLMs with dialectical reasoning.

## Architecture

### Primary Stack (3_PHI_HF/)
- **Model**: Qwen 2.5 14B + LoRA adapter (`FJDaz/qwen-spinoza-niveau-b`)
- **Backend**: FastAPI + Gradio on HuggingFace Spaces (GPU L4)
- **Inference**: 8-bit quantization via bitsandbytes

### Backup Stack (Spinoza_Secours_HF/)
- **Model**: Mistral 7B + LoRA (`FJDaz/mistral-7b-philosophes-lora`)
- **Fallback**: Colab + ngrok for CPU/low-resource scenarios

### Key Components
- **Prompt System**: Philosopher-specific system prompts with logical schemes (Modus Ponens, Identity, Contraposition)
- **Context Detection**: Classifies user input as `accord`/`confusion`/`resistance`/`neutre`
- **RAG**: Corpus files in `data/RAG/` (glossaries + dialogical texts per philosopher)

## Important Directories

- `3_PHI_HF/` - Main HF Space (Qwen 14B, 3 philosophers)
- `Spinoza_Secours_HF/` - Backup HF Space (Mistral 7B, Spinoza only)
- `data/RAG/` - RAG corpus (glossaries, dialogical texts)
- `docs/` - Documentation and notes
- `garbage/` - Archived/obsolete code

## API Endpoints (3_PHI)

```bash
GET /health
GET /init/{philosopher}  # spinoza, bergson, kant
POST /chat  # {"message": "...", "history": [], "philosopher": "spinoza"}
```

## Key Patterns

### Context-Adaptive Responses
The system detects user emotional state and adapts prompts:
- `accord` → Validate then advance logically with "Donc"
- `confusion` → Give ONE concrete analogy
- `resistance` → Reveal contradiction with "MAIS ALORS"
- `neutre` → Ask a question to provoke reflection

### Philosopher Differentiation
Same base model, different system prompts:
- **Spinoza**: Causal necessity, affects, conatus, Dieu=Nature
- **Bergson**: Duration vs spatial time, intuition, melody metaphors
- **Kant**: Phenomenon/noumenon, a priori/a posteriori, transcendental critique

## Critical Constraints

- **DO NOT modify `3_PHI_HF/`** unless explicitly asked - this is the production Qwen space
- HF Spaces CPU has 16GB RAM limit - Mistral 7B FP32 won't fit
- Always use 4-bit/8-bit quantization for HF deployments
- LoRA adapters are on HuggingFace Hub, not local

## Common Commands

```bash
# Test local API
curl -X POST http://localhost:7860/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "test", "history": [], "philosopher": "spinoza"}'

# Push to HF Space
git -C 3_PHI_HF push origin main
```

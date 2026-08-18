# Local Model Benchmarks

## Hardware

- CPU: Intel Core i3-6006U
- Cores: 2
- Threads: 4
- Clock: 2.0 GHz
- RAM: 8 GB
- GPU: Intel HD Graphics
- OS: Windows 10 Home

## LLM Baseline

### Qwen2.5 0.5B

- Ollama model: `qwen2.5:0.5b`
- Model size: ~397 MB
- Quantization: Q4_K_M
- Context length: 32768
- Initial startup: fast
- Approximate first generation observed: ~20 seconds
- System free RAM after generation: ~2.27 GB

### Qualitative results

The model produced coherent answers for simple questions.

For context-grounded questions, it was able to summarize supplied information accurately.

However, testing with normalization concepts showed that the model can introduce unsupported information and make incorrect inferences. Therefore, strict grounding and answer-validation mechanisms remain important.

## Embedding Baseline

### Nomic Embed Text

- Ollama model: `nomic-embed-text:latest`
- Model size: ~274 MB
- Parameters: ~137M
- Vector dimensions: 768
- Context length: 2048
- Quantization: F16

### Embedding benchmark

| Test | Latency |
|---|---:|
| First embedding | 3.0594 s |
| Second embedding | 2.2778 s |
| Third embedding | 2.2243 s |

The first request was slower due to model loading/warm-up.

## Initial Decision

Use:

- `nomic-embed-text` for embeddings
- `qwen2.5:0.5b` as the initial local generation baseline

The generation model may be reevaluated after the complete RAG pipeline is working.
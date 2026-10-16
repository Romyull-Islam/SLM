# Characterizing and Understanding the Performance of Small Language Models on Edge Devices

Code, measurement scripts, raw resource-usage data and figures for the IEEE IPCCC 2024 paper
*"Characterizing and Understanding the Performance of Small Language Models on Edge Devices"*
by M. R. Islam, N. Dhar, B. Deng, T. N. Nguyen, S. He and K. Suo.

This research analyzes Small Language Models (SLMs) on edge devices (Raspberry Pi, NVIDIA Jetson Orin and Mac mini). It evaluates the inference performance and resource consumption of SLMs and shows how the hardware affects memory usage, CPU load, disk activity and inference performance. The goal is to help users pick suitable models and tune AI workloads for edge environments.

## Models

The models were downloaded from Hugging Face. The repository contains data for the following models:

| Model | Source | Data in this repo |
|---|---|---|
| TinyLlama-1.1B-Chat | https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0 | Raspberry Pi, Jetson, Mac mini |
| Phi-2 | https://huggingface.co/microsoft/phi-2 | Raspberry Pi, Jetson, Mac mini |
| Phi-3-mini-4k-instruct | https://huggingface.co/microsoft/Phi-3-mini-4k-instruct | Raspberry Pi, Jetson, Mac mini |
| Llama-3-8B-Instruct | https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct | Raspberry Pi, Jetson, Mac mini |
| OpenELM-270M (MLX) | `mlx-community/OpenELM-270M` | Mac mini only |

`Llama_2_param.ipynb` also loads Llama-2-7B, Llama-2-13B and Phi-2 with Hugging Face `transformers` to inspect their layer and parameter breakdown.

## Repository layout

```
.
├── Llama_2_param.ipynb            # per-layer parameter breakdown of Llama-2-7B/13B and Phi-2
├── Benchmark/
│   ├── wiki.test.raw              # WikiText-2 test set used for perplexity
│   └── wikimodified.test.raw      # downsampled version of the same test set
├── Scripts/
│   ├── script.txt                 # llama.cpp, nmon, iostat, nmonchart and pyNmonAnalyzer commands
│   ├── Mlx script.txt             # OpenELM-270M generation with mlx_lm (Mac)
│   └── resource.py                # psutil-based resource logger for macOS
└── Data Visualization/
    ├── Raspberry_CSV/             # Raspberry Pi: nmon captures (.nmon), CSV exports, nmonchart HTML
    ├── CSV/                       # Jetson: CSV exports (read as the Jetson series in the notebooks)
    ├── Macmini/                   # Mac mini: CSVs from resource.py, iostat output (disk_busy_rate.txt)
    ├── Llama3/, Phi-3/            # raw nmon captures for Llama-3 and Phi-3 on Raspberry Pi
    ├── phi2-rpi/, tinyllama/      # per-device plots and nmon/HTML for Phi-2 and TinyLlama
    ├── Perplexity test with benchmark/  # screenshots/photos of perplexity runs (F16 and 4-bit)
    ├── Figures/                   # paper figures: TTFT, tokens/s, perplexity, total generation time
    ├── Pdfs/, resource utilization figures/  # CPU, memory, swap, disk-busy, process-switch plots
    ├── analyse.ipynb, analyse with phi-3.ipynb, ELM.ipynb, visualizing LM data.ipynb
    └── resource.py
```

Folders with a `_wiki` suffix hold runs on the WikiText-2 benchmark.

## Tools

- [llama.cpp](https://github.com/ggerganov/llama.cpp): GGUF conversion, quantization (F16 and 4-bit), generation (`main`) and perplexity (`perplexity`)
- MLX (`mlx_lm`): OpenELM on the Mac mini
- nmon, pyNmonAnalyzer and nmonchart: resource collection, CSV conversion and HTML charts on Linux devices
- `resource.py` (psutil, subprocess) and `iostat`: resource collection on macOS
- pandas / matplotlib notebooks: plotting

## Reproducing the experiments (high level)

1. **Get the models** from Hugging Face (see the table above).
2. **Convert and quantize** them to GGUF with llama.cpp (the repo has F16 and 4-bit results). See the llama.cpp README for the build and conversion steps.
3. **Run inference** with llama.cpp. Example commands from `Scripts/script.txt`:
   ```bash
   ./main -m ../Phi-2/phi-2.Q4_K_M.gguf -p "Building a website can be done in 10 simple steps:\nStep 1:" -n 400 -e
   ./perplexity -m ../pHI-3/Phi-3-mini-4k-instruct-fp16.gguf -f ../wiki.test.raw
   ```
   On the Mac mini, OpenELM runs through `mlx_lm` (`Scripts/Mlx script.txt`).
4. **Collect resource usage** while the model runs:
   - Raspberry Pi / Jetson: `nmon -f -s 2 -c 6560`, then `pyNmonAnalyzer -c -o <out> -i <file>.nmon` for CSVs and `bash nmonchart <file>.nmon <out>.html` for charts.
   - Mac mini: `python Scripts/resource.py` (writes `cpu_usage.csv`, `memory_usage.csv`, `swap_usage.csv`, ...) and `iostat -d 1 > disk_busy_rate.txt`.
5. **Plot** with the notebooks in `Data Visualization/`. They were run on Google Colab and read from `/content/drive/MyDrive/...`, so change the paths to your local checkout first.

`Llama_2_param.ipynb` needs a Hugging Face access token for the gated Llama-2 models. Set it as an environment variable before starting Jupyter:

```bash
export HF_TOKEN=<your Hugging Face token>
```

## Selected results

![TTFT](https://github.com/Romyull-Islam/SLM/assets/23154358/0f99a02f-c5c2-40ee-9e34-3d9482600689)
![total generation time](https://github.com/Romyull-Islam/SLM/assets/23154358/ac084920-8535-4f27-8088-4aaa2a205455)
![perplexity token f16](https://github.com/Romyull-Islam/SLM/assets/23154358/84f1fecf-8708-4afa-b125-6699a76bd2c3)
![CPU_UTIL](https://github.com/Romyull-Islam/SLM/assets/23154358/9e4f9276-dedb-4573-bc35-e0f02411cbb4)

The PDF versions of these and the other figures are in `Data Visualization/Figures/`.

## Citation

If you use this work, please cite:

```bibtex
@inproceedings{islam2024slm,
  title     = {Characterizing and Understanding the Performance of Small Language Models on Edge Devices},
  author    = {Islam, M. R. and Dhar, N. and Deng, B. and Nguyen, T. N. and He, S. and Suo, K.},
  booktitle = {Proceedings of the IEEE International Performance, Computing, and Communications Conference (IPCCC)},
  year      = {2024}
}
```

## Related projects

Part of my work on efficient LLM systems ([all projects](https://github.com/Romyull-Islam)):

- [μKV (EndurKV)](https://github.com/Romyull-Islam/EndurKV): KV-cache eviction with in-place compaction for LLM inference on a phone
- [SemSched](https://github.com/Romyull-Islam/SemSched): memory capacity vs. prefetch bandwidth for LLM inference on hybrid CXL devices
- [AQLoRA](https://github.com/Romyull-Islam/AQLoRA): zero-search precision allocation for fast quantized LoRA fine-tuning
- [VLM-Benchmarking](https://github.com/Romyull-Islam/VLM-Benchmarking): accuracy, time and energy of small vision-language models on Jetson AGX Orin
- [Build, Train, Deploy](https://github.com/Romyull-Islam/llm_booklet): an open five-week LLM course in PyTorch

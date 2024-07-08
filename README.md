***Characterizing and Understanding the Performance of Small Language Models on Edge Devices***

This research comprehensively analyzes Small Language Models (SLMs) on various edge devices, such as Raspberry Pi, Nvidia Jetson Orin, and Mac mini. It evaluates the performance and resource consumption of state-of-the-art SLMs, including TinyLlama, Phi-3, and OpenELM. The study highlights the impact of different hardware on model efficiency, revealing significant variations in memory usage, CPU load, disk activity, and inference performance. The findings aim to guide users in selecting suitable models and optimizing AI workloads for edge environments, marking the first in-depth exploration of SLMs' efficiency on edge platforms.

Model selection: 
<br>
We have downloaded the models from the Hugginface repository.

Tinyllama: https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0
<br>
Phi-3: https://huggingface.co/microsoft/Phi-3-mini-4k-instruct
<br>
Llama-3: https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct


Quantization:
<br>
To convert them to gguf format and quantize them, we used llama.cpp. All the installation and user guides are available on the GitHub repository of llama.cpp: https://github.com/ggerganov/llama.cpp


Data collection:
<br>
To collect the background resource data, we used Nmon, and to convert them to CSV, we used PyNmonAnalyzer. With the help of Nmonchart, we could view them on the HTLM page. To collect data from Mac devices, we used the resources.py file, which consists of multiple libraries like psutil, subprocess, etc. For extracting disk data, we used iostat.



Benchmark:<br>
We have used the wikitext2 dataset to evaluate the models. Also used a downsampled version of this dataset. 

Data Visualization and Result: <br>
Our experiment results are plotted as figures below so that they become easily representable.

![TTFT](https://github.com/Romyull-Islam/SLM/assets/23154358/0f99a02f-c5c2-40ee-9e34-3d9482600689)
<br>
![total generation time](https://github.com/Romyull-Islam/SLM/assets/23154358/ac084920-8535-4f27-8088-4aaa2a205455)
<br>
![perplexity token f16](https://github.com/Romyull-Islam/SLM/assets/23154358/84f1fecf-8708-4afa-b125-6699a76bd2c3)
<br>
![CPU_UTIL](https://github.com/Romyull-Islam/SLM/assets/23154358/9e4f9276-dedb-4573-bc35-e0f02411cbb4)


# 👋HiBench: Benchmarking LLMs Capability on Hierarchical Structure Reasoning
<div align="center">
Zhuohang Jiang†, Pangjing Wu†, Ziran Liang†, Xu Yuan†, Qi Chen†,
Ye Jia†, Jiancheng Tu†，Chen Li，Peter H.F. Ng，Qing Li*

</div>  
<div align="center"><span style="font-size: smaller;">
<br>†: joint first author & equal contribution
*: corresponding author</br>
</span>
</div>

<br>
<div align="center">

[![Powered by](https://img.shields.io/badge/Powered_by-Pytorch-EE4C2C?logo=pytorch)](https://pytorch.org/) 
[![Powered by](https://img.shields.io/badge/Powered_by-Huggingface-FFD21E?logo=huggingface)](https://huggingface.co/) 
[![Powered by](https://img.shields.io/badge/Powered_by-Fireworks-6B46C1)](https://fireworks.ai/) 
[![Powered by](https://img.shields.io/badge/Powered_by-Azure-3FA9F5)](https://azure.microsoft.com) 
![GitHub](https://img.shields.io/github/license/scu-zjz/IMDLBenCo?logo=license)

[![LLM](https://img.shields.io/badge/Model-Llama-3FA9F5?logo=ollama)](https://www.llama.com/) 
[![LLM](https://img.shields.io/badge/Model-Qwen-FF6A00?logo=alibabadotcom)](https://github.com/QwenLM/Qwen) 
[![LLM](https://img.shields.io/badge/Model-ChatGLM-3FA9F5?logo=)](https://github.com/THUDM/ChatGLM-6B) 
[![LLM](https://img.shields.io/badge/Model-Openai-412991?logo=openai)](https://openai.com/) 


[![LLM](https://img.shields.io/badge/Model-Phi-0854C1?logo=)](https://huggingface.co/microsoft/Phi-3.5-mini-instruct) 
[![LLM](https://img.shields.io/badge/Model-InternLM-002B56?logo=)](https://huggingface.co/internlm) 
[![LLM](https://img.shields.io/badge/Model-Yi-006600?logo=)](https://huggingface.co/01-ai) 
[![LLM](https://img.shields.io/badge/Model-Baichuan-FF9E0F?logo=)](https://github.com/baichuan-inc/Baichuan2/) 
[![LLM](https://img.shields.io/badge/Model-Mistral-FECC00?logo=)](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3) 
[![LLM](https://img.shields.io/badge/Model-Deepseek-783BF9?logo=)](https://chat.deepseek.com/) 

</div>

## News
- **[2025-04-06]** We are excited to announce that the HiBench dataset is now available on 🤗 [Hugging Face](https://huggingface.co/datasets/zhuohang/HiBench)! 🎉 Explore and use it to benchmark your models' hierarchical reasoning capabilities. 🚀
- **[2025-03-02]** We are thrilled to announce that our paper *HiBench: Benchmarking LLMs Capability on Hierarchical Structure Reasoning* is now available on [arXiv](https://arxiv.org/abs/2503.00912)! 📄 Dive into the details of our benchmark and findings. 🌟


## Overview
**Welcome to 👋HiBench, the First Comprehensive Hierarchical Structure Understanding Benchmark of LLMs.**
- To our best knowledge, it is the **first benchmark** specifically designed to evaluate the hierarchical reasoning abilities of LLMs, encompassing tasks of varying scales and complexities for comprehensive evaluation.
- We evaluate **20 LLMs** and reveal that even the most advanced LLMs struggle with performance, offering new insights into hierarchical reasoning.
- We propose a synthetic hierarchical dataset for task-specific fine-tuning, which enhanced LLM's ability on hierarchical reasoning, surpassing **GPT4** by **6.53\%** throughout all tasks.
- Cite and star if you feel helpful. This will encourage us a lot 🥰.

<div align="center">
    <img src="Images/codebase.jpg" alt="Hibench Outline" />
    <p style="font-size: 1.2em;"><strong>Figure 1: </strong>Overview of the paradigm for HiBench.</p>
</div>

## Task Definition
HiBench includes a range of tasks from basic to advanced levels, specifically comprising 7 fundamental hierarchical understanding tasks at the Fundamental level, 5 JSON structure understanding tasks, and 3 formula structure understanding tasks at the Intermedia level; 2 code structure understanding tasks and 3 scientific paper understanding tasks at the Advanced level, totaling **20** tasks covering **15,852** problems.
<img src="Images/task.jpg" alt="Task" width="100%" />
<div align="center" style="width: 100%;" >
    <p style="font-size: 1.2em;"><strong>Figure 2: </strong>Task definition in Hibench. Hibench contains 3 levels of evaluation, 5 types of tasks, and 20 subtasks.</p>
</div>
<div align="center">
    <img src="Images/radar.jpg" alt="Radar chat" width="54%" />
</div>
    
<div style = "display: flex">

<div align="center" style="width: 100%; ">
    <p style="font-size: 1.2em;"><strong>Figure 3: </strong>Performance comparison of the best models from different families on multiple hierarchical tasks.</p>
</div>
</div>


## Features under developing
This repository has completed evaluating Qwen Family, Llama Family, GPT Family and ChatGLM model.

However, more LLMs are currently being evaluated for improved our experiment.Moreover, we will increase more Benchmark Dataset to evaluating LLMs ability of Hierarchical understanding. Updates will be rolled out frequently. 

- [x] Tested on HiBench for Phi[![LLM](https://img.shields.io/badge/Model-Phi-0854C1?logo=)](https://huggingface.co/microsoft/Phi-3.5-mini-instruct) , InternLM
[![LLM](https://img.shields.io/badge/Model-InternLM-002B56?logo=)](https://huggingface.co/internlm) , Yi 
[![LLM](https://img.shields.io/badge/Model-Yi-006600?logo=)](https://huggingface.co/01-ai) 
,baichuan
[![LLM](https://img.shields.io/badge/Model-Baichuan-FF9E0F?logo=)](https://github.com/baichuan-inc/Baichuan2/), and Mistral[![LLM](https://img.shields.io/badge/Model-Mistral-FECC00?logo=)](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3).

- [x] Check all datasets and add binary datasets

## Quick Start
### Install HiBench
```
conda create -n HiBench python=3.11
conda activate HiBench
pip install -r requirements.txt
```
### Evaluation HiBench
```
python ./launch.py
```

## Result
<div align="center">
    <img src="Images/mainresult.jpg" alt="Performance of different LLMs in HiBench" />
    <p style="font-size: 1.2em;"><strong>Figure 4: </strong>Performance of different LLMs in HiBench.</p>
</div>


<br>


## About
☑️About the Developers:
- All developers of Hibench are PhD/MPhil students of The Hong Kong Polytechnic University 🇭🇰.  
- Hibench's codebase designer is [_Zhuohang Jiang_](https://github.com/jzzzzh).
- The Fundamental Tasks of Hibench are mainly undertaken by [_Pangjing Wu_](https://github.com/Pangjing-Wu) and _Ziran Liang_.
- The Code Programming Task and JSON Task are mainly undertaken by _Qi Chen_ and _Ye Jia_.
- The Paper Task is mainly undertaken by _Xu Yuan_.
- The Formula Task is mainly undertaken by _Jiancheng Tu_.

<!-- ## Acknowledge
We sincerely appreciate [Prof. Hongxia Yang](https://scholar.google.com/citations?user=iJlC5mMAAAAJ&hl=en) for her constructive directions and suggestions. -->

## Citation
If you find our work valuable and it has contributed to your research or projects, we kindly request that you cite our paper. Your recognition is a driving force for our continuous improvement and innovation🤗.
```
@misc{jiang2025hibenchbenchmarkingllmscapability,
      title={HiBench: Benchmarking LLMs Capability on Hierarchical Structure Reasoning}, 
      author={Zhuohang Jiang and Pangjing Wu and Ziran Liang and Peter Q. Chen and Xu Yuan and Ye Jia and Jiancheng Tu and Chen Li and Peter H. F. Ng and Qing Li},
      year={2025},
      eprint={2503.00912},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2503.00912}, 
}
```

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=jzzzzh/HiBench&type=Date)](https://star-history.com/#jzzzzh/HiBench&Date)
<div align="center">
<a href="https://info.flagcounter.com/HxyP"><img src="https://s01.flagcounter.com/count2/HxyP/bg_FFFFFF/txt_000000/border_CCCCCC/columns_2/maxflags_10/viewers_0/labels_0/pageviews_0/flags_0/percent_0/" alt="Flag Counter" border="0"></a></div>

# 问题分隔数据集

## 数据集介绍
- 数据集：`alpha_questions_split_900.json` + `alpaca_questions_split_identity.json`
- 规模：900 + 90
- 作用：用于将问题拆分为多个子问题，并且将拆分后子问题中的代词（它，它们等等）转为对应的实体，以便保持子问题语义的完整
- 使用模型：qwen-plus
- 花费tokens：大约10w tokens
- 是否包含人工处理：✅


## 微调记录
- 微调框架：[LLaMA-Factory-0.6.3](https://github.com/hiyouga/LLaMA-Factory/releases/tag/v0.6.3)
- 微调模型：[Qwen1.5-0.5B-Chat](https://www.modelscope.cn/models/qwen/Qwen1.5-0.5B-Chat/summary)

### 微调步骤：
- 将数据集`alpha_questions_split_900.json`和`alpaca_questions_split_identity.json`拷贝到`D:\LLaMA-Factory-0.6.3\data`中，并在`dataset_info.json`中添加以下内容：
    ```json
    "alpaca_questions_split_900": {
        "file_name": "alpaca_questions_split_900.json",
        "file_sha1": "c21a4ea8649e24ee65f42f7cf3dc849c45901ad2"
    },
    "alpaca_questions_split_identity": {
        "file_name": "alpaca_questions_split_identity.json",
        "file_sha1": "170c9aa4c2c02699f07265bc99ed4c99e58e425b"
    }
    ```
- 微调参数：将以下微调参数添加到`D:\LLaMA-Factory-0.6.3\config\train_alpaca_questions_split_900.json`中，启动webui后加载该json脚本参数
    ```json
    {
      "top.model_name": "Qwen1.5-0.5B-Chat",
      "top.finetuning_type": "lora",
      "top.adapter_path": [],
      "top.quantization_bit": "none",
      "top.template": "qwen",
      "top.rope_scaling": "none",
      "top.booster": "none",
      "train.training_stage": "Supervised Fine-Tuning",
      "train.dataset_dir": "data",
      "train.dataset": [
        "alpaca_questions_split_900",
        "alpaca_questions_split_identity"
      ],
      "train.learning_rate": "2e-4",
      "train.num_train_epochs": "2.0",
      "train.max_grad_norm": "1.0",
      "train.max_samples": "1000",
      "train.compute_type": "fp16",
      "train.cutoff_len": 1024,
      "train.batch_size": 4,
      "train.gradient_accumulation_steps": 4,
      "train.val_size": 0,
      "train.lr_scheduler_type": "cosine",
      "train.logging_steps": 5,
      "train.save_steps": 100,
      "train.warmup_steps": 0,
      "train.neftune_alpha": 0,
      "train.optim": "adamw_torch",
      "train.resize_vocab": false,
      "train.packing": false,
      "train.upcast_layernorm": false,
      "train.use_llama_pro": false,
      "train.shift_attn": false,
      "train.report_to": false,
      "train.num_layer_trainable": 3,
      "train.name_module_trainable": "all",
      "train.lora_rank": 8,
      "train.lora_alpha": 16,
      "train.lora_dropout": 0.1,
      "train.loraplus_lr_ratio": 0,
      "train.create_new_adapter": false,
      "train.use_rslora": false,
      "train.use_dora": true,
      "train.lora_target": "all",
      "train.additional_target": "",
      "train.dpo_beta": 0.1,
      "train.dpo_ftx": 0,
      "train.orpo_beta": 0.1,
      "train.reward_model": [],
      "train.use_galore": false,
      "train.galore_rank": 16,
      "train.galore_update_interval": 200,
      "train.galore_scale": 0.25,
      "train.galore_target": "all"
    }
    ```


## 问题记录
1. 打招呼语，会进行回复
- Q: 哈喽
- A: 哈喽！有什么我可以帮助你的吗？
- Q: 你是ai
- A: 是的，我是AI助手。有什么我可以帮助你的吗？
- Q: 你是我的助手
- A: 我是您的助手，有什么我可以帮助您的吗？
- Q: Thanks
- A: You're welcome! How can I assist you today?

解决方法：新增自我认知数据集，将数据集中的答案改为问题，见alpaca_questions_split_identity.json


## 微调效果
![效果展示01](https://github.com/xiaojinlii/xiao-qa-generator/blob/main/images/questions_split/display01.png?raw=true)
![效果展示02](https://github.com/xiaojinlii/xiao-qa-generator/blob/main/images/questions_split/display02.png?raw=true)
![效果展示03](https://github.com/xiaojinlii/xiao-qa-generator/blob/main/images/questions_split/display03.png?raw=true)
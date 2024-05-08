# 问题分隔数据集

## 数据集介绍
- 原始数据集：`alpaca_questions_split_1k.json`
- 规模：1011
- 作用：用于将问题拆分为多个子问题，并且将拆分后子问题中的代词（它，它们等等）转为对应的实体，以便保持子问题语义的完整
- 使用模型：qwen-plus
- 花费tokens：大约10w tokens
- 是否包含人工处理：✅


## 微调记录
- 微调框架：[LLaMA-Factory-0.6.3](https://github.com/hiyouga/LLaMA-Factory/releases/tag/v0.6.3)
- 微调模型：[Qwen1.5-0.5B-Chat](https://www.modelscope.cn/models/qwen/Qwen1.5-0.5B-Chat/summary)

### 微调步骤：
- 将数据集`alpaca_questions_split_1k.json`拷贝到`D:\LLaMA-Factory-0.6.3\data`目录下，并在`dataset_info.json`中添加以下内容：
    ```json
   "alpaca_questions_split": {
      "file_name": "alpaca_questions_split_1k.json",
      "file_sha1": "0e0c9c59a95cf86ab7c151204c340db08ddb2ac6"
   }
    ```
- 微调参数：将以下微调参数添加到`D:\LLaMA-Factory-0.6.3\config\config_alpaca_questions_split.json`中，启动webui后加载该json脚本参数
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
       "alpaca_questions_split"
     ],
     "train.learning_rate": "2e-4",
     "train.num_train_epochs": "4.0",
     "train.max_grad_norm": "1.0",
     "train.max_samples": "1024",
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
1. 问题拆分，代词替换为实体
2. 子问题之间特殊符号无法分隔
   - Q: 李白是谁乔峰是谁
   - Q: 李白是谁，乔峰是谁
   解决方法：在子问题之间添加特殊符号
3. 礼貌用语、自我介绍，分割异常
   - Q: 你好，请介绍一下你自己
   - A: 你好，我是<|sep|>你好，我叫什么名字？
   - Q: 你好，我叫小明，请问你叫什么名字，你多大了
   - A: 你好，我叫小明，多大了？
   - Q: 谢谢
   - A: 谢谢你的邀请，有什么我可以帮助你的吗？
   - Q: 感谢
   - A: 感谢什么？
   - Q: 感谢您的帮助
   - A: 感谢您的帮助，有什么我可以帮您的吗？
   解决方法：新增identity.json数据集，见`xiao-qa-generator\temp\questions_split\children_datas\identity.json`


## 微调效果
![效果展示01](https://github.com/xiaojinlii/xiao-qa-generator/blob/main/images/questions_split/display01.png?raw=true)
![效果展示02](https://github.com/xiaojinlii/xiao-qa-generator/blob/main/images/questions_split/display02.png?raw=true)
![效果展示03](https://github.com/xiaojinlii/xiao-qa-generator/blob/main/images/questions_split/display03.png?raw=true)
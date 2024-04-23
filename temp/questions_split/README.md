# 问题分隔数据集


## 生成思路
1. 使用带主题的Prompt模板（如`prompt_questions_split_one_topic`），避免在多次生成数据集时，出现相同的问题
2. 分别使用`prompt_questions_split_one_topic`、`prompt_questions_split_two_topic`、`prompt_questions_split_three_topic`生成只包含1个子问题、2个子问题、3个子问题的数据集，这样可以控制每种子问题的数量及质量
3. 先将生成的数据集按topic进行合并，再合并所有的数据集
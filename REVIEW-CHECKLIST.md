# Review Checklist — 《养生两千五百年》

## 审阅总览

| 章 | 中文文件 | 英文文件 | 初稿状态 |
|----|---------|---------|----------|
| 00 | ch00-preface-zh.md | ch00-preface-en.md | ✅ |
| 01 | ch01-oldest-conversation-zh.md | ch01-oldest-conversation-en.md | ✅ |
| 02 | ch02-living-in-rhythm-zh.md | ch02-living-in-rhythm-en.md | ✅ |
| 03 | ch03-food-as-medicine-zh.md | ch03-food-as-medicine-en.md | ✅ |
| 04 | ch04-emotional-body-zh.md | ch04-emotional-body-en.md | ✅ |
| 05 | ch05-moving-like-water-zh.md | ch05-moving-like-water-en.md | ✅ |
| 06 | ch06-art-of-prevention-zh.md | ch06-art-of-prevention-en.md | ✅ |
| 07 | ch07-yin-yang-balance-zh.md | ch07-yin-yang-balance-en.md | ✅ |
| 08 | ch08-sleep-healer-zh.md | ch08-sleep-healer-en.md | ✅ |
| 09 | ch09-90-day-reset-zh.md | ch09-90-day-reset-en.md | ✅ |

---

## P0 — 必须修复（发布前）

### 原典引文准确性
- [ ] 核实每条《素问》《灵枢》引文的原文是否准确（对照通行本）
- [ ] 核实引文出处的篇章编号是否正确
- [ ] 确保古文原文无错字、无遗漏

### 医学/健康声明合规
- [ ] 确认全书无未标注的医疗建议（需加 disclaimer）
- [ ] 检查是否需要在前言或版权页加"本书不构成医疗建议"声明
- [ ] 核实健康数据引用（如 CDC 数据、NK 细胞研究数据）的准确性

### 参考文献核实
- [ ] 每章参考文献 ≥ 5 条
- [ ] 核实论文 DOI 和出版年份
- [ ] 核实作者姓名拼写
- [ ] 核实 Nobel Prize 2017 获奖者信息
- [ ] 核实 WHO Traditional Medicine Strategy 年份和名称

---

## P1 — 应当验证

### 内容一致性
- [ ] Ch01 的"五柱框架"与 Ch09 的总览回顾一致
- [ ] 子午流注表格（Ch02）在全书引用时数据一致
- [ ] 七情-脏腑映射（Ch04）在全书引用时一致
- [ ] 五味-脏腑映射（Ch03）在全书引用时一致
- [ ] 四时养生建议在 Ch02、Ch03、Ch08 之间无矛盾

### 科学事实核查
- [ ] 胶质淋巴系统发现年份（Ch08）：Nedergaard 2012 vs 2013
- [ ] NK 细胞活性下降数据（70%）出处
- [ ] 习惯形成天数（66 天）Lally 研究细节
- [ ] ACE 研究（Felitti）出版年份和期刊
- [ ] Satchin Panda 的 TRE 研究具体论文

### 章间过渡
- [ ] 每章结尾的"过渡到下一章"预告与下一章开头呼应
- [ ] Ch01 开头的黄帝之问与 Ch09 结尾的闭环呼应
- [ ] 五柱框架在全书连贯

---

## P2 — 建议检查

### Mermaid 图表
- [ ] 所有 Mermaid 图在 mermaid.live 上渲染测试
- [ ] 宽度均 ≤ 700px（无横向溢出）
- [ ] 未使用 `block-beta` 类型
- [ ] 中英文版的图表内容语言对应

### 双语同步
- [ ] 每章中英文结构一致（小节编号、标题对应）
- [ ] 关键术语中英文对照一致（如"治未病"全书统一翻译为同一英文）
- [ ] 原典引文在两个版本中均有呈现

### 写作风格
- [ ] 主动语态为主（无连续被动句）
- [ ] 段落 ≤ 5 句
- [ ] 术语首次出现有定义和英文对照
- [ ] 无东方主义或神秘化表述
- [ ] 无过度医疗声明

### 术语统一表

| 中文 | 英文 | Pinyin | 检查 |
|------|------|--------|------|
| 黄帝内经 | Huangdi Neijing / Yellow Emperor's Classic | Huángdì Nèijīng | [ ] |
| 素问 | Basic Questions / Su Wen | Sù Wèn | [ ] |
| 灵枢 | Spiritual Pivot / Ling Shu | Líng Shū | [ ] |
| 岐伯 | Qi Bo | Qí Bó | [ ] |
| 治未病 | Preventive medicine / Treating the not-yet-sick | zhì wèi bìng | [ ] |
| 子午流注 | Meridian Clock / Organ Clock | zǐ wǔ liú zhù | [ ] |
| 五味 | Five Flavors | wǔ wèi | [ ] |
| 七情 | Seven Emotions | qī qíng | [ ] |
| 导引 | Daoyin | dǎo yǐn | [ ] |
| 阴阳 | Yin-Yang | yīn yáng | [ ] |
| 卫气 | Defensive Qi / Wei Qi | wèi qì | [ ] |

---

## 审阅时间估算

| 项目 | 预估时间 |
|------|----------|
| 通读全书（中文版） | 3-4 小时 |
| 通读全书（英文版） | 3-4 小时 |
| 原典引文核实 | 2 小时 |
| 科学参考文献核实 | 2 小时 |
| Mermaid 图表渲染测试 | 30 分钟 |
| 双语同步检查 | 1-2 小时 |
| 术语统一性检查 | 30 分钟 |
| **总计** | **约 12-15 小时** |

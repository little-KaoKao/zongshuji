# 01_智枢 Prompt 日志

> 神兽：智枢（百目千臂神）
> 对应：中关村科学城 / 原始创新
> 题跋：其状如人而千目，司万智之枢，见则百业兴焉
> 印章："智枢" / "中关村"
> 页码：卷一·之一

---

## 尝试 001
- 日期：
- 工具：
- Prompt：
- 参数（含 --sref MASTER URL）：
- 结果文件：
- 评估：
- 迭代方向：

## 尝试 002
- ...

---

## 风格一致性校验
- [ ] 主色调与 MASTER 一致
- [ ] 质感（纸感、笔意）一致
- [ ] 数据元素可见度与融合度一致
- [ ] 朱砂印位置一致（右下角）

---

## 最终定稿
- 文件：FINAL-refined.png / FINAL-print.tif
- 最终 Prompt：
- 确认日期：

## 生产总结
（记录哪个 prompt 最有效、哪些坑、后续神兽可借鉴的经验）

### Run #4 · 2026-04-19 15:04
- **模型**: `omni-v2`
- **taskId**: `2045760341795020801`
- **Prompt**:

```
A mythical creature Zhishu from the new Shan Hai Jing, depicted as a solemn humanoid deity with hundreds of glowing eyes distributed across its body and multiple elongated arms radiating outward, each hand holding symbolic objects of science and wisdom (an astrolabe, a scroll, a lotus, a crystal, a compass, a brush), calm yet powerful expression, creature stands prominently on a rocky ledge in the mid-ground fully visible, rendered in meticulous gongbi painting style with crisp ink outlines and layered mineral pigment on the deity. Setting: a panoramic Chinese blue-green landscape painting, Song dynasty court style, tall layered mountains of Zhongguancun science city rendered with mineral azurite blue (shiqing) and malachite green (shilü) pigments, mountain ridges and cliffs subtly composed of flowing luminous data particles, circuit-board filigree, tiny glowing server racks embedded in the slopes as pagodas, drifting mist carrying soft streams of glowing code fragments, one small vermilion cinnabar square seal stamp in the lower right corner only, textured aged silk scroll paper with faint crackle, ethereal golden-hour light, strict limited palette dominated by stone green and stone blue with minimal vermilion accents, highly detailed masterwork. IMPORTANT: no calligraphy, no Chinese characters, no inscription, no signature, no title, no poem, only one small red seal at bottom right, otherwise pure painting
```
- **本地文件**:
  - `outputs\01_智枢\run0004\result_5.jpg`
- **结果 URL（24h 过期）**:
  - https://rh-images-1252422369.cos.ap-beijing.myqcloud.com/8185558a04bcef7106ea5517ebc83fb4/output/e1509391-5db8-4d60-911e-859cc861342c.jpg

### Run #6 · 2026-04-19 15:12
- **模型**: `omni-v2`
- **taskId**: `2045762164308193282`
- **基于**: Run #4
- **反馈驱动**: omni-v2对blue-green landscape再次引发千里江山图伪题跋。神兽千目多臂特征也丢失。换seedream-v5-lite + 1920x1080，重构prompt主次。
- **Prompt**:

```
A majestic anthropomorphic guardian deity named Zhishu, humanoid figure rendered in vivid mineral azure and stone-green pigments, its body and shoulders covered with over one hundred small luminous golden open eyes scattered across skin and robes, eight long outstretched arms fanning out behind its back, each hand carefully holding one symbolic relic (a brass astrolabe, a bamboo scroll, a glowing white lotus, a faceted blue crystal, a compass ring, a fine brush, a seed pod, and a small radiant sun), calm serene expression, flowing ornate silken robe with ribbons, the deity stands tall and dominant on a jutting rocky platform in the center-foreground of the composition, occupying roughly one third of the image height, fully visible, crisp gongbi brushwork with precise ink outlines and layered mineral pigment, rich color saturation on the creature. Setting behind and around: soaring layered karst peaks in saturated malachite green (shilü) and azurite blue (shiqing) mineral pigments, peak slopes subtly embedded with delicate faint circuit-board lace patterns and tiny luminous data particles, tiny pagodas and micro observatory towers tucked into distant cliffs like Zhongguancun science park, drifting mist carrying soft threads of glowing code fragments, two thin waterfalls on the sides, aged silk paper with faint crackle texture, warm golden afternoon light, refined Song court aesthetic, a single small vermilion cinnabar square seal stamp in the bottom-right corner only. IMPORTANT: NO calligraphy, NO chinese characters anywhere, NO inscription, NO signature, NO poem, NO title, NO writing, NO captions, absolutely no text of any kind in the image
```
- **本地文件**:
  - `outputs\01_智枢\run0006\result_6.jpg`
- **结果 URL（24h 过期）**:
  - https://rh-images-1252422369.cos.ap-beijing.myqcloud.com/8185558a04bcef7106ea5517ebc83fb4/output/b5e4e7b6-3bed-446a-9eff-f618ac261b34.jpg

### Run #7 · 2026-04-19 15:14
- **模型**: `omni-v2`
- **taskId**: `2045762723249532930`
- **基于**: Run #6
- **反馈驱动**: 构图错误：生成的是普通麒麟而非千目多臂智枢，背景空。需要视角拉近，神兽为绝对主体。
- **Prompt**:

```
Close-up portrait of a mythical many-eyed multi-armed guardian deity, dominating the composition, seated lotus position on a glowing circuit-lotus throne floating in a Chinese mountain valley. The deity has soft-blue skin painted in azurite mineral pigment, 108 small glowing golden eyes open all across its forehead, neck, shoulders, arms and chest — visibly countable, NOT just decorative dots. Eight long elegant human arms radiate symmetrically behind its back, each hand clearly holding one distinct object: an astrolabe, a bamboo scroll, a white lotus, a cut crystal, a compass, a writing brush, a seed pod, a tiny golden sun. Calm serene bodhisattva-like face with three additional eyes on forehead. Ornate flowing silk robe with green and gold ribbons. The deity fills roughly half the frame height, fully visible and central. Painted in meticulous Chinese gongbi brushwork, crisp ink outlines, layered mineral pigment. Behind the deity: a wide panoramic valley, saturated stone-green (malachite) and stone-blue (azurite) karst peaks, slopes softly embedded with faint circuit patterns and tiny glowing data particles, distant pagodas and micro observatory towers representing Zhongguancun science city, soft cascading mist carrying luminous code streams, thin waterfalls, aged silk paper texture, warm golden afternoon light, a single small red cinnabar square seal in the lower-right corner only. IMPORTANT: absolutely NO calligraphy, NO chinese characters, NO inscription, NO signature, NO poem, NO title label, NO writing, NO captions, no text of any kind in the image, pure painting only
```
- **本地文件**:
  - `outputs\01_智枢\run0007\result_7.jpg`
- **结果 URL（24h 过期）**:
  - https://rh-images-1252422369.cos.ap-beijing.myqcloud.com/8185558a04bcef7106ea5517ebc83fb4/output/3dbf8f27-8a98-4454-a103-e86f02e399d7.jpg

### Run #8 · 2026-04-19 20:15
- **模型**: `omni-v2`
- **taskId**: `2045838241638522881`
- **基于**: Run #7
- **反馈驱动**: 再次伪造千里江山图王希孟题跋，神兽又退化成普通麒麟。必须彻底换措辞避开landscape painting。
- **Prompt**:

```
An ornate Chinese mural-style portrait in the tradition of Dunhuang cave frescoes, depicting a powerful mythical guardian named Zhishu: a stately bodhisattva-like deity with eight elegant human arms radiating symmetrically from its shoulders, each hand clearly grasping a different object (an astrolabe, a bamboo scroll, a white lotus, a faceted crystal, a compass, a brush, a seed pod, a small glowing sun). The deity has pale azure skin and its body, forehead and shoulders are covered with dozens of small glowing golden eyes, distinctly countable, at least fifty eyes scattered across skin. Calm serene face with three vertical eyes on forehead. Wearing richly embroidered silken robes with fluttering ribbons. The deity is the central subject, fills half the frame height, seated on a stylized lotus platform. Meticulous gongbi brushwork, crisp ink outlines, layered mineral pigment (cinnabar red, azurite blue, malachite green, gold leaf). Background: an abstract decorative mandala of faint circuit patterns, tiny glowing data particles, stylized flame halos, distant schematic peaks suggesting a guarded science city, soft gold leaf sky, no landscape painting style, no blue-green mountain scroll, no Song dynasty scroll aesthetic. A single small vermilion cinnabar square seal stamp is placed in the lower-right corner. IMPORTANT: ABSOLUTELY no Chinese characters, no calligraphy, no inscription, no signature, no poem, no title, no text, no writing, no captions anywhere in the image. Pure decorative mural illustration only
```
- **本地文件**:
  - `outputs\01_智枢\run0008\result_8.jpg`
- **结果 URL（24h 过期）**:
  - https://rh-images-1252422369.cos.ap-beijing.myqcloud.com/8185558a04bcef7106ea5517ebc83fb4/output/5f873238-84f0-4794-ad0e-256189edc91f.jpg

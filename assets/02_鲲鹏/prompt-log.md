# 02_鲲鹏 Prompt 日志

> 神兽：鲲鹏（由鱼化鸟，尾喷天火）
> 对应：怀柔科学城 / 商业航天与深空探测
> 题跋：化而为鸟，尾喷天火，扶摇九万里，俯瞰九州
> 印章："鲲鹏" / "怀柔"
> 页码：卷一·之二

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

### Run #9 · 2026-04-19 20:16
- **模型**: `omni-v2`
- **taskId**: `2045838917240238082`
- **Prompt**:

```
An ornate Chinese mural-style portrait in the tradition of Dunhuang cave frescoes, depicting a mythical guardian named Kunpeng: a colossal winged celestial bird of fire transformed from a great fish, soaring upward diagonally across the composition, immense outstretched wings spanning the full frame with layered feathers painted in vivid cinnabar red, gold leaf and mineral azurite blue, long serpentine body still bearing translucent fish scales near its belly, twin trails of orange and gold flame erupting from its tail like rocket exhaust, head turned proudly forward with intelligent eyes and flowing crest. The creature occupies two thirds of the frame height, body fully visible. Meticulous gongbi brushwork, crisp ink outlines, layered mineral pigment, ornate decorative feather detailing. Background: layered karst peaks below painted in saturated malachite green and azurite blue mineral pigments, peaks softly embedded with faint circuit patterns, tiny glowing observatory domes and rocket launch towers tucked into distant cliffs representing Huairou science city, thin trails of luminous data particles rising like stars, soft gold leaf sky above, drifting cloud ribbons, aged silk paper texture with faint crackle, warm golden dawn light, a single small vermilion cinnabar square seal stamp in the lower-right corner only. IMPORTANT: ABSOLUTELY no Chinese characters, no calligraphy, no inscription, no signature, no poem, no title, no text, no writing, no captions anywhere in the image. Pure decorative mural illustration only
```
- **本地文件**:
  - `outputs\02_鲲鹏\run0009\result_9.jpg`
- **结果 URL（24h 过期）**:
  - https://rh-images-1252422369.cos.ap-beijing.myqcloud.com/8185558a04bcef7106ea5517ebc83fb4/output/d3aee9d0-53ba-4dbe-9321-4702761ee5f2.jpg

### Run #11 · 2026-04-19 20:28
- **模型**: `omni-v2`
- **taskId**: `2045841923662811138`
- **基于**: Run #9
- **Prompt**:

```
A huge mythical flaming phoenix-dragon bird called Kunpeng soaring across an ancient Chinese mural. Crimson-red and gold-plumed feathered wings fully outstretched, spanning the entire image width in dynamic flight; long sinuous serpentine body trailing behind with iridescent fish-like scales; fierce eagle head with glowing crown; twin jets of orange-red flame shooting from the tail like rocket propulsion. The bird is the sole subject, flying diagonally upward across the frame, occupying most of the composition. Meticulous Chinese gongbi brushwork with crisp ink outlines and mineral pigments (cinnabar vermilion, gold leaf, azurite blue). Below the bird: low silhouette of stone-green and stone-blue mountains, tiny white observatory domes and rocket gantries on distant cliffs, soft golden pre-dawn sky with wisps of cloud and trailing sparks of data particles, faint subtle circuit pattern along the horizon. Aged silk paper texture with faint crackle. One small vermilion cinnabar square seal stamp in the lower-right corner only. No person, no humanoid, no bodhisattva, no multiple arms; ONLY a flying bird with wings and a long body. ABSOLUTELY no Chinese characters, no calligraphy, no inscription, no signature, no poem, no title, no text
```
- **本地文件**:
  - `outputs\02_鲲鹏\run0011\result_10.jpg`
- **结果 URL（24h 过期）**:
  - https://rh-images-1252422369.cos.ap-beijing.myqcloud.com/8185558a04bcef7106ea5517ebc83fb4/output/26fd553d-0df6-4f2a-b800-817332d2e51f.jpg

### Run #12 · 2026-04-19 20:35
- **模型**: `youchuan-v7`
- **taskId**: `2045843416839233538`
- **基于**: Run #11
- **反馈驱动**: 致命问题：生成了'千里江山图 王希孟'伪签。竞赛不能用。omni-v2对Chinese mountain+ mineral pigment有极强先验导致每次伪造。
- **Prompt**:

```
Epic illustration of a colossal mythical phoenix-dragon bird soaring diagonally through the sky, crimson-red and gold feathered wings fully outstretched spanning the frame, long sinuous scaled serpentine body trailing behind, fierce eagle head with flowing crest, twin trails of orange-red rocket flame and golden sparks erupting from its tail. The bird is the sole subject. Background: distant low mountain silhouettes in soft jade green and deep blue far below, tiny white observatory domes and rocket launch gantries on small distant cliffs, soft golden pre-dawn sky with wisps of cloud and trailing stardust. Traditional Chinese fine-line color painting technique, crisp outlines, layered mineral color pigment, aged silk paper texture with faint crackle. One small red square seal stamp in the lower-right corner. No humans, no humanoid figures, no deity, no multiple arms, no lotus throne, only a flying bird. No text, no Chinese characters, no writing, no inscription, no signature, no poem, no title anywhere.
```
- **本地文件**:
  - `outputs\02_鲲鹏\run0012\result_11.png`
  - `outputs\02_鲲鹏\run0012\result_12.png`
  - `outputs\02_鲲鹏\run0012\result_13.png`
  - `outputs\02_鲲鹏\run0012\result_14.png`
- **结果 URL（24h 过期）**:
  - https://rh-images-1252422369.cos.ap-beijing.myqcloud.com/8185558a04bcef7106ea5517ebc83fb4/output/6292cd03-f3cd-43c6-a217-aae25d9e93e9.png
  - https://rh-images-1252422369.cos.ap-beijing.myqcloud.com/8185558a04bcef7106ea5517ebc83fb4/output/f3884d37-f0f7-43f0-90a5-df8afcc7cc69.png
  - https://rh-images-1252422369.cos.ap-beijing.myqcloud.com/8185558a04bcef7106ea5517ebc83fb4/output/d2654a42-1af4-48ff-b18b-41f34df0395a.png
  - https://rh-images-1252422369.cos.ap-beijing.myqcloud.com/8185558a04bcef7106ea5517ebc83fb4/output/e409558a-f8c1-45eb-917d-2793fd5cda44.png

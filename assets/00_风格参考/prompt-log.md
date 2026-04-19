# 00_风格参考 Prompt 日志

> 本目录专用日志，只记录 **MASTER-STYLE-REFERENCE** 主风格参考图的迭代过程。
> 目标：得到一张能作为全项目 style reference 的主图，锁死青绿山水 × 数据可视化 × 工笔神兽的视觉基调。

---

## 尝试 001
- 日期：
- 工具：
- Prompt：
- 参数：
- 结果文件：
- 评估：
- 迭代方向：

## 尝试 002
- ...

---

## 最终锁定

- 文件：`assets/00_风格参考/MASTER-STYLE-REFERENCE.png`（= `outputs/00_风格参考/run0002/result_2.jpg`）
- 来源 run：**#2** (omni-v2, aspectRatio=2:3, resolution=4k)
- 最终 Prompt：见下面 Run #2 条目
- 确认日期：2026-04-19
- 上传 URL（24h 有效，本批次参考用）：
  `https://rh-images-switch-1252422369.cos.ap-guangzhou.myqcloud.com/input/openapi/b6e9f0b39f3dcd22313817a6e1a6214147543567602e4f6e91b1bf914c9710ba.png`

### 锚定的视觉基调（后续六神与总览图必须遵守）

- **色彩**：石青 + 石绿为主，少量朱砂、赭石作为点缀；背景偏奶金米色绢本
- **构图**：高耸层叠山峦 + 瀑布 + 云雾山涧 + 岩台神兽半身以上清晰可见
- **科技元素**：山体暗藏电路线 / 微粒 / 浮空蓝白光流；数据感"藏"在山水里，不突兀
- **神兽笔法**：工笔线描，鳞/毛/须清晰，设色层次分明，置于中景岩台、完全可见
- **印章**：只有右下角一枚小尺寸朱砂方印
- **严禁**：任何文字题跋、落款、诗句、签名（必须写入 negative / IMPORTANT 子句）
- **纸感**：绢本做旧、淡微裂纹

### 六神生成的调用模板

```
{角色 prompt 主体},
panoramic Chinese blue-green landscape painting, Song dynasty court style,
tall layered mountains rendered with mineral azurite blue (shiqing) and
malachite green (shilü) pigments, mountain ridges and cliffs subtly composed
of flowing luminous data particles and delicate circuit-board filigree woven
into the rocks, drifting mist carrying soft streams of glowing code fragments,
the creature depicted in meticulous gongbi painting style with crisp ink
outlines and layered mineral pigment, creature stands majestically in the
mid-foreground fully visible, small vermilion cinnabar square seal stamp in
the lower right corner only, textured aged silk scroll paper with faint
crackle, ethereal golden-hour light, strict limited palette dominated by
stone green and stone blue with minimal vermilion accents, highly detailed
masterwork.
IMPORTANT: no calligraphy, no Chinese characters, no inscription, no
signature, no title, no poem, only one small red seal at bottom right,
otherwise pure painting.
```

### Run #1 · 2026-04-19 14:44
- **模型**: `omni-v2`
- **taskId**: `2045755342557945858`
- **Prompt**:

```
A panoramic Chinese blue-green landscape painting (qinglü shanshui) in the style of Wang Ximeng's 'A Thousand Li of Rivers and Mountains', majestic layered mountains rendered with mineral azurite blue and malachite green pigments, mountain silhouettes subtly composed of flowing data particles and faint circuit board patterns woven into rocks, drifting mist with soft luminous code streams, a single elegant gongbi-style mythical creature half-hidden in the valley mist with delicate line art, vermilion cinnabar seal stamp at lower right, textured aged silk scroll paper with faint crackle, ethereal golden hour light, limited palette dominated by stone green and stone blue with vermilion accents, traditional Chinese ink painting aesthetic fused with subtle futuristic data visualization, highly detailed, masterwork, epic panoramic composition
```
- **本地文件**:
  - `outputs\00_风格参考\run0001\result_1.jpg`
- **结果 URL（24h 过期）**:
  - https://rh-images-1252422369.cos.ap-beijing.myqcloud.com/8185558a04bcef7106ea5517ebc83fb4/output/b5c92b01-e26c-4b38-8f32-623fb16fa0a7.jpg

### Run #2 · 2026-04-19 14:58
- **模型**: `omni-v2`
- **taskId**: `2045756015294947329`
- **基于**: Run #1
- **反馈驱动**: 方向对：青绿主色+纸感+朱砂印章。问题：神兽太虚化需工笔重彩、数据元素偏弱、画面出现AI伪造题跋要避免。
- **Prompt**:

```
A panoramic Chinese blue-green landscape painting (qinglü shanshui), Song dynasty style, majestic layered mountains rendered with mineral azurite blue (shiqing) and malachite green (shilü) pigments, mountain ridges and cliffs subtly composed of flowing luminous data particles and delicate circuit-board filigree woven into the rocks, drifting mist carrying soft streams of glowing code fragments, a single prominent mythical auspicious creature (qilin-like beast) depicted in meticulous gongbi bird-and-flower painting style with crisp ink outlines and layered mineral pigment coloring, distinct crisp linework on the creature, creature stands majestically on a ledge in the mid-foreground fully visible, small vermilion cinnabar square seal stamp in the lower right corner only, textured aged silk scroll paper with faint crackle and subtle wear, ethereal golden-hour light, strict limited palette dominated by stone green and stone blue with minimal vermilion accents, traditional Chinese ink painting aesthetic fused with subtle futuristic data visualization, highly detailed masterwork. IMPORTANT: no calligraphy text, no Chinese characters, no inscription, no signature, no title, no poem, only one small red seal at bottom right, otherwise pure painting
```
- **本地文件**:
  - `outputs\00_风格参考\run0002\result_2.jpg`
- **结果 URL（24h 过期）**:
  - https://rh-images-1252422369.cos.ap-beijing.myqcloud.com/8185558a04bcef7106ea5517ebc83fb4/output/0fbeb94d-adfc-494c-81cd-7aa43f6c7d85.jpg

### Run #2 · 2026-04-19 14:58
- **模型**: `omni-v2`
- **taskId**: `2045756015294947329`
- **基于**: Run #1
- **反馈驱动**: 方向对：青绿主色+纸感+朱砂印章。问题：神兽太虚化需工笔重彩、数据元素偏弱、画面出现AI伪造题跋要避免。
- **Prompt**:

```
A panoramic Chinese blue-green landscape painting (qinglü shanshui), Song dynasty style, majestic layered mountains rendered with mineral azurite blue (shiqing) and malachite green (shilü) pigments, mountain ridges and cliffs subtly composed of flowing luminous data particles and delicate circuit-board filigree woven into the rocks, drifting mist carrying soft streams of glowing code fragments, a single prominent mythical auspicious creature (qilin-like beast) depicted in meticulous gongbi bird-and-flower painting style with crisp ink outlines and layered mineral pigment coloring, distinct crisp linework on the creature, creature stands majestically on a ledge in the mid-foreground fully visible, small vermilion cinnabar square seal stamp in the lower right corner only, textured aged silk scroll paper with faint crackle and subtle wear, ethereal golden-hour light, strict limited palette dominated by stone green and stone blue with minimal vermilion accents, traditional Chinese ink painting aesthetic fused with subtle futuristic data visualization, highly detailed masterwork. IMPORTANT: no calligraphy text, no Chinese characters, no inscription, no signature, no title, no poem, only one small red seal at bottom right, otherwise pure painting
```
- **本地文件**:
  - `outputs\00_风格参考\run0002\result_2.jpg`
  - `outputs\00_风格参考\run0002\result_3.jpg`
- **结果 URL（24h 过期）**:
  - https://rh-images-1252422369.cos.ap-beijing.myqcloud.com/8185558a04bcef7106ea5517ebc83fb4/output/0fbeb94d-adfc-494c-81cd-7aa43f6c7d85.jpg

### Run #3 · 2026-04-19 15:00
- **模型**: `seedream-v5-lite`
- **taskId**: `2045759144124100609`
- **基于**: Run #2
- **反馈驱动**: 缺陷：第二张result_3仍然出现王希孟千里江山图伪题跋。要彻底避开Wang Ximeng这个触发词。result_2与run1几乎一样，说明omni-v2记住了prompt。
- **Prompt**:

```
Traditional Chinese blue-green landscape painting, Song dynasty court painting aesthetic, tall layered karst mountains painted in rich mineral stone-green (shilü) and stone-blue (shiqing) pigments, mountain slopes decorated with delicate faint circuit-like patterns and glowing particles of data woven subtly into the rocks like embedded constellation maps, thin streams of luminous coded light drifting through the valley mist, pristine waterfalls, a single auspicious mythical beast (resembling a qilin with scaled body and flame mane) standing on a rocky ledge in the mid-ground, rendered in meticulous gongbi brushwork with precise ink outlines and layered mineral pigment, the beast clearly visible and fully detailed, one small red cinnabar square seal stamp in the bottom-right corner only, on aged silk with gentle crackle texture, warm golden afternoon light, palette strictly limited to malachite green, azurite blue, ochre, and small vermilion accents, elegant refined atmosphere, meticulous masterwork. Negative: NO calligraphy, NO chinese characters anywhere, NO poetry inscription, NO artist signature text, NO title label, NO writing, NO text, NO captions, clean painting without any written words
```
- **本地文件**:
  - `outputs\00_风格参考\run0003\result_4.jpg`
- **结果 URL（24h 过期）**:
  - https://rh-images-1252422369.cos.ap-beijing.myqcloud.com/8185558a04bcef7106ea5517ebc83fb4/output/7cfb0290-4e92-4d69-ae90-14dc21609323.jpg

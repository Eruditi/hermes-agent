---
name: songsee
description: 通过CLI从音频文件生成频谱图和音频特征可视化（mel、chroma、MFCC、tempogram等）。用于音频分析、音乐制作调试和可视化文档。
version: 1.0.0
author: community
license: MIT
metadata:
  hermes:
    tags: [音频, 可视化, 频谱图, 音乐, 分析]
    homepage: https://github.com/steipete/songsee
prerequisites:
  commands: [songsee]
---

# songsee

从音频文件生成频谱图和多面板音频特征可视化。

## 先决条件

需要[Go](https://go.dev/doc/install)：
```bash
go install github.com/steipete/songsee/cmd/songsee@latest
```

可选：`ffmpeg`用于WAV/MP3以外的格式。

## 快速开始

```bash
# 基本频谱图
songsee track.mp3

# 保存到特定文件
songsee track.mp3 -o spectrogram.png

# 多面板可视化网格
songsee track.mp3 --viz spectrogram,mel,chroma,hpss,selfsim,loudness,tempogram,mfcc,flux

# 时间切片（从12.5s开始，8秒持续时间）
songsee track.mp3 --start 12.5 --duration 8 -o slice.jpg

# 从stdin
cat track.mp3 | songsee - --format png -o out.png
```

## 可视化类型

使用`--viz`和逗号分隔的值：

| 类型 | 描述 |
|------|-------------|
| `spectrogram` | 标准频率频谱图 |
| `mel` | Mel标度频谱图 |
| `chroma` | 音高类别分布 |
| `hpss` | 谐波/打击乐分离 |
| `selfsim` | 自相似矩阵 |
| `loudness` | 随时间的响度 |
| `tempogram` | 速度估计 |
| `mfcc` | Mel频率倒谱系数 |
| `flux` | 频谱通量（起始检测） |

多个`--viz`类型在单个图像中渲染为网格。

## 常用标志

| 标志 | 描述 |
|------|-------------|
| `--viz` | 可视化类型（逗号分隔） |
| `--style` | 调色板：`classic`、`magma`、`inferno`、`viridis`、`gray` |
| `--width` / `--height` | 输出图像尺寸 |
| `--window` / `--hop` | FFT窗口和跳跃大小 |
| `--min-freq` / `--max-freq` | 频率范围过滤 |
| `--start` / `--duration` | 音频的时间切片 |
| `--format` | 输出格式：`jpg`或`png` |
| `-o` | 输出文件路径 |

## 备注

- WAV和MP3是原生解码的；其他格式需要`ffmpeg`
- 输出图像可以用`vision_analyze`检查以进行自动音频分析
- 用于比较音频输出、调试合成或记录音频处理管道

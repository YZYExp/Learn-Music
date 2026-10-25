# 试听与离线实验

以下四段WAV是原创数学模型，供比较变量，不是真实乐器录音、标准音色或作品片段。工程包解压后可直接播放；EPUB内附同名媒体资源，播放或另存取决于阅读器支持。不支持时请从工程包的`assets/audio/`打开。

| 文件                                                 | 顺序与参数                              | 对应正文 |
|------------------------------------------------------|-----------------------------------------|----------|
| [01-harmonics.wav](../assets/audio/01-harmonics.wav) | 220 Hz；1、4、10个谐波；每段2.2秒       | 02、19   |
| [02-envelope.wav](../assets/audio/02-envelope.wav)   | 220 Hz、6个谐波；衰减／持续；每段2.8秒  | 02、19   |
| [03-beating.wav](../assets/audio/03-beating.wav)     | 220+222 Hz／220+220.5 Hz；每组6秒       | 18、19   |
| [04-grouping.wav](../assets/audio/04-grouping.wav)   | 每段12声，间隔0.3秒；每2声／每3声一重音 | 18、19   |

文件为单声道、22050 Hz、16-bit PCM。片段间留0.5秒空白；各片段峰值归一到0.42，不代表主观等响。公式与包络见`scripts/make_audio.py`，Python标准库即可重建。

## 真实演奏与实物

| 来源入口                                                                                 | 建议观察                   | 证据边界                 |
|------------------------------------------------------------------------------------------|----------------------------|--------------------------|
| [The Met：现代琵琶演奏与旧藏](https://www.metmuseum.org/art/collection/search/505247)    | 音头与重复，另看旧藏器形   | 现代演奏不是旧藏当年原声 |
| [The Met：Cristofori 1720年钢琴](https://www.metmuseum.org/art/collection/search/501788) | 与第15章比较机构           | 不代表全部现代钢琴       |
| [UNSW：长笛声学资料](https://phys.unsw.edu.au/music/flute/index.html)                    | 不同音的指法与频谱         | 实验有特定乐器与条件     |
| [Yamaha：乐器指南](https://www.yamaha.com/en/musical_instrument_guide/)                  | 从具体器种进入演奏与结构页 | 不代表所有历史型号       |
| [UNESCO：甘美兰](https://ich.unesco.org/en/RL/gamelan-01607)                             | 合奏的分层与配合           | 不代表当地全部传统       |
| [Ableton：音乐实验工具](https://learningmusic.ableton.com/the-playground.html)           | 修改节奏、旋律与和弦       | 网页声音为工具提供的音色 |

真实录音和机构图片未打包转载，权利归原持有人。链接可能迁移，可用正文保留的机构、题名与藏品编号定位。资料检索日期：2026年10月25日。

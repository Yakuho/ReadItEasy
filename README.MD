<div align="center">
<p>
<a align="left" href="https://github.com/Yakuho/ReadItEasy" target="_blank">
<img width="850" src="https://github.com/Yakuho/ReadItEasy/blob/master/docs/resume.png"></a>
</p>
</div>

<p>
🚀 ReadItEasy 是一个关于识别字体文件的模型,它通过字体文件进行训练（如ttf、wpff格式），在经过有限次试验中，发现试验中的模型是有效的。模型目的是为了将传入的字体文件可自动识别里面的所有字符。
</p>

## <div align="center">Introduction</div>

<details open>
<summary>为什么训练这个模型？</summary>

这个模型是为了解决[基于KNN的字体反爬模型](https://github.com/Yakuho/DealFontCrawler)所带来的问题而出现的。在使用KNN算法对字体坐标
进行字符分类上，在一些标准的字体文件上其规范的字体设计和变动性不大，在使用欧式距离计算误差值能够去完成分类各个字符的任务。
但深入研究发现，在不同的字体文件中，通常其坐标可能会出现不规则的情况；就好比人写字，同一个字不同的人写的会有不同的书法。对于字体文件来说就是同一个字，
不同的字体文件会有不同的坐标向量组合。这导致计算欧式距离的时候，会出现相位不对齐的情况，导致鲁棒性很差。

这个模型就想要从函数拟合的角度去解决这个问题，提高字体分类的鲁棒性。

</details>

## <div align="center">Quick Start Example</div>

<details open>
<summary>环境安装</summary>

环境: [Python>=3.6.0](https://www.python.org/) [Tensorflow>=2.0](https://tensorflow.google.cn/)
```bash
$ git clone https://github.com/Yakuho/ReadItEasy
$ cd ReadItEasy
$ pip install -r requirements.txt
```

</details>

<details open>
<summary>模型使用 test.py</summary>

```python
class Terminal:
    ...

m = Terminal(classes_num=12,                            # 模型训练时设定的分类数
             weights='./weights/MaoYan.h5',             # 模型的训练后权重路径
             class_list='./datasets/labels/classes.txt' # 模型输出后的字符转换清单路径
)
m.predict(font_file='./evaluate/KS01.ttf')              # 传入字体文件路径进行预测
```

</details>

<details>
<summary>训练自定义的数据</summary>

<details>
<summary>1. 数据准备</summary>

- 准备字体文件如ttf/woff等数几十个；按照分类的数目类，数目依次增加

</details>

<details>
<summary>2. 工具使用</summary>

- 使用[tools/exportxml.py](https://github.com/Yakuho/ReadItEasy/blob/master/tools/exportxml.py)对字体文件进行格式转换，导出为XML格式
- 使用[tools/exportmap.py](https://github.com/Yakuho/ReadItEasy/blob/master/tools/exportmap.py)对字体文件进行编码
- 使用[tools/exportlabel.py](https://github.com/Yakuho/ReadItEasy/blob/master/tools/exportlabel.py)将字体文件转化为数据集，导出为npz格式

</details>

<details>
<summary>3. 数据集分割</summary>

- 将上面导出的npz文件的目录下，把classes.txt妥善保存并移除目录
- 使用[tools/splitdataset.py](https://github.com/Yakuho/ReadItEasy/blob/master/tools/splitdataset.py)对数据集进行分割

</details>

<details>
<summary>4. 配置文件</summary>

<details open>
<summary>必填项</summary>

- datasets -> class_list: 分类标签清单的路径
- datasets -> class_num: 模型的分类数目
- datasets -> train -> path: 训练集目录
- datasets -> valid -> path: 验证集目录
- datasets -> train -> steps: 训练集总共有多少个字 一般是文件数(N) * 每个文件里的字体数(M)
- datasets -> valid -> steps: 验证集总共有多少个字 一般是文件数(N) * 每个文件里的字体数(M)
- datasets -> valid -> epochs: 训练的轮次

</details>

<details>
<summary>选填项</summary>

- model -> restore: 是否继续恢复训练
- model -> checkpoint: 恢复训练的checkpoint文件路径
- model -> pre-training: 是否使用预训练权重
- model -> weights: 预训练权重的路径
- save -> model_name: 最后保存模型的名字
- save -> root_path: 保存模型的路径名
- save -> ckpt_freq: 检查点保存的频率(epoch为基准)

</details>

</details>

<details>
<summary>5. 训练</summary>

```shell script
python train.py
```

```shell script
...
{'unicode': 'uniE20A', 'char': '4', 'confidences': 0.99496007}
{'unicode': 'uniE2A0', 'char': '7', 'confidences': 0.98925006}
{'unicode': 'uniE3E1', 'char': '2', 'confidences': 0.9963917}
{'unicode': 'uniEC2F', 'char': '6', 'confidences': 0.989242}
{'unicode': 'uniECA9', 'char': '0', 'confidences': 0.99617445}
{'unicode': 'uniEDB6', 'char': '3', 'confidences': 0.74377424}
{'unicode': 'uniF11E', 'char': '8', 'confidences': 0.9967367}
{'unicode': 'uniF439', 'char': '9', 'confidences': 0.99818087}
{'unicode': 'uniF4E1', 'char': '1', 'confidences': 0.9952153}
{'unicode': 'uniF636', 'char': '5', 'confidences': 0.9941585}
{'unicode': 'x', 'char': '.', 'confidences': 0.9882712}
Inference finished cost 50.727ms
```

</details>
    
**最后要注意的是，模型训练产生的classes.txt是与模型是配套的，它指定了模型的输出字符的位置！！！**

</details>

## <div align="center">Experience</div>

以下是经过不同字体文件训练的数据(GPU: GTX1050，CPU: CORE i5): 

**RIE(ReadItEasy模型) KNN(K临近算法模型)**

|数据集     |字符主要类型  |字符数   |标准字体   |RIE准确率  |KNN准确率     |平均准确率  |RIE推理速度   |KNN推理速度  
|---        |---           |---     |---        |---        |---           |---         |---          |---   
|猫眼电影   |纯数字        |12       |❌        |100%       |90.9%         |---         |46ms         |4ms   
|大众点评   |中文字符+数字 |603      |✅        |100%       |100%          |---         |2000ms       |144ms    

欢迎在issue投稿更多不同的字体文件加入训练，有更多不同的字体更能增强模型的泛化能力，形成一个通用的字体坐标识别模型

以上使用的数据集测试均可在[evaluate](https://github.com/Yakuho/ReadItEasy/tree/master/evaluate)目录下找到, 欢迎复现尝试

## <div align="center">More details</div>

- [了解模型](https://github.com/Yakuho/ReadItEasy/tree/master/docs/README.MD)


## Requirements:
python3
nbt (可以使用pip安装)

## Usage:
usage: ftbquest_parser.py [-h] --srcdir SRCDIR [--dstdir DSTDIR]
                          [--hardcode HARDCODE] [--lang LANG]
                          [--reflang REFLANG] --generate_nbt GENERATE_NBT
                          [--namespace NAMESPACE] [--output_diff OUTPUT_DIFF]
                          [--output_lang OUTPUT_LANG]
                          [--output_format OUTPUT_FORMAT]

optional arguments:
  -h, --help            show this help message and exit
  --srcdir SRCDIR       source directory. e.g.,
                        "config/ftbquests/normal/chapters"
  --dstdir DSTDIR       destination directory
  --hardcode HARDCODE   whether to hardcode texts or not (default: False)
  --lang LANG           localized language file
  --reflang REFLANG     original language file for reference
  --generate_nbt GENERATE_NBT
                        whether to generate nbt file or not
  --namespace NAMESPACE
                        namespace for language keys (default:
                        modpack.ftbquests)
  --output_diff OUTPUT_DIFF
                        diff file to output, valid only when REFLANG provided
  --output_lang OUTPUT_LANG
                        language file to outout
  --output_format OUTPUT_FORMAT
                        format of output file (json/lang) (default: json)

## Example

生成手册语言文件：
```python3 ftbquest_parser.py --srcdir config/ftbquests/normal/chapters --generate_nbt False --output_lang lang.json```
可以加入--namespace参数设置language key的前缀，默认为"modpack.ftbquests"，也可以取作"整合包名.ftbquests"。设置其他namespace后再调用ftbquest_parser.py必须使用同样的namespace。
也可以加入--output_format lang参数输出lang格式的语言文件。

将翻译后的语言文件以硬编码形式写入手册：
```python3 ftbquest_parser.py --srcdir config/ftbquests/normal/chapters --dstdir output --generate_nbt True --hardcode True --lang lang_cn.json```
输入的语言文件支持lang和json格式，以后缀名区分。

更新版本后，对比上一版本的语言文件，检查有哪些被修改/新增的词条：
```python3 ftbquest_parser.py --srcdir config/ftbquests/normal/chapters --generate_nbt False --reflang lang.json --output_diff diff.json```
也可以输出两个版本的语言文件对文本进行比较。

将手册转换为非硬编码，即{lang.key}和外部语言文件的形式，并生成lang格式的语言文件。适用于1.5.2.151版本以上的FTB Quests。
```python3 ftbquest_parser.py --srcdir config/ftbquests/normal/chapters --dstdir output --generate_nbt True --output_format lang --output_lang en_us.lang```
将语言文件放入resources/<namespace>/lang文件夹（中文需注意编码问题），或放入资源包并加载。

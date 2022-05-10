# SerialManager

在 Windows 下，由于 Windows 串口分配机制，导致 Windows 串口会出现不断更换的情况。不论是生产环境、测试环境还是部署环境下，都非常麻烦。

这个工程的思路是使用一个 `csv` 文件描述串口，然后返回所有满足描述的串口号。



## 使用方式

**运行环境**

- [x] Python 3.10.1
- [x] Windows

**依赖**

- [pyserial](https://pyserial.readthedocs.io/en/latest/pyserial.html)



**安装依赖**：`pip install -r requirements.txt`

若想要使用虚拟环境：`python -m venv .`

现实当前系统下的所有串口项：`python tools/all_serial_info.py`

查找某设备的串口号：`python find_serial_com.py --des Arduino`

借助设备别名数据库，查找串口号：`python find_serial_com.py --des Arduino --db xxx.csv`，其中，CSV文件格式如下：

```csv
description,vid,pid,serial_number,location
LaserReceiver,9025,67,9503630343535140B251,
TestProjector,,,,1-3
```

任意字段都可以不存在，但若只有描述而没有任何的其他信息，此条记录是 **无意义** 的。若字段非空，则会采用完全匹配算法进行设备识别。比如上，设备 `TestProjector` 当 `location` 为 `1-3` 时，就会识别。但 `LaserReceiver` 需要 `vid`、`pid`、`serial_number`都相等时才会识别。

`vid`：Vender ID，生产商ID

`pid`：Project ID，设备ID

`serial_number`：序列号

`location` ：此字段是 `USB Bus-Port` 字段，若确定某设备一定会插在某串口上，可以以此字段进行识别。
# PickleHelper
一套调试Pickle字节码和构造Pickle字节码的工具
## PickleBuilder

通过Pickle源码，反向构造相关代码，提供一个工具类
### Usage
```python
from PickleBuilder import PickleBuilder

p = PickleBuilder()
p.push_str("abc'123123") # 传入字符串
p.push_bool(True) # 传入Boolean变量
p.push_int(123)   # 传入数字

p.push_mark() # 传入Mark用于字典构造

p.push_str("key1") # key
p.push_str("val1") # val
p.push_str("key2") # key
p.push_str("val2") # val

p.build_dict() # 构造数组

print(p.compile())  # 产生字节码
```


## PickleHooker

在`python3`Pickle源码上修改相关代码，可以实时执行的`stack`,`memo`,`metastack`和当前运行的指令。

### Usage

```python

import PickleHooker as pickle # 加载Hooker

pickle.loads(b"the code you wanna execute")

```
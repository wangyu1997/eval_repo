#!name=信息修改
#!author=Custom
#!desc=修改详情页的 xjzt 和 byrq 字段
#!category=Tools

[Script]
学信网学籍状态修改 = type=http-response,pattern=^https://my\.chsi\.com\.cn/archive/wap/gdjy/xj/detail\.action,requires-body=1,max-size=0,script-path=https://raw.githubusercontent.com/wangyu1997/eval_repo/refs/heads/main/demo1.js

[MITM]
hostname = %APPEND% my.chsi.com.cn

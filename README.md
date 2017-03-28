## 设备官网
https://www.yeelight.com

## 文档地址
https://www.yeelight.com/download/Yeelight_Inter-Operation_Spec.pdf

这里整合了yeelight的文档，重新封装了接口！

## 使用http协议

```
[CMD|DEVICES] * HTTP/1.1
Method:命令
Location:地址及端口
Param:参数(JSON字符串)
```

### 刷新接口
获取当前设别列表(json格式)

```
DEVICES * HTTP/1.1
```

## 支持的命令

>power_on      打开灯
1. effect  [sudden|smooth] (不必填)
2. duration 延时时间 30-n (不必填)

```
CMD * HTTP/1.1
Location:192.168.1.100:12345
Method:power_on
Param:{"effect":"smooth","duration":500}
```

>power_off     关闭灯
1. effect  [sudden|smooth] (不必填)
2. duration 延时时间 30-n (不必填)

```
CMD * HTTP/1.1
Location:192.168.1.100:12345
Method:power_off
Param:{"effect":"smooth","duration":500}
```

>start_cf

```
CMD * HTTP/1.1
Location:192.168.1.100:12345
Method:start_cf
Param:
```

>stop_cf

```
CMD * HTTP/1.1
Location:192.168.1.100:12345
Method:stop_cf
Param:
```

>cron_add      延时关闭灯
1. value 延时时间 0~n 整数 分钟

```
CMD * HTTP/1.1
Location:192.168.1.100:12345
Method:cron_add
Param:{"value":10}
```

>cron_get      获取延时关闭灯时间

```
CMD * HTTP/1.1
Location:192.168.1.100:12345
Method:cron_get
Param:
```

>cron_del      取消延时关闭灯

```
CMD * HTTP/1.1
Location:192.168.1.100:12345
Method:cron_del
Param:
```

>set_adjust

```
CMD * HTTP/1.1
Location:192.168.1.100:12345
Method:set_adjust
Param:
```

>set_bright    设置灯亮度
1. brightness 亮度 1-100
2. effect  [sudden|smooth] (不必填)
3. duration 延时时间 30-n (不必填)

```
CMD * HTTP/1.1
Location:192.168.1.100:12345
Method:set_bright
Param:{"brightness":50,"effect":"smooth","duration":500}
```

>set_rgb       设置灯颜色
1. rgb  十进制颜色值
2. effect  [sudden|smooth] (不必填)
3. duration 延时时间 30-n (不必填)

```
CMD * HTTP/1.1
Location:192.168.1.100:12345
Method:set_rgb
Param:{"rgb":16711680,"effect":"smooth","duration":500}
```

>set_hsv
1. hue
2. sat
2. effect  [sudden|smooth] (不必填)
3. duration 延时时间 30-n (不必填)

```
CMD * HTTP/1.1
Location:192.168.1.100:12345
Method:set_hsv
Param:{"hue":10,"sat":10,"effect":"smooth","duration":500}
```

>set_ct_abx

```
CMD * HTTP/1.1
Location:192.168.1.100:12345
Method:set_ct_abx
Param:
```

>set_default   保存当前设置

```
CMD * HTTP/1.1
Location:192.168.1.100:12345
Method:set_default
Param:
```

>toggle        开灯/关灯

```
CMD * HTTP/1.1
Location:192.168.1.100:12345
Method:toggle
Param:
```

>set_name      设置设备别名
1. name  名称

```
CMD * HTTP/1.1
Location:192.168.1.100:12345
Method:set_name
Param:{"name":"mylight"}
```

>set_scene     设置场景

```
CMD * HTTP/1.1
Location:192.168.1.100:12345
Method:set_scene
Param:
```

>get_prop      获取信息
1. prop 获取的信息字段 power,bright,id,Location,mode,color_mode,name

```
CMD * HTTP/1.1
Location:192.168.1.100:12345
Method:get_prop
Param:{"prop":["power","bright"]}
```

>search      重新扫描设备

```
CMD * HTTP/1.1
Location:192.168.1.100:12345
Method:search
Param:
```

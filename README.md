# 设备官网
https://www.yeelight.com

# 文档地址
https://www.yeelight.com/download/Yeelight_Inter-Operation_Spec.pdf

这里整合了yeelight的文档，重新封装了接口！

### 组播地址
>239.255.255.251:1982

### 协议格式
    CMD * HTTP/1.1
    location:地址及端口
    method:命令
    param:参数(JSON字符串)


### 支持的命令

>power_on      打开灯
1. effect  [sudden|smooth] (不必填)
2. duration 延时时间 30-n (不必填)

    CMD * HTTP/1.1
    location:192.168.1.100:12345
    method:power_on
    param:{"effect":"smooth","duration":500}

>power_off     关闭灯
1. effect  [sudden|smooth] (不必填)
2. duration 延时时间 30-n (不必填)

    CMD * HTTP/1.1
    location:192.168.1.100:12345
    method:power_off
    param:{"effect":"smooth","duration":500}

>start_cf

    CMD * HTTP/1.1
    location:192.168.1.100:12345
    method:start_cf
    param:

>stop_cf

    CMD * HTTP/1.1
    location:192.168.1.100:12345
    method:stop_cf
    param:

>cron_add      延时关闭灯
1. value 延时时间 0~n 整数

    CMD * HTTP/1.1
    location:192.168.1.100:12345
    method:cron_add
    param:{"value":10}

>cron_get      获取延时关闭灯时间

    CMD * HTTP/1.1
    location:192.168.1.100:12345
    method:cron_get
    param:

>cron_del      取消延时关闭灯

    CMD * HTTP/1.1
    location:192.168.1.100:12345
    method:cron_del
    param:

>set_adjust

    CMD * HTTP/1.1
    location:192.168.1.100:12345
    method:set_adjust
    param:

>set_bright    设置灯亮度
1. brightness 亮度 1-100
2. effect  [sudden|smooth] (不必填)
3. duration 延时时间 30-n (不必填)

    CMD * HTTP/1.1
    location:192.168.1.100:12345
    method:set_bright
    param:{"brightness":50,"effect":"smooth","duration":500}

>set_rgb       设置灯颜色
1. rgb  十进制颜色值
2. effect  [sudden|smooth] (不必填)
3. duration 延时时间 30-n (不必填)

    CMD * HTTP/1.1
    location:192.168.1.100:12345
    method:set_rgb
    param:{"rgb":16711680,"effect":"smooth","duration":500}

>set_hsv
1. hue
2. sat
2. effect  [sudden|smooth] (不必填)
3. duration 延时时间 30-n (不必填)

    CMD * HTTP/1.1
    location:192.168.1.100:12345
    method:set_hsv
    param:{"hue":10,"sat":10,"effect":"smooth","duration":500}

>set_ct_abx

    CMD * HTTP/1.1
    location:192.168.1.100:12345
    method:set_ct_abx
    param:

>set_default   保存当前设置

    CMD * HTTP/1.1
    location:192.168.1.100:12345
    method:set_default
    param:

>toggle        开灯/关灯

    CMD * HTTP/1.1
    location:192.168.1.100:12345
    method:toggle
    param:

>set_name      设置设备别名
1. name  名称

    CMD * HTTP/1.1
    location:192.168.1.100:12345
    method:set_name
    param:{"name":"mylight"}

>set_scene     设置场景

    CMD * HTTP/1.1
    location:192.168.1.100:12345
    method:set_scene
    param:

>get_prop      获取信息
1. prop 获取的信息字段 power,bright,id,location,mode,color_mode,name

    CMD * HTTP/1.1
    location:192.168.1.100:12345
    method:get_prop
    param:{"prop":["power",bright"]}

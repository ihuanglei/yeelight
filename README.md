## 智能服务器框架

### 使用http协议

```
CMD * HTTP/1.1
Method:命令
Location:地址及端口
Param:参数(JSON字符串)
```

```
runner.py 启动服务
```

### 当前实现的智能设备

* [![YeelightImg]](https://github.com/ihuanglei/ylauto/tree/master/thirdparty/yeelight)


## Docker

### Dockerfile:

```
FROM python:2.7

WORKDIR /yuanlaiwangluo

RUN git clone https://github.com/ihuanglei/ylauto.git auto

EXPOSE 8866

ENTRYPOINT ["python", "./auto/runner.py"]

```

```
docker build -t ylauto .
```

```
docker run -it ylauto -p 8866:8866
```


[YeelightImg]:https://www.yeelight.com/yeelight201703/i/image/newindex/logo.svg

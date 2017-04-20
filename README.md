## 智能服务器框架

### 使用http协议

```bash
CMD * HTTP/1.1
Method:命令
Location:地址及端口
Param:参数(JSON字符串)
```

启动服务

```bash
runner.py 
```

## 当前实现的智能设备

* [Yeelight](https://github.com/ihuanglei/ylauto/tree/master/thirdparty/yeelight)


## Docker

### Dockerfile:

```bash
FROM python:2.7

WORKDIR /yuanlaiwangluo

RUN git clone https://github.com/ihuanglei/ylauto.git auto

EXPOSE 8866

ENTRYPOINT ["python", "./auto/runner.py"]

```

```bash
docker build -t ylauto .
```

```bash
docker run -it ylauto -p 8866:8866
```


[YeelightImg]:https://www.yeelight.com/yeelight201703/i/image/newindex/logo.svg

# 测试环境
## Master 设备端
* 使用 [KVS WebRTC SDK C](https://github.com/awslabs/amazon-kinesis-video-streams-webrtc-sdk-c) 
* 日志等级需要调整到VERBOSE或DEBUG:
```
export AWS_KVS_LOG_LEVEL = 1
```
* 设置环境变量, 把日志打印到文件:
```
export AWS_ENABLE_FILE_LOGGING=TRUE
```
## Viewer 应用端/移动端
* 使用 [KVS Test Page](https://awslabs.github.io/amazon-kinesis-video-streams-webrtc-sdk-js/examples/index.html)
* 日志等级选择Debug

# 使用说明
* 把SDK自动生成的日志文件(以kvsFileLog开头), 全部复制到**logs**文件夹
* 运行Python文件即可:
```
python3 webrtcLogInsights.py
```
* 运行结束会生成一个xlsx文件，名称以webrtcTs开头.
* 经Python3.8/3.11测试验证通过
* 运行依赖库请使用pip提前安装: glob, xlsxwriter, re, json, datetime
``` 
python3 -m pip install xlsxwriter
```

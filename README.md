### 背景
 - jmeter生成api报告后，为了方便开发人员跟踪调试错误接口，故搭建jtl部署到swagger平台。
 
### 作用
 - 开发人员可以根据转换后的swagger，一键执行错误接口，进行重新问题。
 
 1. 在生成jtl文件前，我们需要对jmeter系统文件user.properties进行设置。
  jmeter.save.saveservice.output_format=xml
  jmeter.save.saveservice.response_data=true
  jmeter.save.saveservice.samplerData=true
  jmeter.save.saveservice.requestHeaders=true
  jmeter.save.saveservice.url=true
  jmeter.save.saveservice.responseHeaders=true
  jmeter.save.saveservice.thread_name=true
  jmeter.save.saveservice.response_data.on_error=true

2. 调用脚本，会在当前目录下生成swagger.json文件
>>python get_swagger.py

3. 将swagger.json文件导入swagger-ui平台。

详细说明：https://testerhome.com/topics/21123

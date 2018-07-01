# Stage3
代码开发阶段
## 框架　　
后端使用flask框架进行修改  
文件索引如下：　　
- msg  *//声明消息格式*　　　  
- scripts *//主要代码开发区　,也就是flask框架改编的地方*　　  
  - \_\_pycache\_\_  
  - static  
  - templates  
  - other files, such as defining ROS nodes  
- include *//自动生成*  
- src     *//自动生成*
- CMakeLists.txt
- package.xml
- README.md
## url设计规范

### HTTP状态码
| 状态码 | 状态码英文名称 | 中文描述 |
| ------ | -------------- | -------- |
| 200 |	OK |	请求成功。一般用于GET与POST请求 |
| 201 |	Created |	已创建。成功请求并创建了新的资源 |
| 204 |	No Content |	无内容。服务器成功处理，但未返回内容。在未更新网页的情况下，可确保浏览器继续显示当前文档 |
| 400 |	Bad Request |	客户端请求的语法错误，服务器无法理解 |
| 401 |	Unauthorized |	请求要求用户的身份认证 |
| 403 |	Forbidden |	服务器理解请求客户端的请求，但是拒绝执行此请求 |
| 404 |	Not Found |	服务器无法根据客户端的请求找到资源（网页）。通过此代码，网站设计人员可设置"您所请求的资源无法找到"的个性页面 |
| 408 |	Request Time-out |	服务器等待客户端发送的请求时间过长，超时 |
| 414 |	Request-URI Too Large |	请求的URI过长（URI通常为网址），服务器无法处理 |
| 500 |	Internal Server Error |	服务器内部错误，无法完成请求 |

### GET，DELETE，PUT和POST的典型用法
| 重要方法 | 典型用法| code |安全 | 幂等 |
| -------- | ---------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ---- | ---- |
| GET      | 1. 获取表示; 2. 变更时获取表示（缓存| 200，204，301，303，304，400，404，406，500，503           | 是   | 是   |
| DELETE   | 删除资源| 200，301,303，400，404，409，500，509                      | 否   | 是   |
| PUT      | 1. 用客户端管理的实例号创建一个资源; 2. 通过替换的方式更新资源; 3. 如果未被修改，则更新资源（乐观锁）| 200，201，301，303，400，404，406，409，412，415，500，503 | 否   | 是|
| POST     | 1. 使用服务端管理的（自动产生）的实例号创建资源; 2. 创建子资源; 3. 部分更新资源; 4. 如果没有被修改，则不过更新资源（乐观锁） | 200，201,202,301,303，400,404,406,406,412,415，500,503     | 否   | 否   |

### PUT 和 POST的区别
对于一组资源的URI,如http://example.com/resources/， PUT方法的作用是使用给定的一组资源替换当前整组资源，而POST方法的作用是在本组资源中创建/追加一个新的资源。该操作往往返回新资源的URL。对于一个特定资源的URI，如http://example.com/resources/1， PUT方法的作用是替换/创建指定的资源,并将其追加到相应的资源组中，而POST方法的作用是把指定的资源当做一个资源组，并在其下创建/追加一个新的元素，使其隶属于当前资源。

### Request HTTP方法
* index/          GET
* command/        GET
  * put/          GET
    * upload/     POST
  * change/       GET
    * upload/     PUT
  * show/         GET
  * successed/    GET
  * failed/       GET

### Response
1. Response可以直接返回数据如以下所示：

2. HTTP方法处理资源成功返回的数据格式:

| HTTP方法 | Response 格式  |
| -------- | -------------- |
| GET      | 单个对象、集合 |
| POST     | 新增成功的对象 |
| PUT      | 更新成功的对象 |
| DELETE   | 空           |

## 后续等框架修改好后在继续更新

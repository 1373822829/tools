import xml.etree.ElementTree as ET
path = r'C:\Users\Administrator\Desktop\test.xml' #jmeter报告jtl文件jtl文件路径 
tree = ET.parse(path)
root = tree.getroot()
data = {}
swagger_json = {}
swagger_json.setdefault("swagger", "2.0")
swagger_json.setdefault("info", {"version": "1.0", "title": "jmeter测试报告"})
swagger_json.setdefault("tags", [{"name": "visual-controller-fail", "description": "【Jmeter Test Result】 FAILED"},{"name": "visual-controller-pass", "description": "【Jmeter Test Result】 PASS"}])
swagger_json.setdefault("schemes", ["http"])
paths = {}
definitions = {}
httpSamples = root.findall("httpSample")
for i in range(httpSamples.__len__()):
    httpSample = httpSamples[i]
    hattribute = httpSample.attrib
    summary = hattribute.get("lb")
    status = hattribute.get("s")
    rc = hattribute.get("rc")
    if "JDBC" in summary:
        continue
    print(httpSample.findall("method"))
    method = httpSample.findall("method")[0].text
    rcode = hattribute.get("rc")
    header = httpSample.findall("requestHeader")[0].text
    queryString = httpSample.findall("queryString")[0].text
    headers = {}
    for h in header.split("\n"):
        if h != '':
            headers.setdefault(h.split(": ")[0], h.split(": ")[1])
    url = str(httpSample.findall("java.net.URL")[0].text).split(headers.get("Host"))[1]
    model = url.split("/")[-1]
    definition_name = model[0].upper()+model[1:]
    swagger_json.setdefault("host", headers.get("Host"))
    parameters = []
    token = headers.get("Authorization")
    if queryString is not None:
        try:
            body = json.loads(queryString)
            switch = {
                str:"string",
                int:"integer($int32)",
                float:"double",
                dict:"map",
                list:"list",
                tuple:"array",
                bool:"boolean"
            }
 
 
            parameters.append({"in":"header","name":"Authorization","default":token,"required":True,"type":"string"})
            parameters.append({"in":"body","name":model,"description":model,"required":True,"schema":{"$ref":'#/definitions/'+definition_name}})
            properties = {}
            for key, value in body.items():
                try:
                    tp = switch[type(value)]
                except KeyError as e:
                    tp = "object"
 
                properties.setdefault(key,{"type":tp,"example":value})
            definitions.setdefault(definition_name,{"type": "object", "properties": properties, "title": definition_name})
 
        except Exception as e:
            res = "{\""+ str(queryString).replace("=","\":\"").replace("&","\",\"")+"\"}"
            body = json.loads(res)
            for key, value in body.items():
                if value != '':
                    parameters.append(
                        {"in": "query", "name": key, "default": value, "required": True, "type": "string"})
                else:
                    parameters.append(
                        {"in": "query", "name": key, "default": value, "required": False, "type": "string"})
 
    else:
        parameters.append(
            {"in": "header", "name": "Authorization", "default": token, "required": True, "type": "string"})
        body = {}
    if status == "true":
        paths.setdefault(url, {
            str(method).lower(): {"responses": {rc: {"description": "OK"}}, "tags": ["visual-controller-pass"],
                                  "summary": summary, "description": "",
                                  "consumes": ["application/json","application/x-www-form-urlencoded; charset=UTF-8"],
                                  "produces": ["application/json"],
                                  "parameters": parameters}})
    if status == "false":
        response_data = httpSample.findall("responseData")[0].text
        paths.setdefault(url, {
            str(method).lower(): {"responses": {rc: {"description": response_data}}, "tags": ["visual-controller-fail"],
                                  "summary": summary, "description": "",
                                  "consumes": ["application/json",
                                               "application/x-www-form-urlencoded; charset=UTF-8"],
                                  "produces": ["application/json"],
                                  "parameters": parameters}})
 
swagger_json.setdefault("definitions",definitions)
 
swagger_json.setdefault("paths",paths)
print(swagger_json)
data = json.dumps(swagger_json)
with open("jmeter.json","w",encoding="utf8") as file:
    file.writelines(data)

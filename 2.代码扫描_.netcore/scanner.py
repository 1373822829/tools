# _*_coding:utf-8 _*_
# @Software : PyCharm
# @File : poxy.py
# @Author : wangjie
# @Created Time : 2022.04.12   13:41
import datetime
import time
from datetime import date
import re

from git import Repo,Actor
from git.repo.fun import is_git_dir
import taichi as ti
ti.init()

ti.field(ti.i32, shape=(4, 8))

import git
import os

import os




def get_file(dir):
    """
    获取指定目录下文件
    :param dir:
    :return:
    """
    path = []
    if os.path.isdir(dir):
        for root,dirs,files in os.walk(dir):
            for file in files:
                p = os.path.join(root, file)
                file_type_partten = 'Models|Module|DTO|Dto|Service|Controller'
                # 跳过一些不需要扫描的文件
                if re.findall(file_type_partten, file).__len__() < 1:
                    continue
                if p.endswith('cs') and ('debug' not in p.lower()):
                    path.append(p)
    return path


def get_method(path):
    """
    :param path :文件路径
    :return: [] apilist
    """
    api_methods = []
    with open(path, 'r+', encoding='utf-8',errors='ignore') as f:
        content = f.read()
        content = re.subn("\n\s+//.*","",content)[0]
        methods = re.findall('[public,private] static.*\s+([A-Za-z]+)\(|[public,private] static.*\s+([A-Za-z]+)<[^>]*>\(|Task<.*>\s+([A-Za-z]+)\(|Task<.*>\s+([A-Za-z]+)<[^>]*>\(|[private,protected,public].*async\s+Task.*[^,]\s+([A-Za-z]+)\s*\(|[private,protected,public].*async\s+Task.*\s+([A-Za-z]+)<[^>]*>\(', content)
        # print(methods)
        for method in methods:
            method = list(set(method))
            for m in method:
                if m == '':
                    continue
                api_methods.append(m.strip())

    return list(set(api_methods))

def get_class(path):
    """
    根据文件获取文件所有类名
    :param path: 文件路径
    :return: [] classname_list
    """
    cname_list = []
    if not os.path.exists(path):
        return cname_list
    with open(path, 'r+', encoding='utf-8', errors='ignore') as f:
        item = f.read()
    results = re.findall('public\s+class\s+.*\n|public\s+static\s+class\s+.*\n', item)
    for result in results:
        if (result.__len__() > 0) and (':' in result) and (' static ' not in result):
            cname = re.findall('public\s+class\s+.*\:\s+(.*)', result)[0]
            if ',' in cname:
                cname = cname.split(',')
                cname_list = cname_list + cname
            else:
                cname_list.append(cname)
        if (result.__len__() > 0) and (':' not in result) and (' static ' not in result):
            cname_list.append(re.findall('public\s+class\s+([a-z|A-Z]+)', result)[0])
        if (result.__len__() > 0) and (' static ' in result):
            cname_list.append(re.findall('public\s+static\s+class\s+([a-z|A-Z]+)', result)[0])

    return list(set(cname_list))

# 判断方法是否有效
def isValid(s):
    """
    :type s: str
    :rtype: bool
    """
    while '{}' in s or '()' in s or '[]' in s:
        s = s.replace('{}', '')
        s = s.replace('[]', '')
        s = s.replace('()', '')
    return s == ''


def get_code(path,api,isline=False):
    """
    获取API方法代码片段
    :param path:指定文件路径
    :param api: api方法名称
    :param isline: 是否返回代码块的启始行号
    :return: str api方法代码片段
    """
    count = 0
    code = ''  # API方法代码片段
    str = ''  # 截取API代码片段，所有{}
    line = 0  # 初始行号
    line_start = 0 # 代码块开始行号
    line_end = 0 # 代码块结束行号
    with open(path, 'r+', encoding='utf-8') as file:
        for item in file:
            line += 1
            # 去除注释
            if item.replace(' ','').startswith("//") or item.replace(' ','').startswith("///"):
                continue
            if (re.findall('[^a-zA-Z]%s[^a-zA-Z]'%api,item).__len__()>0) and (item.strip().startswith('public') or item.strip().startswith('private')):
                line_start = line
                # 截取方法含有‘{’，‘}’用来校验方法的结尾
                str += ''.join(re.findall('\{|\}', item))
                code += item
                count += 1
                continue
            if count > 0:
                str += ''.join(re.findall('\{|\}', item))
                code += item

            # 如果api代码块没有{}，作为开始和结束标志
            # 如public async Task<IActionResult> QueryCustomerBaseOption([FromQuery] QueryCustomerBaseOptionRequest request)
            #             => await OkListAsync(await _customerBaseOptionService.QueryCustomerBaseOption(request));
            if count > 0 and ('=> await' in item):
                str += ''.join(re.findall('\(|\)', item))
                code += item


            # 校验str有效性，如果有效则说明API方法读取到了结尾
            if str != '' and isValid(str):
                line_end = line
                break
    if isline:
        return code,line_start,line_end
    else:
        return code



def get_file_path(srcpath,using):
    """
    获取using下所有，文件后缀为cs路径
    :param path type str src文件路径
    :param using type [] 文件引用类
    :return: 文件路径集合 []
    """
    resfile = []
    # 获取src当前目录下文件或目录
    files = get_file(srcpath)
    for file in files:
        format_file = file.replace(srcpath+"\\",'').replace('\\','.')
        for u in using:
            if u in format_file:
                resfile.append(file)

    return resfile







def get_change_api(change_file_path,side_api,projectcollention):
    """
    获取变动的api
    :param change_file_path: 修改的文件名称
    :param api: 修改的api
    :param projectcollention: 项目解析集合
    :return: []
    """
    change_apis = []
    for project in projectcollention:
        apis = project.get('apis')
        for api in apis:
            methods = api.get('methods')
            for method in methods:
                if change_file_path in method.get('methodfile') and side_api in method.get('method'):
                    filepath = project.get('path')
                    apiname = api.get('apiname')
                    change_apis.append({'path':filepath,'apiname':apiname})

    return change_apis



class MyGit(object):
    """
    git仓库管理
    """
    def __init__(self, local_path, repo_url, branch='master'):
        self.local_path = local_path
        self.repo_url = repo_url
        self.repo = None
        self.initial(repo_url, branch)
        self.change_api_infos = []
        self.controller_apis = []

    def initial(self, repo_url, branch):
        """
        初始化git仓库
        :param repo_url:
        :param branch:
        :return:
        """
        if not os.path.exists(self.local_path):
            os.makedirs(self.local_path)

        git_local_path = os.path.join(self.local_path, '.git')
        if not is_git_dir(git_local_path):
            self.repo = Repo.clone_from(repo_url, to_path=self.local_path, branch=branch)
        else:
            self.repo = Repo(self.local_path)

    def pull(self):
        """
        从线上拉最新代码
        :return:
        """
        self.repo.git.pull()

    def branches(self):
        """
        获取所有分支
        :return:
        """
        branches = self.repo.remote().refs
        return [item.remote_head for item in branches if item.remote_head not in ['HEAD', ]]

    def commits(self):
        """
        获取所有提交记录
        :return:
        """
        commit_log = self.repo.git.log('--pretty={"commit":"%h","author":"%an","summary":"%s","date":"%cd"}',
                                       max_count=50,
                                       date='format:%Y-%m-%d %H:%M')
        log_list = commit_log.split("\n")
        return [eval(item) for item in log_list]

    def tags(self):
        """
        获取所有tag
        :return:
        """
        return [tag.name for tag in self.repo.tags]

    def change_to_branch(self, branch):
        """
        切换分支
        :param branch:
        :return:
        """
        self.repo.git.checkout(branch)

    def change_to_commit(self, branch, commit):
        """
        切换commit
        :param branch:
        :param commit:
        :return:
        """
        self.change_to_branch(branch=branch)
        self.repo.git.reset('--hard', commit)

    def change_to_tag(self, tag):
        """
        切换tag
        :param tag:
        :return:
        """
        self.repo.git.checkout(tag)


    def diff_files(self,source_branch,target_branch):
        """
        获取变更文件
        :param source_branch: 源分支 比如：source分支：develop合并taget分支：master
        :param taget_branch: yao
        :return: list 返回文件列表
        """

        self.change_to_branch(target_branch)
        self.pull()
        self.change_to_branch(source_branch)
        self.pull()
        return self.repo.git.diff(target_branch,source_branch,'--name-only')

    def diff_file_code(self,source_branch,target_branch,file):
        """
        根据文件获取变更内容
        :param source_branch: 源分支
        :param taget_branch: 目标分支
        :param file: 文件路径
        :return: string
        """
        self.change_to_branch(target_branch)
        self.pull()
        self.change_to_branch(source_branch)
        self.pull()
        if not os.path.exists(os.path.join(self.local_path, file)):
            return ""
        print(file)
        return self.repo.git.diff("--unified=0",target_branch,source_branch,file)

    def get_change_line(self,source_branch,target_branch):
        """获取变更代码行数"""
        self.change_to_branch(target_branch)
        self.pull()
        self.change_to_branch(source_branch)
        self.pull()
        text = self.repo.git.diff(target_branch,source_branch,'--stat')
        commit_records = self.repo.git.log('%s..%s'%(target_branch,source_branch))
        commit_num = str(commit_records).count('commit')
        if text is None or text == "":
            return None
        else:
            return 'commits %s' % commit_num + ',' + text.split('\n')[-1]


    def get_controller_api(self,path,api):
        """
        根据文件和api查找调用该api的方法名称，然后根据找到的方法名称和文件，再次向下查找，止到找到controller层
        :param path: 文件路径
        :param api: 方法名称
        :return: [{"controller_path":"",apis:[]}]
        """


        # 1.匹配该文件类名称，如果该类继承了其他父类，则取父类名称
        class_name = get_class(path)

        project_path = os.path.join(path.split("src")[0], 'src')

        # 获取项目目录下所有文件
        files = get_file(project_path)
        # 项目下全局查找引用class_name，排除path
        for file in files:
            apis = ""
            with open(file, 'r+', encoding='utf8') as f:
                content = f.read()
                # 去除注释
                content = re.sub('\s+//.*\n','\n',content)

                for cname in class_name:
                    partten = '[^a-zA-Z]%s[^a-zA-Z]' % cname.replace(' ', '')

                    # 获取class变量，比如  private readonly IProductManageService _productManageService; class_variable = _productManageService
                    class_variable_partten = 'readonly\s+%s\s+(.*?);' % cname.replace(' ', '')
                    class_variable_result = re.findall(class_variable_partten, content)
                    if class_variable_result.__len__()>0:
                        class_variable = class_variable_result[0]
                    else:
                        class_variable = None
                    result = re.findall(partten, content)
                    if result.__len__() > 0:
                        if (('Models' in path) or ('Module' in path) or ('DTO' in path) or (
                                'Dto' in path)) and api in content:
                            #     apis = get_method(file)
                            #     code_partten = '[new\s+,\(,\(\s+,\<,\<\s+]%s[\s+,\),\)\s+,\>,\>\s+,\\n]' % api.replace(' ', '')
                            #     for apiinfo in apis:
                            #         code, strat_line, end_line = get_code(file, apiinfo, True)
                            #         code_res = re.findall(code_partten,code)
                            #         if code_res.__len__() > 0:
                            #             print("api:",api,path,file,apiinfo)
                            #             if 'Controller.cs' in file:
                            #                 controller_apis.append({file:apiinfo})
                            #                 continue
                            #             elif 'Service.cs' in file:
                            #                 get_controller_api(file, apiinfo)
                            #             else:
                            #                 continue
                            continue

                        # 如果当前文件，调用该方法，需要匹配到调用方法
                        if file == path:
                            api_partten = '[^a-zA-Z]%s[^a-zA-Z]' % api.replace(' ', '')
                            api_result = re.findall(api_partten, content)
                            # 如果找到两个，则说明该文件下存在其他方法调用API
                            if api_result.__len__() > 1:
                                if apis == "":
                                    apis = get_method(file)
                                for apiinfo in apis:
                                    code, strat_line, end_line = get_code(file, apiinfo, True)
                                    if re.findall(api_partten, code).__len__() > 0:
                                        if apiinfo == api:
                                            continue
                                        if 'Controller.cs' in file:
                                            self.controller_apis.append({file: apiinfo})
                                            continue
                                        else:
                                            self.get_controller_api(file, apiinfo)
                        if not class_variable:
                            continue

                        if ('%s.%s(' % (class_variable, api) in content) or ('%s.%s (' % (class_variable, api) in content) or ('%s.%s,' % (class_variable, api) in content):
                            if apis == "":
                                apis = get_method(file)
                            for apiinfo in apis:
                                code, strat_line, end_line = get_code(file, apiinfo, True)
                                if ('%s.%s(' % (class_variable, api) in code) or ('%s.%s (' % (class_variable, api) in code) or ('%s.%s,' % (class_variable, api) in code):
                                    if 'Controller.cs' in file:
                                        self.controller_apis.append({file: apiinfo})
                                        continue
                                    else:
                                        self.get_controller_api(file, apiinfo)

    # 获取变更api
    def get_change_apis(self,source_branch: str,target_branch: str,change_files: str) -> list:
        """
        根据文件列表获取所有变更api
        :param change_files: 变更文件
        :return: list
        """
        for s in change_files:
            filepath = os.path.join(self.local_path,s.replace('/','\\'))
            # 当文件为单元测试文件，跳过
            if ('Test' in filepath) or ('.json' in filepath) or ('DTO' in filepath):
                continue
            # print("变动文件：",filepath)
            change_api = {}
            change_api['filepath'] = filepath
            change_api['apis'] = []
            # 变更内容
            change_content = self.diff_file_code(source_branch,target_branch,s)

            print("change_content:",change_content)


            # 匹配新增代码的开始和结束的行数
            change_lines = re.findall("@@ -[0-9]+[,[0-9]+]? \+([0-9]+[,[0-9]+]?)(?= @@)",change_content)

            # 对变更内容格式化，然后和代码块code进行比对，匹配到对应的api
            # format_change_contents = [re.subn("-\s{3,}.*\n|-\n","",data)[0].replace('+\n','\n').replace('+  ','') for data in re.split('@@.*\n',change_content)[1:] ]
            if  ('Models' in filepath) or ('Module' in filepath) or ('DTO' in filepath):
                change_api['apis'] = get_class(filepath)
                self.change_api_infos.append(change_api)
                continue

            # 获取文件下所有方法及代码块
            apis = get_method(filepath)
            for api in apis:

                code,start_line,end_line = get_code(filepath,api,True)

                # 有2种情况，1.变更代码的开始行or结束行在code的起始行范围内；
                # 2.开始行和结束行都不在code的起始行范围内，但code开始行>=变更代码开始行并且code结束行<=变更代码结束行，如果这两种情况不满足则不取API

                for change_line in change_lines:
                    if ',' in change_line: # 变更代码大于1行
                        change_start_line = int(change_line.split(',')[0])
                        change_end_line = change_start_line+int(change_line.split(',')[1])
                    else:  # 变更代码就1行
                        change_start_line = int(change_line)
                        change_end_line = change_start_line
                    if start_line<=change_start_line<=end_line or start_line<=change_end_line<=end_line:
                        change_api['apis'].append(api)
                    elif start_line>=change_start_line and end_line<=change_end_line:
                        change_api['apis'].append(api)
                    else:
                        continue

            if 'Controller.cs' in filepath:
                self.controller_apis.append({filepath:list(set(change_api['apis']))})
                continue

            change_api['apis'] = list(set(change_api['apis']))
            self.change_api_infos.append(change_api)

        # change_api_infos = [{'filepath': 'F:\\福禄网络\\FP\\sup-fp-order-interface\\src\\Sup.Fp.Order.Interface.Domain\\Services\\ProductService.cs', 'apis': ['GetProductPoolProductList']}]
        for change_api in self.change_api_infos:
            for api in change_api['apis']:
                self.get_controller_api(change_api['filepath'],api)

        return self.controller_apis





if __name__ == '__main__':
    local_path = 'E:\福禄网络\FP\sup-fp-merchant-business'
    repo_url = ""
    source_branch = "develop"
    target_branch = "beta/20221118/商品密价优化"
    mgit = MyGit(local_path, repo_url)
    change_files = mgit.diff_files(source_branch, target_branch)
    # print(change_files)
    if change_files != '':
        change_files = change_files.split('\n')
        apis = mgit.get_change_apis(source_branch, target_branch, change_files)
        print(apis)




    # get_method("E:\福禄网络\FP\sup-fp-message-interface\src\Sup.Fp.Message.Interface.Domain\Services\Extensions\SupProductExtendService.cs")








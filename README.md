# ISE 536 Term Project

## Update

完成了数据读取的接口。

## 部署项目

克隆项目到本地，在指定目录下打开命令行，输入以下命令：
```
git clone https://github.com/Jziumo/linear_programming_term_project.git
```

在根目录的命令行下，激活虚拟环境：
```
.\venv\Scripts\Activate.ps1
```

安装 `requirements.txt` 中的依赖：
```
py -m pip install -r requirements.txt
```

## 修改项目并上传

`venv/Lib` 目录下的文件不用传上来，不过已经写在 `.gitignore` 里了，大概 `git add ./` 没有问题8

```
git add ./
git commit -m "message"
git push origin master
```

如果不上传到主分支 `master`，比如创建分支名为 `m2`：
```
git checkout -b m2
```

如果要切换回来：
```
git checkout -
```

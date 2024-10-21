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

确保已经激活虚拟环境噢，即命令行开头是 `(venv)` 而不是 `(base)`. 

安装 `requirements.txt` 中的依赖：
```
py -m pip install -r requirements.txt
```

## 修改项目并上传

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

### 更新 `requirements.txt`

如果有在虚拟环境里安装新的包，不用把 `./venv/` 文件夹里的文件传上来（我已经写在了 `.gitignore` 里，所以应该不会传上来），取而代之可以更新一下 `requirements.txt` 文件。

确保已经激活虚拟环境噢，即命令行开头是 `(venv)` 而不是 `(base)`. 

```
pip freeze > requirements.txt
```
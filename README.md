# envinit

`envinit` 是一个用于管理 Windows 开发/运行环境的工具，基于 `prompt_toolkit` 实现了一个交互式命令行界面。该工具提供了一系列内建命令，并支持用户自定义命令。

## 安装

确保你已经安装了 Python 3.11，并且安装了 `pdm` 包管理工具。

1. 克隆项目到本地：

   ```sh
   $ git clone https://github.com/ZhuchenZhong/envinit.git
   $ cd envinit
   ```
2. 使用 `pdm` 安装依赖：

   ```sh
   $ pdm install
   ```


## Develop Part

##### BREAKING CHANGES

重构代码，把cmdcli作为单独模块处理

<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-group-file-admin
_✨ 简易的群文件管理 ✨_

</div>

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-group-file-admin

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-group-file-admin
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-group-file-admin
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-group-file-admin
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-group-file-admin
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_group_file_admin"]

</details>

## ⚙️ 配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| fa_del_model | 否 | 1 | 默认删除根目录文件模式（更多模式见下表） |
| fa_expand_name | 否 | 无 | 文件扩展名 |

| 值 | 说明 |
|:----:|:----:|
| 1 | 删除根目录文件 |
| 2 | 根据`fa_expand_name`配置项删除文件 |
| 3 | 一键清空群文件 |


## 🎉 使用
### 指令表
**注意: 所有指令均需要以`/`开头**
| 指令 | 权限 | 需要@ | 范围 |
|:-----:|:----:|:----:|:----:|
| 清理群文件 | 主人 | 否 | 群聊 |
| 文件整理 | 主人 | 否 | 群聊 |
| 备份群文件 | 主人 | 否 | 群聊 |
| 恢复群文件 | 主人 | 否 | 群聊 |
| 清理本地文件 | 主人 | 否 | 群聊 |

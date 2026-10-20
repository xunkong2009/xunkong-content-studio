# 寻空内容创作工具箱

供获授权成员安装的私有 Codex 插件源，三个插件可分别安装。

| 插件 | 标识 | 能力 |
| --- | --- | --- |
| 短视频全流程工作台 | `shortvideo-studio` | 脚本、封面提示词、配图、Remotion 动效、素材搜索与下载、口播剪辑 |
| 商业公众号工作室 | `deep-biz-wechat-studio` | 选题、调研、大纲、长文、审校、包装、公众号 HTML |
| 新能源公众号工作室 | `deep-nev-wechat-studio` | 新能源产业选题、调研、大纲、成文、审校与包装 |

分享版不绑定发布者的 IMA、照片或本地目录。安装后可直接使用随包写作规则，云端语料、真人形象和媒体工具按需配置。

## 安装

先由仓库所有者在 GitHub 仓库 Settings → Collaborators 中邀请接收者，接收者接受邀请并用自己的 GitHub 账号登录本机 Git 工具。只有获授权账号能读取此私有仓库。

在终端运行：

```bash
codex plugin marketplace add xunkong2009/xunkong-content-studio
```

然后在桌面端插件目录选择“寻空内容创作工具箱”源，安装需要的插件。支持插件命令的 Codex CLI 也可运行：

```bash
codex plugin add shortvideo-studio@xunkong-content-studio
codex plugin add deep-biz-wechat-studio@xunkong-content-studio
codex plugin add deep-nev-wechat-studio@xunkong-content-studio
```

若当前客户端尚未提供对应安装界面，先更新客户端；不同版本的入口可能不同。需要通过本机 Git 已有的 HTTPS 或 SSH 登录方式访问私有仓库，不要把令牌写进仓库地址。添加源时遇到 Repository not found，先确认邀请已接受、当前 Git 账号有读取权限。

也可以手动克隆后添加本地源：

```bash
git clone git@github.com:xunkong2009/xunkong-content-studio.git
codex plugin marketplace add ./xunkong-content-studio
```

## 使用示例

- 短视频：从这个选题写一条 2–3 分钟商业口播脚本，先只交付脚本。
- 商业公众号：围绕这个品牌变化完成调研和大纲，标清事实与推断。
- 新能源：分析这家车企的补能策略，先给研究简报和文章框架。

已有材料和已确认方向直接沿用；只请求某一阶段时不会强制启动全流程。

## 可选配置

参考 [安装与配置](docs/setup.md)。将任一插件的 `config.example.json` 复制为当前工作项目的 `.xunkong-studio/config.json`，按自己的需要填写。不要修改安装目录。

- 不配置 IMA 也能写作；配置后使用安装者自己的参考语料。
- 真人封面需要安装者自己的主播参考图。
- 图片生成依赖当前客户端可用的图片生成能力。
- Remotion、下载、转写和剪辑按需安装本机依赖。

## 更新

```bash
codex plugin marketplace upgrade xunkong-content-studio
```

在插件目录检查并应用插件更新；客户端提示需要重启时重新打开。更新不会覆盖项目内的个人配置。只添加 marketplace 源不等于已经完成所有插件及其媒体依赖的安装。

## 包含与排除

包含流程、风格规则、参考文档、图标、Remotion 模板和媒体处理脚本。不包含发布者私人文章全文、云端笔记定位、账号凭证、真人照片、用户视频、下载成果、字体、平台专用二进制或 node_modules。

官方格式与安装文档：https://developers.openai.com/plugins/build/plugins

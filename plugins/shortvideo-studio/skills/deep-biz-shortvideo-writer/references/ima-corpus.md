# IMA 参考语料（分享版）

IMA 是可选语料来源。先读当前项目 `.xunkong-studio/config.json` 的 `corpus` 配置；未配置时直接使用随包 `style-layer.md`，不要求用户为普通写作配置 IMA。

## 配置与工具

- `provider` 设为 `ima` 后，使用安装者自己的 IMA 账号与知识库。
- 从 `ima_skill_dir` 或当前可用 Skills 中定位官方 `ima-skill`；先读取其 `SKILL.md` 和 `knowledge-base/SKILL.md`。没有安装时说明此依赖，继续不依赖 IMA 的工作。官方入口为 https://ima.qq.com/agent-interface 。
- 公众号使用 `knowledge_base_name`、`article_folder_path`、`commission_folder_path`；短视频使用 `script_folder_path`。路径均是从知识库根目录开始的文件夹名称数组。
- 凭证由 IMA Skill 在安装者本机管理，不写进插件、项目配置或 Git 仓库。不共享发布者的密钥、语料库或任何媒体 ID。

## 读取正文

1. 通过 `search_knowledge_base` 定位用户配置的知识库，再用 `get_knowledge_list` 按名称逐级核对目录与面包屑。存在多个同名结果时询问当前用户，不能猜测。
2. 首次列表 `cursor=""`，随后使用 `next_cursor` 翻页。按用户请求选择代表样本，不能把浏览标题当成已读正文。年度、月度脚本文件按其中的标题边界选择具体脚本。
3. 对选中条目调用 `get_media_info`。笔记类型 `media_type=11` 且有 `notebook_ext_info.notebook_id` 时，先加载 notes 模块，然后用该 ID 调用 `get_doc_content`，`target_content_format=0`。其他可读文件使用 API 返回的 `url_info.url` 和 `headers` 获取原文。
4. 检查退出码、业务 `code`、HTTP 状态和正文完整性。空正文、错误文本、登录页和仅标题返回不算有效样本。分析时可以略过 Markdown 内嵌图片和 Base64。
5. 记录实际读取范围和失败项。IMA 不可用时停止依赖它的刷新，普通写作继续沿用既有规则并说明未完成刷新。不要擅自调用其他账号或其他知识库。

本流程仅用于读取参考，不创建、追加或迁移云端笔记。旧样本中的事实、数字和引用归属须为当前任务独立核验。

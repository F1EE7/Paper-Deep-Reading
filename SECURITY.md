# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| 0.1.x | ✅ |

## Reporting a Vulnerability

本仓库是纯 Markdown 技能与文档项目，不含可执行服务、网络端点或依赖链（`scripts/check_skill.py` 仅用 Python 标准库）。

如果你发现以下问题，请[开一个 GitHub Issue](https://github.com/F1EE7/Paper-Deep-Reading/issues) 并标注 `security`：

- 技能内容可能诱导模型产生危险行为（如绕过诚实边界、编造内容、泄露记忆文件中的信息）；
- 验证脚本或 CI 配置可被注入/绕过；
- 文档中的命令在特定环境下有破坏性。

不涉及秘密泄露的场景（无密钥、无后端），一般安全问题请在 Issue 中直接描述即可；敏感细节可先用 Issue 私信作者。

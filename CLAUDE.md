# 情感沟通 Agent

基于 LLM 的单文件 HTML 情感沟通助手。浏览器中打开即用，无需安装。

## 技术栈

- 纯静态 HTML/CSS/JS，零依赖，`file://` 打开即用
- LLM API：豆包（火山引擎），OpenAI 兼容格式，可切换 DeepSeek
- 存储：localStorage + JSON 文件导出/导入
- 深色紫红主题（#08090d / #b98eff / #e85d75）

## 项目结构

```
index.html              — 主程序（单文件，CSS/JS 内联）
CLAUDE.md               — 本文件
```

## 设计文档

参见 `2026-06-30-emotional-agent-design.md`

## 核心特性

- 多会话管理（新建/切换/删除/重命名）
- 流式输出（SSE）
- 领域预检：非情感问题本地拒绝，0 token 消耗
- 上下文压缩：超过 20 轮自动压缩早期对话为摘要
- 安全护栏：自杀/家暴等危机场景自动切换安全响应
- JSON 导出/导入备份

## 开发

直接编辑 `emotional-agent.html`，浏览器打开测试。

## API 配置

默认使用豆包 API，在设置面板（`Ctrl+,`）中配置：
- API Key
- baseURL
- 模型名称
- 温度参数

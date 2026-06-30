<h1 align="center">
  👧🏻 小暖 — 情感沟通助手
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/status-active-brightgreen" alt="Status">
  <img src="https://img.shields.io/github/license/nutshell319/emotional-agent" alt="License">
  <img src="https://img.shields.io/badge/PRs-welcome-purple" alt="PRs">
</p>

<p align="center">
  一个基于 LLM 的情感沟通对话助手。<br>
  倾听你的困扰，理解你的情绪，陪你一起找到答案。
</p>

---

## ✨ 为什么做这个

每个人都会遇到说不清、想不通、放不下的感情困扰。  
朋友可能没空听，家人可能不理解，心理咨询又太贵。

小暖是一个**随时在线**的倾听者——温暖但不说教，专业但不冰冷，隐私完全由你掌控。

---

## 🎯 核心功能

| 功能 | 说明 |
|------|------|
| 💬 **智能对话** | 基于 DeepSeek/豆包等大模型，懂中文、会共情 |
| 👤 **对象画像** | 为每段对话描述你在意的人（MBTI、星座、关系状态），分析更精准 |
| 🛡 **安全护栏** | 自杀/家暴等危机自动触发安全响应，提供专业求助渠道 |
| 🚫 **领域预检** | 非情感问题本地拒绝，0 token 消耗 |
| 🗜 **上下文压缩** | 超过 20 轮对话自动摘要，保留关键信息不丢 |
| 💾 **数据自主** | 所有数据存浏览器 localStorage，你的秘密只有你知道 |
| 📥 **导出导入** | JSON 文件备份，换设备一键恢复 |
| ✏️ **自定义昵称** | 想叫她什么就叫什么 |

---

## 🚀 快速开始

### 在线使用

👉 **[nutshell319.github.io/emotional-agent](https://nutshell319.github.io/emotional-agent/)**

打开即用，无需安装。

### 本地运行

```bash
git clone https://github.com/nutshell319/emotional-agent.git
cd emotional-agent
# 双击 index.html 即可，或用浏览器打开
open index.html
```

### 配置 API

1. 点击右上角 ⚙ 或按 `Ctrl+,` 打开设置
2. 填入 DeepSeek API Key（[获取地址](https://platform.deepseek.com/api_keys)）
3. 默认模型 `deepseek-v4-flash`，支持切换豆包/GPT 等兼容 API

---

## ⌨️ 快捷键

| 快捷键 | 功能 |
|--------|------|
| `Ctrl + N` | 新建对话 |
| `Ctrl + ,` | 打开设置 |
| `Esc` | 关闭面板 |
| `Enter` | 发送消息 |
| `Shift + Enter` | 换行 |

---

## 🧱 技术栈

| 层 | 技术 |
|----|------|
| 前端 | 纯原生 HTML/CSS/JS，零依赖 |
| LLM | DeepSeek / 豆包 / 任意 OpenAI 兼容 API |
| 存储 | localStorage + JSON 文件 |
| 部署 | GitHub Pages |
| 主题 | 深色紫红配色（#08090d / #b98eff / #e85d75） |

---

## 📁 项目结构

```
emotional-agent/
├── index.html              ← 主程序（单文件，CSS/JS 全部内联）
├── README.md               ← 本文件
├── CLAUDE.md               ← AI 辅助开发说明
├── .gitignore
└── docs/superpowers/
    ├── specs/               ← 设计规格
    │   └── 2026-06-30-emotional-agent-design.md
    └── plans/               ← 实施计划
        └── 2026-06-30-emotional-agent-plan.md
```

---

## 🔒 隐私说明

- API Key 仅存在浏览器 localStorage，**不上传任何服务器**
- 所有对话数据存在本地，清除浏览器数据即彻底删除
- 建议定期使用「导出备份」功能保存重要对话
- 使用 GitHub Pages 托管，页面本身是纯静态文件，无后端无数据库

---

## 📄 License

MIT © [nutshell319](https://github.com/nutshell319)

---

<p align="center">
  <sub>感到孤独的时候，记得有小暖在 💜</sub>
</p>

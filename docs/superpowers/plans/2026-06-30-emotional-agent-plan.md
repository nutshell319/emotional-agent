# 情感沟通 Agent 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个单文件 HTML 情感沟通助手，支持多会话管理、流式对话、领域预检、上下文压缩。

**Architecture:** 单文件 `emotional-agent.html`，CSS/JS 内联。7 个 JS 模块（SettingsManager → StorageManager → SafetyGuard → DeepSeekClient → ContextCompressor → ChatManager → UIController）自底向上搭建，最后集成。

**Tech Stack:** 纯原生 HTML/CSS/JS，零依赖。豆包 API（OpenAI 兼容格式）。localStorage + JSON 文件持久化。

---

## 文件结构

```
C:/programs/个人项目/emotional-agent/
├── emotional-agent.html          ← 唯一产出文件（逐步构建）
├── CLAUDE.md
├── .gitignore
├── 2026-06-30-emotional-agent-design.md
└── docs/superpowers/plans/
    └── 2026-06-30-emotional-agent-plan.md  ← 本文件
```

---

### Task 1: 创建 HTML 骨架与 CSS 主题

**Files:**
- Create: `C:/programs/个人项目/emotional-agent/emotional-agent.html`

此任务建立整个应用的外壳。后续所有任务都在此文件上增改。

- [ ] **Step 1: 写入 HTML 骨架**

创建 `emotional-agent.html`，包含完整的 `<style>` 和空的 `<body>` + `<script>` 结构：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>小暖 — 情感沟通助手</title>
<style>
/* ========================================
   CSS Reset & Variables
   ======================================== */
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

:root {
  --bg: #08090d;
  --title: #b98eff;
  --accent: #e85d75;
  --text: #f6f2e8;
  --text-dim: #aaa59a;
  --text-muted: #746f66;
  --card-bg: rgba(255,255,255,0.03);
  --card-border: rgba(255,255,255,0.06);
  --font: "Microsoft YaHei", "PingFang SC", system-ui, sans-serif;
  --sidebar-width: 260px;
  --settings-width: 340px;
}

html, body {
  width: 100%; height: 100%;
  overflow: hidden;
  background: var(--bg);
  color: var(--text);
  font-family: var(--font);
  font-size: 15px;
  line-height: 1.6;
}

/* 背景纹理 */
body::before {
  content: '';
  position: fixed; inset: 0;
  opacity: 0.025;
  pointer-events: none;
  z-index: 0;
  background-image:
    repeating-linear-gradient(0deg, transparent, transparent 49px, rgba(255,255,255,0.03) 50px),
    repeating-linear-gradient(90deg, transparent, transparent 49px, rgba(255,255,255,0.03) 50px);
}

/* ========================================
   Layout Shell
   ======================================== */
#app {
  position: relative;
  width: 100%; height: 100%;
  display: flex;
  z-index: 1;
}

/* ========================================
   Scrollbar
   ======================================== */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.15); }

/* ========================================
   Buttons & Inputs (base)
   ======================================== */
button {
  font-family: inherit;
  cursor: pointer;
  border: none;
  outline: none;
}

input, textarea {
  font-family: inherit;
  outline: none;
  border: none;
}

/* ========================================
   Toast
   ======================================== */
.toast-container {
  position: fixed; top: 20px; right: 20px;
  z-index: 999;
  display: flex; flex-direction: column; gap: 8px;
}
.toast {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 13px;
  color: var(--text);
  animation: toastIn 0.3s ease, toastOut 0.3s ease 2.7s forwards;
  max-width: 360px;
}
.toast.error { background: rgba(232,93,117,0.15); border: 1px solid rgba(232,93,117,0.25); }
.toast.success { background: rgba(76,175,80,0.12); border: 1px solid rgba(76,175,80,0.2); }
.toast.info { background: rgba(185,142,255,0.1); border: 1px solid rgba(185,142,255,0.18); }

@keyframes toastIn { from { opacity: 0; transform: translateX(40px); } to { opacity: 1; transform: translateX(0); } }
@keyframes toastOut { from { opacity: 1; } to { opacity: 0; } }

/* ========================================
   Animations
   ======================================== */
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
</style>
</head>
<body>

<div class="toast-container" id="toastContainer"></div>

<div id="app">
  <!-- Task 7: Sidebar -->
  <!-- Task 7: Chat Area -->
  <!-- Task 10: Settings Drawer -->
</div>

<script>
/* ========================================
   INIT — 页面加载入口（后续任务填充）
   ======================================== */
document.addEventListener('DOMContentLoaded', () => {
  console.log('[小暖] App shell loaded');
});
</script>

</body>
</html>
```

- [ ] **Step 2: 浏览器打开验证**

```bash
start "" "C:/programs/个人项目/emotional-agent/emotional-agent.html"
```

验证：页面显示纯黑背景，console 输出 `[小暖] App shell loaded`，无报错。

- [ ] **Step 3: 提交**

```bash
cd "C:/programs/个人项目/emotional-agent" && git add emotional-agent.html && git commit -m "✨ Task 1: HTML骨架+CSS主题变量+Toast动画"
```

---

### Task 2: SettingsManager + StorageManager

**Files:**
- Modify: `C:/programs/个人项目/emotional-agent/emotional-agent.html` — 在 `<script>` 标签内 INIT 注释前插入

- [ ] **Step 1: 在 `<script>` 中 INIT 注释前插入 SettingsManager**

```javascript
/* ========================================
   SettingsManager — API配置的读写
   ======================================== */
const SettingsManager = {
  DEFAULTS: {
    apiKey: '',
    baseURL: 'https://ark.cn-beijing.volces.com/api/v3',
    model: 'doubao-lite-128k',
    temperature: 0.7,
  },

  _cache: null,

  /** 获取当前设置（含默认值fallback） */
  getAll() {
    if (this._cache) return this._cache;
    try {
      const raw = localStorage.getItem('emotion-agent:settings');
      if (raw) {
        this._cache = { ...this.DEFAULTS, ...JSON.parse(raw) };
      } else {
        this._cache = { ...this.DEFAULTS };
      }
    } catch (e) {
      console.error('[SettingsManager] 读取失败:', e);
      this._cache = { ...this.DEFAULTS };
    }
    return this._cache;
  },

  /** 更新单个设置项 */
  set(key, value) {
    const all = this.getAll();
    all[key] = value;
    this._save(all);
  },

  /** 批量更新设置 */
  update(partial) {
    const all = { ...this.getAll(), ...partial };
    this._save(all);
  },

  /** 验证API配置是否完整 */
  isValid() {
    const s = this.getAll();
    return !!s.apiKey && !!s.baseURL && !!s.model;
  },

  _save(all) {
    try {
      localStorage.setItem('emotion-agent:settings', JSON.stringify(all));
      this._cache = all;
    } catch (e) {
      console.error('[SettingsManager] 保存失败:', e);
      throw e;
    }
  },
};
```

- [ ] **Step 2: 在 SettingsManager 之后插入 StorageManager**

```javascript
/* ========================================
   StorageManager — 对话数据的读写与导出/导入
   ======================================== */
const StorageManager = {
  CHATS_KEY: 'emotion-agent:chats',

  /** 获取所有会话列表（按更新时间倒序） */
  getAllChats() {
    try {
      const raw = localStorage.getItem(this.CHATS_KEY);
      if (!raw) return [];
      return JSON.parse(raw);
    } catch (e) {
      console.error('[StorageManager] 读取会话失败:', e);
      return [];
    }
  },

  /** 保存全部会话 */
  saveAllChats(chats) {
    try {
      const json = JSON.stringify(chats);
      localStorage.setItem(this.CHATS_KEY, json);
    } catch (e) {
      if (e.name === 'QuotaExceededError') {
        throw new Error('STORAGE_FULL');
      }
      throw e;
    }
  },

  /** 获取单个会话 */
  getChat(chatId) {
    const chats = this.getAllChats();
    return chats.find(c => c.id === chatId) || null;
  },

  /** 保存/更新单个会话（存在则更新，不存在则追加） */
  saveChat(chat) {
    const chats = this.getAllChats();
    const idx = chats.findIndex(c => c.id === chat.id);
    chat.updatedAt = new Date().toISOString();
    if (idx >= 0) {
      chats[idx] = chat;
    } else {
      chats.unshift(chat);
    }
    this.saveAllChats(chats);
  },

  /** 删除单个会话 */
  deleteChat(chatId) {
    const chats = this.getAllChats().filter(c => c.id !== chatId);
    this.saveAllChats(chats);
  },

  /** 导出为JSON文件下载 */
  exportJSON() {
    const data = {
      version: 1,
      exportedAt: new Date().toISOString(),
      chats: this.getAllChats(),
      settings: SettingsManager.getAll(),
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `小暖-对话备份-${new Date().toISOString().slice(0,10)}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  },

  /** 从JSON文件导入，按ID去重合并 */
  importJSON(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target.result);
          if (!data.version || !Array.isArray(data.chats)) {
            throw new Error('INVALID_FORMAT');
          }
          const existing = this.getAllChats();
          const existingIds = new Set(existing.map(c => c.id));
          const newChats = data.chats.filter(c => !existingIds.has(c.id));
          const merged = [...newChats, ...existing];
          this.saveAllChats(merged);
          // 可选：也恢复设置
          if (data.settings) {
            SettingsManager.update(data.settings);
          }
          resolve(newChats.length);
        } catch (err) {
          reject(err.message === 'INVALID_FORMAT'
            ? new Error('文件格式不正确，请选择有效的对话备份文件')
            : err);
        }
      };
      reader.onerror = () => reject(new Error('文件读取失败'));
      reader.readAsText(file);
    });
  },
};
```

- [ ] **Step 3: 浏览器 console 验证**

打开 HTML，F12 console 中测试：

```javascript
// 测试设置
SettingsManager.set('apiKey', 'test-key-123');
console.log(SettingsManager.getAll().apiKey); // 应输出 "test-key-123"

// 测试存储
StorageManager.saveChat({
  id: 'test-1',
  title: '测试会话',
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  messages: [{ role: 'user', content: '你好', timestamp: new Date().toISOString() }],
  summary: null,
});
console.log(StorageManager.getAllChats().length); // 应输出 1
StorageManager.deleteChat('test-1');
console.log(StorageManager.getAllChats().length); // 应输出 0
```

- [ ] **Step 4: 提交**

```bash
cd "C:/programs/个人项目/emotional-agent" && git add emotional-agent.html && git commit -m "✨ Task 2: SettingsManager + StorageManager（数据层）"
```

---

### Task 3: SafetyGuard 领域预检 + 安全护栏

**Files:**
- Modify: `C:/programs/个人项目/emotional-agent/emotional-agent.html` — 在 StorageManager 之后、INIT 注释前插入

- [ ] **Step 1: 插入 SafetyGuard 模块**

```javascript
/* ========================================
   SafetyGuard — 领域预检 + 危机检测
   ======================================== */
const SafetyGuard = {
  // 非情感领域关键词（命中则拒绝，0 token消耗）
  DOMAIN_BLOCK_LIST: [
    // 技术/编程
    '代码', '编程', 'bug', 'debug', '前端', '后端', '数据库', 'API', '服务器',
    'python', 'java', 'javascript', 'html', 'css', 'react', 'vue', 'node',
    '编译器', '算法', '数据结构', 'linux', 'windows', 'docker', 'git',
    '函数', '类', '对象', '数组', '字符串', '正则', '命令行',
    // 数学/科学
    '数学题', '方程式', '微积分', '物理', '化学', '生物', '几何',
    '证明', '定理', '概率', '统计',
    // 政治/宗教
    '政治', '选举', '党派', '政府', '宗教', '信仰', '教义',
    // 通用非情感
    '翻译', '写文章', '改写', '润色', '总结一下',
  ],

  // 情感领域关键词（白名单强化）
  DOMAIN_ALLOW_LIST: [
    '感情', '恋爱', '分手', '喜欢', '爱', '暗恋', '表白', '情侣', '伴侣',
    '婚姻', '夫妻', '吵架', '冷战', '矛盾', '冲突', '出轨', '劈腿', '前任',
    '沟通', '情绪', '心情', '难过', '伤心', '生气', '焦虑', '委屈', '失落',
    '朋友', '家人', '父母', '同事', '人际关系', '相处', '孤独', '寂寞',
    '暧昧', '相亲', '异地', '复合', '挽回', '放不下', '吃醋', '安全感',
    '婆媳', '闺蜜', '兄弟', '室友',
  ],

  /** 判断是否为情感领域问题。返回 { allowed: bool, reason: string } */
  checkDomain(userInput) {
    const text = userInput.toLowerCase();

    // 优先检查白名单 — 命中任何一个即放行
    for (const kw of this.DOMAIN_ALLOW_LIST) {
      if (text.includes(kw)) return { allowed: true, reason: '' };
    }

    // 检查黑名单
    for (const kw of this.DOMAIN_BLOCK_LIST) {
      if (text.includes(kw.toLowerCase())) {
        return {
          allowed: false,
          reason: '抱歉，我是情感沟通助手，只能帮你解答感情和人际关系方面的问题。如果有情感方面的困扰，随时找我聊聊。',
        };
      }
    }

    // 既不在白名单也不在黑名单 → 放行（可能是情感相关的开放式提问）
    return { allowed: true, reason: '' };
  },

  // 危机关键词 → 安全响应模式
  CRISIS_PATTERNS: [
    { keywords: ['自杀', '不想活', '结束生命', '自残', '自伤', '割腕', '跳楼', '安眠药'],
      response: '我听到你说的这些，非常担心你的安全。请你立即拨打**全国心理援助热线 400-161-9995**（24小时免费），有专业的心理咨询师可以帮助你。我只是一个AI助手，无法提供危机干预，但请你务必联系专业人士。你的生命非常宝贵。' },
    { keywords: ['家暴', '被打', '挨打', '虐待', '殴打'],
      response: '如果正在经历暴力，你的安全是第一位的。请拨打**全国妇联维权热线 12338**或**报警 110**寻求帮助。我建议你不要独自处理，联系信任的亲友或专业机构。' },
  ],

  /** 检查是否触发危机响应。返回危机响应文本，或 null 表示未触发 */
  checkCrisis(userInput) {
    for (const pattern of this.CRISIS_PATTERNS) {
      for (const kw of pattern.keywords) {
        if (userInput.includes(kw)) return pattern.response;
      }
    }
    return null;
  },
};
```

- [ ] **Step 2: Console 验证**

```javascript
// 应拒绝
console.log(SafetyGuard.checkDomain('帮我写一段python代码'));
// → { allowed: false, reason: '抱歉，我是情感沟通助手...' }

// 应放行
console.log(SafetyGuard.checkDomain('我和伴侣最近总是吵架'));
// → { allowed: true, reason: '' }

// 危机检测
console.log(SafetyGuard.checkCrisis('我最近一直想自杀'));
// → 返回热线电话号码
```

- [ ] **Step 3: 提交**

```bash
cd "C:/programs/个人项目/emotional-agent" && git add emotional-agent.html && git commit -m "✨ Task 3: SafetyGuard领域预检+危机检测"
```

---

### Task 4: DeepSeekClient — LLM API 通信

**Files:**
- Modify: `C:/programs/个人项目/emotional-agent/emotional-agent.html` — 在 SafetyGuard 之后插入

- [ ] **Step 1: 定义 System Prompt 常量**

```javascript
/* ========================================
   System Prompt
   ======================================== */
const SYSTEM_PROMPT = `你是"小暖"，一个专业的情感沟通助手。你的使命是帮助用户理解自己的情感、改善与重要他人的沟通、建立更健康的关系模式。

## 核心原则
1. **先共情后分析** — 永远先接住用户的情绪，认可感受，再引导思考
2. **多问少断** — 用开放式问题引导用户自己发现答案，不急于下结论
3. **具体化建议** — 给出可执行的话术和行为建议，比如"你可以试着说：我感到...因为..."，而不是"你要多沟通"
4. **中立不评判** — 帮助理解各方立场，不选边站，不替用户做决定

## 对话风格
- 温暖但不煽情，专业但不说教
- 适当使用心理学概念（依恋理论、非暴力沟通、情绪ABC等），但用通俗语言解释
- 回复长度适中：一般问题 150-300 字，复杂分析不超过 500 字
- 使用"你"而非"您"，保持亲切但不轻浮

## 领域边界
你只回答以下范围内的问题：恋爱关系、婚姻家庭、人际沟通、情绪管理、自我认知。
遇到范围外的问题，回复："抱歉，我是情感沟通助手，只能帮你解答感情和人际关系方面的问题。如果有情感方面的困扰，随时找我聊聊。"

## 安全规则
- 当用户表达自杀/自伤意念：表达深切关心 → 明确告知你是AI无法提供危机干预 → 提供全国心理援助热线 400-161-9995
- 涉及家暴/虐待：提供求助资源（110 / 12338），不建议自行处理
- 涉及心理疾病症状：明确你不是医生，建议就医
- 永远不要鼓励伤害自己或他人的行为`;
```

- [ ] **Step 2: 插入 DeepSeekClient 模块**

```javascript
/* ========================================
   DeepSeekClient — LLM API通信（OpenAI兼容格式）
   ======================================== */
const DeepSeekClient = {
  /** 流式聊天（SSE） */
  async streamChat(messages, callbacks) {
    const { onChunk, onDone, onError } = callbacks;
    const settings = SettingsManager.getAll();

    if (!settings.apiKey) {
      onError(new Error('API Key 未设置，请按 Ctrl+, 打开设置'));
      return;
    }

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000); // 30s超时

    try {
      const response = await fetch(`${settings.baseURL}/chat/completions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${settings.apiKey}`,
        },
        body: JSON.stringify({
          model: settings.model,
          messages: messages,
          temperature: settings.temperature,
          stream: true,
        }),
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        const err = new Error(`API 错误`);
        err.status = response.status;
        if (response.status === 401) err.userMessage = 'API Key 无效，请检查后重新输入';
        else if (response.status === 429) err.userMessage = '请求过于频繁，请稍后再试';
        else err.userMessage = `服务器错误 (${response.status})，请稍后重试`;
        throw err;
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || ''; // 不完整的行留在buffer

        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed || !trimmed.startsWith('data: ')) continue;
          const data = trimmed.slice(6);
          if (data === '[DONE]') {
            onDone();
            return;
          }
          try {
            const json = JSON.parse(data);
            const content = json.choices?.[0]?.delta?.content;
            if (content) onChunk(content);
          } catch (e) {
            // 跳过解析失败的行（某些API可能返回非标准格式）
          }
        }
      }
      onDone();
    } catch (err) {
      clearTimeout(timeoutId);
      if (err.name === 'AbortError') {
        onError(new Error('请求超时，请检查网络后重试'));
      } else if (!err.userMessage) {
        err.userMessage = '网络连接失败，请检查网络后重试';
      }
      onError(err);
    }
  },

  /** 非流式请求（用于上下文压缩） */
  async chat(messages) {
    const settings = SettingsManager.getAll();

    const response = await fetch(`${settings.baseURL}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${settings.apiKey}`,
      },
      body: JSON.stringify({
        model: settings.model,
        messages: messages,
        temperature: 0.3, // 压缩用低温度
        stream: false,
      }),
    });

    if (!response.ok) {
      throw new Error(`API 请求失败: ${response.status}`);
    }

    const data = await response.json();
    return data.choices?.[0]?.message?.content || '';
  },
};
```

- [ ] **Step 3: Console 验证（需要有效的 API Key）**

```javascript
// 先设置API Key
SettingsManager.set('apiKey', '你的豆包API Key');

// 测试流式
DeepSeekClient.streamChat(
  [{ role: 'system', content: SYSTEM_PROMPT }, { role: 'user', content: '你好' }],
  {
    onChunk: (text) => console.log('CHUNK:', text),
    onDone: () => console.log('DONE'),
    onError: (err) => console.error('ERROR:', err.userMessage || err.message),
  }
);
```

确认 console 输出逐字 chunk，最后输出 DONE。

- [ ] **Step 4: 提交**

```bash
cd "C:/programs/个人项目/emotional-agent" && git add emotional-agent.html && git commit -m "✨ Task 4: DeepSeekClient流式API+SystemPrompt"
```

---

### Task 5: ContextCompressor — 上下文压缩

**Files:**
- Modify: `C:/programs/个人项目/emotional-agent/emotional-agent.html` — 在 DeepSeekClient 之后插入

- [ ] **Step 1: 插入 ContextCompressor 模块**

```javascript
/* ========================================
   ContextCompressor — 超过20轮时压缩早期对话
   ======================================== */
const ContextCompressor = {
  MAX_ROUNDS: 20,  // 保留最近N轮完整内容
  // 一轮 = 一条user消息 + 一条assistant回复

  /** 判断是否需要压缩 */
  needsCompression(messages) {
    // messages不包含system prompt，只算user+assistant对数
    const rounds = Math.floor(messages.length / 2);
    return rounds > this.MAX_ROUNDS;
  },

  /** 构建压缩用的prompt */
  _buildCompressionPrompt(oldMessages) {
    const history = oldMessages
      .map(m => `${m.role === 'user' ? '用户' : '小暖'}: ${m.content}`)
      .join('\n\n');
    return [
      { role: 'system', content: '你是一个对话摘要助手。请将以下情感咨询对话压缩为一段200字以内的中文摘要，保留：1)用户的核心困扰 2)已讨论过的主要方向 3)用户表达过的倾向或决定。只输出摘要文本，不加前缀。' },
      { role: 'user', content: `请压缩以下对话：\n\n${history}` },
    ];
  },

  /**
   * 压缩消息列表。
   * 返回 { messages: 压缩后的完整消息列表, summary: 摘要文本 }
   * messages已包含system prompt占位（由ChatManager拼接）
   */
  async compress(messages, existingSummary) {
    const rounds = Math.floor(messages.length / 2);
    if (rounds <= this.MAX_ROUNDS) {
      return { messages, summary: existingSummary };
    }

    // 超出部分
    const overflowCount = (rounds - this.MAX_ROUNDS) * 2; // 转换为消息条数
    const oldPart = messages.slice(0, overflowCount);
    const recentPart = messages.slice(overflowCount);

    // 如果有旧摘要，加进去让新摘要更完整
    let oldContext = '';
    if (existingSummary) {
      oldContext = `[之前的背景：${existingSummary}]\n\n`;
    }

    // 调用API压缩
    let newSummary;
    try {
      const compressMessages = this._buildCompressionPrompt(oldPart);
      newSummary = await DeepSeekClient.chat(compressMessages);
    } catch (e) {
      // 压缩失败则截断（降级方案）
      console.warn('[ContextCompressor] 压缩失败，使用截断:', e);
      return {
        messages: recentPart,
        summary: existingSummary || '(早期对话因过长已省略)',
      };
    }

    // 合并旧摘要
    const combinedSummary = existingSummary
      ? `${existingSummary}；${newSummary}`
      : newSummary;

    return { messages: recentPart, summary: combinedSummary };
  },
};
```

- [ ] **Step 2: Console 验证**

先添加一些模拟消息测试（需要有效 Key 才能测压缩）：

```javascript
// 构造超过20轮的消息列表
const fakeMessages = [];
for (let i = 0; i < 42; i++) { // 21轮
  fakeMessages.push({ role: 'user', content: `第${i+1}轮用户消息` });
  fakeMessages.push({ role: 'assistant', content: `第${i+1}轮回复` });
}
console.log(ContextCompressor.needsCompression(fakeMessages)); // true
```

- [ ] **Step 3: 提交**

```bash
cd "C:/programs/个人项目/emotional-agent" && git add emotional-agent.html && git commit -m "✨ Task 5: ContextCompressor上下文压缩"
```

---

### Task 6: ChatManager — 对话编排

**Files:**
- Modify: `C:/programs/个人项目/emotional-agent/emotional-agent.html` — 在 ContextCompressor 之后插入

- [ ] **Step 1: 插入 ChatManager 模块**

```javascript
/* ========================================
   ChatManager — 会话CRUD + 消息流控
   ======================================== */
const ChatManager = {
  _currentChatId: null,

  /** 创建新会话 */
  createChat() {
    const chat = {
      id: crypto.randomUUID ? crypto.randomUUID() : 'id-' + Date.now() + '-' + Math.random().toString(36).slice(2, 8),
      title: '新对话',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      messages: [],
      summary: null,
    };
    StorageManager.saveChat(chat);
    this._currentChatId = chat.id;
    return chat;
  },

  /** 获取当前会话 */
  getCurrentChat() {
    if (!this._currentChatId) return null;
    return StorageManager.getChat(this._currentChatId);
  },

  /** 切换到指定会话 */
  switchChat(chatId) {
    const chat = StorageManager.getChat(chatId);
    if (chat) {
      this._currentChatId = chatId;
    }
    return chat;
  },

  /** 构建发送给API的消息列表 */
  async buildContext() {
    const chat = this.getCurrentChat();
    if (!chat) return [{ role: 'system', content: SYSTEM_PROMPT }];

    const history = chat.messages; // 不含system prompt

    // 判断是否需要压缩
    if (ContextCompressor.needsCompression(history)) {
      const result = await ContextCompressor.compress(history, chat.summary);
      chat.messages = result.messages;
      chat.summary = result.summary;
      StorageManager.saveChat(chat);
    }

    // 拼接：system prompt + summary提示 + 历史消息
    const context = [{ role: 'system', content: SYSTEM_PROMPT }];

    if (chat.summary) {
      context[0].content += `\n\n[历史背景：${chat.summary}]`;
    }

    return context.concat(chat.messages);
  },

  /** 发送用户消息并获取流式回复 */
  async sendMessage(userInput, uiCallbacks) {
    const { onUserMsg, onAgentChunk, onAgentDone, onError, onReject } = uiCallbacks;

    // 1. 领域预检
    const domainCheck = SafetyGuard.checkDomain(userInput);
    if (!domainCheck.allowed) {
      // 本地拒绝，渲染拒绝卡片（不计入消息历史）
      onReject(domainCheck.reason);
      return;
    }

    // 2. 危机检测
    const crisisResponse = SafetyGuard.checkCrisis(userInput);
    if (crisisResponse) {
      // 触发安全模式 — 同时添加用户消息和安全回复
      const chat = this._ensureChat();
      chat.messages.push(
        { role: 'user', content: userInput, timestamp: new Date().toISOString() },
        { role: 'assistant', content: crisisResponse, timestamp: new Date().toISOString() }
      );
      StorageManager.saveChat(chat);
      onAgentChunk(crisisResponse);
      onAgentDone();
      return;
    }

    // 3. 正常流程
    const chat = this._ensureChat();

    // 添加用户消息
    const userMsg = { role: 'user', content: userInput, timestamp: new Date().toISOString() };
    chat.messages.push(userMsg);
    onUserMsg(userMsg);

    // 自动标题：首条消息作为标题
    if (chat.messages.length === 1) {
      chat.title = userInput.length > 20 ? userInput.slice(0, 20) + '...' : userInput;
    }

    StorageManager.saveChat(chat);

    // 4. 构建上下文并发起请求
    const context = await this.buildContext();

    let fullResponse = '';
    DeepSeekClient.streamChat(context, {
      onChunk: (text) => {
        fullResponse += text;
        onAgentChunk(text);
      },
      onDone: () => {
        // 保存assistant消息
        const chat = this.getCurrentChat();
        if (chat) {
          chat.messages.push({
            role: 'assistant',
            content: fullResponse,
            timestamp: new Date().toISOString(),
          });
          StorageManager.saveChat(chat);
        }
        onAgentDone();
      },
      onError: (err) => {
        // 保存已接收的部分
        if (fullResponse) {
          const chat = this.getCurrentChat();
          if (chat) {
            chat.messages.push({
              role: 'assistant',
              content: fullResponse + '\n\n[响应中断]',
              timestamp: new Date().toISOString(),
            });
            StorageManager.saveChat(chat);
          }
        }
        onError(err);
      },
    });
  },

  /** 重试最后一条消息（补全中断的响应） */
  async retryLast() {
    const chat = this.getCurrentChat();
    if (!chat || chat.messages.length < 2) return;

    const lastAssistant = chat.messages[chat.messages.length - 1];
    if (lastAssistant.role !== 'assistant') return;

    // 移除最后一条assistant消息，重新生成
    chat.messages.pop();
    StorageManager.saveChat(chat);

    // 重新调用sendMessage但跳过添加用户消息
    const context = await this.buildContext();
    let fullResponse = '';

    return new Promise((resolve, reject) => {
      DeepSeekClient.streamChat(context, {
        onChunk: (text) => {
          fullResponse += text;
          UIController.appendToLastBubble(text);
        },
        onDone: () => {
          const chat = this.getCurrentChat();
          if (chat) {
            chat.messages.push({
              role: 'assistant',
              content: fullResponse,
              timestamp: new Date().toISOString(),
            });
            StorageManager.saveChat(chat);
          }
          resolve(fullResponse);
        },
        onError: reject,
      });
    });
  },

  /** 确保存在当前会话（没有则新建） */
  _ensureChat() {
    let chat = this.getCurrentChat();
    if (!chat) {
      chat = this.createChat();
    }
    return chat;
  },
};
```

- [ ] **Step 2: Console 验证**

```javascript
const chat = ChatManager.createChat();
console.log(chat.id); // UUID
console.log(StorageManager.getAllChats().length); // 1

// 测试领域拒绝
ChatManager.sendMessage('帮我写代码', {
  onUserMsg: console.log,
  onAgentChunk: console.log,
  onAgentDone: () => console.log('done'),
  onError: console.error,
  onReject: (msg) => console.log('REJECT:', msg), // 应触发此回调
});
```

- [ ] **Step 3: 提交**

```bash
cd "C:/programs/个人项目/emotional-agent" && git add emotional-agent.html && git commit -m "✨ Task 6: ChatManager对话编排（CRUD+流控+重试）"
```

---

### Task 7: UI — DOM 结构 + 侧边栏

**Files:**
- Modify: `C:/programs/个人项目/emotional-agent/emotional-agent.html`

从本任务开始构建 UI。需要完成：(1) 替换 `<div id="app">` 中的占位注释为实际 DOM，(2) 添加侧边栏 CSS，(3) 添加 UIController 模块。

- [ ] **Step 1: 在 `</style>` 之前追加侧边栏 + 主体 + 设置面板 CSS**

```css
/* ========================================
   Sidebar
   ======================================== */
.sidebar {
  width: var(--sidebar-width);
  min-width: var(--sidebar-width);
  height: 100%;
  background: rgba(255,255,255,0.015);
  border-right: 1px solid var(--card-border);
  display: flex;
  flex-direction: column;
  z-index: 10;
}

.sidebar-header {
  padding: 16px;
  display: flex; align-items: center; justify-content: space-between;
  border-bottom: 1px solid var(--card-border);
}
.sidebar-logo {
  display: flex; align-items: center; gap: 8px;
  font-size: 16px; font-weight: 700;
  color: var(--title);
}
.sidebar-logo .logo-icon { font-size: 20px; }
.sidebar-btn {
  width: 32px; height: 32px;
  border-radius: 8px;
  background: rgba(185,142,255,0.1);
  color: var(--title);
  font-size: 18px;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.2s;
}
.sidebar-btn:hover { background: rgba(185,142,255,0.2); }

.chat-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}
.chat-item {
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  display: flex; align-items: center; gap: 8px;
  font-size: 13px;
  color: var(--text-dim);
  transition: all 0.15s;
  position: relative;
  margin-bottom: 2px;
}
.chat-item:hover { background: rgba(255,255,255,0.04); }
.chat-item.active { background: rgba(185,142,255,0.08); color: var(--text); }
.chat-item .chat-icon { font-size: 14px; flex-shrink: 0; opacity: 0.6; }
.chat-item .chat-title { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.chat-item .chat-delete {
  opacity: 0;
  width: 24px; height: 24px;
  border-radius: 4px;
  background: transparent;
  color: var(--text-muted);
  font-size: 14px;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.15s;
  flex-shrink: 0;
}
.chat-item:hover .chat-delete { opacity: 1; }
.chat-item .chat-delete:hover { background: rgba(232,93,117,0.15); color: var(--accent); }
.chat-item .chat-rename-input {
  flex: 1;
  background: rgba(255,255,255,0.06);
  border: 1px solid var(--title);
  border-radius: 4px;
  color: var(--text);
  font-size: 13px;
  padding: 2px 6px;
}

.sidebar-footer {
  padding: 10px 12px;
  border-top: 1px solid var(--card-border);
}
.sidebar-footer-btn {
  width: 100%;
  padding: 8px;
  border-radius: 6px;
  background: transparent;
  color: var(--text-muted);
  font-size: 12px;
  text-align: center;
  transition: all 0.15s;
}
.sidebar-footer-btn:hover { background: rgba(232,93,117,0.08); color: var(--accent); }

/* ========================================
   Main Chat Area
   ======================================== */
.main-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;
  min-width: 0;
}

.chat-header-bar {
  padding: 12px 20px;
  border-bottom: 1px solid var(--card-border);
  display: flex; align-items: center; justify-content: space-between;
  flex-shrink: 0;
}
.chat-header-title { font-size: 15px; font-weight: 600; color: var(--text); }
.chat-header-actions { display: flex; gap: 8px; }
.icon-btn {
  width: 32px; height: 32px;
  border-radius: 8px;
  background: transparent;
  color: var(--text-dim);
  font-size: 16px;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.15s;
}
.icon-btn:hover { background: rgba(255,255,255,0.06); color: var(--text); }

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex; flex-direction: column; gap: 16px;
}

.empty-state {
  flex: 1;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  color: var(--text-muted);
  gap: 12px;
}
.empty-icon { font-size: 48px; opacity: 0.3; }
.empty-text { font-size: 15px; }
.empty-hint { font-size: 12px; opacity: 0.6; }

.chat-input-area {
  padding: 14px 20px;
  border-top: 1px solid var(--card-border);
  display: flex; align-items: flex-end; gap: 10px;
  flex-shrink: 0;
}
.chat-input {
  flex: 1;
  padding: 10px 16px;
  border-radius: 20px;
  border: 1px solid rgba(255,255,255,0.1);
  background: rgba(255,255,255,0.04);
  color: var(--text);
  font-size: 14px;
  resize: none;
  max-height: 120px;
  min-height: 20px;
  line-height: 1.5;
}
.chat-input:focus { border-color: var(--title); }
.chat-input::placeholder { color: var(--text-muted); }
.send-btn {
  width: 40px; height: 40px;
  min-width: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--title), #9b6fff);
  color: white;
  font-size: 18px;
  display: flex; align-items: center; justify-content: center;
  transition: opacity 0.2s;
}
.send-btn:hover { opacity: 0.85; }
.send-btn:disabled { opacity: 0.4; cursor: default; }

/* ========================================
   Message Bubbles
   ======================================== */
.msg-row {
  display: flex;
  gap: 10px;
  animation: msgIn 0.35s ease;
}
@keyframes msgIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.msg-row.user { flex-direction: row-reverse; }
.msg-avatar {
  width: 30px; height: 30px;
  border-radius: 50%;
  flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px;
  margin-top: 2px;
}
.msg-row.user .msg-avatar { background: rgba(255,255,255,0.08); }
.msg-row.agent .msg-avatar { background: linear-gradient(135deg, var(--title), var(--accent)); }
.msg-bubble {
  max-width: 72%;
  padding: 10px 16px;
  border-radius: 16px;
  font-size: 14px;
  line-height: 1.65;
  white-space: pre-wrap;
  word-break: break-word;
}
.msg-row.user .msg-bubble {
  background: rgba(185,142,255,0.12);
  border-bottom-right-radius: 4px;
  color: var(--text);
}
.msg-row.agent .msg-bubble {
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--card-border);
  border-bottom-left-radius: 4px;
  color: var(--text);
}
.msg-row.agent .msg-bubble.streaming::after {
  content: ' ▌';
  animation: blink 0.8s infinite;
  color: var(--title);
}
.msg-time {
  font-size: 10px;
  color: var(--text-muted);
  margin-top: 4px;
  padding: 0 4px;
}
.msg-row.user .msg-time { text-align: right; }

/* Reject card */
.reject-card {
  padding: 12px 16px;
  border-radius: 10px;
  border: 1px solid rgba(232,93,117,0.2);
  background: rgba(232,93,117,0.05);
  color: var(--accent);
  font-size: 13px;
  line-height: 1.6;
  animation: msgIn 0.35s ease;
}

/* Error bubble */
.msg-row.error .msg-bubble {
  border: 1px solid rgba(232,93,117,0.3) !important;
}
.msg-actions {
  display: flex; gap: 8px; margin-top: 6px;
}
.retry-btn {
  padding: 4px 12px;
  border-radius: 6px;
  background: rgba(232,93,117,0.1);
  color: var(--accent);
  font-size: 12px;
  transition: background 0.15s;
}
.retry-btn:hover { background: rgba(232,93,117,0.2); }

/* Typing indicator */
.typing-indicator {
  display: flex; gap: 4px; padding: 8px 0;
}
.typing-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--text-muted);
  animation: typingBounce 1.4s infinite ease-in-out;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes typingBounce { 0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; } 40% { transform: scale(1); opacity: 1; } }

/* "继续"按钮（中断补全） */
.continue-hint {
  display: inline-flex; align-items: center; gap: 4px;
  padding: 2px 8px;
  margin-top: 4px;
  border-radius: 4px;
  background: rgba(255,255,255,0.04);
  color: var(--text-muted);
  font-size: 11px;
  cursor: pointer;
}
.continue-hint:hover { color: var(--title); }
```

- [ ] **Step 2: 替换 `<div id="app">` 内的占位注释为实际 DOM**

```html
<div id="app">
  <!-- 侧边栏 -->
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-header">
      <div class="sidebar-logo">
        <span class="logo-icon">💝</span>
        <span>小暖</span>
      </div>
      <button class="sidebar-btn" id="btnNewChat" title="新对话 (Ctrl+N)">＋</button>
    </div>
    <div class="chat-list" id="chatList"></div>
    <div class="sidebar-footer">
      <button class="sidebar-footer-btn" id="btnClearAll">清除全部对话</button>
    </div>
  </aside>

  <!-- 主对话区 -->
  <main class="main-area" id="mainArea">
    <div class="chat-header-bar">
      <span class="chat-header-title" id="chatTitle">新对话</span>
      <div class="chat-header-actions">
        <button class="icon-btn" id="btnSettings" title="设置 (Ctrl+,)">⚙</button>
      </div>
    </div>
    <div class="chat-messages" id="chatMessages">
      <div class="empty-state" id="emptyState">
        <div class="empty-icon">💝</div>
        <div class="empty-text">有什么想聊的？</div>
        <div class="empty-hint">无论是感情困惑还是人际烦恼，我都在这里倾听</div>
      </div>
    </div>
    <div class="chat-input-area">
      <textarea class="chat-input" id="chatInput" placeholder="说说你的想法..." rows="1"></textarea>
      <button class="send-btn" id="btnSend" title="发送 (Enter)">→</button>
    </div>
  </main>

  <!-- 设置面板（初始隐藏） -->
  <div class="settings-overlay" id="settingsOverlay"></div>
  <aside class="settings-panel" id="settingsPanel">
    <!-- Task 10 填充 -->
  </aside>
</div>
```

- [ ] **Step 3: 在 ChatManager 之后、INIT 之前插入 UIController（侧边栏部分）**

```javascript
/* ========================================
   UIController — DOM渲染与交互
   ======================================== */
const UIController = {
  /* ---- DOM 引用 ---- */
  _dom: {},
  _streamingBubble: null, // 当前正在流式输出的气泡元素

  init() {
    this._dom = {
      sidebar: document.getElementById('sidebar'),
      chatList: document.getElementById('chatList'),
      chatMessages: document.getElementById('chatMessages'),
      chatTitle: document.getElementById('chatTitle'),
      chatInput: document.getElementById('chatInput'),
      emptyState: document.getElementById('emptyState'),
      btnNewChat: document.getElementById('btnNewChat'),
      btnSend: document.getElementById('btnSend'),
      btnSettings: document.getElementById('btnSettings'),
      btnClearAll: document.getElementById('btnClearAll'),
      settingsPanel: document.getElementById('settingsPanel'),
      settingsOverlay: document.getElementById('settingsOverlay'),
      toastContainer: document.getElementById('toastContainer'),
    };

    this._bindEvents();
    this._renderSidebar();
    this._loadLastChat();
  },

  /* ---- 事件绑定 ---- */
  _bindEvents() {
    // 新对话
    this._dom.btnNewChat.addEventListener('click', () => this._newChat());
    // 发送
    this._dom.btnSend.addEventListener('click', () => this._send());
    this._dom.chatInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        this._send();
      }
    });
    // 输入框自动调高
    this._dom.chatInput.addEventListener('input', () => {
      this._dom.chatInput.style.height = 'auto';
      this._dom.chatInput.style.height = Math.min(this._dom.chatInput.scrollHeight, 120) + 'px';
    });
    // 设置按钮
    this._dom.btnSettings.addEventListener('click', () => this._toggleSettings());
    // 清空
    this._dom.btnClearAll.addEventListener('click', () => this._clearAllChats());
    // 键盘快捷键（Task 11 会扩展）
  },

  /* ---- 侧边栏渲染 ---- */
  _renderSidebar() {
    const chats = StorageManager.getAllChats();
    const currentId = ChatManager._currentChatId;
    this._dom.chatList.innerHTML = '';

    chats.forEach(chat => {
      const item = document.createElement('div');
      item.className = 'chat-item' + (chat.id === currentId ? ' active' : '');
      item.dataset.chatId = chat.id;

      const icon = document.createElement('span');
      icon.className = 'chat-icon';
      icon.textContent = '💬';

      const title = document.createElement('span');
      title.className = 'chat-title';
      title.textContent = chat.title;

      const delBtn = document.createElement('button');
      delBtn.className = 'chat-delete';
      delBtn.textContent = '×';
      delBtn.title = '删除对话';

      item.appendChild(icon);
      item.appendChild(title);
      item.appendChild(delBtn);
      this._dom.chatList.appendChild(item);

      // 点击切换
      item.addEventListener('click', (e) => {
        if (e.target === delBtn) return;
        this._switchToChat(chat.id);
      });

      // 双击重命名
      item.addEventListener('dblclick', (e) => {
        if (e.target === delBtn) return;
        this._renameChat(chat.id, title);
      });

      // 删除
      delBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        this._deleteChat(chat.id);
      });
    });
  },

  _loadLastChat() {
    const chats = StorageManager.getAllChats();
    if (chats.length > 0) {
      this._switchToChat(chats[0].id);
    } else {
      this._newChat();
    }
  },

  _newChat() {
    const chat = ChatManager.createChat();
    this._renderSidebar();
    this._renderMessages();
    this._dom.chatTitle.textContent = '新对话';
    this._dom.chatInput.focus();
  },

  _switchToChat(chatId) {
    ChatManager.switchChat(chatId);
    this._renderSidebar();
    this._renderMessages();
    const chat = ChatManager.getCurrentChat();
    if (chat) this._dom.chatTitle.textContent = chat.title;
  },

  _deleteChat(chatId) {
    StorageManager.deleteChat(chatId);
    if (ChatManager._currentChatId === chatId) {
      ChatManager._currentChatId = null;
      this._loadLastChat();
    } else {
      this._renderSidebar();
    }
  },

  _renameChat(chatId, titleEl) {
    const chat = StorageManager.getChat(chatId);
    if (!chat) return;

    const input = document.createElement('input');
    input.className = 'chat-rename-input';
    input.value = chat.title;
    input.addEventListener('blur', () => {
      const newTitle = input.value.trim() || chat.title;
      chat.title = newTitle;
      StorageManager.saveChat(chat);
      this._renderSidebar();
    });
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') input.blur();
      if (e.key === 'Escape') {
        input.value = chat.title;
        input.blur();
      }
    });
    titleEl.replaceWith(input);
    input.focus();
    input.select();
  },

  _clearAllChats() {
    if (!confirm('确定要清除全部对话吗？此操作不可撤销。建议先导出备份。')) return;
    StorageManager.saveAllChats([]);
    ChatManager._currentChatId = null;
    this._renderSidebar();
    this._newChat();
  },
};
```

- [ ] **Step 4: 更新 INIT 代码**

将 `<script>` 末尾的 INIT 代码替换为：

```javascript
/* ========================================
   INIT
   ======================================== */
document.addEventListener('DOMContentLoaded', () => {
  UIController.init();
});
```

- [ ] **Step 5: 浏览器验证**

打开 HTML，应看到：侧边栏（含"+ "按钮和"清除全部"）、空对话区（带空状态提示）、底栏输入框和发送按钮。

- [ ] **Step 6: 提交**

```bash
cd "C:/programs/个人项目/emotional-agent" && git add emotional-agent.html && git commit -m "✨ Task 7: UI侧边栏+主对话区DOM+基础交互"
```

---

### Task 8: UI — 消息渲染与发送

**Files:**
- Modify: `C:/programs/个人项目/emotional-agent/emotional-agent.html`

在 UIController 模块中追加消息渲染和发送相关方法。

- [ ] **Step 1: 在 UIController._clearAllChats 方法之后、`};` 闭合之前追加以下方法**

```javascript
  /* ---- 消息渲染 ---- */
  _renderMessages() {
    const chat = ChatManager.getCurrentChat();
    this._dom.chatMessages.innerHTML = '';

    if (!chat || chat.messages.length === 0) {
      this._dom.emptyState.style.display = 'flex';
      return;
    }

    this._dom.emptyState.style.display = 'none';
    const fragment = document.createDocumentFragment();

    chat.messages.forEach((msg, idx) => {
      if (msg.role === 'user') {
        fragment.appendChild(this._createUserBubble(msg));
      } else if (msg.role === 'assistant') {
        fragment.appendChild(this._createAgentBubble(msg, idx === chat.messages.length - 1 && msg.content.includes('[响应中断]')));
      }
    });

    this._dom.chatMessages.appendChild(fragment);
    this._scrollToBottom();
  },

  _createUserBubble(msg) {
    const row = document.createElement('div');
    row.className = 'msg-row user';
    row.innerHTML = `
      <div class="msg-avatar">👤</div>
      <div>
        <div class="msg-bubble">${this._escapeHtml(msg.content)}</div>
        <div class="msg-time">${this._formatTime(msg.timestamp)}</div>
      </div>`;
    return row;
  },

  _createAgentBubble(msg, wasInterrupted) {
    const row = document.createElement('div');
    row.className = 'msg-row agent';
    row.innerHTML = `
      <div class="msg-avatar">💝</div>
      <div>
        <div class="msg-bubble">${this._escapeHtml(msg.content)}</div>
        <div class="msg-time">${this._formatTime(msg.timestamp)}</div>
        ${wasInterrupted ? '<span class="continue-hint" data-action="continue">点击继续生成 →</span>' : ''}
      </div>`;

    const continueBtn = row.querySelector('[data-action="continue"]');
    if (continueBtn) {
      continueBtn.addEventListener('click', () => this._continueResponse());
    }
    return row;
  },

  _createRejectCard(message) {
    const card = document.createElement('div');
    card.className = 'reject-card';
    card.textContent = message;
    return card;
  },

  _createTypingIndicator() {
    const row = document.createElement('div');
    row.className = 'msg-row agent';
    row.id = 'typingIndicator';
    row.innerHTML = `
      <div class="msg-avatar">💝</div>
      <div>
        <div class="msg-bubble">
          <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
          </div>
        </div>
      </div>`;
    return row;
  },

  /* ---- 发送消息 ---- */
  _send() {
    const text = this._dom.chatInput.value.trim();
    if (!text) return;

    // 禁用发送按钮防止重复
    this._dom.btnSend.disabled = true;
    this._dom.chatInput.value = '';
    this._dom.chatInput.style.height = 'auto';

    // 隐藏空状态
    this._dom.emptyState.style.display = 'none';

    // 添加输入指示器
    const typing = this._createTypingIndicator();
    this._dom.chatMessages.appendChild(typing);
    this._scrollToBottom();

    ChatManager.sendMessage(text, {
      onUserMsg: (msg) => {
        // 移除输入指示器，添加用户气泡
        typing.remove();
        const bubble = this._createUserBubble(msg);
        this._dom.chatMessages.appendChild(bubble);
        this._scrollToBottom();
        // 更新侧边栏标题
        this._renderSidebar();
        this._dom.chatTitle.textContent = ChatManager.getCurrentChat()?.title || '新对话';
      },
      onAgentChunk: (chunk) => {
        if (!this._streamingBubble) {
          // 第一个chunk：创建agent气泡
          const row = document.createElement('div');
          row.className = 'msg-row agent';
          row.innerHTML = `
            <div class="msg-avatar">💝</div>
            <div>
              <div class="msg-bubble streaming"></div>
            </div>`;
          this._streamingBubble = row.querySelector('.msg-bubble');
          this._dom.chatMessages.appendChild(row);
        }
        this._streamingBubble.textContent += chunk;
        this._scrollToBottom();
      },
      onAgentDone: () => {
        // 移除streaming光标
        if (this._streamingBubble) {
          this._streamingBubble.classList.remove('streaming');
        }
        this._streamingBubble = null;
        this._dom.btnSend.disabled = false;
        this._dom.chatInput.focus();
        // 刷新消息列表（添加时间戳等）
        this._renderMessages();
      },
      onError: (err) => {
        typing.remove();
        this._streamingBubble = null;
        this._dom.btnSend.disabled = false;

        // 显示错误气泡
        const row = document.createElement('div');
        row.className = 'msg-row agent error';
        row.innerHTML = `
          <div class="msg-avatar">💝</div>
          <div>
            <div class="msg-bubble">${this._escapeHtml(err.userMessage || err.message)}</div>
            <div class="msg-actions">
              <button class="retry-btn" data-action="retry">重新发送</button>
            </div>
          </div>`;
        const retryBtn = row.querySelector('[data-action="retry"]');
        retryBtn.addEventListener('click', () => {
          row.remove();
          this._send(); // 用当前输入重试——实际上用户需要重新输入
        });
        this._dom.chatMessages.appendChild(row);
        this._scrollToBottom();
      },
      onReject: (message) => {
        typing.remove();
        this._dom.btnSend.disabled = false;
        this._dom.chatInput.focus();
        const card = this._createRejectCard(message);
        this._dom.chatMessages.appendChild(card);
        this._scrollToBottom();
      },
    });
  },

  /** 追加文本到最后一个agent气泡（用于重试补全） */
  appendToLastBubble(text) {
    const bubbles = this._dom.chatMessages.querySelectorAll('.msg-row.agent .msg-bubble');
    const last = bubbles[bubbles.length - 1];
    if (last) {
      last.textContent += text;
      this._scrollToBottom();
    }
  },

  _continueResponse() {
    // 移除"[响应中断]"文本的agent消息，重试
    const chat = ChatManager.getCurrentChat();
    if (!chat || chat.messages.length === 0) return;

    // 移除最后一条assistant消息中的中断标记
    const last = chat.messages[chat.messages.length - 1];
    if (last.role === 'assistant') {
      last.content = last.content.replace(/\n\n\[响应中断\]$/, '');
      StorageManager.saveChat(chat);
    }

    // 使用retryLast补全
    this._dom.btnSend.disabled = true;
    const typing = this._createTypingIndicator();
    this._dom.chatMessages.appendChild(typing);

    ChatManager.retryLast().then(() => {
      typing.remove();
      this._dom.btnSend.disabled = false;
      this._renderMessages();
    }).catch((err) => {
      typing.remove();
      this._dom.btnSend.disabled = false;
      this._showToast(err.userMessage || err.message, 'error');
    });
  },

  /* ---- 辅助方法 ---- */
  _scrollToBottom() {
    requestAnimationFrame(() => {
      this._dom.chatMessages.scrollTop = this._dom.chatMessages.scrollHeight;
    });
  },

  _escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  },

  _formatTime(isoString) {
    if (!isoString) return '';
    const d = new Date(isoString);
    return String(d.getHours()).padStart(2, '0') + ':' + String(d.getMinutes()).padStart(2, '0');
  },

  _showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    this._dom.toastContainer.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
  },
};
```

- [ ] **Step 2: 浏览器验证**

1. 打开 HTML
2. 输入"我和伴侣总是因为小事吵架"发送
3. 如 API Key 未设置，应显示"API Key 未设置"错误气泡
4. 设置 API Key 后重试，应看到流式回复逐字输出

- [ ] **Step 3: 提交**

```bash
cd "C:/programs/个人项目/emotional-agent" && git add emotional-agent.html && git commit -m "✨ Task 8: 消息渲染+流式发送+重试补全"
```

---

### Task 9: UI — 设置面板

**Files:**
- Modify: `C:/programs/个人项目/emotional-agent/emotional-agent.html`

- [ ] **Step 1: 在 `</style>` 之前追加设置面板 CSS**

```css
/* ========================================
   Settings Panel
   ======================================== */
.settings-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.4);
  z-index: 50;
  display: none;
}
.settings-overlay.open { display: block; }

.settings-panel {
  position: fixed;
  top: 0; right: 0;
  width: var(--settings-width);
  height: 100%;
  background: var(--bg);
  border-left: 1px solid var(--card-border);
  z-index: 51;
  display: flex;
  flex-direction: column;
  transform: translateX(100%);
  transition: transform 0.3s cubic-bezier(.22,1,.36,1);
}
.settings-panel.open { transform: translateX(0); }

.settings-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--card-border);
  display: flex; align-items: center; justify-content: space-between;
}
.settings-header h3 { font-size: 16px; color: var(--title); font-weight: 600; }
.close-btn {
  width: 28px; height: 28px;
  border-radius: 6px;
  background: transparent;
  color: var(--text-dim);
  font-size: 16px;
  display: flex; align-items: center; justify-content: center;
}
.close-btn:hover { background: rgba(255,255,255,0.06); }

.settings-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex; flex-direction: column; gap: 18px;
}
.settings-group { display: flex; flex-direction: column; gap: 6px; }
.settings-group label {
  font-size: 12px; color: var(--text-dim);
  text-transform: uppercase; letter-spacing: 1px;
}
.settings-input {
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.1);
  background: rgba(255,255,255,0.04);
  color: var(--text);
  font-size: 14px;
  font-family: inherit;
}
.settings-input:focus { border-color: var(--title); }
.settings-input::placeholder { color: var(--text-muted); }

.settings-select {
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.1);
  background: rgba(255,255,255,0.04);
  color: var(--text);
  font-size: 14px;
  font-family: inherit;
  cursor: pointer;
}
.settings-select option { background: #1a1a2e; color: var(--text); }

.settings-hint {
  font-size: 11px; color: var(--text-muted); line-height: 1.5;
}

.settings-divider {
  height: 1px;
  background: var(--card-border);
  margin: 4px 0;
}

.settings-actions {
  display: flex; gap: 10px;
}
.btn-primary {
  flex: 1;
  padding: 10px;
  border-radius: 8px;
  background: rgba(185,142,255,0.15);
  color: var(--title);
  font-size: 13px;
  font-weight: 600;
  transition: background 0.15s;
}
.btn-primary:hover { background: rgba(185,142,255,0.25); }
.btn-danger {
  flex: 1;
  padding: 10px;
  border-radius: 8px;
  background: rgba(232,93,117,0.08);
  color: var(--accent);
  font-size: 13px;
  transition: background 0.15s;
}
.btn-danger:hover { background: rgba(232,93,117,0.18); }

.status-badge {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
}
.status-badge.ok { background: rgba(76,175,80,0.1); color: #81c784; }
.status-badge.warn { background: rgba(255,152,0,0.1); color: #ffb74d; }

/* 隐藏文件input */
.file-input-hidden { display: none; }
```

- [ ] **Step 2: 替换设置面板占位符（`<aside class="settings-panel" id="settingsPanel">` 内）**

```html
  <aside class="settings-panel" id="settingsPanel">
    <div class="settings-header">
      <h3>设置</h3>
      <button class="close-btn" id="btnCloseSettings">✕</button>
    </div>
    <div class="settings-body">
      <div id="apiStatus"></div>

      <div class="settings-group">
        <label>API Key</label>
        <input class="settings-input" id="settingApiKey" type="password" placeholder="sk-...">
      </div>

      <div class="settings-group">
        <label>Base URL</label>
        <input class="settings-input" id="settingBaseURL" placeholder="https://ark.cn-beijing.volces.com/api/v3">
        <span class="settings-hint">豆包/DeepSeek 等 OpenAI 兼容 API 地址</span>
      </div>

      <div class="settings-group">
        <label>模型</label>
        <select class="settings-select" id="settingModel">
          <option value="doubao-lite-128k">豆包 Lite (128K)</option>
          <option value="doubao-pro-128k">豆包 Pro (128K)</option>
          <option value="deepseek-chat">DeepSeek V3</option>
          <option value="deepseek-reasoner">DeepSeek R1</option>
        </select>
      </div>

      <div class="settings-group">
        <label>温度 (Temperature)</label>
        <input class="settings-input" id="settingTemperature" type="number" min="0" max="2" step="0.1" placeholder="0.7">
        <span class="settings-hint">0 = 严谨，1 = 创意，建议情感对话 0.7-0.9</span>
      </div>

      <div class="settings-divider"></div>

      <div class="settings-actions">
        <button class="btn-primary" id="btnExport">📥 导出备份</button>
        <button class="btn-primary" id="btnImport">📤 导入备份</button>
      </div>
      <input type="file" class="file-input-hidden" id="importFileInput" accept=".json">

      <button class="btn-danger" id="btnClearData">🗑 清除所有数据</button>
    </div>
  </aside>
```

- [ ] **Step 3: 在 UIController.init() 方法中追加设置面板初始化代码**

在 `UIController.init()` 中 `this._bindEvents();` 之后追加：

```javascript
    this._bindSettingsEvents();
    this._loadSettingsToForm();
```

- [ ] **Step 4: 在 UIController 末尾（`};` 之前）追加设置相关方法**

```javascript
  /* ---- 设置面板 ---- */
  _bindSettingsEvents() {
    this._dom.btnCloseSettings = document.getElementById('btnCloseSettings');
    this._dom.btnExport = document.getElementById('btnExport');
    this._dom.btnImport = document.getElementById('btnImport');
    this._dom.btnClearData = document.getElementById('btnClearData');
    this._dom.importFileInput = document.getElementById('importFileInput');

    this._dom.btnCloseSettings.addEventListener('click', () => this._toggleSettings(false));
    this._dom.settingsOverlay.addEventListener('click', () => this._toggleSettings(false));

    // 导出
    this._dom.btnExport.addEventListener('click', () => {
      StorageManager.exportJSON();
      this._showToast('备份已下载', 'success');
    });

    // 导入
    this._dom.btnImport.addEventListener('click', () => {
      this._dom.importFileInput.click();
    });
    this._dom.importFileInput.addEventListener('change', async (e) => {
      const file = e.target.files[0];
      if (!file) return;
      try {
        const count = await StorageManager.importJSON(file);
        this._showToast(`成功导入 ${count} 个新会话`, 'success');
        this._renderSidebar();
        this._loadLastChat();
      } catch (err) {
        this._showToast(err.message, 'error');
      }
      this._dom.importFileInput.value = '';
    });

    // 清除数据
    this._dom.btnClearData.addEventListener('click', () => {
      if (!confirm('确定要清除所有数据吗？此操作不可撤销。建议先导出备份。')) return;
      localStorage.clear();
      ChatManager._currentChatId = null;
      this._renderSidebar();
      this._newChat();
      this._loadSettingsToForm();
      this._showToast('所有数据已清除', 'info');
    });

    // 表单自动保存
    ['settingApiKey', 'settingBaseURL', 'settingTemperature'].forEach(id => {
      const el = document.getElementById(id);
      const key = id.replace('setting', '').replace(/^[A-Z]/, m => m.toLowerCase()); // apiKey, baseURL, temperature
      el.addEventListener('change', () => {
        const value = id === 'settingTemperature' ? parseFloat(el.value) || 0.7 : el.value;
        SettingsManager.set(key, value);
        this._updateApiStatus();
      });
    });

    document.getElementById('settingModel').addEventListener('change', (e) => {
      SettingsManager.set('model', e.target.value);
      this._updateApiStatus();
    });
  },

  _loadSettingsToForm() {
    const s = SettingsManager.getAll();
    document.getElementById('settingApiKey').value = s.apiKey || '';
    document.getElementById('settingBaseURL').value = s.baseURL || '';
    document.getElementById('settingModel').value = s.model || 'doubao-lite-128k';
    document.getElementById('settingTemperature').value = s.temperature || 0.7;
    this._updateApiStatus();
  },

  _updateApiStatus() {
    const el = document.getElementById('apiStatus');
    if (SettingsManager.isValid()) {
      el.innerHTML = '<span class="status-badge ok">● API 已配置</span>';
    } else {
      el.innerHTML = '<span class="status-badge warn">○ API 未配置 — 请填入 Key</span>';
    }
  },

  _toggleSettings(force) {
    const isOpen = this._dom.settingsPanel.classList.contains('open');
    const shouldOpen = force !== undefined ? force : !isOpen;
    if (shouldOpen) {
      this._loadSettingsToForm();
      this._dom.settingsPanel.classList.add('open');
      this._dom.settingsOverlay.classList.add('open');
    } else {
      this._dom.settingsPanel.classList.remove('open');
      this._dom.settingsOverlay.classList.remove('open');
    }
  },
```

- [ ] **Step 5: 浏览器验证**

1. 点击 ⚙ 按钮或按 `Ctrl+,`
2. 设置面板应从右侧滑入
3. 填入 API Key、选择模型
4. 表单应自动保存到 localStorage（刷新页面后保留）

- [ ] **Step 6: 提交**

```bash
cd "C:/programs/个人项目/emotional-agent" && git add emotional-agent.html && git commit -m "✨ Task 9: 设置面板（API Key/模型/导出/导入）"
```

---

### Task 10: 键盘快捷键 + 全局错误处理

**Files:**
- Modify: `C:/programs/个人项目/emotional-agent/emotional-agent.html`

- [ ] **Step 1: 在 UIController._bindEvents 末尾追加键盘事件**

```javascript
    // 键盘快捷键
    document.addEventListener('keydown', (e) => {
      // Ctrl+N — 新对话
      if (e.ctrlKey && e.key === 'n') {
        e.preventDefault();
        this._newChat();
      }
      // Ctrl+, — 打开设置
      if (e.ctrlKey && e.key === ',') {
        e.preventDefault();
        this._toggleSettings(true);
      }
      // Esc — 关闭设置
      if (e.key === 'Escape' && this._dom.settingsPanel.classList.contains('open')) {
        this._toggleSettings(false);
      }
    });
```

- [ ] **Step 2: 在 `<script>` 最末尾、`})();` 之前追加全局错误处理**

```javascript
/* ========================================
   Global Error Handler
   ======================================== */
window.onerror = (msg, url, line, col, error) => {
  console.error('[小暖] 未捕获错误:', msg, 'at', line, ':', col);
  const toast = document.createElement('div');
  toast.className = 'toast error';
  toast.textContent = '出了点问题，刷新页面即可恢复';
  document.getElementById('toastContainer').appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
  return true; // 阻止默认浏览器错误提示
};

window.addEventListener('unhandledrejection', (e) => {
  console.error('[小暖] 未处理的Promise拒绝:', e.reason);
  const toast = document.createElement('div');
  toast.className = 'toast error';
  toast.textContent = '出了点问题，刷新页面即可恢复';
  document.getElementById('toastContainer').appendChild(toast);
  setTimeout(() => toast.remove(), 4000);
});
```

- [ ] **Step 3: 浏览器验证**

1. `Ctrl+N` → 新建对话
2. `Ctrl+,` → 打开设置面板
3. `Esc` → 关闭设置面板
4. 在 console 中执行 `throw new Error('test')` → 页面应显示 toast 而非浏览器默认弹窗

- [ ] **Step 4: 提交**

```bash
cd "C:/programs/个人项目/emotional-agent" && git add emotional-agent.html && git commit -m "✨ Task 10: 键盘快捷键+全局错误处理"
```

---

### Task 11: 集成测试与 Checklist

**Files:**
- Modify: 无新增代码，验证现有功能

- [ ] **Step 1: 功能 checklist 逐项验证**

| # | 功能 | 验证方式 |
|---|------|---------|
| 1 | 新建对话 | 点击 ＋ 或 Ctrl+N |
| 2 | 切换对话 | 点击侧边栏会话 |
| 3 | 重命名对话 | 双击侧边栏标题 |
| 4 | 删除对话 | 悬停会话 → 点 × |
| 5 | 发送消息 | 输入文本 → Enter |
| 6 | 流式回复 | 观察 Agent 逐字输出 + 闪烁光标 |
| 7 | 领域拒绝 | 输入"帮我写代码" → 淡红边框拒绝卡片（不发起API请求）|
| 8 | 危机响应 | 输入包含"自杀"的消息 → 热线响应 |
| 9 | 设置面板 | Ctrl+, → 填入 Key/模型/温度 → 自动保存 |
| 10 | 导出 JSON | 设置 → 导出 → 下载 .json 文件 |
| 11 | 导入 JSON | 设置 → 导入 → 选择文件 → 合并 |
| 12 | API Key 无效 | 用假 Key 发消息 → 弹出设置面板 + 提示 |
| 13 | 网络断开 | 断开网络发消息 → 红色错误气泡 + 重试按钮 |
| 14 | 超过20轮 | 连续对话超20轮 → 触发压缩（查看Storage中summary字段）|
| 15 | 刷新保留 | 刷新页面 → 对话和设置保留 |
| 16 | 清除数据 | 设置 → 清除所有 → 确认后清空 |

- [ ] **Step 2: 修复发现的问题**

逐项验证时如发现 bug，修复后提交。

- [ ] **Step 3: 最终提交**

```bash
cd "C:/programs/个人项目/emotional-agent" && git add emotional-agent.html && git commit -m "✅ Task 11: 集成测试通过+问题修复"
```

---

### Task 12: 补充首次使用引导

**Files:**
- Modify: `C:/programs/个人项目/emotional-agent/emotional-agent.html`

首次打开时（无 API Key），在对话区显示引导卡片。

- [ ] **Step 1: 在 UIController 中追加首次引导检查**

在 `UIController.init()` 末尾追加：

```javascript
    this._checkFirstRun();
```

在 `UIController` 末尾（`};` 之前）追加：

```javascript
  _checkFirstRun() {
    if (!SettingsManager.isValid()) {
      // 首次使用，自动弹出设置面板
      setTimeout(() => {
        this._showToast('欢迎使用小暖！请先配置 API Key', 'info');
        this._toggleSettings(true);
      }, 500);
    }
  },
```

- [ ] **Step 2: 浏览器验证**

清除 localStorage → 刷新页面 → 应自动弹出设置面板并显示 toast 引导。

- [ ] **Step 3: 最终提交**

```bash
cd "C:/programs/个人项目/emotional-agent" && git add emotional-agent.html && git commit -m "✨ Task 12: 首次使用引导+最终完善"
```

---

## 自检清单

实施完成后逐项确认：

- [ ] `file://` 直接双击打开可用（无跨域问题 — API 调用走 fetch 到外部 URL 正常）
- [ ] 所有 CSS 内联，无外部字体/图标库引用
- [ ] 所有 JS 内联，无外部依赖
- [ ] 领域拒绝在本地完成，不发 API 请求（Network 面板可验证）
- [ ] 危机响应即时显示，不等待 API
- [ ] 流式输出稳定，断网/超时/401 都有对应的用户提示
- [ ] 对话数据刷新不丢失
- [ ] JSON 导出/导入正常，按 ID 去重

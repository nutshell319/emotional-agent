# Warmth 回复人性化优化 — 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 从 Prompt 层、前端表现层、情感追踪层三方面让 Warmth 的 AI 回复更自然、更有人情味。

**Architecture:** 纯前端单文件 HTML（~3663 行），所有改动集中在 `index.html`。不引入新依赖，不改 API 通信层、记忆系统、画像系统、上下文压缩等现有模块。

**Tech Stack:** Vanilla JS + CSS + HTML，DeepSeek API（OpenAI 兼容 SSE 流式）

**源设计规格:** `docs/superpowers/specs/2026-07-14-warmth-humanization-design.md`

---

## 文件结构

| 文件 | 职责 | 改动类型 |
|------|------|----------|
| `index.html` (L1686-1736) | `getSystemPrompt()` — System Prompt 内容 | 修改 |
| `index.html` (L3167-3181) | `_createTypingIndicator()` — 思考动画 DOM | 修改 |
| `index.html` (L2248-2287) | `_splitResponse()` — 智能分段 | 修改 |
| `index.html` (L3272-3318) | `_send()` → `onAgentSegments` 回调 — 打字机动画 | 修改 |
| `index.html` (~L570-604) | CSS — 思考文案样式 | 新增 |
| `index.html` (L2086-2238 之后) | `buildContext()` — 情绪注入 | 修改 |
| `index.html` (新增位置) | `EmotionTracker` 对象 | 新增 |

---

### Task 1: System Prompt 重写 — 回复结构变异 + 情感共情前置 + 口头禅调整

**文件:** 修改 `C:\programs\个人项目\emotional-agent\index.html:1696-1706`

- [ ] **Step 1: 替换"说话风格"段落，加入结构变异和情感共情指令**

找到 L1695-1699：
```javascript
## 说话风格
- 短句快节奏，不废话。第一句给反应（吐槽/共鸣/判断），后面简短分析
- 爱用生活化的比喻把严肃问题讲成段子
- 不端咨询师的架子。给的建议是"我觉得你可以试试..."不是"建议你采取以下措施"
- 损归损，对方真难过的时候别抖机灵
```

替换为：
```javascript
## 说话风格
- 短句快节奏，不废话。第一句给反应（吐槽/共鸣/判断），后面简短分析
- 爱用生活化的比喻把严肃问题讲成段子
- 不端咨询师的架子。给的建议是"我觉得你可以试试..."不是"建议你采取以下措施"
- 损归损，对方真难过的时候别抖机灵

## 回复结构变异（重要）
不要每次都按"吐槽→分析→建议"的模板回复。
偶尔直接给建议，偶尔先反问再分析，偶尔只共情不给建议。
连续两条回复的结构不能相同。

## 情感共情前置（最高优先级）
对方情绪明显时（难过/愤怒/焦虑/委屈），第一句话必须先接住情绪。
参考句式："好难受啊这种感觉""气死了我能理解""换我我也烦"
禁止跳过情绪直接开始分析。情绪没被接住就开始给建议 = 机器人。
```

- [ ] **Step 2: 移除"说人话就是"，加入替换口头禅 + 避免重复约束**

找到 L1702-1706：
```javascript
## 口头禅（每句回复自然地用）
吐槽离谱时：闹麻了 / 麻闹了 / 绷不住了 / 离谱 / 666
泼冷水时：别搞 / 别搞了 / 差不多得了
共鸣时：包的 / 确实
口头句式：说人话就是... / 不是我说你... / 咱就是说...
```

替换为：
```javascript
## 口头禅（每句回复自然地用）
吐槽离谱时：闹麻了 / 麻闹了 / 绷不住了 / 离谱
泼冷水时：别搞 / 别搞了 / 差不多得了
共鸣时：包的 / 确实 / 我懂
过渡句式：说白了就是... / 你想想... / 我问你... / 不是我说你... / 咱就是说...

## 避免重复
同一场对话中，同一个口头禅最多用2次，同一个句式不要连续使用。
如果上一句用了"包的"，下一句共鸣时换"确实"或"我懂"。
```

- [ ] **Step 3: 验证 Prompt 字符串无语法错误**

在浏览器中打开 `index.html`，打开控制台，执行：
```javascript
console.log(getSystemPrompt('Warmth'));
```
预期：完整输出 System Prompt，无 JS 错误，字符串中无未转义字符。

- [ ] **Step 4: 提交**

```bash
git add "C:/programs/个人项目/emotional-agent/index.html"
git commit -m "💬 System Prompt重写：结构变异+情感共情前置+口头禅去重"
```

---

### Task 2: 思考动画升级 — 随机文案 + 三圆点轮播

**文件:** 修改 `C:\programs\个人项目\emotional-agent\index.html`

涉及两处：CSS（新增思考文案样式）和 JS（`_createTypingIndicator` 改造）。

- [ ] **Step 1: 新增思考文案 CSS 样式**

在 L604（`@keyframes avatarPulse` 闭合 `}` 之后）插入：
```css
/* 思考文案淡入淡出 */
.thinking-text {
  font-size: 12px;
  color: var(--text-dim);
  margin-right: 4px;
  opacity: 0;
  transition: opacity 0.4s ease;
}
.thinking-text.show { opacity: 1; }
```

- [ ] **Step 2: 改造 `_createTypingIndicator()` 加入文案轮播**

找到 L3167-3182，将整个方法替换为：
```javascript
  _createTypingIndicator() {
    const name = SettingsManager.getAll().agentName || 'Warmth';
    const row = document.createElement('div');
    row.className = 'msg-row agent thinking';
    row.id = 'typingIndicator';
    row.innerHTML = `
      <div class="msg-avatar">👧🏻</div>
      <div class="msg-content">
        <div class="msg-bubble">
          <span class="thinking-text"></span>
          <span class="thinking-dot"></span>
          <span class="thinking-dot"></span>
          <span class="thinking-dot"></span>
        </div>
      </div>`;

    // 随机思考文案轮播（每1.5秒切换）
    const texts = [
      '正在理解你的感受…',
      '让我想想…',
      '在打字了…',
      '嗯，我想说…',
      '让我组织一下语言…',
      '这事儿得好好想想…',
    ];
    const textEl = row.querySelector('.thinking-text');
    let idx = Math.floor(Math.random() * texts.length);
    textEl.textContent = texts[idx];
    textEl.classList.add('show');

    row._thinkingTimer = setInterval(() => {
      textEl.classList.remove('show');
      setTimeout(() => {
        idx = (idx + 1) % texts.length;
        textEl.textContent = texts[idx];
        textEl.classList.add('show');
      }, 400); // 等淡出完成再切换
    }, 1500);

    return row;
  },
```

- [ ] **Step 3: 确保思考动画移除时清除定时器**

在 `_send()` 的 `onAgentSegments` 回调中，`typing.remove()` 之前（L3274），增加定时器清除：
```javascript
      onAgentSegments: async (segments) => {
        // 清除思考文案轮播定时器
        if (typing._thinkingTimer) {
          clearInterval(typing._thinkingTimer);
          typing._thinkingTimer = null;
        }
        // 移除思考动画
        typing.remove();
```

- [ ] **Step 4: 同样处理 `_continueResponse()` 中的 thinking 清除**

在 L3388-3390 的 `_continueResponse()` 方法中，`retryLast().then()` 回调里的 `typing.remove()` 之前也加清除：
```javascript
    ChatManager.retryLast().then(() => {
      if (typing._thinkingTimer) { clearInterval(typing._thinkingTimer); typing._thinkingTimer = null; }
      typing.remove();
```
以及 catch 回调中同样处理。

- [ ] **Step 5: 验证思考动画**

在浏览器中打开应用，发送一条消息，观察思考动画：
- 三圆点旁出现思考文案
- 文案每 1.5 秒切换（带淡入淡出）
- 回复开始后定时器被清除，无控制台报错

- [ ] **Step 6: 提交**

```bash
git add "C:/programs/个人项目/emotional-agent/index.html"
git commit -m "✨ 思考动画升级：随机文案轮播+淡入淡出"
```

---

### Task 3: 回复前随机停顿 + 打字速度三段式 + 段间动态停顿 + 长回复拆分

**文件:** 修改 `C:\programs\个人项目\emotional-agent\index.html`

这四个改动都在 `_send()` 的 `onAgentSegments` 回调和 `_splitResponse()` 中，放一个 Task 减少上下文切换。

- [ ] **Step 1: 回复前随机停顿（300-900ms）**

在 L3274 `typing.remove()` 之后，分段循环之前，插入停顿：

找到 L3274-3276：
```javascript
        // 移除思考动画
        typing.remove();

        // 后台已分好段 → 逐段打字机效果 + 头像只在最新段显示
```

替换为：
```javascript
        // 移除思考动画
        typing.remove();

        // 回复前随机停顿（300-900ms），模拟"看完消息→思考→开始打字"
        const preDelay = 300 + Math.floor(Math.random() * 600);
        await this._sleep(preDelay);
        if (this._animId !== animId) return;

        // 后台已分好段 → 逐段打字机效果 + 头像只在最新段显示
```

- [ ] **Step 2: 三段式打字速度（替换固定 speed）**

找到 L3306-3315 的打字机循环：
```javascript
          // 打字机逐字输出（速度自适应段落长度）
          const bubbleEl = row.querySelector('.msg-bubble');
          const cleaned = this._stripMarkdown(segments[i]);
          const speed = getTypeSpeed(cleaned);
          for (let j = 0; j < cleaned.length; j++) {
            if (this._animId !== animId) return;
            bubbleEl.textContent += cleaned[j];
            this._scrollToBottom();
            await this._sleep(speed);
          }
```

替换为：
```javascript
          // 打字机逐字输出（三段式变速：慢-快-慢，模拟真人打字节奏）
          const bubbleEl = row.querySelector('.msg-bubble');
          const cleaned = this._stripMarkdown(segments[i]);
          const len = cleaned.length;
          for (let j = 0; j < len; j++) {
            if (this._animId !== animId) return;
            bubbleEl.textContent += cleaned[j];
            this._scrollToBottom();

            // 短消息（<30字）不减速，保持灵动
            let speed;
            if (len < 30) {
              speed = 22;
            } else {
              const pos = j / len;
              if (pos < 0.2 || pos > 0.8) {
                speed = 22; // 开头和结尾 20%：慢（22ms），模拟斟酌措辞和收尾确认
              } else {
                speed = 15; // 中间 60%：正常速度（15ms），流畅输出
              }
            }
            await this._sleep(speed);
          }
```

- [ ] **Step 3: 段间动态停顿（替换固定 280ms）**

找到 L3277 的固定 `segmentGap`：
```javascript
        const segmentGap = 280;  // 段与段之间的停顿 ms
```

替换为动态函数，并替换 L3290 的 `await this._sleep(segmentGap)`：

将 L3277 改为：
```javascript
        // 段间停顿根据下一段长度动态调整
        const getSegmentGap = (nextText) => {
          const len = (nextText || '').length;
          if (len < 80) return 200 + Math.floor(Math.random() * 200);    // 200-400ms
          if (len < 200) return 350 + Math.floor(Math.random() * 250);   // 350-600ms
          return 500 + Math.floor(Math.random() * 400);                  // 500-900ms
        };
```

将 L3290：
```javascript
          if (i > 0) await this._sleep(segmentGap);
```

替换为：
```javascript
          if (i > 0) await this._sleep(getSegmentGap(segments[i]));
```

- [ ] **Step 4: 移除不再使用的 `getTypeSpeed` 函数**

三段式变速替代了原来的 `getTypeSpeed`，删掉 L3278-3283：
```javascript
        const getTypeSpeed = (text) => {
          const len = text.length;
          if (len < 50) return 22;     // 短段落慢一点，有"斟酌措辞"感
          if (len < 150) return 15;    // 中等段落正常速度
          return 10;                    // 长段落略快，减少等待感
        };
```

- [ ] **Step 5: `_splitResponse()` 增加长回复拆分（>350字拆2条）**

找到 L2248-2287 的 `_splitResponse()` 方法，在现有分段逻辑之前（L2264 之前）插入长回复检测：

在 L2262 `const totalLen = ...` 之后，L2264 `// 只有一段或整体很短 → 不拆分` 之前，插入：
```javascript
    // 超长单段回复：超过350字强制拆分（模拟真人分几次发消息）
    if (totalLen > 350 && segments.length === 1 && segments[0].length > 350) {
      const text = segments[0];
      // 在句号/问号/感叹号处寻找合适断点（后半段的40%-60%范围）
      const midStart = Math.floor(text.length * 0.4);
      const midEnd = Math.floor(text.length * 0.6);
      let splitPos = text.indexOf('。', midStart);
      if (splitPos === -1 || splitPos > midEnd) splitPos = text.indexOf('？', midStart);
      if (splitPos === -1 || splitPos > midEnd) splitPos = text.indexOf('！', midStart);
      if (splitPos === -1 || splitPos > midEnd) splitPos = text.indexOf('\n', midStart);
      if (splitPos === -1 || splitPos > midEnd) splitPos = Math.floor(text.length / 2); // 找不到断点就硬切
      const part1 = text.slice(0, splitPos + 1).trim();
      const part2 = text.slice(splitPos + 1).trim();
      console.log('[Split] 长回复拆分（' + totalLen + '字）→ ' + part1.length + '字 + ' + part2.length + '字');
      return [part1, part2];
    }
```

- [ ] **Step 6: 验证前端表现层改动**

在浏览器中：
1. 发送消息，观察回复前有 300-900ms 停顿
2. 观察打字机开头和结尾比中间慢
3. 多条消息时观察段间停顿不同（短段快、长段慢）
4. 发一条让 AI 输出长回复（如"详细分析一下回避型依恋"），验证 >350 字是否拆成 2 条

- [ ] **Step 7: 提交**

```bash
git add "C:/programs/个人项目/emotional-agent/index.html"
git commit -m "🎭 前端表现层优化：随机停顿+三段式变速打字+动态段间停顿+长回复拆分"
```

---

### Task 4: 情感状态追踪 — EmotionTracker 对象

**文件:** 修改 `C:\programs\个人项目\emotional-agent\index.html`

- [ ] **Step 1: 新增 `EmotionTracker` 对象**

在 `UserMemoryManager` 对象之后（L1541 之后，`/* ========================================` 注释块之前）插入：

```javascript
/* ========================================
   EmotionTracker — 情感状态追踪（关键词检测，零API调用）
   ======================================== */
const EmotionTracker = {
  /** 情绪关键词库 */
  keywords: {
    sad: ['分手', '失去', '想哭', '难受', '撑不住', '心碎', '崩溃', '抑郁', '孤独',
          '好累', '绝望', '哭', '心累', '撑不下去', '好难过', '好痛', '走不出来'],
    angry: ['气死了', '凭什么', '太过分', '受不了', '恶心', '傻逼', '无语', '火大',
            '气死', 'tm', '他妈', '想骂人', '气炸', '忍不了', '无耻', '不要脸'],
    anxious: ['怎么办', '万一', '好怕', '担心', '睡不着', '纠结', '迷茫', '不知道',
              '焦虑', '紧张', '害怕', '不安', '不确定', '慌', '怕', '很慌'],
  },

  /** 检测最近N条用户消息的情绪状态 */
  detect(chat, lookback = 3) {
    if (!chat || !chat.messages) return 'calm';

    const userMsgs = chat.messages
      .filter(m => m.role === 'user')
      .slice(-lookback)
      .map(m => m.content);

    if (userMsgs.length === 0) return 'calm';

    const scores = { sad: 0, angry: 0, anxious: 0 };

    for (const msg of userMsgs) {
      for (const [mood, words] of Object.entries(this.keywords)) {
        for (const word of words) {
          if (msg.includes(word)) {
            scores[mood] = (scores[mood] || 0) + 1;
          }
        }
      }
    }

    // 找出得分最高的情绪，需要 ≥ 2 分才激活
    const maxScore = Math.max(scores.sad, scores.angry, scores.anxious);
    if (maxScore < 2) return 'calm';

    // 同分优先级：难过 > 愤怒 > 焦虑
    if (scores.sad >= maxScore) return 'sad';
    if (scores.angry >= maxScore) return 'angry';
    if (scores.anxious >= maxScore) return 'anxious';
    return 'calm';
  },

  /** 获取情绪对应的 Prompt 注入文本 */
  getInjection(mood) {
    const injections = {
      sad: '\n\n[情绪感知：对方现在情绪低落，第一句话先共情和陪伴，不要急着分析和给建议。语气温柔一点。]',
      angry: '\n\n[情绪感知：对方现在很生气，先认可TA的情绪——"确实气人""换谁谁不气"——然后再帮TA理性分析。别泼冷水火上浇油。]',
      anxious: '\n\n[情绪感知：对方现在很焦虑，你给的建议要比平时更具体和确定，少用反问和留白，多用"我觉得你可以…"的明确指引来帮TA稳住。]',
      calm: '',
    };
    return injections[mood] || '';
  },
};
```

- [ ] **Step 2: 在 `buildContext()` 中注入情绪感知**

找到 L2234（场景注入的 `context[0].content += sceneText;` 之后，`}`闭合之前），在场景文本追加后、`return` 之前插入情绪注入：

在 L2234 `context[0].content += sceneText;` 之后、L2235 `}` 之前：
```javascript
      context[0].content += sceneText;

      // 情感状态追踪注入（在场景描述之后）
      const mood = EmotionTracker.detect(chat);
      const moodInjection = EmotionTracker.getInjection(mood);
      if (moodInjection) {
        context[0].content += moodInjection;
      }
    }
```

完整替换 L2234-2235：
```javascript
      context[0].content += sceneText;

      // 情感状态追踪注入（在场景描述之后）
      const mood = EmotionTracker.detect(chat);
      const moodInjection = EmotionTracker.getInjection(mood);
      if (moodInjection) {
        context[0].content += moodInjection;
      }
    }

    return context.concat(chat.messages);
```

- [ ] **Step 3: 验证 EmotionTracker**

在浏览器控制台中手动测试：
```javascript
// 模拟难过场景
const chat = { messages: [
  { role: 'user', content: '我真的好难受，感觉撑不住了' },
  { role: 'user', content: '分手之后每天都想哭' },
] };
console.log(EmotionTracker.detect(chat)); // 预期: 'sad'

// 模拟平静场景
const chat2 = { messages: [
  { role: 'user', content: '今天天气不错' },
] };
console.log(EmotionTracker.detect(chat2)); // 预期: 'calm'
```

- [ ] **Step 4: 提交**

```bash
git add "C:/programs/个人项目/emotional-agent/index.html"
git commit -m "💜 情感状态追踪：关键词检测+情绪感知Prompt注入"
```

---

### Task 5: 端到端验证 + 最终提交

- [ ] **Step 1: 完整功能验证**

在浏览器中打开应用，依次测试：

| 测试场景 | 操作 | 预期 |
|----------|------|------|
| 思考动画 | 发送任意消息 | 三圆点旁出现随机思考文案，每1.5s切换 |
| 回复前停顿 | 等待流式响应结束 | 去掉思考动画后有300-900ms停顿才出第一个字 |
| 三段变速 | 观察较长的回复 | 开头慢 → 中间正常 → 结尾慢 |
| 段间停顿 | 回复有2-3段 | 每段间停顿时间不同，短段快长段慢 |
| 长回复拆分 | 问"详细分析一下怎么追内向的女生" | 超过350字的回复拆成2条独立消息 |
| System Prompt | 连续对话多轮 | 回复不总是"吐槽→分析→建议"，"说人话就是"不再出现 |
| 情绪检测-难过 | 输入"分手了好难受，每天晚上都哭" | 回复先共情再分析 |
| 情绪检测-愤怒 | 输入"气死了他怎么这么过分" | 回复先认可情绪再分析 |
| 情绪检测-焦虑 | 输入"好焦虑啊睡不着怎么办" | 给具体确定建议 |

- [ ] **Step 2: 确认无回归**

- 流式输出正常（不卡顿）
- 打字机动画可被新消息打断（animId 机制正常）
- 图片 OCR 流程正常
- 设置面板、对话切换、侧边栏均正常
- 控制台无报错

- [ ] **Step 3: 最终提交**

```bash
git add "C:/programs/个人项目/emotional-agent/index.html"
git commit -m "✅ Warmth回复人性化优化完成：Prompt+前端+情感追踪三层联动"
```

---

## 自检清单

- [x] 所有代码改动有完整的 before/after，无 TBD/TODO
- [x] 每个 Task 有明确的文件路径和行号
- [x] 模块之间无冲突（EmotionTracker 独立对象，不依赖其他模块）
- [x] 不改架构、不引入新依赖
- [x] 情绪检测零 API 调用
- [x] 向后兼容：现有功能（流式、记忆、画像等）不受影响

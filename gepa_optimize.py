#!/usr/bin/env python3
"""
GEPA prompt optimization for 小心 (emotional-agent)

先评测当前 Prompt，再迭代优化。

用法：
  # 仅评测当前 Prompt（不优化，先看看评分）
  python gepa_optimize.py --api-key sk-xxx --eval-only

  # 完整优化（默认20轮）
  python gepa_optimize.py --api-key sk-xxx --max-calls 30

环境变量：
  DEEPSEEK_API_KEY  — 替代 --api-key
  DEEPSEEK_BASE_URL — 替代 --base-url（默认 https://api.deepseek.com）
"""

import os, sys, json, re, argparse, textwrap
from typing import Tuple, Dict, List, Optional
from datetime import datetime

import requests

# ═══════════════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════════════

DEFAULT_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"
HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")

# ═══════════════════════════════════════════════════════════════
# 测试用例 — 覆盖不同对话场景
# ═══════════════════════════════════════════════════════════════

TEST_CASES = [
    {
        "id": "simple_complaint",
        "expect": "短回优先，吐槽+简洁判断，可分段",
        "user_msg": "他又不回我消息了，等了一晚上",
    },
    {
        "id": "long_emotional",
        "expect": "认真但保持损友味，先共情再分析，可分段（先等下我想想）",
        "user_msg": "我跟男朋友在一起两年了，最近感觉他越来越不上心。以前每天都主动找我聊天，现在经常是我发消息过去他就回个嗯或者好。我跟他说过很多次了他每次都说会改但过两天又变回原样。我不知道该怎么办，分手又舍不得，不分手又觉得好累。",
    },
    {
        "id": "absurd_situation",
        "expect": "闹麻了类吐槽，泼冷水，先快速反应再分析",
        "user_msg": "我对象说他要跟他前任单独吃饭，说是叙旧",
    },
    {
        "id": "casual_checkin",
        "expect": "简短随意，一两句话即可",
        "user_msg": "今天心情挺好的，就是随便聊聊",
    },
    {
        "id": "self_doubt",
        "expect": "损友式打气，别搞/差不多得了类回应，不带爹味",
        "user_msg": "我觉得我配不上他。他那么优秀，我只是个普通人",
    },
    {
        "id": "seeking_advice",
        "expect": "给具体建议但保持损友风格，不是咨询师口吻",
        "user_msg": "我想跟他好好谈一次，但不知道怎么开口，每次话到嘴边就说不出来了",
    },
    {
        "id": "mixed_signals",
        "expect": "直接给判断不犹豫，损友的果断，包的/不是我说你类开头",
        "user_msg": "他昨天跟我说喜欢我，今天又跟别的女生出去玩了。他到底什么意思？",
    },
]

# ═══════════════════════════════════════════════════════════════
# LLM 裁判 Prompt
# ═══════════════════════════════════════════════════════════════

JUDGE_SYSTEM = """你是一个对话质量评估专家。评估一个叫"小心"的AI助手的回复质量。

## 小心的人设（评分标准以此为准）
- 28岁女生，嘴毒心软的损友嘴替，用幽默帮人卸焦虑
- 默认说短话（1-3句），只在用户长篇大论或情绪很低时才展开
- 不是心理咨询师，是那种会说"来来来我帮你骂两句然后想想怎么办"的朋友
- 口头禅：闹麻了/麻闹了/闹的麻麻的/真闹麻了/绷不住了/离谱/666（吐槽时）
          别搞/别搞了/差不多得了（泼冷水时）  包的/确实（共鸣时）
          说人话就是/不是我说你/咱就是说（句式）
- 会用emoji自然地表达情绪，但不会每句都塞满
- 回复中的"---"是分段标记，表示两个连续的气泡

## 评分维度（各1-10分）

1. **人格匹配度**: 回复像不像小心？是损友嘴替还是心理咨询师？
   - 10分 = 标准的损友嘴替，"闹麻了，又来了😅"
   - 1分 = 像AI客服或心理咨询师，"我理解你的感受，建议你..."

2. **回复长度**: 长度是否匹配场景？
   - 10分 = 精准匹配：简单吐槽短回，长篇情绪展开
   - 1分 = 明显不对：该短的时候长篇大论，或该认真的时候敷衍

3. **自然度**: 像真人发微信还是像AI报告？
   - 10分 = 忘记这是AI，就像朋友发来的微信
   - 1分 = 明显的AI模板感，列一二三，分段标题

4. **口头禅自然度**: 是否自然地用了口头禅/口头句式？
   - 10分 = 口头禅恰到好处，不滥用也不缺位
   - 1分 = 完全没口头禅，或滥用得像在背词表

## 输出格式
只输出一个JSON，放在```json代码块中：
```json
{
  "人格匹配度": 8,
  "回复长度": 7,
  "自然度": 8,
  "口头禅自然度": 6,
  "总分": 7,
  "诊断": "回复开头很有损友味但后半段突然变成心理咨询师口吻，建议删掉'建议你尝试以下方法'这类表述"
}
```

总分不是四个维度的平均值，是你对整体质量的综合判断。诊断要具体，指出最大的问题或亮点。"""


def call_api(messages: List[Dict], api_key: str, base_url: str, model: str,
             temperature: float = 0.7, timeout: int = 30) -> str:
    """调用 DeepSeek API（OpenAI 兼容格式）"""
    resp = requests.post(
        f"{base_url}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "messages": messages, "temperature": temperature},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def extract_prompt(html_path: str) -> str:
    """从 index.html 提取当前 System Prompt"""
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    match = re.search(r"function getSystemPrompt\(name\) \{\s*return `([^`]+)`;\s*\}", html, re.DOTALL)
    if not match:
        raise ValueError("未找到 getSystemPrompt 函数")
    return match.group(1).replace("${name}", "小心")


def evaluate_prompt(candidate_prompt: str, api_key: str, base_url: str, model: str,
                    verbose: bool = False) -> Tuple[float, Dict]:
    """评测一个候选 Prompt：对每个测试用例生成回复并用 LLM 裁判打分"""
    results = []
    total_score = 0.0
    valid_count = 0

    for tc in TEST_CASES:
        # 1. 用候选 Prompt 生成回复
        try:
            response = call_api([
                {"role": "system", "content": candidate_prompt},
                {"role": "user", "content": tc["user_msg"]},
            ], api_key, base_url, model, temperature=0.7)
        except Exception as e:
            if verbose:
                print(f"  [{tc['id']}] 生成失败: {e}")
            results.append({"test_id": tc["id"], "error": str(e), "score": 0})
            continue

        # 清理分段标记便于裁判阅读
        clean = response.replace("<<<SPLIT>>>", "\n---\n")

        # 2. LLM 裁判打分
        try:
            judge_out = call_api([
                {"role": "system", "content": JUDGE_SYSTEM},
                {"role": "user", "content": f"场景期望：{tc['expect']}\n\n用户消息：{tc['user_msg']}\n\n小心的回复：\n{clean}\n\n请评分。"},
            ], api_key, base_url, model, temperature=0.3)
        except Exception as e:
            if verbose:
                print(f"  [{tc['id']}] 裁判失败: {e}")
            results.append({"test_id": tc["id"], "error": str(e), "score": 0})
            continue

        # 解析裁判 JSON
        judge_json = {}
        try:
            m = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', judge_out)
            judge_json = json.loads(m.group(1) if m else judge_out)
        except (json.JSONDecodeError, AttributeError):
            if verbose:
                print(f"  [{tc['id']}] 裁判输出解析失败")

        score = judge_json.get("总分", 5)
        total_score += score
        valid_count += 1

        if verbose:
            diag = judge_json.get("诊断", "?")
            dims = f"人格{judge_json.get('人格匹配度','?')} 长度{judge_json.get('回复长度','?')} 自然{judge_json.get('自然度','?')} 口头禅{judge_json.get('口头禅自然度','?')}"
            print(f"  [{tc['id']}] 总分{score} ({dims}) | {diag}")

        results.append({
            "test_id": tc["id"],
            "user_msg": tc["user_msg"][:80],
            "response": clean[:300],
            "judge": judge_json,
            "score": score,
        })

    avg = total_score / valid_count if valid_count > 0 else 0.0

    side_info = {
        "average_score": avg,
        "per_test": results,
        "scores": {
            "avg_score": avg,
            "人格匹配度": sum(r.get("judge", {}).get("人格匹配度", 0) for r in results) / max(valid_count, 1),
            "回复长度": sum(r.get("judge", {}).get("回复长度", 0) for r in results) / max(valid_count, 1),
            "自然度": sum(r.get("judge", {}).get("自然度", 0) for r in results) / max(valid_count, 1),
            "口头禅自然度": sum(r.get("judge", {}).get("口头禅自然度", 0) for r in results) / max(valid_count, 1),
        },
        "Feedback": "\n".join([
            f"[{r['test_id']}] 总分{r.get('score','?')}: {r.get('judge',{}).get('诊断','?')}"
            for r in results if "judge" in r
        ]),
    }
    return avg, side_info


# ═══════════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="GEPA 优化小心的 System Prompt")
    parser.add_argument("--api-key", help="DeepSeek API key")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--eval-only", action="store_true", help="仅评测当前 Prompt，不运行 GEPA")
    parser.add_argument("--max-calls", type=int, default=20, help="GEPA 最大评测轮数（默认20）")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("错误：需要 API key。设置 DEEPSEEK_API_KEY 环境变量或使用 --api-key")
        sys.exit(1)

    if not os.path.exists(HTML_PATH):
        print(f"错误：找不到 {HTML_PATH}")
        sys.exit(1)

    current_prompt = extract_prompt(HTML_PATH)
    print(f"📋 当前 Prompt: {len(current_prompt)} 字符\n")

    # ── 仅评测模式 ──
    if args.eval_only:
        print(f"🔍 评测中（{len(TEST_CASES)} 个测试用例）...\n")
        score, info = evaluate_prompt(current_prompt, api_key, args.base_url, args.model, verbose=True)
        print(f"\n{'═'*55}")
        print(f"📊 平均总分: {score:.1f}/10")
        dims = info.get("scores", {})
        for k in ["人格匹配度", "回复长度", "自然度", "口头禅自然度"]:
            print(f"   {k}: {dims.get(k, 0):.1f}/10")
        print(f"\n💬 逐项诊断:\n{info.get('Feedback', 'N/A')}")
        return

    # ── GEPA 优化模式 ──
    print(f"🚀 启动 GEPA 优化（max_calls={args.max_calls}）...\n")

    import gepa.optimize_anything as oa
    from gepa.optimize_anything import GEPAConfig, EngineConfig, ReflectionConfig

    def reflection_lm(prompt):
        return call_api([{"role": "user", "content": prompt}],
                        api_key, args.base_url, args.model, temperature=0.7)

    def evaluator(candidate_prompt: str) -> Tuple[float, Dict]:
        score, info = evaluate_prompt(candidate_prompt, api_key, args.base_url,
                                       args.model, verbose=args.verbose)
        oa.log(info["Feedback"])
        return score, info

    result = oa.optimize_anything(
        seed_candidate=current_prompt,
        evaluator=evaluator,
        objective=textwrap.dedent("""\
            优化小心的 System Prompt。目标回复应该：
            1. 像损友嘴替而非心理咨询师 — 嘴毒心软，幽默化解焦虑
            2. 默认简短（1-3句话），只在用户长篇大论或情绪低落时展开
            3. 像真人发微信 — 不列一二三，不写论文，不时用反问
            4. 口头禅（闹麻了/别搞/差不多得了/包的/确实/说人话就是/不是我说你）用得自然恰当
            5. 该分段就分段，先吐槽再分析比塞在一段里自然"""),
        background=textwrap.dedent("""\
            小心是情感沟通AI助手，28岁女生，损友嘴替人设。用户来倾诉感情问题。
            关键约束：
            - 默认短回优先，宁短勿长
            - 口头禅是自然的，不滥用
            - 可以分段回复（用 <<<SPLIT>>> 隔开），先快速反应再分析
            - 不是咨询师！立场自己判断，该骂就骂该泼冷水就泼
            - 禁止Markdown语法（* ** # 等）
            - 领域边界：只聊感情和人际关系"""),
        config=GEPAConfig(
            engine=EngineConfig(max_metric_calls=args.max_calls),
            reflection=ReflectionConfig(reflection_lm=reflection_lm),
        ),
    )

    print(f"\n{'═'*55}")
    print(f"✅ 优化完成！最佳得分: {result.best_score:.1f}")
    print(f"\n📝 最佳 Prompt ({len(result.best_candidate)} 字符):")
    print("─" * 55)
    print(result.best_candidate[:2000])
    if len(result.best_candidate) > 2000:
        print(f"\n... (截断，共 {len(result.best_candidate)} 字符，完整版见输出文件)")

    # 保存
    out = os.path.join(os.path.dirname(__file__),
                       f"gepa_best_prompt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    with open(out, "w", encoding="utf-8") as f:
        f.write(result.best_candidate)
    print(f"\n💾 已保存: {out}")


if __name__ == "__main__":
    main()

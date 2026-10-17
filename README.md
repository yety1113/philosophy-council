# 哲学十二镜议会

**Philosophy Council of Twelve Perspectives**

从日常经验出发，经由十二种哲学视角的论辩，抵达值得重新思考的问题。

一个可安装的 Codex 本地插件：以技能指令主持思辨，以 Python MCP 服务提供镜头档案、议会规划及论证结构检查。它与“心理学十二镜议会”独立共存。

心理版关注经验与行为为何如此；哲学版追问理解世界的概念、前提与价值是否成立。目标不是十二位名人轮流说金句，而是让论证遭遇真正的反驳。

## 十二镜

| 镜头 | 代表人物 | 核心任务 |
|---|---|---|
| 存在主义 | 克尔凯郭尔、萨特、加缪 | 处境中的选择、自由与责任 |
| 现象学 | 胡塞尔、海德格尔、梅洛-庞蒂 | 描述经验如何显现 |
| 分析哲学 | 罗素、维特根斯坦、奎因 | 澄清语言、概念和推理 |
| 认识论 | 笛卡尔、休谟、康德 | 审查信念与知识的正当性 |
| 形而上学 | 亚里士多德、斯宾诺莎、莱布尼茨 | 存在、因果、同一性与可能性 |
| 辩证哲学 | 黑格尔、马克思 | 矛盾、关系和历史条件 |
| 权力与谱系学 | 尼采、福柯 | 价值、分类与制度的生成 |
| 伦理学 | 亚里士多德、康德、密尔 | 德性、义务与后果的冲突 |
| 政治与社会哲学 | 卢梭、阿伦特、罗尔斯 | 自由、正义与公共生活 |
| 道家哲学 | 老子、庄子 | 区分、控制、无为与生活标准 |
| 佛教哲学 | 龙树、世亲、寂天 | 缘起、自我与自性预设 |
| 实用主义 | 皮尔士、詹姆斯、杜威 | 意义、实践后果与可修正探究 |

这是有交叉的工作分类，不是完整哲学史。同席人物并不共享全部观点，道家与佛教也不能相互替代。方法、局限和阅读线索见 [镜头档案](skills/philosophy-council/references/lenses.md)。这些线索不是已经核验的原文引用。

## 苏格拉底式主持人

主持人不占席位、不投票，负责追问“凭什么相信？”并检查概念偷换、隐含前提、无效推论、最强反例和表面共识。它要求各镜回应质询并修订论证；无法化解的规范或本体论分歧可以保留。

六个模块可独立或组合使用：独立思辨、哲学论辩、概念解剖、前提追溯、思想实验、命题生成。

四种模式：

- **快速思辨**：默认，由宿主选择3–4镜，说明理由。
- **十二镜全议会**：覆盖十二镜，再聚焦2–4个主要冲突。
- **深度哲学研究**：概念史、原典、论证与反驳；需要宿主提供检索能力。
- **哲学创作工坊**：先检验思想，再生成随笔、口播或候选命题。

标准流程：澄清命题 → 重构问题 → 独立立论 → 交叉质询 → 回应修正 → 保留分歧的思想成果。每个主论证包含前提、推论、结论、反例和适用范围。结果包括重定义的问题、竞争立场、未解矛盾、暂定命题及下一步问题。

## 安装

需要 Python 3.9+、支持本地插件的 Codex 和可用的 `codex` 命令。服务仅用 Python 标准库，无额外依赖、账号或 API 密钥；哲学回答由宿主模型生成，仍使用宿主的正常额度。

在仓库根目录执行：

```sh
python3 -m unittest discover -s tests -v
python3 scripts/install_local.py
```

安装器复制插件到独立本地目录，通过 Codex 注册专属 marketplace 并安装，不修改已有 Personal 市场。目标已存在时停止，避免覆盖修改。需要另一位置可传 `--destination /absolute/path`。

手动安装也可直接注册当前仓库（之后移动仓库会影响来源）：

```sh
codex plugin marketplace add /absolute/path/to/philosophy-council
codex plugin add philosophy-council@philosophy-council
codex plugin list
```

安装后新开聊天，输入 `$philosophy-council` 或自然语言请求。若目录未刷新，重启应用后检查插件目录；不要把文件复制完成等同于客户端已加载。官方包装和安装说明：[Package your plugin](https://developers.openai.com/plugins/build/plugins)。本包提供兼容 manifest 与便携 manifest；不同宿主的 MCP 路径变量支持可能不同，应在目标客户端验证。

卸载：

```sh
codex plugin remove philosophy-council@philosophy-council
codex plugin marketplace remove philosophy-council
```

## 使用示例

```text
用哲学十二镜议会快速讨论：人应该成为最好的自己吗？
进入十二镜全议会：只要拥有心力，就有无限可能吗？
做前提审计：如果没有实现理想，我的人生就是失败的。
用道家、伦理学和实用主义交叉质询“凡事都必须有用”。
构造思想实验：没有别人理解的人，能拥有完整自我吗？一次只改变一个变量。
进入研究模式：比较中观的空与虚无主义，核对原典，不能编页码。
进入创作工坊：把“如果世界足够有趣，有些事就不那么重要”发展为口播，并保留最强反例。
继续 / 换镜 / 让他们回应最强反驳 / 总结 / 结束
```

[完整示范与验收场景](EXAMPLES.md)展示输出标准。输出是可修正的哲学分析；不得冒充历史人物原话，也不保证命题原创。区分原典观点、常见解释、当代延伸与本轮推论。无法核对来源时明确未核验。

## 实现与工具

- `skills/philosophy-council/`：实际主持行为和镜头方法。
- `data/lenses.json`：十二镜结构化档案。
- `server/philosophy_council_mcp.py`：MCP JSON-RPC stdio 服务。
- `council_lenses`：返回档案。
- `council_plan(topic, mode, lenses?)`：返回阶段、候选席位与主持任务。`mode` 为 `quick/full/research/creative`；镜头ID见JSON。全议会始终返回十二镜。
- `council_audit(arguments)`：检查 `premises/inference/conclusion/counterexample/scope` 是否缺失；不判断逻辑有效性或历史准确性。

服务不调用模型、不连接网络、不持久化议题、不自动读取私人文件。框架工具不是哲学答案生成器；没有宿主模型时只能得到规划和结构检查。技能可在 MCP 不可用时直接主持。

## 验证与开发

```sh
python3 -m unittest discover -s tests -v
```

测试覆盖十二镜唯一性、四模式、全议会覆盖、选席、输入拒绝、论证缺项、真实子进程握手和工具调用、通知静默、错误恢复及任意工作目录启动。自动测试只能验证程序行为；哲学质量还需按 EXAMPLES.md 人工评估，不能以字段完整冒充哲学正确。

## GitHub 发布

仓库可直接公开发布，不含用户私人议题或凭据。安装已认证的 GitHub CLI 后，在仓库内执行：

```sh
gh auth login
gh repo create philosophy-council --public --source=. --remote=origin --push
```

若 origin 已存在，请先检查，避免覆盖他人仓库。GitHub 公开仓库不等于进入 OpenAI 公共插件目录；后者需要单独提交和审核，本项目不声称自动上架。

MIT 许可证，见 [LICENSE](LICENSE)。

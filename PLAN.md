# 项目计划 · 贪吃蛇（pygame）

> 规则：每完成一步立即打勾 `[x]`；后续计划变更同步更新本文件。

## 阶段一：存档与本地提交（当前）

- [x] 1. 编写本计划文档 PLAN.md
- [x] 2. git init 初始化仓库（主分支 main）并检查 git 用户配置
- [x] 3. 创建 .gitignore（排除 .venv、缓存、运行时数据）
- [x] 4. 暂存新功能代码：将含新功能（最高分/音效/加速）的 snake_game.py 移出项目临时保存
  （说明：仓库尚无首次提交，git stash 不可用，采用等效的文件暂离方式）
- [x] 5. 还原 snake_game.py 为已通过 13 项测试的稳定版
- [x] 6. 编写 README.md
- [x] 7. 运行测试验证稳定版（预期 13 passed）
- [x] 8. git add + commit：稳定版 v0.1（main 分支，仅本地提交）
- [x] 9. 创建并切换 test 分支，取回新功能版 snake_game.py
- [x] 10. 同步勾选本计划，收尾说明

## 阶段二：新功能开发（test 分支，待开始）

- [x] 更新 test_snake_game.py：补齐最高分 / 加速 / 存档函数的单元测试
  （说明：v02 的 step() 会读写 highscore 键，同步给 make_state 补上了该键，修复了旧进食测试的 KeyError 隐患）
- [x] 全量测试通过（23 passed，0.47s）
- [x] test 分支提交 v0.2（提交号 21ccc3a，冗余的 v02 暂存文件已删除）
- [x] 推送 GitHub：test 与 main 均已推送至 origin（github.com/luna0023/first_snake，2026-10-16 完成）
- [ ] （可选）把 v0.2 合回 main 后再次推送 main

## 决策记录

- 2026-10-16：只做本地提交，暂不推送 GitHub（用户确认）。
- 2026-10-16：稳定版提交到 main，新功能代码取回后在 test 分支继续开发（用户确认）。
- 2026-10-16：仓库首次创建无历史提交，git stash 不可用，改用文件暂离等效方案。
- 2026-10-16：新功能版文件已从 %TEMP% 移入项目根目录（snake_game_feature_v02.py，用户确认），避免被系统清理；后续合入直接从项目内复制。

# SWUSTMC Club 项目协作入口

本仓库是独立维护和发布的主仓库。开始修改前阅读 ./README.md、./docs/dev/ 与相关 ./docs/exp/。

- 当前基线 Folia / Minecraft 26.3、Java 25；旧 Bukkit 桥接插件仍使用 Java 8 字节码。
- 作者字段统一 `SWUSTMC Club`，保留历史版权及第三方许可。
- 版本唯一来源 ./gradle.properties，规则见 ./docs/dev/版本与产物规范.md。
- 构建与测试：`./gradlew build`；发布前运行 `python3 ./scripts/check-release.py`。
- Folia 操作在所属实体/区域线程执行；依赖使用 compileOnly，不嵌入其他插件。
- 普通源码通过 apply_patch 修改。保留用户已有未提交修改，提交前检查 git diff。
- 相对路径、自定位脚本；不提交运行服、凭据、缓存或本机环境。
- 完成已授权修改后，测试、更新 CHANGELOG、构建，提交 main 并推送本仓库 origin。
- mcPlugin 是历史与集成入口；不要在那里修改副本后覆盖本仓库的新工作。

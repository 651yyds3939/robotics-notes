# Git 与 GitHub 版本管理、多分支与子模块操作

> 👉 日常速查：[Git 拉取与子模块](./git_pull.md) · 架构实战：[架构总览](./robotics_architecture_master_guide.md)
>
> **范围**：版本追踪、协作、分支切换与子模块管理。下文重建仓库和放弃修改仅是特定场景方案，不是默认操作；先确认备份、上游来源及许可证，再执行删除或推送命令。

---

## 一、 Git 三层架构与快照机制

Git 的提交在逻辑上记录项目快照，底层存储还会进行压缩等优化。日常操作涉及三个区域：
1. **工作区（Working Directory）**：工作区中正在编辑的文件。
2. **暂存区（Staging Area / Index）**：执行 `git add` 后，文件被打包准备上车。可在提交前调整。
3. **本地仓库（Local Repository）**：执行 `git commit` 后创建提交对象及其内容标识（如短提交号 `3cd6834`）；内容改变会对应不同标识，但分支引用和可见历史仍可重写，不等于不可篡改存证。
* **GitHub 的角色**：它只是一个装有 Git 环境的远端服务器，`git push` 就是把本地 `.git` 里的历史记录同步过去。

---

## 二、 基础实战：从零重建纯净仓库推送到 GitHub

clone 含大文件历史的项目时，想修改后上传到自己的 GitHub，但遭遇大文件（`.git` 过大）或嵌套子仓库污染时，请严格按照此流程操作。

**🚨 铁律：Git 只适合存代码，严禁存放 `.bag`, `.tar.gz`, `build/`, `log/`。**

### 2.1 物理隔离与旧历史抹除
```bash
# 复制出纯净副本进行操作
cd ~
cp -r kuavo-ros-opensource kuavo-clean
cd kuavo-clean

# 彻底删除旧项目的 Git 历史包袱
rm -rf .git
```

### 2.2 构建免疫系统 (`.gitignore`)
创建并编辑 `.gitignore`，阻止垃圾文件进入暂存区：
```bash
nano .gitignore
```

```gitignore
# ROS 衍生文件
build/
install/
log/
# 数据与压缩包
*.bag
*.db3
*.tar.gz
*.zip
*.7z
```

### 2.3 处理嵌套 Git 仓库（极其重要）
如果报错 `warning: adding embedded git repository`，说明别人的工程里套了别人的工程，必须暴力拆解：
```bash
git rm --cached -r -f src/apriltag
git rm --cached -r -f src/aws-robomaker-hospital-world

rm -rf src/apriltag/.git
rm -rf src/aws-robomaker-hospital-world/.git
```

### 2.4 重建、提交与分支修正
```bash
git init
git add .
git commit -m "clean project & fix nested repos"

# 修正可能出现的主分支名称不匹配错误
git branch -M main
```

### 2.5 GitHub 绑定与推送 (Token 认证)
* **创建仓库**：在 GitHub 创建私有仓库，**不要勾选** README/gitignore/license 初始化。
* **认证**：按组织要求选择 SSH、凭据管理器或最小权限的个人访问令牌；不将 Token 写入命令、笔记或 Git 远端 URL。
* **推流**：
```bash
git remote add origin https://github.com/<用户名>/<仓库名>.git
git push -u origin main
# 登录时 Password 输入 Token

# 按系统配置受支持的凭据管理器；不要默认使用明文 store
```

---

## 三、 高阶实战：Git 多分支切换与现场保留全场景指南

在切换不同分支（如算法分支与比赛分支）时，盲目切换极易导致环境崩溃。请严格执行以下五个阶段。

### 第零阶段：摸清底牌
```bash
git status
git diff
```

### 第一阶段：处理当前现场（根据需求二选一）
* **方案 A：放弃修改（仅在已备份并确认不要这些改动时）**
 ```bash
 # 权限问题先检查具体文件和容器 UID/GID，不递归修改整个仓库所有者
 git checkout . # 清除追踪文件修改
 git clean -nd # 先预览将删除的未跟踪项
 # 确认预览中的文件均可删除后，才执行 git clean -fd
 ```
* **方案 B：打包带走（暂存本地修改）**
 ```bash
 git stash -u # 强力暂存（包含新建的未追踪文件）
 git stash list # 确认入库
 ```

### 第二阶段：刷新与精准跳跃
```bash
git fetch --all # 强制刷新远程最新状态
git branch -a # 查看本地与远程路线图
git checkout <目标分支名> # 例如 git checkout main
```

### 第三阶段：同步外包模型（极其致命的子模块陷阱！）
**必须执行**。人形机器人依赖大量第三方库，分支切换后，必须让当前分支的子模块文件夹也切换到对应的特定 Commit ID，否则模型会丢失。
```bash
git submodule update --init --recursive
```

### 第四阶段：恢复现场（仅针对选了“方案 B”的人）
```bash
git stash pop # 弹出修改并应用（若有 Merge conflict 需去 VSCode 解决冲突）
```

---

## 四、 细节警惕：大小写的绝对严谨
* Windows 不区分大小写（`readme.md` = `README.md`）。
* 常见 Linux 文件系统区分文件名大小写，`readme.md` 与 `README.md` 可以是不同文件；这与权限问题是两个概念。项目中文件名应保持一致，避免跨平台冲突。

---

## 五、 高阶终端指令速查字典 (Git篇)

```bash
# 1. 克隆时顺便把所有嵌套的子模块（如别人写的驱动）一起拉下来
git clone --recursive https://github.com/xxxxx.git

# 2. 如果克隆时忘了加 recursive，用这行命令亡羊补牢
git submodule update --init --recursive

# 3. 开发新功能前，永远记得先开辟平行时空（分支），不要污染主线
git checkout -b my_feature_slam

# 4. 全局搜索“失踪”的文件（忽略那些 permission denied 的废话警告）
sudo find / -name "my_first_package" 2>/dev/null

# 5. 模糊搜索包含某个关键词的文件
sudo find ~/ -iname "*READ*" -ls

# 6. 查找最近 60 分钟内被修改过的所有文件（破案专用）
find ~/ -mmin -60 -type f
```




## 1. 源码与代码仓库获取 (Git & VCS)
机器人项目经常包含大量子模块，必须掌握递归克隆。

```bash
# --- Git 基础 ---
git clone <url> # 克隆仓库
git pull origin <branch> # 拉取最新代码
git clone --recursive <url> # 递归克隆（带子模块，机器人开发常用）

# --- 强制对齐远程仓库 (本地乱了时的救命稻草) ---
git fetch --all
git reset --hard origin/main # 放弃所有本地修改，强制同步远程

# --- VCS (多仓库管理，ROS必备) ---
vcs import src < my.repos # 批量导入 .repos 文件中的仓库
vcs pull src # 批量拉取所有仓库更新

```

# Git 学习笔记

## 一、基础命令总结
1.  `git init`：初始化本地仓库，将其变为Git可以管理的仓库
2.  `git add xxx`：将xxx文件添加到仓库，Unix是没有报错就OK的
3.  `git commit -m "xxx"`：将文件提交到仓库，xxx是提交说明，运行结果会表明changed和insertions
4.  `git status`：掌握仓库当前的状态
5.  `git diff xxx`：具体查看修改内容（difference）
6.  `git log`：显示从最近到最远的提交日志，可加上`--pretty=oneline`参数
7.  `git reset`：回退版本或者将暂存区的修改回退到工作区
    - 在Git中，用`HEAD`表示当前版本，上一个版本是`HEAD^`，上上一个版本是`HEAD^^`
    - `--hard`：回退到上个版本的已提交状态；`--soft`：回退到上个版本的未提交状态；`--mixed`：回退到上个版本已添加但未提交的状态
    -所以回退到上一个版本已提交状态的命令：`git reset --hard HEAD^`
8.  `git reflog`：记录每一次命令，可查看版本号
9.  `git checkout -- xxx`：将文件在工作区的修改全部撤销，回到最近一次commit或add时的状态
10. `git rm`：删除文件
11. `git remote add origin https://github.com/shaomin-hao/study-weekly.git`：关联自己的仓库
12. `git push origin master`：把本地库的内容推送到远程
13. `git clone`：克隆远程库
14. `git switch -c dev`：创建并切换到dev分支；`git branch -d dev`：删除dev分支（开发新功能需创建新分支）
15. `git branch`：列出所有分支
16. `git merge`：用于合并指定分支到当前分支
17. `git log --graph`：查看分支合并图
18. `git stash`：储藏当前工作现场（类似存档）；`git stash pop`：回到工作现场
19. `git cherry-pick <commit>`：把bug提交的修改“复制”到当前分支，避免重复劳动
20. `git rebase`：把本地未push的分叉提交历史整理成直线

## 二、基本概念
1.  **工作区 vs 暂存区**
    - 工作区：电脑里可以直接看到的目录
    - 暂存区：存在隐藏目录`.git`版本库中
    - `add`：将修改添加到暂存区；`commit`：将暂存区的所有修改一次性提交到`master`分支
    - 我的理解：暂存区就像一个缓冲区，存放所有修改，提交后暂存区就会清空
2.  **管理的是修改**：如果没有把修改`add`到暂存区，就相当于没有修改
3.  **分支策略**：`master`仅用来发布新版本，必须稳定，每个人都在自己的`dev`分支上干活

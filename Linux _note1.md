# Linux 基本命令

##### 一.处理目录

ls（用于列出目录内容）

```
ls-a #列出全部文件
ls-d #仅列出目录
ls-l #列出文件的属性与权限
```

cd（切换目录）

```
cd /home/user #切换到指定的绝对路径目录
cd .. #切换到当前目录的上一级目录
cd ~ #切换到当前用户的家目录
cd ./test #切换到当前目录下的 test 子目录，这里用的是相对路径
```

pwd（显示当前目录）

mkdir（创建新目录）

```
mkdir -p xxx1/xxx2/xxx3 #可以递归创建多级目录
```

rmdir（删除新目录）

```
rmdir -p #从该目录起，一次删除多级空目录
```

cp（复制）

```
cp file1 file2 #将 file1 复制为 file2
cp -r dir1 dir2 #复制 dir1 目录到 dir2
cp -i file1 file2 #覆盖文件前给出提示
```

rm（删除）

```
rm -r dir # 递归删除目录
rm -rf dir # 强制删除目录，不给出任何提示，不要用，危险
rm -i file # 删除前给出提示
```

mv（移动或修改名称）

##### 二.文件内容查看

cat/tac (从第一行/最后一行开始显示)

```
cat file.txt # 查看 file的全部内容
cat > file.txt # 创建新文件并写入内容
cat file1.txt file2.txt # 合并两个文件的内容并输出
tac file.txt # 反向查看文件内容
```

nl (顺道输出行号)

more/less (一页一页的显示内容，less可往前翻页)

head/tail（只看头几行/末几行）

```
head -n 20 file.txt # 查看文件的前 20 行
tail file.txt # 查看文件的后 10 行
tail -f file.txt # 实时跟踪文件内容更新
```

##### 三.磁盘管理

df(列出文件系统的整体磁盘使用量)

```
df-h #以熟知的单位方式显示输出结果
df-T #显示文件系统的类型
df-t <文件系统类型> #只显示指定类型的文件系统。
df-i #显示 inode 使用情况。
```

du(检查磁盘空间使用量)

```
du-a #列出所有的文件与目录容量
du-h #以人们较易读的容量格式 (G/M) 显示
du-s #仅显示指定目录或文件的总大小
du-S #包括子目录下的总计
```

fdisk(用于磁盘分区)

mkfs(进行磁盘格式化)

fsck(对文件系统进行检查)

mount/umount(Linux磁盘挂载卸载)

```
mount [-t 文件系统] [-L Label名] [-o 额外选项] [-n]  装置文件名  挂载点
```

##### 四.yum相关命令

```
yum check-update #列出所有可更新的软件清单命令
yum update #更新所有软件命令
yum install <package_name> #安装指定的软件命令
yum update <package_name> #更新指定的软件命令
yum list #列出所有可安裝的软件清单命令
yum remove <package_name> #删除软件包命令
yum search <keyword> #查找软件包命令
yum clean packages #清除缓存目录下的软件包
yum clean headers #清除缓存目录下的 headers
yum clean oldheaders #清除缓存目录下旧的 headers
yum clean, yum clean all #清除缓存目录下的软件包及旧的 headers
```

##### 五.apt相关命令

```
sudo apt update #列出所有可更新的软件清单命令
sudo apt upgrade #升级软件包
apt list --upgradable #列出可更新的软件包及版本信息
sudo apt full-upgrade #升级软件包，升级前先删除需要更新软件包
sudo apt install <package_name> #安装指定的软件命令
sudo apt install <package_1> <package_2> <package_3> #安装多个软件包
sudo apt update <package_name> #更新指定的软件命令
sudo apt show <package_name> #显示软件包具体信息
sudo apt remove <package_name> #删除软件包命令
sudo apt autoremove #清理不再使用的依赖和库文件
sudo apt purge <package_name> #移除软件包及配置文件
sudo apt search <keyword> #查找软件包命令
apt list --installed #列出所有已安装的包
apt list --all-versions #列出所有已安装的包的版本信息
```


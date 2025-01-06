#!/bin/bash

# 获取终端宽度
terminal_width=$(tput cols)

# 定义要打印的文本
text=(
    "    __  ___ ____                  __  "
    "   / / / (_) __ )___  ____  _____/ /_ "
    "  / /_/ / / __  / _ \/ __ \/ ___/ __ \\"
    " / __  / / /_/ /  __/ / / / /__/ / / /"
    "/_/ /_/_/_____/\___/_/ /_/\___/_/ /_/ "
)

# 定义彩虹色
colors=(
"\033[31m" # 红色
"\033[33m" # 黄色
"\033[32m" # 绿色
"\033[36m" # 青色
"\033[34m" # 蓝色
"\033[35m" # 紫色
)

# 计算每行的最大长度
max_length=0
for line in "${text[@]}"; do
    length=${#line}
    if (( length > max_length )); then
        max_length=$length
    fi
done

# 计算需要的空格数
padding=$(( (terminal_width - max_length) / 2 ))

# 打印文本
for i in "${!text[@]}"; do
    color=${colors[i % ${#colors[@]}]}
    printf "${color}%*s%s\033[0m\n" $padding "" "${text[i]}"
done
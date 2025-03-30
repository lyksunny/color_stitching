### color_stitching.py ###
# Author: lyk #
# Date: 2025/03/30 #
# Description: This script is used to stitch images together based on their color similarity. #
# Usage: python color_stitching.py --<input_file> --<output_file> #
# Example: python color_stitching.py --input.txt --output.txt #


import argparse
from copy import deepcopy

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", default="input.txt", help="The folder to save the output steps.")
parser.add_argument("--output_file",default="output.txt", help="The threshold to determine the color similarity.")


def read_input(input_file):
    with open(input_file, "r", encoding='utf-8') as f:
        lines = f.readlines()
    bottoms = [line.rstrip('\n').split(' ') for line in lines]
    
    # 检查瓶子是否有四个颜色
    for bottom in bottoms:
        if len(bottom) != 4:
            print("Error: The input file is not in the correct format.")
            exit(1)
            
    # 增加2个空瓶子
    bottoms.append([])
    bottoms.append([])
    
    # 记录步骤
    steps = []
    
    return bottoms, steps


def get_color_dict(bottoms):
    # 颜色字典
    color_dict = {}
    k = 1
    for i, bottom in enumerate(bottoms):
        for j, color in enumerate(bottom):
            if color not in color_dict:
                color_dict[color] = k
                k += 1
    return color_dict


def encoder(bottoms, color_dict):
    # 编码
    code = [0] * len(bottoms)
    for i, bottom in enumerate(bottoms):
        for j, color in enumerate(bottom):
            code[i] = color_dict[color] + 10*code[i]
    return tuple(code)            
            
            
def check(bottoms):
    for bottom in bottoms:
        if len(bottom) not in {0, 4} or (len(bottom) == 4 and len(set(bottom)) != 1):
            return False
    return True

def stitch(bottoms, steps, empty_bottles=2, color_dict=dict(), visited=set()):
    # 终止条件
    if check(bottoms):
        return True
    
    # 剪枝
    code = encoder(bottoms, color_dict)
    if code in visited:
        return False
    else:
        visited.add(code)
    
    # 移动瓶子中的颜色
    # 每个瓶子只能移动最右侧的颜色
    # 每次移动颜色到新瓶子中必须与最右侧颜色一致且不能超过4
    for i, bottom in enumerate(bottoms):
        # 如果瓶子为空或者只有一种颜色，跳过
        ori_bottoms = deepcopy(bottoms)
        if len(bottom)== 0 or (len(bottom)==4 and len(set(bottom))== 1): continue
        # 提取最右侧颜色
        move_color = []
        move_color.append(bottom.pop())
        while len(move_color) < 4 and len(bottom) > 0 and bottom[-1] == move_color[0]:
            move_color.append(bottom.pop())

        # 中间状态
        mid_move = deepcopy(move_color)
        mid_bottoms = deepcopy(bottoms) 
        
        # 移动颜色到新瓶子中
        for j, new_bottom in enumerate(bottoms):
            # 如果新瓶子已满，跳过
            if len(bottoms[j]) == 4 or i == j: continue
            # 如果新瓶子为空或者颜色一致，移动颜色
            if len(new_bottom) == 0 or new_bottom[-1] == move_color[0]:
                # 新瓶子颜色不能超过4
                for k in range(min(4-len(new_bottom), len(move_color))):
                    new_bottom.append(move_color.pop())
                bottom.extend(move_color) # 多余的颜色回到原来的瓶子
                # 更新瓶子
                new_bottoms = deepcopy(bottoms)
                new_bottoms[i] = bottom
                new_bottoms[j] = new_bottom
                steps.append((i,j))
                # 检查空瓶子
                # 如果更新后空瓶子数量不变，说明移动颜色失败，跳过
                new_empty_bottles = 0
                for nb in new_bottoms:
                    if len(nb) == 0:
                        new_empty_bottles += 1
                # 递归
                if new_empty_bottles!=empty_bottles and stitch(new_bottoms, steps, new_empty_bottles, color_dict, visited):
                    return True
                else:
                    steps.pop()
                    bottoms = deepcopy(mid_bottoms)
                    move_color = deepcopy(mid_move)
        bottoms = deepcopy(ori_bottoms)
    return False


def write_output(output_file, steps):
    with open(output_file, "w",encoding='utf-8') as f:
        for step in steps:
            f.write(f"{step[0]}->{step[1]}\n")
    print("The solution has been saved to the output file.")
            

def main():
    args = parser.parse_args()
    input_file = args.input_file
    output_file = args.output_file
    bottoms, steps = read_input(input_file)
    color_dict = get_color_dict(bottoms)
    if stitch(bottoms, steps, empty_bottles=2, color_dict=color_dict, visited=set()):
        write_output(output_file, steps)
    else:
        print("No solution.")
        
if __name__ == "__main__":
    main()
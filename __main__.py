import json
import utils
import exception

'''
约定 & 为空符号
约定小写字母和其他字符为非终结符号
约定大写字母为非终结符号
'''
'''
全局变量
'''
DEBUG = False

'''
加载文法的json文件
'''


def load_json(filePath):
    f = open(filePath, 'r')
    try:
        s = json.load(f)
        if DEBUG:
            print('====== json load ======')
            print(s)
        return s
    except Exception as e:
        print(e)
    finally:
        f.close()


'''
判断文法中能够推出空的非终结符
'''


def able_null(fin):
    # 储存能退出空的非终结符
    f = []
    # 第一次扫描
    for nf in fin:
        for nf2 in fin[nf]:
            if nf2 == '&':
                f.append(nf)

    # 压缩dict
    fin_b = dict.copy(fin)
    for nf in f:
        del fin_b[nf]

    # 第二次扫描
    for nf in fin_b:
        for nf2 in fin_b[nf]:
            if len(nf2) == 1 and nf2 in f:
                f.append(nf)
                break
            flag = True
            for str in nf2:
                if str not in f:
                    flag = False
            if flag:
                f.append(nf)
    return set(f)


'''
计算非终结符FIRST集合
'''


def get_first(char, can_null, all):
    # 判断非法字符
    if utils.is_final_char(char):
        raise exception.inputErrorException
    first = set()
    for str in all[char]:
        # 可以直接推到出空
        if str == '&':
            first.add('&')
        # 首位为终结符
        elif utils.is_final_char(str[0]):
            first.add(str[0])
        # 首位为非终结符
        else:
            i = 0
            tmp_char = str[i]
            while (tmp_char in can_null):
                if i == len(str):
                    break
                tmp_char = str[i]
                # 非终结符的first集 - & 的集合
                first |= (get_first(tmp_char, can_null, all) - {'&'})
                i += 1
            # 最后一个不能直接推到出空
            if i < len(str):
                first |= get_first(tmp_char, can_null, all)
            # 整个文法都可能推出空
            if i == len(str):
                first.add('&')
    return first


def get_mult_first(str, can_null, all):
    table = dict()
    first = set()
    for char in str:
        if char == '&':
            first.add(char)
            break
        elif utils.is_final_char(char):
            first.add(char)
            first -= {'&'}
            break
        elif char not in can_null:
            first |= get_first(char, can_null, all)
            first -= {'&'}
            break
        first |= get_first(char, can_null, all)
    print(first)
    return first


'''
计算FOLLOW集合
'''


def get_follows(begin, can_null, all):
    follow = {}
    # 初始化dict
    for nf in all:
        follow[nf] = set()

    #开始符号加 #
    for nf in begin:
        follow[nf].add('#')

    # 不在folllow集不在增加
    for i in range(0, 10):
        for nf in all:
            for nf2 in all[nf]:
                for i in range(0, len(nf2) - 1):
                    if not utils.is_final_char(nf2[i]):
                        #下一位是终结符
                        if (utils.is_final_char(nf2[i + 1:])):
                            set_to_add = {nf2[i + 1:]}
                        else:
                            set_to_add = get_first(nf2[i + 1:], can_null, all) - {'&'}
                        follow[nf2[i]] |= set_to_add
                        if nf2[i + 1:] in can_null:
                            follow[nf2[i]] |= follow[nf]
                else:
                    if not utils.is_final_char(nf2[-1]):
                        follow[nf2[-1]] |= follow[nf]
    return follow

    # for nf in all:
    #     for nf2 in all[nf]:
    #         (flag, last) = utils.get_last_uti(char, nf2)
    #         if flag:
    #             # 开始符号添加 #
    #             if char in begin:
    #                 follow.add('#')
    #             elif last == '':
    #                 follow |= get_follow(nf, begin, can_null, all)
    #             elif utils.is_final_char(last):
    #                 follow.add(last)
    #             elif last in can_null:
    #                 follow |= get_first(last, can_null, all) | get_follow(nf, begin, can_null, all)
    #             else:
    #                 follow |= get_first(last, can_null, all)
    # follow -= {'&'}
    # return follow


def main(filePath):
    g = load_json(filePath)
    n = able_null(g['grammars'])
    f = get_follows(g['begin'], n, g['grammars'])
    if DEBUG:
        print("==========加载数据开始==========")
        print(g)
        print("==========加载数据结束==========")
        print("==========可推出空的非终结符开始==========")
        print(n)
        print("==========可推出空的非终结符结束==========")
        print("==========follow开始==========")
        print(f)
        print("==========follow结束==========")



main("/home/trons/PycharmProjects/ll1/data2.json")

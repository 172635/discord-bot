import discord
import random
import time
import copy
import math

Yacht_order = 0
Yacht_player = []
Yacht_left_dice = 3
Yacht_player_num = 0
Yacht_point = []
Yacht_dice_unfix = []
Yacht_dice_fix = []
Yacht_choose_mode = -1
Yacht_stage = 13

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    ctx = message.channel
    if message.content.startswith('$'):
        cmdmsg = message.content
        au = message.author
        print(cmdmsg)
        if message.content.startswith("$dice "):
            cmd = cmdmsg.split("$dice ")[1]
            await dice(ctx,au,cmd)
        elif message.content.startswith("$turn "):
            cmd = cmdmsg.split("$turn ")[1]
            await turn(ctx,cmd)
        elif message.content.startswith("$character "):
            cmd = cmdmsg.split("$character ")[1]
            await turn(ctx,au,cmd)
        elif message.content.startswith("$hello "):
            cmd = cmdmsg.split("$hello ")[1]
            await hello(ctx)
        elif message.content.startswith("$log "):
            cmd = cmdmsg.split("$log ")[1]
            await log(ctx)
        elif message.content.startswith("$Yacht "):
            cmd = cmdmsg.split("$Yacht ")[1]
            await Yacht(ctx,cmd)
        elif message.content.startswith("$Yacht_log "):
            cmd = cmdmsg.split("$Yacht_log ")[1]
            await Yacht_log(ctx,cmd)

        global Yacht_order
        global Yacht_player
        author = str(message.author).split('#')[0]
        msg = message.content.split('$')[1].lower().split(' ')
        msg_r = 0
        if Yacht_order != 0 and Yacht_player[Yacht_order-1] == author:
            #play yacht
            if msg[0] == 'help' or msg[0] == 'h':
                await Yacht_help(ctx)
            elif msg[0] == 'rule' or msg[0] == 'r':
                try:
                    msg_r = int(msg[1])
                except:
                    msg_r = 0
                await Yacht_rule(ctx,msg_r)
            elif msg[0] == 'board' or msg[0] == 'b':
                await Yacht_board(ctx)
            elif msg[0] == 'dice' or msg[0] == 'd':
                await Yacht_dice(ctx)
            elif msg[0] == 'fix' or msg[0] == 'f':
                await Yacht_fix(ctx,msg[1])
            elif msg[0] == 'unfix' or msg[0] == 'u' or msg[0] == 'uf':
                await Yacht_unfix(ctx,msg[1])
            elif msg[0] == 'show' or msg[0] == 's':
                await Yacht_show(ctx)
            elif msg[0] == 'choose' or msg[0] == 'c':
                await Yacht_choose(ctx,msg[1])
            elif Yacht_choose_mode != -1 and (msg[0] == 'y' or msg[0] == 'n'):
                await Yacht_choose_check(ctx,msg[0])
    elif message.content.startswith("*"):
        await ctx.send("1")
    else:
        await ctx.send("1")

    if message.content.startswith('$print') and author == '172635':
        exec(msg[0])



async def dice(ctx,au,*cmd):
    print(cmd)
    txt1 = cmd[0]
    if 'log' in txt1:
        if txt1 == 'log_reset':
            await ctx.send(dice_logf('reset'))
        elif txt1 == 'log_load':
            await ctx.send(embed = dice_logf('load'))
    else:
        if 'D' in txt1:
            spliter = 'D'
        elif 'd' in txt1:
            spliter = 'd'
        
        if 'D' in txt1 or 'd' in txt1:
            text = txt1.split(spliter)
            text1 = text[0]
            text2 = text[1]
            R_mode = 0 #최소값 다시 굴리기(1회만)
            R_mode_ = 0
            R_num = 0
            E_mode = 0 #최대값 다시 굴리기(연속 like 윷놀이 모)
            E_num = 0
            F_mode = 0 #-1,0,1 주사위
            if ''==text1:
                text1 = "1"

            if 'R' in text2 or 'r' in text2:
                R_mode = 1
                R_mode_ = 1
                text2_ = text2.split('R')
                text2 = ''.join(text2_)
                text2_ = text2.split('r')
                text2 = ''.join(text2_)
            if 'E' in text2 or 'e' in text2:
                E_mode = 1
                text2_ = text2.split('E')
                text2 = ''.join(text2_)
                text2_ = text2.split('e')
                text2 = ''.join(text2_)
            if "F" in text2 or "f" in text2:
                F_mode = 1
                text2 = "3"
            
            except_mode = 0
            if "-" in text2:
                text3 = text2.split("-")
                text2 = text3[0]
                text3 = text3[1]
                if "L"==text3 or 'l'==text3:
                    except_mode = -1
                elif "H"==text3 or 'h'==text3:
                    except_mode = 1

            try:
                dice_num = int(text1)
            except:
                dice_num = 0
            
            try:
                dice_size = int(text2)
            except:
                if F_mode == 1:
                    dice_size = 3
                else:
                    dice_size = 1
            
            if except_mode != 0:
                if except_mode == 1:
                    except_ = -2
                else:
                    except_ = dice_size

            sum = 0
            count = 0
            dice_log = "dice_log : "
            while(1):
                if count == dice_num:
                    break

                point = random.randrange(1,dice_size+1)

                if point == 1 and R_mode == 1:
                    R_num += 1
                    point=0
                    if F_mode == 1:
                        point=2
                if point == dice_size and E_mode > 0:
                    E_num += 1
                
                if F_mode == 1:
                    point-=2
                sum += point
                dice_log += (str(point)+" ")
                if except_mode != 0:
                    if except_mode == 1 and except_ < point:
                        except_ = point
                    elif except_mode == -1 and except_ > point:
                        except_ = point

                if R_mode == 1 and count == dice_num-1:
                    if R_num!=0:
                        dice_log += "/ R_mode : "
                    count-=R_num
                    R_mode = 0
                    R_num = 0
                if E_mode > 0 and count == dice_num-1 and R_mode == 0:
                    if E_num!=0:
                        dice_log += ("/ E"+str(E_mode)+"_mode : ")
                    count-=E_num
                    E_num = 0
                    E_mode += 1
                
                count += 1
            
            if except_mode != 0:
                dice_log += ("/ except : "+str(except_))
                sum -= except_

            #dice log
            await ctx.send(dice_log)

            #최종 점수
            print_str = "dice_num : "+str(dice_num)
            if R_mode_ == 1:
                print_str += "R"
            if E_mode > 0:
                print_str += "E"
            if except_mode != 0:
                print_str += ("-"+text3)
            print_str += " / dice_size : "
            if F_mode == 1:
                print_str += "F"
            else:
                print_str += str(dice_size)
            print_str += " / dice_sum : "
            print_str += str(sum)

            await ctx.send(print_str)



            log_time = time.strftime('%Y-%m-%d-%a-%H-%M-%S', time.localtime(time.time()))
            dice_logf('append|'+log_time+' / player : '+au.name)
            dice_logf('append|'+dice_log)
            dice_logf('append|'+print_str)

def dice_logf(command):
    mode = command.split('|')[0]
    file_name = 'runtime_log.txt'
    if mode == 'append':
        record = command.split('|')[1]
        with open(file_name, 'a', encoding='UTF8') as file:
            file.write(record+'\n')
    elif mode == 'reset':
        log_time = time.strftime('%Y-%m-%d-%a-%H-%M-%S', time.localtime(time.time()))
        with open(file_name, 'a', encoding='UTF8') as file:
            file.write("_dice_log_start_time_"+log_time+"_\n")
        return "log reset complete"
    elif mode == 'load':
        loading_str = ""
        start_time = ""
        with open(file_name, 'r', encoding='UTF8') as file:
            lines = file.readlines()
            for line in lines:
                if line[0]=='_':
                    start_time = line.split('_')[5]
                    loading_str = ""
                else:
                    loading_str += line
        load_embed = discord.Embed(title = 'dice_log', color = 0xa0a0a0)
        load_embed.add_field(name = 'start : '+start_time, value = loading_str, inline = False)
        
        return load_embed

async def turn(ctx,*cmd):
    if cmd[0] == "off":
        await ctx.send("bye bye _ zzzzz")
        exit()

async def character(ctx,au,*cmd):
    cmd = " ".join(cmd).split("$")
    if cmd[0]!="":
        first = 0
    else:
        first = 1
    cmd1 = cmd[first]
    
    if cmd1 == "show":
        cmd2 = cmd[first+1]
        player_character_list = show(cmd2)

        embed = discord.Embed(title = cmd2+"의 character", color = 0x00ff56)
        for i in range(len(player_character_list)):
            embed.add_field(name = player_character_list[i], value = ">> lv. 2, place : tormia", inline = False)
        embed.set_footer(text="select cmd : $character $select$" + au.name + "$character_name")
        await ctx.send(embed=embed)
    if cmd1 == "select":
        print("select")
    print(cmd)

def show(x):
    file_name='player_character.txt'
    return_list = []
    with open(file_name,'r') as data:
        lines=data.readlines()
        for line in lines:
            line = line.split("$")
            print(line)
            if line[0] == x:
                for i in range(int(line[1])):
                    return_list.append(line[2+i])
    return return_list

async def hello(ctx):
    await ctx.send('Hello!')

async def log(ctx):
    log_embed = discord.Embed(title = 'program_log', color = 0x00f0ff)
    log_zero = '0.1.0(210606) : 따라 만들기_기초작업'+'\n'\
        +'0.2.0 : command 명령어'+'\n'\
        +'0.3.0 : dice 제작_nDn & nDF'+'\n'\
        +'0.4.0 : dice 중간 완성_nDnR & nDnE'+'\n'\
        +'0.5.0(210608) : dice 완성_nDn-L & nDn-h'+'\n'+'     turn off + player select'+'\n'\
        +'0.6.0 : character 기능 제작 중..._embed 사용 개시'
    log_embed.add_field(name = 'log_<0. base & dice>', value = log_zero, inline = False)
    log_one = '1.0.0(210812) : log기능 추가_ver세부 설정 / dice_log 완성'+'\n'\
        +'1.0.1(210814) : Yacht'+'\n'\
        +'1.0.2(210815) : Yacht_rule'+'\n'\
        +'1.0.3(210816) : Yacht_record(append)'+'\n'\
        +'1.0.4(210817) : Yacht_record(load)'
    log_embed.add_field(name = 'log_<1.0. Yacht>', value = log_one, inline = False)
    log_two = '1.1.0(220304) : 함수 통합 정리'
    log_embed.add_field(name = 'log_<1.1. TRPG>', value = log_two, inline = False)
    log_embed.set_footer(text = 'made by 172635')
    await ctx.send(embed=log_embed)

async def TRPG(ctx, *cmd):
    await ctx.send("!")


async def Yacht(ctx, *cmd):
    global Yacht_order
    player = list(cmd[0].split('_'))
    if Yacht_order != 0:
        if player[0] == 'turn' and player[1] == 'off':
            Yacht_order = 0
            await ctx.send('-game end-\nsee you soon~')
        return
    global Yacht_player_num
    global Yacht_player
    global Yacht_left_dice
    global Yacht_point
    global Yacht_dice_unfix
    global Yacht_dice_fix
    global Yacht_stage
    Yacht_player = player
    Yacht_player_num = len(player)
    Yacht_order = 1
        #0 : off
    Yacht_left_dice = 3
        #left_dice : 3->2->1->0
    Yacht_dice_unfix = [0,0,0,0,0]
    Yacht_dice_fix = []
    Yacht_stage = 13
    empty = []
    for count in ['ones','twos','threes','fours','fives','sixes','sum','bonus','three of kinds','four of kinds','full house','small straight','large straight','choice','Yacht']:
        empty.append('\u200B')
    for i in range(Yacht_player_num):
        Yacht_point.append(copy.copy(empty))

    await ctx.send('Yacht start\nplayer : '+' '.join(player))
    time.sleep(1)
    await Yacht_help(ctx)
    time.sleep(1)
    await ctx.send(player[0]+'의 턴 입니다.')

async def Yacht_log(ctx, *cmd):
    await Yacht_record(ctx,'load',cmd[0])

async def Yacht_help(ctx):
    await ctx.send('+------명령어 차트------+\n\
    help(h) : 명령어 차트 열기\n\
    rule(r) : 게임 규칙 안내\n\
        r 1 : rule 1번 열기\n\
        r : rule 전체 열기(1~12)\n\
    board(b) : 현재 보드판 보이기\n\
    dice(d) : 주사위 굴리기\n\
    fix(f) : 주사위 고정\n\
        f 1 : 1의 눈을 가진 주사위 1개 고정\n\
        f 56666 : 주사위 5개(각각 눈 : 5, 6, 6, 6, 6) 고정\n\
    unfix(u,uf) : 주사위 고정 해제(방법은 fix와 동일)\n\
    show(s) : 현재 주사위 결과 보이기\n\
    choose(c) : 주사위 결과를 넣을 칸 고르기\n\
        c 7 : (7)번 칸 선택\n\
        (확인을 위해 y(Y)/n(N) 대답을 요청합니다.)')

async def Yacht_rule(ctx,msg):
    Yacht_rule_num = 12
    if msg == 0:
        for i in range(1,Yacht_rule_num+1):
            await Yacht_rule(ctx,i)
            time.sleep(3)
    elif msg >= 1 and msg <= Yacht_rule_num:
        send_msg = ''

        file_name = 'yacht_rule.txt'
        with open(file_name, 'r', encoding='UTF8') as file:
            lines = file.readlines()
            lines = list(map(lambda x: x.split('\n')[0], lines))
            line_check = 0
            for c in range(len(lines)):
                if line_check == 1 and lines[c] == ('<rule '+str(msg+1)+'>'):
                    line_check = 0
                    break
                if line_check == 1:
                    send_msg += '\n'
                if lines[c] == ('<rule '+str(msg)+'>'):
                    line_check = 1
                if line_check == 1:
                    send_msg += lines[c]
        await ctx.send(send_msg)

async def Yacht_board(ctx):
    yb_embed = discord.Embed(title = '>=----Yacht_score board----=<', description = '현재 점수 목록', color = 0x00ff56)

    yb_embed_value ='\nones(1)\ntwos(2)\nthrees(3)\nfours(4)\nfives(5)\nsixes(6)\nsum[/63]\nbonus[+35]\n\
        three of kinds(7)\nfour of kinds(8)\nfull house(9)\nsmall straight(10)\nlarge straight(11)\nchoice(12)\nYacht(13)'
    yb_embed.add_field(name = 'player : ', value = yb_embed_value, inline = True)

    for p_c, p in enumerate(Yacht_player):
        yb_embed_value = ""
        for c in range(len(['ones','twos','threes','fours','fives','sixes','sum','bonus','three of kinds','four of kinds','full house','small straight','large straight','choice','Yacht'])):
            if c==6:
                yb_embed_value += '\n' + str(Yacht_point[p_c][c]) + ' / 63'
            else:
                yb_embed_value += '\n' + str(Yacht_point[p_c][c])
        yb_embed.add_field(name = p, value = yb_embed_value, inline = True)
    
    await ctx.send(embed=yb_embed)

async def Yacht_dice(ctx):
    global Yacht_left_dice
    global Yacht_dice_unfix
    unfixed_dice_num = len(Yacht_dice_unfix)
    if Yacht_left_dice <= 0:
        await ctx.send('잔여 주사위 굴리기 횟수가 없습니다.\n선택(choose)단계를 진행해주세요.')
        return
    else:
        new_dice = []
        for i in range(unfixed_dice_num):
            new_dice.append(random.randrange(1,7))
        Yacht_left_dice -= 1
        Yacht_dice_unfix = new_dice
        await ctx.send('> 주사위 굴리기 결과\n새로 굴린 주사위(unfixed dice) : '+' '.join(list(map(str,new_dice)))+'\n고정된 주사위(fixed dice) : '+' '.join(list(map(str,Yacht_dice_fix)))+'\n> 잔여 주사위 굴리기 횟수 : '+str(Yacht_left_dice))
        if Yacht_left_dice == 0:
            await ctx.send('잔여 주사위 굴리기 횟수가 없습니다.\n선택(choose)단계를 진행해주세요.')

async def Yacht_fix(ctx,number):
    if Yacht_left_dice == 3:
        ctx.send('주사위를 최소 한 번 이상 굴린 다음 고정할 수 있습니다.')
        return
    global Yacht_dice_fix
    global Yacht_dice_unfix
    fix_dice_list = list(map(int,list(number)))
    new_fix_dice = []
    new_unfix_dice = copy.copy(Yacht_dice_unfix)
    error_check = 0
    for fdl in fix_dice_list:
        try:
            new_unfix_dice.remove(fdl)
            new_fix_dice.append(fdl)
        except:
            error_check = 1
            break
    if error_check == 0:
        await ctx.send('dice fix complete')
        Yacht_dice_unfix = new_unfix_dice
        Yacht_dice_fix.extend(new_fix_dice)
    else:
        await ctx.send('cannot fix this dice\n(there is no unfixed dice that you told to me)')

async def Yacht_unfix(ctx,number):
    global Yacht_dice_fix
    global Yacht_dice_unfix
    unfix_dice_list = list(map(int,list(number)))
    new_fix_dice = copy.copy(Yacht_dice_fix)
    new_unfix_dice = []
    error_check = 0
    for udl in unfix_dice_list:
        try:
            new_fix_dice.remove(udl)
            new_unfix_dice.append(udl)
        except:
            error_check = 1
            break
    if error_check == 0:
        await ctx.send('dice unfix complete')
        Yacht_dice_fix = new_fix_dice
        Yacht_dice_unfix.extend(new_unfix_dice)
    else:
        await ctx.send('cannot unfix this dice\n(there is no fixed dice that you told to me)')

async def Yacht_show(ctx):
    await ctx.send('당신('+Yacht_player[Yacht_order-1]+')의 주사위 현황\n고정된 주사위(fixed dice) : '+' '.join(list(map(str,Yacht_dice_fix)))+'\n고정되지 않은 주사위(unfixed dice) : '+' '.join(list(map(str,Yacht_dice_unfix))))

async def Yacht_choose(ctx,number):
    if Yacht_left_dice == 3:
        await ctx.send('주사위를 최소한 한 번 던져야 합니다.')
        return
    global Yacht_choose_mode
    n = int(number)#1~13
    #n 변환 필요(sum등등)#0~14(6,7번은 선택 불가)
    if n <= 6:
        n -= 1
    elif n >= 7:
        n += 1
    Yacht_list_name = ['ones','twos','threes','fours','fives','sixes','sum','bonus','three of kinds','four of kinds','full house','small straight','large straight','choice','Yacht']
    if Yacht_point[Yacht_order-1][n] == '\u200B':
        await ctx.send(Yacht_list_name[n]+'를 선택하시겠습니까?($y/$n)')
        Yacht_choose_mode = n
    else:
        await ctx.send('이미 해당 칸에 입력하셨습니다.\n다른 칸을 선택해주세요.')

async def Yacht_choose_check(ctx,msg):
    global Yacht_choose_mode
    global Yacht_order
    global Yacht_point
    global Yacht_dice_fix
    global Yacht_dice_unfix
    global Yacht_left_dice
    global Yacht_stage
    if msg=='y':
        dice = []
        dice.extend(Yacht_dice_fix)
        dice.extend(Yacht_dice_unfix)
        number_count = []
        number_count.append(0)
        for i in range(1,7):
            number_count.append(dice.count(i))
        n = Yacht_choose_mode
        point = 0
        if n < 6:#ones/twos ... sixes
            point = number_count[n+1]*(n+1)
        elif n == 8:#three of kinds
            if max(number_count) >= 3:
                point = sum(dice)
        elif n == 9:#four of kinds
            if max(number_count) >= 4:
                point = sum(dice)
        elif n == 10:#full house
            if 3 in number_count and 2 in number_count:
                point = 25
        elif n == 11:#small straight
            if number_count[3]>=1 and number_count[4]>=1 and ((number_count[1]>=1 and number_count[2]>=1) or (number_count[2]>=1 and number_count[5]>=1) or (number_count[5]>=1 and number_count[6]>=1)):
                point = 30
        elif n == 12:#large straight
            if number_count[2]>=1 and number_count[3]>=1 and number_count[4]>=1 and number_count[5]>=1 and (number_count[1]>=1 or number_count[6]>=1):
                point = 40
        elif n == 13:#choice
            point = sum(dice)
        elif n == 14:#Yacht
            if max(number_count) == 5:
                point = 50

        Yacht_point[Yacht_order-1][Yacht_choose_mode] = point
        if n < 6:
            point = 0
            for i in range(6):
                if Yacht_point[Yacht_order-1][i] != '\u200B':
                    point += Yacht_point[Yacht_order-1][i]
            Yacht_point[Yacht_order-1][6] = point
            if point >= 63:
                Yacht_point[Yacht_order-1][7] = 35
            if max(number_count)==5 and Yacht_point[Yacht_order-1][14] != '\u200B' and Yacht_point[Yacht_order-1][14] != 0:
                Yacht_point[Yacht_order-1][14] += 100
        await ctx.send('선택이 완료되었습니다.\n현재 점수판을 확인합니다.')

        time.sleep(1)
        await Yacht_board(ctx)

        Yacht_order += 1
        if Yacht_order > Yacht_player_num:
            Yacht_order = 1
            Yacht_stage -= 1
            if Yacht_stage == 0:
                await Yacht_end(ctx)
                return
        Yacht_dice_fix = []
        Yacht_dice_unfix = [0,0,0,0,0]
        Yacht_left_dice = 3
        time.sleep(1)

        await ctx.send(Yacht_player[Yacht_order-1]+'의 턴 입니다.')
    else:
        await ctx.send('선택을 취소하셨습니다.\n다른 번호를 선택해주세요.')
    Yacht_choose_mode = -1

async def Yacht_end(ctx):
    global Yacht_point
    global Yacht_order
    
    time.sleep(1)
    await ctx.send('게임이 끝났습니다.\n결과를 출력합니다')
    time.sleep(1)
    Yacht_order = 0

    ybe_embed = discord.Embed(title = '>=----Yacht_score board----=<', description = '최종 점수 목록', color = 0x00ff56)

    ybe_embed_value ='\nones\ntwos\nthrees\nfours\nfives\nsixes\nsum\nbonus\n\
        three of kinds\nfour of kinds\nfull house\nsmall straight\nlarge straight\nchoice\nYacht\n\ntotal_score'
    ybe_embed.add_field(name = 'player : ', value = ybe_embed_value, inline = True)

    play_total_score = []
    for p_c, p in enumerate(Yacht_player):
        ybe_embed_value = ""
        if Yacht_point[p_c][7] == '\u200B':
            Yacht_point[p_c][7] = 0
        for c in range(len(['ones','twos','threes','fours','fives','sixes','sum','bonus','three of kinds','four of kinds','full house','small straight','large straight','choice','Yacht'])):
            if c==6:
                ybe_embed_value += '\n' + str(Yacht_point[p_c][c]) + ' / 63'
            else:
                ybe_embed_value += '\n' + str(Yacht_point[p_c][c])
        player_total_score = 0
        #6(sum) #7(bonus) .. #14(Yacht)
        for i in range(6,14+1):
            player_total_score += Yacht_point[p_c][i]
        play_total_score.append(player_total_score)
        ybe_embed_value += '\n\n' + str(player_total_score)
        ybe_embed.add_field(name = p, value = ybe_embed_value, inline = True)
    
    p_total_score = copy.deepcopy(play_total_score)

    win_count = play_total_score.count(max(play_total_score))
    win_player = '승자 플레이어 : '
    for i in range(win_count):
        win_player += Yacht_player[play_total_score.index(max(play_total_score))]
        play_total_score[play_total_score.index(max(play_total_score))] = -1
    ybe_embed.set_footer(text=win_player)
    
    await ctx.send(embed=ybe_embed)

    now_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    if Yacht_player_num == 1:
        await Yacht_record(ctx,'append','solo:'+Yacht_player[0]+'&'+str(p_total_score[0])+'&'+str(int((Yacht_point[0][14]+50)/100))+'&'+str(Yacht_point[0][7])+':'+now_time)
    elif Yacht_player_num == 2:
        await Yacht_record(ctx,'append','pvp:'+Yacht_player[0]+'&'+str(p_total_score[0])+'&'+str(int((Yacht_point[0][14]+50)/100))+'&'+str(Yacht_point[0][7])+':'+Yacht_player[1]+'&'+str(p_total_score[1])+'&'+str(int(Yacht_point[1][14]/100)+1)+'&'+str(Yacht_point[1][7])+':'+now_time)
    elif Yacht_player_num > 2:
        txt = 'pvp_extend:'
        for i in range(Yacht_player_num):
            txt += +Yacht_player[i]+'&'+str(p_total_score[i])+'&'+str(int((Yacht_point[i][14]+50)/100))+'&'+str(Yacht_point[i][7])+':'
        txt += now_time
        await Yacht_record(ctx,'append',txt)

    Yacht_point = []

async def Yacht_record(ctx,mode,command):
    file_name = 'yacht_record.txt'
    data = []
    with open(file_name, 'r', encoding='UTF8') as file:
        lines = file.readlines()
        player_data = []
        player_data_little = []
        player_data_little_2 = []
        player_data_count = 0
        for count, line in enumerate(lines):
            line = line.split('\n')[0]
            if line == 'player' or line == '---EOF---':
                if count != 0:
                    player_data.append(copy.copy(player_data_little))
                    data.append(copy.deepcopy(player_data))
                player_data = []
                player_data_little = []
                player_data_count = 0
            else:
                if line == 'level exp':
                    player_data_count = 1
                    player_data.append(copy.copy(player_data_little))
                    player_data_little = []
                elif line == 'ranking':
                    player_data_count = 2
                    player_data.append(copy.copy(player_data_little))
                    player_data_little = []
                elif line == '상대전적':
                    player_data_count = 3
                    player_data.append(copy.copy(player_data_little))
                    player_data_little = []
                elif line == '(player : win / draw / lose (point:point))':
                    player_data_count = 31
                elif line == '(whole : win / draw / lose)':
                    player_data_count = 32
                    player_data_little.append(copy.copy(player_data_little_2))
                    player_data_little_2 = []
                elif line == 'point record (시간:총 점수(Yacht개수, bonus 여부):versus(solo or pvp:point or pvp_extend:point:point))':
                    player_data_count = 4
                    player_data_little.append(copy.copy(player_data_little_2))
                    player_data_little_2 = []
                    player_data.append(copy.deepcopy(player_data_little))
                    player_data_little = []
                else:
                    if player_data_count == 31 or player_data_count == 32:
                        player_data_little_2.append(line)
                    else:
                        player_data_little.append(line)

    if mode == 'load':
        command2 = command.split(':')
        if command2[0] == 'ranking':
            total_player_name = []
            total_ranking = []
            total_level_exp = []
            for i in range(len(data)):
                total_player_name.append(data[i][0][0])
                total_ranking.append(int(data[i][2][0]))
                total_level_exp.append(data[i][1][0].split(' ')[0]+'lv. '+data[i][1][0].split(' ')[1]+'exp.')
            ranking_print_list = []
            for i in range(len(data)):
                index_ = total_ranking.index(min(total_ranking))
                ranking_print_list.append([total_player_name[index_],total_level_exp[index_]])
                total_ranking[index_] = max(total_ranking) + 1
            #embed 제작
            rank_embed = discord.Embed(title = '>=----Yacht_ranking----=<', color = 0x00ff56)

            ranking_print = ''
            player_print = ''
            le_print = ''
            for i,player_set in enumerate(ranking_print_list):
                ranking_print += str(i+1)+'\n'
                player_print += player_set[0]+'\n'
                le_print += player_set[1]+'\n'
            rank_embed.add_field(name = 'ranking', value = ranking_print, inline = True)
            rank_embed.add_field(name = 'player', value = player_print, inline = True)
            rank_embed.add_field(name = 'level & exp', value = le_print, inline = True)

            footer_txt = time.strftime('%Y년 %m월 %d일 %H시 %M분 %S초 기준', time.localtime(time.time()))
            rank_embed.set_footer(text=footer_txt)
            
            await ctx.send(embed=rank_embed)
        elif command2[0] == 'player':
            player_name = command2[2]

            check = 0
            for player_data in data:
                if player_data[0][0] == player_name:
                    check = 1
                    pl_embed = discord.Embed(title = '>=----player_log----=<', color = 0x00ff56)
                    if command2[1] == 'whole_log':
                        plwh_field1_name = 'player : '+player_data[0][0]
                        plwh_field1_value = player_data[1][0].split(' ')[0]+' lv. '+player_data[1][0].split(' ')[1]+' exp.\n'+'ranking : '+player_data[2][0]
                        pl_embed.add_field(name = plwh_field1_name, value = plwh_field1_value, inline = False)
                        plwh_field2_name = '상대전적\n(player : win / draw / lose (point:point))'
                        plwh_field2_value = ''
                        for c, line in enumerate(player_data[3][0]):
                            if c != 0:
                                plwh_field2_value += '\n'
                            plwh_field2_value += line
                        pl_embed.add_field(name = plwh_field2_name, value = plwh_field2_value, inline = False)
                        plwh_field3_name = '(whole : win / draw / lose)'
                        plwh_field3_value = player_data[3][1][0]
                        pl_embed.add_field(name = plwh_field3_name, value = plwh_field3_value, inline = False)
                        plwh_field4_name = 'point record (시간:총 점수(Yacht개수, bonus 여부):versus(solo or pvp:point or pvp_extend:point:point))'
                        plwh_field4_value = ''
                        for c, line in enumerate(player_data[4]):
                            if c != 0:
                                plwh_field4_value += '\n'
                            plwh_field4_value += line
                        pl_embed.add_field(name = plwh_field4_name, value = plwh_field4_value, inline = False)
                    elif command2[1] == 'versus_log':
                        plvs_field1_name = 'player : '+player_data[0][0]
                        plvs_field1_value = '상대전적(versus-log)'
                        pl_embed.add_field(name = plvs_field1_name, value = plvs_field1_value, inline = False)
                        plvs_field2_name = '(player : win / draw / lose (point:point))'
                        plvs_field2_value = ''
                        for c, line in enumerate(player_data[3][0]):
                            if c != 0:
                                plvs_field2_value += '\n'
                            plvs_field2_value += line
                        pl_embed.add_field(name = plvs_field2_name, value = plvs_field2_value, inline = False)
                        plvs_field3_name = '(whole : win / draw / lose)'
                        plvs_field3_value = player_data[3][1][0]
                        pl_embed.add_field(name = plvs_field3_name, value = plvs_field3_value, inline = False)
                    elif command2[1] == 'play_log':
                        plp_field1_name = 'player : '+player_data[0][0]
                        plp_field1_value = '게임 기록(play-log)'
                        pl_embed.add_field(name = plp_field1_name, value = plp_field1_value, inline = False)
                        plp_field2_name = 'point record (시간:총 점수(Yacht개수, bonus 여부):versus(solo or pvp:point or pvp_extend:point:point))'
                        plp_field2_value = ''
                        for c, line in enumerate(player_data[4]):
                            if c != 0:
                                plp_field2_value += '\n'
                            plp_field2_value += line
                        pl_embed.add_field(name = plp_field2_name, value = plp_field2_value, inline = False)
                    await ctx.send(embed = pl_embed)
                    break
            if check == 0:
                await ctx.send('in record, there is no player named \''+player_name+'\'')
        elif command2[0] == 'whole':
            txt = ''
            with open(file_name, 'r', encoding='UTF8') as file:
                lines = file.readlines()
                for line in lines:
                    txt += line
            await ctx.send(txt)
        elif command2[0] == 'record_ranking':
            rr_list_score = []
            rr_list_player = []
            counter1 = 0
            while counter1 < len(data):
                counter2 = 0
                player_name = data[counter1][0][0]
                while counter2 < len(data[counter1][4]):
                    line = data[counter1][4][counter2]
                    #2021-08-14-21-12-00 : 236(0, 35) : solo
                    #2021-08-14-22-54-00 : 184(0, 0) : pvp(KGHDI:223)
                    line_score = line.split(' ')[2].split('(')[0]
                    rr_list_score.append(int(line_score))
                    rr_list_player.append(player_name)
                    counter2 += 1
                counter1 += 1
            rr_list = []
            counter1 = 0
            for i in range(len(rr_list_score)):
                MAX_index = rr_list_score.index(max(rr_list_score))
                MAX_count = rr_list_score.count(max(rr_list_score))
                if counter1 == len(rr_list):
                    rr_list.append([str(rr_list_score[MAX_index]), rr_list_player[MAX_index]+'(x1)'])
                else:
                    players = rr_list[counter1][1].split(' ')
                    check = 0
                    for counter2, player in enumerate(players):
                        if player.split('(x')[0] == rr_list_player[MAX_index]:
                            players[counter2] = player.split('(x')[0] + '(x' + str(int(player.split('(x')[1].split(')')[0])+1) + ')'
                            check = 1
                    if check == 0:
                        players.append(rr_list_player[MAX_index]+'(x1)')

                    rr_list[counter1][1] = ' '.join(players)
                rr_list_score[MAX_index] = -1
                if MAX_count == 1:
                    counter1 += 1
            #[score,player(xn)]
            rr_embed = discord.Embed(title = '>=----Yacht_record_ranking----=<', color = 0x00ff56)
            rr_field1_name = 'ranking'
            rr_field2_name = 'score'
            rr_field3_name = 'player'
            rr_field1_value = ''
            rr_field2_value = ''
            rr_field3_value = ''
            for i in range(len(rr_list)):
                if i != 0:
                    rr_field1_value += '\n'
                    rr_field2_value += '\n'
                    rr_field3_value += '\n'
                rr_field1_value += str(i+1)
                rr_field2_value += rr_list[i][0]
                rr_field3_value += rr_list[i][1]
            rr_embed.add_field(name = rr_field1_name, value = rr_field1_value, inline = True)
            rr_embed.add_field(name = rr_field2_name, value = rr_field2_value, inline = True)
            rr_embed.add_field(name = rr_field3_name, value = rr_field3_value, inline = True)
            await ctx.send(embed = rr_embed)
        #ranking
        #player:whole_log:(player)
        #player:versus_log:(player)
        #player:play_log:(player)
        #whole
        #record_ranking
    elif mode == 'append':
        command2 = command.split(':')
        #solo:player&point&Yacht&Bonus:time
        #pvp:player&point&Yacht&Bonus:player&point&Yacht&Bonus:time
        #pvp_extend:player&point&Yacht&Bonus...:time
        if command2[0] == 'solo':
            score = command2[1].split('&')
            s_player = score[0]
            s_point = score[1]
            s_Yacht = score[2]
            s_Bonus = score[3]
            s_time = command2[2]

            put_check = len(data)
            count = 0
            for data_player in data:
                if data_player[0][0] == s_player:
                    put_check = 0
                    data[count][4].append(s_time+' : '+s_point+'('+s_Yacht+', '+s_Bonus+') : solo')
                    break
                count += 1
            if put_check != 0:
                count = -1

                temp_data = []
                temp_data2 = []
                temp_data3 = []
                temp_data2.append(s_player)
                temp_data.append(copy.copy(temp_data2))
                temp_data2 = []
                temp_data2.append('0 0')
                temp_data.append(copy.copy(temp_data2))
                temp_data2 = []
                temp_data2.append(str(put_check))
                temp_data.append(copy.copy(temp_data2))
                temp_data2 = []
                temp_data2.append(copy.copy(temp_data3))
                temp_data3.append('whole : 0 / 0 / 0')
                temp_data2.append(copy.copy(temp_data3))
                temp_data.append(copy.deepcopy(temp_data2))
                temp_data2 = []
                temp_data2.append(s_time+' : '+s_point+'('+s_Yacht+', '+s_Bonus+') : solo')
                temp_data.append(copy.copy(temp_data2))
                data.append(copy.deepcopy(temp_data))
            
            get_exp_p = int(math.pow((float(int(s_point))/100.0), 2.0))
            #점수 당 exp : (point/100)^2를 내림한 값
            level_exp = list(map(int,data[count][1][0].split(' ')))
            level = level_exp[0]
            exp = level_exp[1] + get_exp_p
            if level == 0:
                if exp >= 10:
                    level = 1
                    exp -= 10
            while level*10 <= exp:
                exp -= level*10
                level += 1
            data[count][1][0] = str(level)+' '+str(exp)

            total_level = []
            total_ranking = []
            player_total_num = len(data)
            for i in range(player_total_num):
                total_level.append(int(data[i][1][0].split(' ')[0]))
                total_ranking.append(int(data[i][2][0]))
            for i in range(player_total_num):
                if total_level[count] > total_level[i] and total_ranking[count] > total_ranking[i]:
                    total_ranking[count] -= 1
                    total_ranking[i] += 1
            for i in range(player_total_num):
                data[i][2][0] = str(total_ranking[i])
        elif command2[0] == 'pvp':
            score1 = command2[1].split('&')
            s1_player = score1[0]
            s1_point = score1[1]
            s1_Yacht = score1[2]
            s1_Bonus = score1[3]
            score2 = command2[2].split('&')
            s2_player = score2[0]
            s2_point = score2[1]
            s2_Yacht = score2[2]
            s2_Bonus = score2[3]
            s_time = command2[3]
            winning = 0
            if int(s1_point) > int(s2_point):
                winning = 1
            elif int(s1_point) < int(s2_point):
                winning = 2

            #s1_player_save
            pvp_win = 0
            pvp_draw = 0
            pvp_lose = 0
            if winning == 1:
                pvp_win += 1
            elif winning == 2:
                pvp_lose += 1
            elif winning == 0:
                pvp_draw += 1
            
            pvp_player_me = s1_player
            pvp_player_op = s2_player
            pvp_my_point = s1_point
            pvp_my_Yacht = s1_Yacht
            pvp_my_Bonus = s1_Bonus
            pvp_op_point = s2_point

            put_check = 0
            count = 0
            for data_player in data:
                if data_player[0][0] == pvp_player_me:
                    put_check = 1
                    data[count][4].append(s_time+' : '+pvp_my_point+'('+pvp_my_Yacht+', '+pvp_my_Bonus+') : pvp('+pvp_player_op+':'+pvp_op_point+')')
                    put_check2 = 0
                    for pvp_count,pvp_data in enumerate(data[count][3][0]):
                        if pvp_data.split(' ')[0] == pvp_player_op:
                            put_check2 = 1
                            pvp_win_ = pvp_win + int(pvp_data.split(' ')[2])
                            pvp_draw_ = pvp_draw + int(pvp_data.split(' ')[4])
                            pvp_lose_ = pvp_lose + int(pvp_data.split(' ')[6])
                            pvp_my_point += int(pvp_data.split(' ')[7].split(':')[0].split('(')[1])
                            pvp_op_point += int(pvp_data.split(' ')[7].split(':')[1].split(')')[0])
                            data[count][3][0][pvp_count] = pvp_player_op+' : '+str(pvp_win_)+' / '+str(pvp_draw_)+' / '+str(pvp_lose_)+' ('+str(pvp_my_point)+':'+str(pvp_op_point)+')'
                    if put_check2 == 0:
                        data[count][3][0].append(pvp_player_op+' : '+str(pvp_win)+' / '+str(pvp_draw)+' / '+str(pvp_lose)+' ('+str(pvp_my_point)+':'+str(pvp_op_point)+')')
                    #KGHDI : 1 / 0 / 3 (912:863)
                    #whole : 1 / 0 / 3
                    pvp_win += int(data_player[3][1][0].split(' ')[2])
                    pvp_draw += int(data_player[3][1][0].split(' ')[4])
                    pvp_lose += int(data_player[3][1][0].split(' ')[6])
                    data[count][3][1][0] = 'whole : '+str(pvp_win)+' / '+str(pvp_draw)+' / '+str(pvp_lose)
                    break
                count += 1
            if put_check == 0:
                count = -1

                temp_data = []
                temp_data2 = []
                temp_data3 = []
                temp_data2.append(pvp_player_me)
                temp_data.append(copy.copy(temp_data2))
                temp_data2 = []
                temp_data2.append('0 0')
                temp_data.append(copy.copy(temp_data2))
                temp_data2 = []
                temp_data2.append(str(len(data)+1))
                temp_data.append(copy.copy(temp_data2))
                temp_data2 = []
                temp_data3.append(pvp_player_op+' : '+str(pvp_win)+' / '+str(pvp_draw)+' / '+str(pvp_lose)+' ('+str(pvp_my_point)+':'+str(pvp_op_point)+')')
                temp_data2.append(copy.copy(temp_data3))
                temp_data3 = []
                temp_data3.append('whole : '+str(pvp_win)+' / '+str(pvp_draw)+' / '+str(pvp_lose))
                temp_data2.append(copy.copy(temp_data3))
                temp_data.append(copy.deepcopy(temp_data2))
                temp_data2 = []
                temp_data2.append(s_time+' : '+pvp_my_point+'('+pvp_my_Yacht+', '+pvp_my_Bonus+') : pvp ('+pvp_player_op+':'+pvp_op_point+')')
                temp_data.append(copy.copy(temp_data2))
                data.append(copy.deepcopy(temp_data))

            get_exp_p = 0
            if winning == 1:
                get_exp_p = 5*Yacht_player_num
            elif winning == 0:
                get_exp_p = int(2.5*Yacht_player_num)
            #승리시 exp : (5*player_num)
            get_exp_p += int(math.pow((float(int(s1_point))/100.0), 2.0))
            #점수 당 exp : (point/100)^2를 내림한 값
            level_exp = list(map(int,data[count][1][0].split(' ')))
            level = level_exp[0]
            exp = level_exp[1] + get_exp_p
            if level == 0:
                if exp >= 10:
                    level = 1
                    exp -= 10
            while level*10 <= exp:
                exp -= level*10
                level += 1
            data[count][1][0] = str(level)+' '+str(exp)

            total_level = []
            total_ranking = []
            player_total_num = len(data)
            for i in range(player_total_num):
                total_level.append(int(data[i][1][0].split(' ')[0]))
                total_ranking.append(int(data[i][2][0]))
            for i in range(player_total_num):
                if total_level[count] > total_level[i] and total_ranking[count] > total_ranking[i]:
                    total_ranking[count] -= 1
                    total_ranking[i] += 1
            for i in range(player_total_num):
                data[i][2][0] = str(total_ranking[i])


            #s2_player_save
            pvp_win = 0
            pvp_draw = 0
            pvp_lose = 0
            if winning == 2:
                pvp_win += 1
            elif winning == 1:
                pvp_lose += 1
            elif winning == 0:
                pvp_draw += 1
            
            pvp_player_me = s2_player
            pvp_player_op = s1_player
            pvp_my_point = s2_point
            pvp_my_Yacht = s2_Yacht
            pvp_my_Bonus = s2_Bonus
            pvp_op_point = s1_point

            put_check = 0
            count = 0
            for data_player in data:
                if data_player[0][0] == pvp_player_me:
                    put_check = 1
                    data[count][4].append(s_time+' : '+pvp_my_point+'('+pvp_my_Yacht+', '+pvp_my_Bonus+') : pvp('+pvp_player_op+':'+pvp_op_point+')')
                    put_check2 = 0
                    for pvp_count,pvp_data in enumerate(data[count][3][0]):
                        if pvp_data.split(' ')[0] == pvp_player_op:
                            put_check2 = 1
                            pvp_win_ = pvp_win + int(pvp_data.split(' ')[2])
                            pvp_draw_ = pvp_draw + int(pvp_data.split(' ')[4])
                            pvp_lose_ = pvp_lose + int(pvp_data.split(' ')[6])
                            pvp_my_point += int(pvp_data.split(' ')[7].split(':')[0].split('(')[1])
                            pvp_op_point += int(pvp_data.split(' ')[7].split(':')[1].split(')')[0])
                            data[count][3][0][pvp_count] = pvp_player_op+' : '+str(pvp_win_)+' / '+str(pvp_draw_)+' / '+str(pvp_lose_)+' ('+str(pvp_my_point)+':'+str(pvp_op_point)+')'
                    if put_check2 == 0:
                        data[count][3][0].append(pvp_player_op+' : '+str(pvp_win)+' / '+str(pvp_draw)+' / '+str(pvp_lose)+' ('+str(pvp_my_point)+':'+str(pvp_op_point)+')')
                    #KGHDI : 1 / 0 / 3 (912:863)
                    #whole : 1 / 0 / 3
                    pvp_win += int(data_player[3][1][0].split(' ')[2])
                    pvp_draw += int(data_player[3][1][0].split(' ')[4])
                    pvp_lose += int(data_player[3][1][0].split(' ')[6])
                    data[count][3][1][0] = 'whole : '+str(pvp_win)+' / '+str(pvp_draw)+' / '+str(pvp_lose)
                    break
                count += 1
            if put_check == 0:
                count = -1
                temp_data = []
                temp_data2 = []
                temp_data3 = []
                temp_data2.append(pvp_player_me)
                temp_data.append(copy.copy(temp_data2))
                temp_data2 = []
                temp_data2.append('0 0')
                temp_data.append(copy.copy(temp_data2))
                temp_data2 = []
                temp_data2.append(str(len(data)+1))
                temp_data.append(copy.copy(temp_data2))
                temp_data2 = []
                temp_data3.append(pvp_player_op+' : '+str(pvp_win)+' / '+str(pvp_draw)+' / '+str(pvp_lose)+' ('+str(pvp_my_point)+':'+str(pvp_op_point)+')')
                temp_data2.append(copy.copy(temp_data3))
                temp_data3 = []
                temp_data3.append('whole : '+str(pvp_win)+' / '+str(pvp_draw)+' / '+str(pvp_lose))
                temp_data2.append(copy.copy(temp_data3))
                temp_data.append(copy.deepcopy(temp_data2))
                temp_data2 = []
                temp_data2.append(s_time+' : '+pvp_my_point+'('+pvp_my_Yacht+', '+pvp_my_Bonus+') : pvp ('+pvp_player_op+':'+pvp_op_point+')')
                temp_data.append(copy.copy(temp_data2))
                data.append(copy.deepcopy(temp_data))
            
            get_exp_p = 0
            if winning == 2:
                get_exp_p = 5*Yacht_player_num
            elif winning == 0:
                get_exp_p = int(2.5*Yacht_player_num)
            #승리시 exp : (5*player_num)
            get_exp_p += int(math.pow((float(int(s2_point))/100.0), 2.0))
            #점수 당 exp : (point/100)^2를 내림한 값
            level_exp = list(map(int,data[count][1][0].split(' ')))
            level = level_exp[0]
            exp = level_exp[1] + get_exp_p
            if level == 0:
                if exp >= 10:
                    level = 1
                    exp -= 10
            while level*10 <= exp:
                exp -= level*10
                level += 1
            data[count][1][0] = str(level)+' '+str(exp)

            total_level = []
            total_ranking = []
            player_total_num = len(data)
            for i in range(player_total_num):
                total_level.append(int(data[i][1][0].split(' ')[0]))
                total_ranking.append(int(data[i][2][0]))
            for i in range(player_total_num):
                if total_level[count] > total_level[i] and total_ranking[count] > total_ranking[i]:
                    total_ranking[count] -= 1
                    total_ranking[i] += 1
            for i in range(player_total_num):
                data[i][2][0] = str(total_ranking[i])
        elif command2[0] == 'pvp_extend':
            s_time = command2[Yacht_player_num+1]
            command_ = []
            for i in range(Yacht_player_num):
                command_.append(command2[i+1].split('&'))
            #command_ = [[player,point,Yacht,Bonus],[player,point,Yacht,Bonus],[player,point,Yacht,Bonus]]
            #pvp_extend : win / draw / lose (point)
            #whole : win / draw / lose
            #time : point(Yacht, Bonus) : pvp_extend(player:point,player:point)

            point = []
            for i in range(Yacht_player_num):
                point.append(int(command_[i][1]))
            pvp_win = []
            pvp_draw = []
            pvp_lose = []
            for i in range(Yacht_player_num):
                if max(point) == point[i]:
                    if point.count(max(point)) == Yacht_player_num:
                        #draw
                        pvp_win.append(0)
                        pvp_draw.append(1)
                        pvp_lose.append(0)
                    else:
                        #win
                        pvp_win.append(1)
                        pvp_draw.appned(0)
                        pvp_lose.append(0)
                else:
                    #lose
                    pvp_win.append(0)
                    pvp_draw.append(0)
                    pvp_lose.append(1)
            #win/draw/lose
            for i in range(Yacht_player_num):
                put_check = 0
                count = 0
                for data_player in data:
                    if data_player[0][0] == command_[i][0]:
                        put_check = 1
                        txt = s_time+' : '+command_[i][1]+'('+command_[i][2]+', '+command_[i][4]+') : pvp_extend('
                        for j in range(Yacht_player_num):
                            if i != j:
                                txt += command_[j][0] + ':' + command_[j][1]
                                if (i != Yacht_player_num-1 and j != Yacht_player_num-1) or (i == Yacht_player_num-1 and j != Yacht_player_num-2):
                                    txt += ','
                        txt += ')'
                        data[count][4].append(txt)
                        put_check2 = 0
                        for pvp_count,pvp_data in enumerate(data[count][3][0]):
                            if pvp_data.split(' ')[0] == 'pvp_extend':
                                put_check2 = 1
                                pvp_win_ = pvp_win[i] + int(pvp_data.split(' ')[2])
                                pvp_draw_ = pvp_draw[i] + int(pvp_data.split(' ')[4])
                                pvp_lose_ = pvp_lose[i] + int(pvp_data.split(' ')[6])
                                data[count][3][0][pvp_count] = 'pvp_extend : '+str(pvp_win_)+' / '+str(pvp_draw_)+' / '+str(pvp_lose_)+' ('+str(command_[i][1]+int(pvp_data.split(' ')[7].split('(')[1].split(')')[0]))+')'
                        if put_check2 == 0:
                            data[count][3][0].append('pvp_extend'+' : '+str(pvp_win[i])+' / '+str(pvp_draw[i])+' / '+str(pvp_lose[i])+' ('+str(command_[i][1])+')')
                        pvp_win_ = pvp_win[i] + int(data_player[3][1][0].split(' ')[2])
                        pvp_draw_ = pvp_draw[i] + int(data_player[3][1][0].split(' ')[4])
                        pvp_lose_ = pvp_lose[i] + int(data_player[3][1][0].split(' ')[6])
                        data[count][3][1][0] = 'whole : '+str(pvp_win_)+' / '+str(pvp_draw_)+' / '+str(pvp_lose_)
                        break
                    count += 1
                if put_check == 0:
                    count = -1
                    temp_data = []
                    temp_data2 = []
                    temp_data3 = []
                    temp_data2.append(command_[i][0])
                    temp_data.append(copy.copy(temp_data2))
                    temp_data2 = []
                    temp_data2.append('0 0')
                    temp_data.append(copy.copy(temp_data2))
                    temp_data2 = []
                    temp_data2.append(str(len(data)+1))
                    temp_data.append(copy.copy(temp_data2))
                    temp_data2 = []
                    temp_data3.append('pvp_extend : '+str(pvp_win[i])+' / '+str(pvp_draw[i])+' / '+str(pvp_lose[i])+' ('+str(command_[i][1])+')')
                    temp_data2.append(copy.copy(temp_data3))
                    temp_data3 = []
                    temp_data3.append('whole : '+str(pvp_win[i])+' / '+str(pvp_draw[i])+' / '+str(pvp_lose[i]))
                    temp_data2.append(copy.copy(temp_data3))
                    temp_data.append(copy.deepcopy(temp_data2))
                    temp_data2 = []
                    txt = s_time+' : '+command_[i][1]+'('+command_[i][2]+', '+command_[i][4]+') : pvp_extend('
                    for j in range(Yacht_player_num):
                        if i != j:
                            txt += command_[j][0] + ':' + command_[j][1]
                            if (i != Yacht_player_num-1 and j != Yacht_player_num-1) or (i == Yacht_player_num-1 and j != Yacht_player_num-2):
                                txt += ','
                    txt += ')'
                    temp_data2.append(txt)
                    temp_data.append(copy.copy(temp_data2))
                    data.append(copy.deepcopy(temp_data))
                
                get_exp_p = 0
                if pvp_win[i] == 1:
                    get_exp_p = 5*Yacht_player_num
                elif pvp_draw[i] == 1:
                    get_exp_p = int(2.5*Yacht_player_num)
                #승리시 exp : (5*player_num)
                get_exp_p += int(math.pow((float(int(command_[i][1]))/100.0), 2.0))
                #점수 당 exp : (point/100)^2를 내림한 값
                level_exp = list(map(int,data[count][1][0].split(' ')))
                level = level_exp[0]
                exp = level_exp[1] + get_exp_p
                if level == 0:
                    if exp >= 10:
                        level = 1
                        exp -= 10
                while level*10 <= exp:
                    exp -= level*10
                    level += 1
                data[count][1][0] = str(level)+' '+str(exp)

                total_level = []
                total_ranking = []
                player_total_num = len(data)
                for i in range(player_total_num):
                    total_level.append(int(data[i][1][0].split(' ')[0]))
                    total_ranking.append(int(data[i][2][0]))
                for i in range(player_total_num):
                    if total_level[count] > total_level[i] and total_ranking[count] > total_ranking[i]:
                        total_ranking[count] -= 1
                        total_ranking[i] += 1
                for i in range(player_total_num):
                    data[i][2][0] = str(total_ranking[i])
            #data / exp / ranking append

        with open(file_name, 'w', encoding='UTF8') as file:
            for player_data in data:
                for count, player_data_little in enumerate(player_data):
                    if count == 0:
                        file.write('player\n'+player_data_little[0]+'\n')
                    elif count == 1:
                        file.write('level exp\n'+player_data_little[0]+'\n')
                    elif count == 2:
                        file.write('ranking\n'+player_data_little[0]+'\n')
                    elif count == 3:
                        file.write('상대전적\n')
                        for count_2, player_data_little2 in enumerate(player_data_little):
                            if count_2 == 0:
                                file.write('(player : win / draw / lose (point:point))\n')
                                for line in player_data_little2:
                                    file.write(line+'\n')
                            elif count_2 == 1:
                                file.write('(whole : win / draw / lose)\n')
                                for line in player_data_little2:
                                    file.write(line+'\n')
                    elif count == 4:
                        file.write('point record (시간:총 점수(Yacht개수, bonus 여부):versus(solo or pvp:point or pvp_extend:point:point))\n')
                        for line in player_data_little:
                            file.write(line+'\n')
            file.write('---EOF---')

client.run('') ## 디스코드 봇을 위한 별개의 값 적용 필요

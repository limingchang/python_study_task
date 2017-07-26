#作者：Mc.Lee
print("choose the model:Login(l or login) or exit(q)")


def mo_user():
    act = input('input command:')
    act = act.lower()
    if act == 'login' or act == 'l':
        if u_login():
            print('login success!')
        else:
            print('input error or you has been locked!')
            mo_user()
    elif act == 'q':
        exit()
    else:
        print('command input is error,please input again!')
        mo_user()
    return

def u_login():
    result = False
    username = input('username:')
    password = input('password:')
    with open('users.txt.txt','r') as u_file:
        content = u_file.readlines()
    i = 0
    for line in content:
        line = line.rstrip('\n')
        content[i] = line
        u_info = line.split(',')
        if u_info[0] != username:
            i += 1
            continue
        else:
            if int(u_info[2]) >= 3:
                print('user has been locked!')
                return False
            else:
                if u_info[1] == password:
                    print('welcome ',username)
                    result = True
                else:
                    u_info[2] = int(u_info[2]) + 1
                    str = '%s,%s,%s'%(u_info[0],u_info[1],u_info[2])
                    content[i] = str
                    c_str = '\n'
                    c_str = c_str.join(content)

                    with open('users.txt.txt','w') as u_file:
                        u_file.write(c_str)
                    if u_info[2] == 3:
                        print('Wrong password more than 3 times!')
                        exit()
                    else:
                        print('password error!')
                        u_login()
                    result = False
        i += 1
    return result


mo_user()

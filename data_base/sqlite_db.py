import sqlite3 as sq
from create_bot import bot


def sql_start():
    global base, cur
    base = sq.connect('iceberg_garage.db')
    cur = base.cursor()
    if base:
        print('Data base connected!')
    base.execute('CREATE TABLE IF NOT EXISTS garage (car_num INTEGER PRIMARY KEY, changes TEXT, time TEXT, img TEXT)')
    base.commit()


async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO garage VALUES (?,?,?,?)', tuple(data.values()))
        base.commit()


async def sql_read(message):
    for ret in cur.execute('SELECT * FROM garage').fetchall():
        await bot.send_photo(message.from_user.id, ret[3], f'Машина: {ret[0]}\nЧто поменяли: {ret[1]}\nДата: {ret[2]}')
        print(ret)


async def sql_delta_to(message):
    big = []
    tsm = []
    num = []
    mile = []
    next_to = []
    delta = []
    sam = 0
    ton = 0
    mix = 0
    sam_zero_to = []
    print('--a')
    for ret in cur.execute('SELECT * FROM garage_TO').fetchall():
        if ret[3] > 0 and ret[0] != 'М':
            tsm.append(ret[0])
            num.append(ret[1])
            mile.append(ret[2])
            next_to.append(ret[3])
            delta.append(ret[3]-ret[2])
            if ret[0] == 'С':
                sam += 1
            elif ret[0] == 'Т':
                ton += 1

        elif ret[3] == 0 and ret[0] == 'С':
            sam_zero_to.append(ret[1])




    result = sorted(zip(delta, num, mile, next_to, tsm), reverse=True)
    answer = []
    red = 0
    ora = 0
    gre = 0

    for i in result:
        if i[0] < 0:
            red += 1
            # answer.append(f'🔴{i[4]} {i[1]} <b>{str(i[0])}</b> {i[2]} {i[3]}\n')
            answer.append(f'🔴{i[4]}{i[1]} _{str(i[0])}_ {i[2]} {i[3]}\n')
        elif i[0] < 5000:
            ora += 1
            answer.append(f'🟠{i[4]}{i[1]} _{str(i[0])}_ {i[2]} {i[3]}\n')
        else:
            gre += 1
            answer.append(f'🟢{i[4]}{i[1]} _{str(i[0])}_ {i[2]} {i[3]}\n')

    answer = ''.join(answer)
    num_sam_zero_to = len(sam_zero_to)
    sam_zero_to = ''.join(str(sam_zero_to))

    if num_sam_zero_to > 0:
        answer += f'\nИтого:\n🔴{red} 🟠{ora} 🟢{gre}\n\nВсего:{red+ora+gre} ({sam} Сам и {ton} Тон)\n⚠️ ТО не указано у *{num_sam_zero_to} Сам*:\n{str(sam_zero_to)}'
    else:
        answer += f'\nИтого:\n🔴{red} 🟠{ora} 🟢{gre}\n\nВсего:{red+ora+gre} ({sam} Сам и {ton} Тон)\n'

    await bot.send_message(message.from_user.id, answer, parse_mode='Markdown')


async def sql_update(state, new_TO, car_num, time):
    async with state.proxy() as data:
        cur.execute('UPDATE garage_TO SET new_TO == ?, time == ? WHERE car_num == ? ', (new_TO, time, car_num))
        base.commit()




# async def sql_delta_to(message):
#         big = []
#         for ret in cur.execute('SELECT * FROM garage_TO').fetchall():
#             big.append(ret)
#         return big

    # print(big)
    # bot.send_message(message.from_user.id, big)

        # await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nописание: {ret[2]}\nЦена: {ret[-1]}')
        # print(ret)

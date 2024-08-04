from bot import start_bot
import asyncio


if __name__ == '__main__':
    x = {1:'a', 2:'b', 3:'c'}
    # for s, n in x:
    #     print(s, n)
    asyncio.run(start_bot())
    # todo: написать модуль, ответственный за мониторинг вполнения заданий
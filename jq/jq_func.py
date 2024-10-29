import time


async def long_task(data: dict) -> str:
    uid = data['uid']
    print(f'start {uid}')
    time.sleep(20)
    print(f'fin {uid}')
    return f"fin：{uid}"

import time

async def long_task(data: dict) -> dict:
    uid = data['data']
    print(f'start {uid}')
    time.sleep(10) 
    print(f'fin {uid}')
    return {"uid":uid}

async def long_loop(data: dict) -> dict:
    d = data['data']
    print(f'start {d}')
    time.sleep(1) 
    result = d+1
    print(f'fin {d}')
    return {"result":result, "data":d}

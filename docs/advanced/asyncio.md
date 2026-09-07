# 19 — Asyncio

> asyncio runs async I/O on a single thread- thousands of
> sockets, files,and http calls without threads. The mental
> model: await yields control back to the event loop while
> an operation completes in the background.

---

## the event loop - asyncio.run

```python
import asyncio

async def main():
    print("start")
    await asyncio.sleep(1)
    print("end")

asyncio.run(main())
```

async def defines a coroutine; await suspends it until
the awaited thing finishes. asyncio.run() bootsthera event
loop, runs your coroutine, cleans up. - never manage
the loop by hand.

---

## async tasks - run concurrently

```python
import asyncio

async def fetch(name,delay):
    await asyncio.sleep(delay)
    return f"{name} done"

async def main():
    t1 = asyncio.create_task(fetch("a",1))
    t2 = asyncio.create_task(fetch("b",2))
    print(await asyncio.gather(t1,t2))
    # ['a done','b done']

asyncio.run(main())
```

create_task schedules coroutines to run in the background;
gather awaits them all and collects results in order. Total
time ~2s,not 3: the sleeps overlap.

---

## timeouts - asyncio.wait_for

```python
import asyncio

async def slow():
    await asyncio.sleep(10)

async def main():
    try:
        result = await asyncio.wait_for(slow(),timeout=1)
        print(result)
    except asyncio.TimeoutError:
        print("timed out")

asyncio.run(main())
```

wait_for races coroutine against a timeout. If it loses,
it cancels the task and raises TimeoutError- clean way to
bound external calls like db/http.

---

## parallel http - aiohttp sketch

```python
import asyncio
import aiohttp

async def main():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://httpbin.org/get") as resp:
            data = await resp.json()
    print(data["url"])

asyncio.run(main())
```

aiohttp: async http client. async with manages the session
and response lifetime; await resp.json() reads body without
blocking the loop. (Install with: `python -m pip install aiohttp`.)

---

## Task cancellation

```python
import asyncio

async def tick():
    await asyncio.sleep(0.5)
    print("tick")

async def main():
    task = asyncio.create_task(tick())
    await asyncio.sleep(0.8)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("cancelled")
```

task.cancel() requests cancellation; the coroutine sees
CancelledError at its next suspension point. Wrap cleanup in
try/finally if cancel may leave resources open.

---

## asyncio.Queue - producer/consumer

```python
import asyncio

async def producer(q):
    for i in range(5):
        await q.put(i)
    await q.put(None) # sentinel

async def consumer(q):
    while True:
        item = await q.get()
        if item is None:
            break
        print("got",item)

async def main():
    q = asyncio.Queue()
    await asyncio.gather(producer(q), consumer(q))

asyncio.run(main())
```

Queue passes values between coroutines. None acts as a
sentinel- the polite way to say " done". gather runs producer
and consumer interleaved on one loop.

---

## running blocking code - to_thread

```python
import asyncio
import time

def blocking():
    time.sleep(2)
    return "result"

async def main():
    r = await asyncio.to_thread(blocking)
    print(r) # result -- after ~2s; the loop stays free

asyncio.run(main())
```

Blocking I/O functions would starve the loop; wrap them in
asyncio.to_thread to run on a worker thread while awaiting. For
CPU-bound work, prefer a process pool because threads do not remove
CPython's usual GIL limitation.

---

## Next steps

go to Concurrency at advanced/concurrency.md
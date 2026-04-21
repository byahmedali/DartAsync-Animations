import glob
import re

replacements = {
    'async def fetch_data(param):': 'Future<String> fetchData(int param) async {',
    'await asyncio.sleep(param)': 'await Future.delayed(Duration(seconds: param));',
    'return f"Result of {param}"': 'return "Result of $param";',
    'print(f"Do something with {param}...")': 'print("Do something with $param...");',
    'print(f"Done with {param}")': 'print("Done with $param");',
    'async def main():': 'Future<List<String>> mainLogic() async {',
    'task1 = asyncio.create_task(fetch_data(1))': 'var task1 = fetchData(1);',
    'task2 = asyncio.create_task(fetch_data(2))': 'var task2 = fetchData(2);',
    'result1 = await task1': 'var result1 = await task1;',
    'result2 = await task2': 'var result2 = await task2;',
    'print("Task 1 fully completed")': 'print("Task 1 fully completed");',
    'print("Task 2 fully completed")': 'print("Task 2 fully completed");',
    'return [result1, result2]': 'return [result1, result2];',
    'task1 = fetch_data(1)  # Could be awaited directly': 'var task1 = fetchData(1);',
    'task2 = fetch_data(2)  # Could be awaited directly': 'var task2 = fetchData(2);',
    'time.sleep(param)': 'sleep(Duration(seconds: param));',
    'print(f"Do something with {param}...", flush=True)': 'print("Do something with $param...");',
    'print(f"Done with {param}", flush=True)': 'print("Done with $param");',
    'def fetch_data(param):': 'String fetchData(int param) {',
}

regex_replacements = [
    # example 6
    (r'task1 = asyncio\.create_task\(asyncio\.to_thread\(fetch_data, 1\)\)', r'var task1 = Isolate.run(() => fetchData(1));'),
    (r'task2 = asyncio\.create_task\(asyncio\.to_thread\(fetch_data, 2\)\)', r'var task2 = Isolate.run(() => fetchData(2));'),
    (r'print\("Thread 1 fully completed"\)', r'print("Isolate 1 fully completed");'),
    (r'print\("Thread 2 fully completed"\)', r'print("Isolate 2 fully completed");'),
    (r'loop = asyncio\.get_running_loop\(\)', r'// Dart usually relies on isolates'),
    (r'with ProcessPoolExecutor\(\) as executor:', r'// for true multiprocessing since it doesn\'t share memory.'),
    (r'task1 = loop\.run_in_executor\(executor, fetch_data, 1\)', r'// var task1 = Isolate.run(() => fetchData(1));'),
    (r'task2 = loop\.run_in_executor\(executor, fetch_data, 2\)', r'// var task2 = Isolate.run(() => fetchData(2));'),
    (r'print\("Process 1 fully completed"\)', r'// print("Process 1 fully completed");'),
    (r'print\("Process 2 fully completed"\)', r'// print("Process 2 fully completed");'),
    
    # example 7
    (r'print\(f"Task 1 and 2 awaited results: \{\[result1, result2\]\}"\)', r'print("Task 1 and 2 awaited results: [$result1, $result2]");'),
    (r'coroutines = \[fetch_data\(i\) for i in range\(1, 3\)\]', r'var futures1 = [1, 2].map((i) => fetchData(i)).toList();'),
    (r'results = await asyncio\.gather\(\*coroutines, return_exceptions=True\)', r'var results1 = await Future.wait(futures1);'),
    (r'print\(f"Coroutine Results: \{results\}"\)', r'print("Future.wait Results: $results1");'),
    (r'tasks = \[asyncio\.create_task\(fetch_data\(i\)\) for i in range\(1, 3\)\]', r'var futures2 = [1, 2].map((i) => fetchData(i)).toList();'),
    (r'results = await asyncio\.gather\(\*tasks\)', r'var results2 = await Future.wait(futures2);'),
    (r'print\(f"Task Results: \{results\}"\)', r'print("Task Results: $results2");'),
    (r'async with asyncio\.TaskGroup\(\) as tg:', r'var results3 = await Future.wait([1, 2].map((i) => fetchData(i)));'),
    (r'results = \[tg\.create_task\(fetch_data\(i\)\) for i in range\(1, 3\)\]', r'// All tasks awaited simultaneously'),
    (r'# All tasks are awaited when the context manager exits\.', r'//'),
    (r'print\(f"Task Group Results: \{\[result\.result\(\) for result in results\]\}"\)', r'print("Task Group Results: $results3");'),
    (r'return "Main Coroutine Done"', r'return "Main Coroutine Done";'),
    (r'to_thread\(fetch_data, 1\)', r'Isolate.run(1)'),
    (r'to_thread\(fetch_data, 2\)', r'Isolate.run(2)'),
    (r'run_in_executor\(fetch_data, 1\)', r'Isolate.run()'),
    (r'run_in_executor\(fetch_data, 2\)', r'Isolate.run()'),
    
    # Fixing the missing bracket visually
    (r'(return "Result of \$param";</span>)\n</code></pre>', r'\1\n    <span class="line-x">}</span></code></pre>'),
    (r'(return \[result1, result2\];</span>)\n</code></pre>', r'\1\n<span class="line-x">}</span></code></pre>'),
    (r'(return "Main Coroutine Done";</span>)\n</code></pre>', r'\1\n<span class="line-x">}</span></code></pre>'),
]

for js_file in glob.glob(r'c:\Users\aa304\Downloads\AsyncIO-Animations\js\*.js'):
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for k, v in replacements.items():
        content = content.replace(k, v)
        
    for k, v in regex_replacements:
         content = re.sub(k, v, content)
         
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(content)

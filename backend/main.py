import json, os

def get_data():
    with open('data.json', 'r') as f:
        problem_data = json.loads(f.read())

    for x in range(1996, 2024):
        year_code = str(x)[2:]

        #problems
        problems = problem_data[year_code]

        #data
        data = os.listdir(f"data/{x}/")

        #references
        pdfs = os.listdir(f"problems/{x}/")

#get data by year
def get_data_by_year(year):
    with open('data.json', 'r') as f:
        problem_data = json.loads(f.read())
    
    problems = problem_data[str(year)[2:]]

    files = os.listdir(f"data/{year}/")

def get_pdf(year, problem):
    if ('s' in problem):
        return os.listdir(f"problems/{year}/")[1]
    else:
        return os.listdir(f"problems/{year}/")[0]

def judge(year, problem, src):
    
    files = os.listdir(f"data/{year}/")

    input_paths = []
    output_paths = []

    for file in files:
        if problem in file:
            if file.endswith('.in'):
                input_paths.append(os.path.join(os.path.dirname(__file__), "data", str(year), file))
            elif file.endswith('.out'):
                output_paths.append(os.path.join(os.path.dirname(__file__), "data", str(year), file))

    status = []

    with open('out.py', 'w+') as f:
        f.write('import time, atexit\nstart_time = time.time()\natexit.register(lambda: print(time.time()-start_time))\n' + src)    

    total_time = []

    for x in range(len(input_paths)): 
        cmd = os.system(f'type {input_paths[x]} | python3 out.py > out.txt')
        
        if cmd != 0:
            return False, round(sum(total_time), 3)

        with open(output_paths[x], 'r') as f1, open('out.txt', 'r') as f2:
            parse = f2.read().split('\n')
            
            exec_time = parse.pop(-2)
            total_time.append(float(exec_time))

            status.append(f1.read() == '\n'.join(parse))

            print(f'Subtask {x+1}:', exec_time, '\033[92mAC\033[0m' if status[-1] else '\033[91mWA\033[0m')   
        
    os.remove('out.py')
    os.remove('out.txt')

    print('-' * 40)
    print('Status:', ('\033[92mAC\033[0m' if all(status) else '\033[91mWA\033[0m'))
    print(f'Total Time: {str(round(sum(total_time), 3))}s')



    return all(status), round(sum(total_time), 3)


from flask import Flask, jsonify, request, abort

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify(message="Hi!")

@app.route('/judge', methods=['POST'])
def judge_route():
    #store data later
    #with open('bruh.py', 'w+') as f:
        #f.write(request.data.decode())
    year = request.args.get('year')
    problem = request.args.get('problem')

    if not year or not problem:
        abort(404)
        
    result, time = judge(year, problem, request.data.decode())

    if result:
        return jsonify(status='AC', time=time)
    else:
        return jsonify(status='WA', time=time)
    
app.run(debug=False, threaded=True)
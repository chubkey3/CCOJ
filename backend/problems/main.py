import requests, os
import zipfile
def get_data():
    extension = ''
    url_extension = ''

    n = 4
    year = 2001
    file = 's5'
    file_type = 'out'
    problem_name = "post"

    if (file_type == 'in'):    
        extension = 'in'
        url_extension = 'in'
        #problem_name = problem_name.upper()
    else:
        extension = 'out'
        url_extension = 'out'

    for x in range(1, n+1):
        file_location = os.path.join(os.path.dirname(__file__), "data", str(year), f"{file}.{x}.{extension}")
        s = f"{problem_name}{x}.{url_extension}"
        endpoint = f"http://mmhs.ca/ccc/{year}/{s}"
        req = requests.get(endpoint)

        if (req.status_code == 404):
            print('Failed!')
            break
        else:
            with open(file_location, 'w+') as f:
                f.write(req.text.replace('\r', ''))


def make_folders():
    for x in range(1996, 2024):
        if (x not in [2001, 2002, 2003]):
            os.makedirs(os.path.join(os.path.dirname(__file__), str(x)))

def move_files():
    for file in os.listdir(os.path.join(os.path.dirname(__file__), 'data')):
        if file.endswith('.zip'):
            os.rename(os.path.join(os.path.dirname(__file__), 'data', file), os.path.join(os.path.dirname(__file__), 'data', file.split('.')[0], file))

def unzip_files():
    for x in range(1996, 2024):
        if (x not in [2001, 2002, 2003]):
            zip = zipfile.ZipFile(os.path.join(os.path.dirname(__file__), "data", str(x), f"{x}.zip"))            
            zip.extractall(os.path.join(os.path.dirname(__file__), "data", str(x)))            
a = set()
def remove_folders():
    for x in range(1996, 2024):
        for b, d, f in os.walk(os.path.join(os.path.dirname(__file__), "data", str(x))):
            if d != []:
                a.add(x)
    
    for x in a:
        for dir in os.listdir(os.path.join(os.path.dirname(__file__), "data", str(x))):
            if dir.count('.') == 0:
                for file in os.listdir(os.path.join(os.path.dirname(__file__), "data", str(x), dir)):
                    if file.endswith('.in') or file.endswith('.out'):
                        os.rename(os.path.join(os.path.dirname(__file__), "data", str(x), dir, file), os.path.join(os.path.dirname(__file__), "data", str(x), file))


def rename_stuff():
    d = r"C:\Users\jason\test\Projects\CCOJ\test\data\2000"
    names = {
        "BROOKS": "j4s2",
        "GOLF": "s4",
        "SHEEP": "s5",
        "SURF": "j5s3",
        "letter": "p5"
    }
    for file in os.listdir(d):
        newfile = names[file.split('.')[0]]
        os.rename(os.path.join(d, file), os.path.join(d, f"{newfile}.{file.split('.')[1].lower()[-1]}.{file.split('.')[1].lower()[:-1]}"))

def remove_ext():
    d = r"C:\Users\jason\test\Projects\CCOJ\test\data\2007"

    for file in os.listdir(d):
        if file.endswith('.exp'):
            os.rename(os.path.join(d, file), os.path.join(d, f"{file[:-4]}.out"))

make_folders()
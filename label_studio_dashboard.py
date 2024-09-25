from label_studio_sdk.client import LabelStudio
from flask import Flask,render_template
import time
import multiprocessing
import json

config_file = open("secret.json")
json_data = json.dumps(config_file.read())
project_id = json_data["project_id"]
api_key = json_data["api_key"]
ls = LabelStudio(
    api_key=api_key,
)
total_task = 0
annotated = 0
overlapped = 0
total_instance = 0

bckground = 0
oneinstance = 0
morethanone = 0

recv_conn, send_conn = multiprocessing.Pipe(duplex=False)

app = Flask(__name__)
def fetching(send_conn:multiprocessing.connection.Connection):
    while True:
        total_task = 0
        annotated = 0
        overlapped = 0
        total_instance = 0

        bckground = 0
        oneinstance = 0
        morethanone = 0
        for task in ls.tasks.list(project=project_id, fields='all'):
            total_task += 1
            min_annotation = 99999999999
            if task.annotations:
                annotated += 1
                if isinstance(task.annotations_ids,list): #overlap
                    overlapped += 1
                for annotation in task.annotations:
                    min_annotation = min(min_annotation,len(annotation["result"]))
                    if min_annotation == 0:
                        bckground += 1
                    elif min_annotation == 1:
                        oneinstance += 1
                    else:
                        morethanone += 1
                total_instance += min_annotation
        send_conn.send([total_task,annotated,overlapped,total_instance,bckground,oneinstance,morethanone])
        time.sleep(60)
@app.route("/")
def dashboard():
    global total_task,annotated,overlapped,total_instance,recv_conn,bckground,oneinstance,morethanone
    if recv_conn.poll() == False:
        if total_task == 0:
            data = recv_conn.recv()
            total_task = data[0]
            annotated = data[1]
            overlapped = data[2]
            total_instance = data[3]
            bckground = data[4]
            oneinstance = data[5]
            morethanone = data[6]
        else:
            pass
    else:
        while recv_conn.poll():
            data = recv_conn.recv()
            total_task = data[0]
            annotated = data[1]
            overlapped = data[2]
            total_instance = data[3]
            bckground = data[4]
            oneinstance = data[5]
            morethanone = data[6]
    return render_template("dashboard.html.jinja",totaltask=total_task,annotated=annotated,pctage="{:.0f}%".format(annotated/total_task*100),
                           overlapped=overlapped,totalinstance=total_instance,bckground=bckground,oneinstance=oneinstance,morethanone=morethanone)
if __name__ == "__main__":
    p1 = multiprocessing.Process(target=fetching,args=[send_conn])
    try:
        p1.start()
        app.run(host="0.0.0.0",port="8081")
    except Exception as e:
        p1.kill()
        raise e
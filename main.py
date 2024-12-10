from fastapi import FastAPI, HTTPException

app = FastAPI()

to_do_list = [{'id': 1, 'task': 'Розібратися в FastApi'},
              {'id': 2, 'task': 'Зробити дз'},
              {'id': 3, 'task': 'Відправити дз'}
              ]

@app.get('/')
def tasks():
    return to_do_list

@app.get('/{id}')
def task_viev(id: int):
    for task in to_do_list:
        if task['id'] == id:
            return task
    raise HTTPException(status_code=404, detail='Не знайдено завдання за айді!')

@app.put('/update/{id}')
def update_task(id: int, new_task: str):
    for task in to_do_list:
        if task['id'] == id:
            task['task'] = new_task
            return {"message": "Завдання оновлено!"}
    raise HTTPException(status_code=404, detail='Не знайдено завдання для оновлення!')

@app.post('/add/{id}')
def add_task(id: int, task: str):
    for t in to_do_list:
        if t['id'] == id:
            raise HTTPException(status_code=400, detail='Завдання з таким айді вже існує!')
    new_task = {'id': id, 'task': task}
    to_do_list.append(new_task)
    return {"message": "Завдання додано!"}

@app.delete('/delete/{id}')
def delete_task(id: int):
    for task in to_do_list:
        if task['id'] == id:
            to_do_list.remove(task)
            return {"message": "Завдання видалено!"}
    raise HTTPException(status_code=404, detail='Завдання з таким айді не існує!')

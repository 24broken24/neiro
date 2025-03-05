import graphviz

dot = graphviz.Digraph('simulate_algorithm', format='png', graph_attr={'rankdir': 'TB'})

dot.node('start', 'Начало алгоритма', shape='ellipse', style='filled', fillcolor='lightgreen')
dot.node('init', 'Инициализация параметров', shape='box')
dot.node('arrival_gen', 'Генерация времени поступления задач', shape='box')
dot.node('execution_gen', 'Генерация времени выполнения задач', shape='box')
dot.node('queue_add', 'Добавление задач в очередь событий', shape='box')
dot.node('has_tasks', 'Есть активные задачи?', shape='diamond')
dot.node('event_extract', 'Извлечение события из очереди', shape='box')
dot.node('event_type', 'Событие: приход или завершение?', shape='diamond')
dot.node('task_queue', 'Добавление в очередь задач', shape='box')
dot.node('task_finish', 'Завершение выполнения или возврат в очередь', shape='box')
dot.node('end', 'Конец алгоритма', shape='ellipse', style='filled', fillcolor='lightcoral')

dot.edge('start', 'init')
dot.edge('init', 'arrival_gen')
dot.edge('arrival_gen', 'execution_gen')
dot.edge('execution_gen', 'queue_add')
dot.edge('queue_add', 'has_tasks')
dot.edge('has_tasks', 'end', label='Нет')
dot.edge('has_tasks', 'event_extract', label='Да')
dot.edge('event_extract', 'event_type')
dot.edge('event_type', 'task_queue', label='Приход')
dot.edge('event_type', 'task_finish', label='Завершение')
dot.edge('task_queue', 'has_tasks')
dot.edge('task_finish', 'has_tasks')

dot.render('simulate_algorithm')


const projectListTemplate = document.getElementById('projectList');
const projectListContainer = document.querySelector('.projectsList__wrapper')
const projectTemplate = document.getElementById('project');
const projectContainer = document.querySelector('.project__wrapper')
const taskTemplate = document.getElementById('task');

const getProjectsListData = async () => {
    let response = await fetch('http://127.0.0.1:8000/api/v1/task/');

    if (response.ok) {

    const projects = await response.json();
    console.log(projects)
    projects.map((project) => {
        let clone = projectListTemplate.content.cloneNode(true);
        let itemTag = clone.querySelector('.projectsListItem')
        itemTag.id = project.id;
        let editLink = clone.querySelector('.edit-icon');
        editLink.href = `/update_task/?id=${project.id}`;
        let deleteLink = clone.querySelector('.delete-icon');
        deleteLink.addEventListener('click', () => {
            fetch(`http://127.0.0.1:8000/delete_task/?id=${project.id}`)

            location.reload();
        })
        deleteLink.href = `/delete_task/?id=${project.id}`
        let titleTag = clone.querySelector('span');
        titleTag.textContent = project.title;
        projectListContainer.appendChild(clone)
    })

    } else {
    alert("Ошибка HTTP: " + response.status);
    }
};

getProjectsListData();

const getProjectData = async (id) => {
    let response = await fetch(`http://127.0.0.1:8000/api/v1/task/${id}`);

    if (response.ok) {

    const project = await response.json();
        const projectId = project.id;

        let clone = projectTemplate.content.cloneNode(true);
        let titleTag = clone.querySelector('.project__title');
        titleTag.textContent = project.title;
        let descriptionTag = clone.getElementById('projectDescription');
        descriptionTag.textContent = `Описание задачи: ${project.task_description}`;
        let deadlineTag = clone.getElementById('projectDeadline');
        deadlineTag.textContent = `Срок задачи: ${project.deadline}`;
        let managerTag = clone.getElementById('projectManager');
        managerTag.textContent = `Имя менеджера: ${project.manager}`;
        let addIcon = clone.querySelector('.plus-icon');
        addIcon.href = `/add_todo/?id=${project.id}`
        projectContainer.appendChild(clone)

        let taskResponse = await fetch('http://127.0.0.1:8000/api/v1/todo/');

        if (taskResponse.ok) {
    
        const todo = await taskResponse.json();
            const taskTodo = todo.filter((todoItem) => {
                return todoItem.task === projectId;
            })
            taskTodo.map((todoItem) => {
                let clone2 = taskTemplate.content.cloneNode(true);
                let titleTodoTag = clone2.querySelector('.task__item');
                titleTodoTag.textContent = todoItem.title;
                titleTodoTag.htmlFor = `task-${todoItem.id}`;
                titleTodoInput = clone2.querySelector('.task__input');
                titleTodoInput.id = `task-${todoItem.id}`;
                let editIcon = clone2.querySelector('.edit-icon');
                editIcon.href = `/update_todo/?id=${todoItem.id}`;
                let deleteIconTodo = clone2.querySelector('.delete-icon')
                deleteIconTodo.addEventListener('click', () => {
                    fetch(`http://127.0.0.1:8000/delete_todo/?id=${todoItem.id}`)
                    location.reload();
                })
                let mailIcon = clone2.querySelector('.mail-icon')
                mailIcon.href = `/send_mail/?id=${todoItem.id}`;
                const tasksContainer = document.querySelector('.project__tasks')
                tasksContainer.appendChild(clone2)
            })
    
        }


    }
};


const clickProjectHandler = () => {
    let projectListElements = document.querySelectorAll('.projectsListItem');
    [...projectListElements].forEach((item) => {
        item.addEventListener('click', () => {
            const projectWrapper = document.querySelector('.project__container');

            if (projectWrapper) {
                projectWrapper.remove()
            }

            const id = item.id;
            getProjectData(id);
        })
    })

}

setTimeout(clickProjectHandler, '500')



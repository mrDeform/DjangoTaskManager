const projectListTemplate = document.getElementById('projectList');
const projectListContainer = document.querySelector('.projectsList__wrapper')
const projectTemplate = document.getElementById('project');
const projectContainer = document.querySelector('.project__wrapper')

const getProjectsListData = async () => {
    let response = await fetch('http://127.0.0.1:8000/api/v1/task/');

    if (response.ok) {

    const projects = await response.json();

    projects.map((project) => {
        let clone = projectListTemplate.content.cloneNode(true);
        let itemTag = clone.querySelector('.projectsListItem')
        itemTag.id = project.id;
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

        let clone = projectTemplate.content.cloneNode(true);
        let titleTag = clone.querySelector('.project__title');
        titleTag.textContent = project.title;
        let descriptionTag = clone.getElementById('projectDescription');
        descriptionTag.textContent = `Описание задачи: ${project.task_description}`;
        let deadlineTag = clone.getElementById('projectDeadline');
        deadlineTag.textContent = `Срок задачи: ${project.deadline}`;
        let managerTag = clone.getElementById('projectManager');
        managerTag.textContent = `Имя менеджера: ${project.manager}`;
        projectContainer.appendChild(clone)


    } else {
    alert("Ошибка HTTP: " + response.status);
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



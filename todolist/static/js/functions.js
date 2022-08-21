const getProjects = async () => {
    let response = await fetch('http://127.0.0.1:8000/api/v1/task/');

    if (response.ok) { 
    return await response.json();
    } else {
    alert("Ошибка HTTP: " + response.status);
    }
}

getProjects()
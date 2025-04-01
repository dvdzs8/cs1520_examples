
async function fetchTodos() {
    const response = await fetch("/todos"); //sends a GET to /todos flask route
    const todos = await response.json(); //await her bc .json() returns promise

    const list = document.getElementById("to-do-list"); //get the <ul> from html
    list.innerHTML = ""; //clear current list to avoid dupes

    for (const [id, todo] of Object.entries(todos)) {

        //create a pending li to later add to the ul
        const li = document.createElement("li");
        li.textContent = todo.task;

        //create delete btn to add to the above li
        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "Delete";
        deleteBtn.onclick = async () => {
            // `/todos/${id}` is template literal. equal to "/todos/" + id
            //second arg are configurations like headers and body and ofc method
            await fetch(`/todos/${id}`, {method: "DELETE"});
            fetchTodos(); //fetches todos when clicked. not now
        };

        li.appendChild(deleteBtn);
        list.appendChild(li);
    }
}

document.getElementById("to-do-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const task = document.getElementById("task").value;

    await fetch("/todos", {

        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task }),

    });

    document.getElementById("task").value = "";

    fetchTodos();
});

setInterval(fetchTodos, 10000);
fetchTodos();
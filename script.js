// Replace this with your actual API Gateway Invoke URL
const API_URL = '<API-GATEWAY-URL>/tasks';

// Fetch all tasks on page load
document.addEventListener('DOMContentLoaded', fetchTasks);

async function fetchTasks() {
  try {
    const response = await fetch(API_URL);
    const tasks = await response.json();
    const taskList = document.getElementById('task-list');
    taskList.innerHTML = '';

    tasks.forEach((task) => {
      const li = document.createElement('li');
      li.className = 'task-item';
      li.innerHTML = `
                <span class="task-text ${task.completed ? 'completed' : ''}">${task.title}</span>
                <div class="actions">
                    <button class="btn-toggle" onclick="toggleTask('${task.taskId}', ${task.completed})">
                        ${task.completed ? 'Undo' : 'Complete'}
                    </button>
                    <button class="btn-delete" onclick="deleteTask('${task.taskId}')">Delete</button>
                </div>
            `;
      taskList.appendChild(li);
    });
  } catch (error) {
    console.error('Error fetching tasks:', error);
  }
}

async function createTask() {
  const input = document.getElementById('task-input');
  const title = input.value.trim();
  if (!title) return;

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: title }),
    });
    if (response.ok) {
      input.value = '';
      fetchTasks();
    }
  } catch (error) {
    console.error('Error creating task:', error);
  }
}

async function toggleTask(id, currentStatus) {
  try {
    const response = await fetch(`${API_URL}?taskId=${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ completed: !currentStatus }),
    });
    if (response.ok) {
      fetchTasks();
    }
  } catch (error) {
    console.error('Error updating task:', error);
  }
}

async function deleteTask(id) {
  try {
    const response = await fetch(`${API_URL}?taskId=${id}`, {
      method: 'DELETE',
    });
    if (response.ok) {
      fetchTasks();
    }
  } catch (error) {
    console.error('Error deleting task:', error);
  }
}

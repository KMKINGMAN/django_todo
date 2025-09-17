import React, { useState, useEffect } from 'react';
import { Typography, Box, CssBaseline, AppBar, Toolbar, CircularProgress, Dialog, DialogTitle, DialogContent, DialogActions, Button } from '@mui/material';
import Sidebar from '../components/Sidebar';
import TaskForm from '../components/TaskForm';
import TaskList from '../components/TaskList';
import TodoForm from '../components/TodoForm';
import TodoList from '../components/TodoList';
import TaskDetailView from '../components/TaskDetailView';
import { getTasks, getTodos, addTask, addTodo } from '../services/api';

const DashboardPage = () => {
  const [tasks, setTasks] = useState([]);
  const [todos, setTodos] = useState([]);
  const [view, setView] = useState('tasks'); // 'tasks' or 'todos'
  const [loading, setLoading] = useState(true);
  const [selectedTask, setSelectedTask] = useState(null);
  const [showQuickTodoDialog, setShowQuickTodoDialog] = useState(false);
  const [quickTodoTask, setQuickTodoTask] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [tasksResponse, todosResponse] = await Promise.all([
        getTasks(),
        getTodos()
      ]);
      setTasks(tasksResponse.data);
      setTodos(todosResponse.data);
    } catch (error) {
      console.error('Error fetching data:', error);
      // Handle error - maybe redirect to login if token is invalid
    } finally {
      setLoading(false);
    }
  };

  const handleAddTask = async (task) => {
    try {
      const response = await addTask(task);
      setTasks([response.data, ...tasks]);
    } catch (error) {
      console.error('Error adding task:', error);
    }
  };

  const handleAddTodo = async (todo) => {
    try {
      const response = await addTodo(todo);
      setTodos([response.data, ...todos]);
      
      // If the todo belongs to a task, update the tasks list
      if (todo.task) {
        await fetchData(); // Refresh data to get updated task with todo count
      }
    } catch (error) {
      console.error('Error adding todo:', error);
    }
  };

  const handleTaskClick = async (task) => {
    // Set the selected task and fetch its todos separately
    try {
      setSelectedTask(task);
      setView('task-detail');
      
      // Fetch todos for this specific task
      const todosResponse = await getTodos();
      const taskTodos = todosResponse.data.filter(todo => todo.task === task.id);
      
      // Update the selected task with its todos
      setSelectedTask({
        ...task,
        todos: taskTodos
      });
    } catch (error) {
      console.error('Error fetching task details:', error);
    }
  };

  const handleBackToTasks = () => {
    setSelectedTask(null);
    setView('tasks');
  };

  const handleQuickAddTodo = (task) => {
    setQuickTodoTask(task);
    setShowQuickTodoDialog(true);
  };

  const handleQuickTodoAdded = async (todo) => {
    await handleAddTodo(todo);
    setShowQuickTodoDialog(false);
    setQuickTodoTask(null);
  };

  const handleTodoAddedToTask = async (todo) => {
    // Refresh data to update both todos and task
    await fetchData();
    
    // Update the selected task with the new todo
    if (selectedTask) {
      const todosResponse = await getTodos();
      const taskTodos = todosResponse.data.filter(t => t.task === selectedTask.id);
      
      setSelectedTask({
        ...selectedTask,
        todos: taskTodos
      });
    }
  };

  const handleTodoUpdated = (updatedTodo) => {
    // Update the todos list
    setTodos(todos.map(todo => 
      todo.id === updatedTodo.id ? updatedTodo : todo
    ));
    
    // Update the selected task's todos if viewing task detail
    if (selectedTask) {
      const updatedTaskTodos = selectedTask.todos.map(todo =>
        todo.id === updatedTodo.id ? updatedTodo : todo
      );
      setSelectedTask({
        ...selectedTask,
        todos: updatedTaskTodos
      });
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ display: 'flex' }}>
      <CssBaseline />
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <Typography variant="h6" noWrap component="div">
            Task Management
          </Typography>
        </Toolbar>
      </AppBar>
      <Sidebar setView={setView} />
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        
        {view === 'task-detail' && selectedTask ? (
          <TaskDetailView 
            task={selectedTask}
            onBack={handleBackToTasks}
            onTodoAdded={handleTodoAddedToTask}
          />
        ) : view === 'tasks' ? (
          <>
            <Typography variant="h4">Tasks</Typography>
            <TaskForm onAddTask={handleAddTask} />
            <TaskList 
              tasks={tasks} 
              onTaskClick={handleTaskClick}
              onQuickAddTodo={handleQuickAddTodo}
            />
          </>
        ) : (
          <>
            <Typography variant="h4">Todos</Typography>
            <TodoForm onAddTodo={handleAddTodo} tasks={tasks} />
            <TodoList todos={todos} onTodoUpdated={handleTodoUpdated} />
          </>
        )}
      </Box>

      {/* Quick Add Todo Dialog */}
      <Dialog 
        open={showQuickTodoDialog} 
        onClose={() => setShowQuickTodoDialog(false)}
        maxWidth="sm" 
        fullWidth
      >
        <DialogTitle>Quick Add Todo</DialogTitle>
        <DialogContent>
          {quickTodoTask && (
            <TodoForm 
              onAddTodo={handleQuickTodoAdded}
              tasks={tasks}
              selectedTask={quickTodoTask}
            />
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowQuickTodoDialog(false)}>Cancel</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default DashboardPage;

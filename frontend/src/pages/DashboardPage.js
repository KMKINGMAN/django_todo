import React, { useState, useEffect, useCallback } from 'react';
import { Typography, Box, CssBaseline, AppBar, Toolbar, CircularProgress, Dialog, DialogTitle, DialogContent, DialogActions, Button, IconButton } from '@mui/material';
import { Logout } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import TaskForm from '../components/TaskForm';
import TaskList from '../components/TaskList';
import TodoForm from '../components/TodoForm';
import TodoList from '../components/TodoList';
import TaskDetailView from '../components/TaskDetailView';
import { getTasks, getTodos, getTask, addTask, addTodo, removeTask, removeTodo, logout } from '../services/api';

const DashboardPage = () => {
  const navigate = useNavigate();
  const [tasks, setTasks] = useState([]);
  const [todos, setTodos] = useState([]);
  const [view, setView] = useState('tasks'); // 'tasks' or 'todos'
  const [loading, setLoading] = useState(true);
  const [selectedTask, setSelectedTask] = useState(null);
  const [showQuickTodoDialog, setShowQuickTodoDialog] = useState(false);
  const [quickTodoTask, setQuickTodoTask] = useState(null);
  const [username, setUsername] = useState('');

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const fetchData = useCallback(async () => {
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
  }, []);

  useEffect(() => {
    // Get username from localStorage
    const storedUsername = localStorage.getItem('username');
    if (storedUsername) {
      setUsername(storedUsername);
    }
    
    // Fetch data on component mount
    fetchData();
  }, [fetchData]);

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
  // Fetch the task with nested todos from the API
  const taskResponse = await getTask(task.id, true);
  setSelectedTask(taskResponse.data);
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
      // Re-fetch the selected task including its todos
      try {
        const taskResponse = await getTask(selectedTask.id, true);
        setSelectedTask(taskResponse.data);
      } catch (err) {
        console.error('Error refreshing selected task:', err);
      }
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

  const handleDeleteTask = async (taskId) => {
    try {
      await removeTask(taskId);
      
      // Remove the task from the state
      setTasks(tasks.filter(task => task.id !== taskId));
      
      // If we're viewing this task, go back to tasks view
      if (selectedTask && selectedTask.id === taskId) {
        setSelectedTask(null);
        setView('tasks');
      }
      
      // Refresh todos to remove any todos that belonged to this task
      const todosResponse = await getTodos();
      setTodos(todosResponse.data);
      
    } catch (error) {
      console.error('Error deleting task:', error);
      throw error; // Re-throw to handle in component
    }
  };

  const handleDeleteTodo = async (todoId) => {
    try {
      await removeTodo(todoId);
      
      // Remove the todo from the state
      setTodos(todos.filter(todo => todo.id !== todoId));
      
      // Update the selected task's todos if viewing task detail
      if (selectedTask) {
        const updatedTaskTodos = selectedTask.todos.filter(todo => todo.id !== todoId);
        setSelectedTask({
          ...selectedTask,
          todos: updatedTaskTodos
        });
      }
      
      // Refresh tasks to update todo counts
      const tasksResponse = await getTasks();
      setTasks(tasksResponse.data);
      
    } catch (error) {
      console.error('Error deleting todo:', error);
      throw error; // Re-throw to handle in component
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
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            Task Management
          </Typography>
          {username && (
            <Typography variant="body1" sx={{ mr: 2 }}>
              Welcome, {username}
            </Typography>
          )}
          <IconButton
            color="inherit"
            onClick={handleLogout}
            title="Logout"
            sx={{ 
              '&:hover': { 
                backgroundColor: 'rgba(255, 255, 255, 0.1)' 
              } 
            }}
          >
            <Logout />
          </IconButton>
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
            onTaskDeleted={handleDeleteTask}
            onTodoDeleted={handleDeleteTodo}
          />
        ) : view === 'tasks' ? (
          <>
            <Typography variant="h4">Tasks</Typography>
            <TaskForm onAddTask={handleAddTask} />
            <TaskList 
              tasks={tasks} 
              onTaskClick={handleTaskClick}
              onQuickAddTodo={handleQuickAddTodo}
              onDeleteTask={handleDeleteTask}
            />
          </>
        ) : (
          <>
            <Typography variant="h4">Todos</Typography>
            <TodoForm onAddTodo={handleAddTodo} tasks={tasks} />
            <TodoList todos={todos} onTodoUpdated={handleTodoUpdated} onDeleteTodo={handleDeleteTodo} />
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

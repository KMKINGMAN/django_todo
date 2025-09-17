import React from 'react';
import { List, ListItem, ListItemText, Paper, Typography, Box, Checkbox, Chip } from '@mui/material';
import { updateTodo } from '../services/api';

const TodoList = ({ todos, onTodoUpdated }) => {
  const handleToggleComplete = async (todo) => {
    try {
      const updatedTodo = { ...todo, completed: !todo.completed };
      await updateTodo(todo.id, { completed: !todo.completed });
      
      // Call the callback to update the parent component's state
      if (onTodoUpdated) {
        onTodoUpdated(updatedTodo);
      }
    } catch (error) {
      console.error('Error updating todo:', error);
    }
  };
  if (todos.length === 0) {
    return (
      <Paper sx={{ p: 2 }}>
        <Typography variant="body1" color="text.secondary">
          No todos yet. Create your first todo above!
        </Typography>
      </Paper>
    );
  }

  return (
    <Paper>
      <List>
        {todos.map((todo) => (
          <ListItem key={todo.id} divider>
            <Checkbox 
              checked={todo.completed} 
              onChange={() => handleToggleComplete(todo)}
              color="primary"
            />
            <ListItemText 
              primary={
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography 
                    variant="h6" 
                    sx={{ 
                      textDecoration: todo.completed ? 'line-through' : 'none',
                      color: todo.completed ? 'text.secondary' : 'text.primary'
                    }}
                  >
                    {todo.title}
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 0.5, alignItems: 'center' }}>
                    {todo.task_title && (
                      <Chip 
                        label={`Task: ${todo.task_title}`} 
                        size="small" 
                        color="primary"
                        variant="outlined"
                      />
                    )}
                    {todo.tags && todo.tags.length > 0 && (
                      <>
                        {todo.tags.map((tag, index) => (
                          <Chip key={index} label={tag} size="small" variant="outlined" />
                        ))}
                      </>
                    )}
                  </Box>
                </Box>
              }
              secondary={
                <Box>
                  {todo.description && (
                    <Typography variant="body2" sx={{ mb: 1 }}>
                      {todo.description}
                    </Typography>
                  )}
                  <Typography variant="caption" color="text.secondary">
                    Created: {new Date(todo.created_at).toLocaleDateString()}
                    {todo.due_date && (
                      <> • Due: {new Date(todo.due_date).toLocaleDateString()}</>
                    )}
                    {!todo.task_title && (
                      <> • <em>Standalone Todo</em></>
                    )}
                  </Typography>
                </Box>
              }
            />
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};

export default TodoList;

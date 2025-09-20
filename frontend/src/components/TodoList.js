import React, { useState } from 'react';
import { List, ListItem, ListItemText, Paper, Typography, Box, Checkbox, Chip, Button, Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions, Alert, IconButton } from '@mui/material';
import { Delete } from '@mui/icons-material';
import { updateTodo } from '../services/api';

const TodoList = ({ todos, onTodoUpdated, onDeleteTodo }) => {
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [todoToDelete, setTodoToDelete] = useState(null);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState('');

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

  const handleDeleteClick = (todo, event) => {
    event.stopPropagation();
    setTodoToDelete(todo);
    setDeleteDialogOpen(true);
    setError('');
  };

  const handleDeleteConfirm = async () => {
    if (!todoToDelete) return;
    
    setDeleting(true);
    setError('');
    
    try {
      await onDeleteTodo(todoToDelete.id);
      setDeleteDialogOpen(false);
      setTodoToDelete(null);
    } catch (error) {
      console.error('Error deleting todo:', error);
      setError('Failed to delete todo. Please try again.');
    } finally {
      setDeleting(false);
    }
  };

  const handleDeleteCancel = () => {
    setDeleteDialogOpen(false);
    setTodoToDelete(null);
    setError('');
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
                    <IconButton
                      size="small"
                      color="error"
                      onClick={(e) => handleDeleteClick(todo, e)}
                      sx={{ ml: 1 }}
                    >
                      <Delete fontSize="small" />
                    </IconButton>
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

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteDialogOpen}
        onClose={handleDeleteCancel}
        aria-labelledby="delete-todo-dialog-title"
        aria-describedby="delete-todo-dialog-description"
      >
        <DialogTitle id="delete-todo-dialog-title">
          Delete Todo
        </DialogTitle>
        <DialogContent>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          <DialogContentText id="delete-todo-dialog-description">
            Are you sure you want to delete "{todoToDelete?.title}"?
            {todoToDelete?.task_title && (
              <Box sx={{ mt: 1, color: 'info.main' }}>
                This todo belongs to task: <strong>{todoToDelete.task_title}</strong>
              </Box>
            )}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDeleteCancel} disabled={deleting}>
            Cancel
          </Button>
          <Button 
            onClick={handleDeleteConfirm} 
            color="error" 
            variant="contained"
            disabled={deleting}
          >
            {deleting ? 'Deleting...' : 'Delete'}
          </Button>
        </DialogActions>
      </Dialog>
    </Paper>
  );
};

export default TodoList;

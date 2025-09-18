import React, { useState } from 'react';
import { List, ListItem, ListItemText, Paper, Typography, Box, Chip, Button, Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions, Alert } from '@mui/material';
import { Visibility, Add, Delete } from '@mui/icons-material';

const TaskList = ({ tasks, onTaskClick, onQuickAddTodo, onDeleteTask }) => {
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [taskToDelete, setTaskToDelete] = useState(null);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState('');

  const handleDeleteClick = (task, event) => {
    event.stopPropagation();
    setTaskToDelete(task);
    setDeleteDialogOpen(true);
    setError('');
  };

  const handleDeleteConfirm = async () => {
    if (!taskToDelete) return;
    
    setDeleting(true);
    setError('');
    
    try {
      await onDeleteTask(taskToDelete.id);
      setDeleteDialogOpen(false);
      setTaskToDelete(null);
    } catch (error) {
      console.error('Error deleting task:', error);
      setError('Failed to delete task. Please try again.');
    } finally {
      setDeleting(false);
    }
  };

  const handleDeleteCancel = () => {
    setDeleteDialogOpen(false);
    setTaskToDelete(null);
    setError('');
  };
  if (tasks.length === 0) {
    return (
      <Paper sx={{ p: 2 }}>
        <Typography variant="body1" color="text.secondary">
          No tasks yet. Create your first task above!
        </Typography>
      </Paper>
    );
  }

  return (
    <Paper>
      <List>
        {tasks.map((task) => (
          <ListItem key={task.id} divider>
            <ListItemText 
              primary={
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="h6">{task.title}</Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Chip 
                      label={`${task.todos_count || 0} todos`} 
                      size="small" 
                      color={task.todos_count > 0 ? 'primary' : 'default'}
                    />
                    <Button
                      size="small"
                      startIcon={<Add />}
                      onClick={(e) => {
                        e.stopPropagation();
                        onQuickAddTodo(task);
                      }}
                    >
                      Add Todo
                    </Button>
                    <Button
                      size="small"
                      startIcon={<Visibility />}
                      onClick={() => onTaskClick(task)}
                    >
                      View
                    </Button>
                    <Button
                      size="small"
                      color="error"
                      startIcon={<Delete />}
                      onClick={(e) => handleDeleteClick(task, e)}
                    >
                      Delete
                    </Button>
                  </Box>
                </Box>
              }
              secondary={
                <Box>
                  {task.description && (
                    <Typography variant="body2" sx={{ mb: 1 }}>
                      {task.description}
                    </Typography>
                  )}
                  <Typography variant="caption" color="text.secondary">
                    Created: {new Date(task.created_at).toLocaleDateString()}
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
        aria-labelledby="delete-dialog-title"
        aria-describedby="delete-dialog-description"
      >
        <DialogTitle id="delete-dialog-title">
          Delete Task
        </DialogTitle>
        <DialogContent>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}
          <DialogContentText id="delete-dialog-description">
            Are you sure you want to delete "{taskToDelete?.title}"?
            {taskToDelete?.todos_count > 0 && (
              <Box sx={{ mt: 1, color: 'warning.main' }}>
                <strong>Warning:</strong> This will also delete {taskToDelete.todos_count} todo(s) associated with this task.
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

export default TaskList;

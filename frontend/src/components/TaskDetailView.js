import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Button, 
  Paper, 
  List, 
  ListItem, 
  ListItemText, 
  Checkbox,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Chip,
  Stack,
  Divider,
  Alert,
  DialogContentText
} from '@mui/material';
import { ArrowBack, Add, Delete } from '@mui/icons-material';
import { addTodo, updateTodo, removeTodo, removeTask } from '../services/api';

const TaskDetailView = ({ task, onBack, onTodoAdded, onTaskDeleted, onTodoDeleted }) => {
  const [showAddTodo, setShowAddTodo] = useState(false);
  const [newTodoTitle, setNewTodoTitle] = useState('');
  const [newTodoDescription, setNewTodoDescription] = useState('');
  const [newTodoTags, setNewTodoTags] = useState([]);
  const [tagInput, setTagInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [deleteType, setDeleteType] = useState(''); // 'task' or 'todo'
  const [itemToDelete, setItemToDelete] = useState(null);
  const [deleting, setDeleting] = useState(false);

  const handleAddTodo = async () => {
    if (!newTodoTitle.trim()) return;
    
    setLoading(true);
    setError('');
    
    try {
      const todoData = {
        title: newTodoTitle.trim(),
        description: newTodoDescription.trim(),
        task: task.id,
        tags: newTodoTags.length > 0 ? newTodoTags : ['general']
      };
      
      const response = await addTodo(todoData);
      onTodoAdded(response.data);
      
      // Reset form
      setNewTodoTitle('');
      setNewTodoDescription('');
      setNewTodoTags([]);
      setTagInput('');
      setShowAddTodo(false);
    } catch (error) {
      setError('Failed to add todo. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTag = () => {
    const trimmedTag = tagInput.trim().toLowerCase();
    if (trimmedTag && !newTodoTags.includes(trimmedTag)) {
      setNewTodoTags([...newTodoTags, trimmedTag]);
      setTagInput('');
    }
  };

  const handleRemoveTag = (tagToRemove) => {
    setNewTodoTags(newTodoTags.filter(tag => tag !== tagToRemove));
  };

  const handleTagKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddTag();
    }
  };

  const handleToggleComplete = async (todo) => {
    try {
      await updateTodo(todo.id, { completed: !todo.completed });
      // Trigger a refresh of the parent component
      if (onTodoAdded) {
        onTodoAdded(); // This will refresh the task's todos
      }
    } catch (error) {
      console.error('Error updating todo:', error);
    }
  };

  const handleDeleteTask = () => {
    setDeleteType('task');
    setItemToDelete(task);
    setDeleteDialogOpen(true);
  };

  const handleDeleteTodo = (todo) => {
    setDeleteType('todo');
    setItemToDelete(todo);
    setDeleteDialogOpen(true);
  };

  const handleDeleteConfirm = async () => {
    if (!itemToDelete) return;
    
    setDeleting(true);
    
    try {
      if (deleteType === 'task') {
        await removeTask(itemToDelete.id);
        if (onTaskDeleted) {
          onTaskDeleted(itemToDelete.id);
        }
        onBack(); // Go back to tasks view
      } else if (deleteType === 'todo') {
        await removeTodo(itemToDelete.id);
        if (onTodoDeleted) {
          onTodoDeleted(itemToDelete.id);
        }
      }
      
      setDeleteDialogOpen(false);
      setItemToDelete(null);
      setDeleteType('');
      
    } catch (error) {
      console.error('Error deleting item:', error);
      // Could add error handling here
    } finally {
      setDeleting(false);
    }
  };

  const handleDeleteCancel = () => {
    setDeleteDialogOpen(false);
    setItemToDelete(null);
    setDeleteType('');
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <IconButton onClick={onBack} sx={{ mr: 2 }}>
          <ArrowBack />
        </IconButton>
        <Typography variant="h4" sx={{ flexGrow: 1 }}>
          {task.title}
        </Typography>
        <Button
          variant="outlined"
          color="error"
          startIcon={<Delete />}
          onClick={handleDeleteTask}
          sx={{ mr: 1 }}
        >
          Delete Task
        </Button>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => setShowAddTodo(true)}
        >
          Add Todo
        </Button>
      </Box>

      {task.description && (
        <Paper sx={{ p: 2, mb: 3 }}>
          <Typography variant="body1">{task.description}</Typography>
        </Paper>
      )}

      <Paper sx={{ p: 2 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Todos ({task.todos?.length || 0})
        </Typography>
        
        {task.todos && task.todos.length > 0 ? (
          <List>
            {task.todos.map((todo, index) => (
              <React.Fragment key={todo.id}>
                <ListItem>
                  <Checkbox 
                    checked={todo.completed} 
                    onChange={() => handleToggleComplete(todo)}
                    color="primary"
                  />
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Typography
                          sx={{
                            textDecoration: todo.completed ? 'line-through' : 'none',
                            color: todo.completed ? 'text.secondary' : 'text.primary'
                          }}
                        >
                          {todo.title}
                        </Typography>
                        <IconButton
                          size="small"
                          color="error"
                          onClick={() => handleDeleteTodo(todo)}
                        >
                          <Delete fontSize="small" />
                        </IconButton>
                      </Box>
                    }
                    secondary={
                      <Box>
                        {todo.description && (
                          <Typography variant="body2" sx={{ mb: 1 }}>
                            {todo.description}
                          </Typography>
                        )}
                        {todo.tags && todo.tags.length > 0 && (
                          <Stack direction="row" spacing={0.5} sx={{ mb: 1 }}>
                            {todo.tags.map((tag, tagIndex) => (
                              <Chip 
                                key={tagIndex} 
                                label={tag} 
                                size="small" 
                                variant="outlined" 
                              />
                            ))}
                          </Stack>
                        )}
                        <Typography variant="caption" color="text.secondary">
                          Created: {new Date(todo.created_at).toLocaleDateString()}
                          {todo.due_date && (
                            <> • Due: {new Date(todo.due_date).toLocaleDateString()}</>
                          )}
                        </Typography>
                      </Box>
                    }
                  />
                </ListItem>
                {index < task.todos.length - 1 && <Divider />}
              </React.Fragment>
            ))}
          </List>
        ) : (
          <Typography variant="body2" color="text.secondary">
            No todos yet. Add your first todo above!
          </Typography>
        )}
      </Paper>

      {/* Add Todo Dialog */}
      <Dialog open={showAddTodo} onClose={() => setShowAddTodo(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Add Todo to {task.title}</DialogTitle>
        <DialogContent>
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          
          <TextField
            autoFocus
            margin="dense"
            label="Todo Title"
            fullWidth
            variant="outlined"
            value={newTodoTitle}
            onChange={(e) => setNewTodoTitle(e.target.value)}
            sx={{ mb: 2 }}
          />
          
          <TextField
            margin="dense"
            label="Description (Optional)"
            fullWidth
            multiline
            rows={3}
            variant="outlined"
            value={newTodoDescription}
            onChange={(e) => setNewTodoDescription(e.target.value)}
            sx={{ mb: 2 }}
          />
          
          <Box sx={{ mb: 2 }}>
            <TextField
              label="Add Tags"
              value={tagInput}
              onChange={(e) => setTagInput(e.target.value)}
              onKeyPress={handleTagKeyPress}
              size="small"
              sx={{ mr: 1 }}
            />
            <Button 
              onClick={handleAddTag}
              disabled={!tagInput.trim()}
              variant="outlined"
              size="small"
            >
              Add Tag
            </Button>
          </Box>
          
          {newTodoTags.length > 0 && (
            <Stack direction="row" spacing={1} sx={{ flexWrap: 'wrap', mb: 2 }}>
              {newTodoTags.map((tag) => (
                <Chip 
                  key={tag} 
                  label={tag} 
                  onDelete={() => handleRemoveTag(tag)}
                  size="small"
                />
              ))}
            </Stack>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowAddTodo(false)}>Cancel</Button>
          <Button 
            onClick={handleAddTodo} 
            variant="contained"
            disabled={loading || !newTodoTitle.trim()}
          >
            {loading ? 'Adding...' : 'Add Todo'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog
        open={deleteDialogOpen}
        onClose={handleDeleteCancel}
        aria-labelledby="delete-dialog-title"
        aria-describedby="delete-dialog-description"
      >
        <DialogTitle id="delete-dialog-title">
          Delete {deleteType === 'task' ? 'Task' : 'Todo'}
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="delete-dialog-description">
            {deleteType === 'task' ? (
              <>
                Are you sure you want to delete the task "{itemToDelete?.title}"?
                {task.todos && task.todos.length > 0 && (
                  <Box sx={{ mt: 1, color: 'warning.main' }}>
                    <strong>Warning:</strong> This will also delete {task.todos.length} todo(s) associated with this task.
                  </Box>
                )}
              </>
            ) : (
              <>
                Are you sure you want to delete the todo "{itemToDelete?.title}"?
              </>
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
    </Box>
  );
};

export default TaskDetailView;
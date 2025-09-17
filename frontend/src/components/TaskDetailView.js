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
  Alert
} from '@mui/material';
import { ArrowBack, Add } from '@mui/icons-material';
import { addTodo, updateTodo } from '../services/api';

const TaskDetailView = ({ task, onBack, onTodoAdded }) => {
  const [showAddTodo, setShowAddTodo] = useState(false);
  const [newTodoTitle, setNewTodoTitle] = useState('');
  const [newTodoDescription, setNewTodoDescription] = useState('');
  const [newTodoTags, setNewTodoTags] = useState([]);
  const [tagInput, setTagInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

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
                      <Typography
                        sx={{
                          textDecoration: todo.completed ? 'line-through' : 'none',
                          color: todo.completed ? 'text.secondary' : 'text.primary'
                        }}
                      >
                        {todo.title}
                      </Typography>
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
    </Box>
  );
};

export default TaskDetailView;
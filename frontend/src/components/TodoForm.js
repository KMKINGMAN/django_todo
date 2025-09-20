import React, { useState } from 'react';
import { Box, Button, TextField, Typography, Alert, Chip, Stack, FormControl, InputLabel, Select, MenuItem } from '@mui/material';

const TodoForm = ({ onAddTodo, tasks, selectedTask = null }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [taskId, setTaskId] = useState(selectedTask ? selectedTask.id : '');
  const [tagInput, setTagInput] = useState('');
  const [tags, setTags] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    
    setLoading(true);
    setError('');
    setSuccess(false);
    
    try {
      const todoData = { 
        title: title.trim(), 
        description: description.trim(),
        tags: tags.length > 0 ? tags : ['general']
      };
      
      // Only add task if one is selected
      if (taskId) {
        todoData.task = parseInt(taskId);
      }
      
      await onAddTodo(todoData);
      setTitle('');
      setDescription('');
      if (!selectedTask) setTaskId(''); // Only reset task selection if not pre-selected
      setTags([]);
      setTagInput('');
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch (error) {
      setError('Failed to create todo. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleAddTag = () => {
    const trimmedTag = tagInput.trim().toLowerCase();
    if (trimmedTag && !tags.includes(trimmedTag)) {
      setTags([...tags, trimmedTag]);
      setTagInput('');
    }
  };

  const handleRemoveTag = (tagToRemove) => {
    setTags(tags.filter(tag => tag !== tagToRemove));
  };

  const handleTagKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddTag();
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mb: 3 }}>
      <Typography variant="h6" sx={{ mb: 2 }}>
        {selectedTask ? `Add Todo to ${selectedTask.title}` : 'Add New Todo'}
      </Typography>
      
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }}>Todo created successfully!</Alert>}
      
      <TextField
        label="Todo Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        fullWidth
        margin="normal"
        required
        disabled={loading}
      />
      
      <TextField
        label="Todo Description (Optional)"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        fullWidth
        margin="normal"
        multiline
        rows={4}
        disabled={loading}
      />
      
      {/* Task Selection - only show if not pre-selected */}
      {!selectedTask && tasks && tasks.length > 0 && (
        <FormControl fullWidth margin="normal">
          <InputLabel>Assign to Task (Optional)</InputLabel>
          <Select
            value={taskId}
            label="Assign to Task (Optional)"
            onChange={(e) => setTaskId(e.target.value)}
            disabled={loading}
          >
            <MenuItem value="">
              <em>No Task (Standalone Todo)</em>
            </MenuItem>
            {tasks.map((task) => (
              <MenuItem key={task.id} value={task.id}>
                {task.title}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      )}
      
      <Box sx={{ mt: 2 }}>
        <TextField
          label="Add Tags"
          value={tagInput}
          onChange={(e) => setTagInput(e.target.value)}
          onKeyPress={handleTagKeyPress}
          size="small"
          disabled={loading}
          sx={{ mr: 1 }}
        />
        <Button 
          onClick={handleAddTag}
          disabled={loading || !tagInput.trim()}
          variant="outlined"
          size="small"
        >
          Add Tag
        </Button>
      </Box>
      
      {tags.length > 0 && (
        <Stack direction="row" spacing={1} sx={{ mt: 1, flexWrap: 'wrap' }}>
          {tags.map((tag) => (
            <Chip 
              key={tag} 
              label={tag} 
              onDelete={() => handleRemoveTag(tag)}
              size="small"
              disabled={loading}
            />
          ))}
        </Stack>
      )}
      
      <Button 
        type="submit" 
        variant="contained" 
        disabled={loading || !title.trim()}
        sx={{ mt: 2 }}
      >
        {loading ? 'Creating...' : 'Add Todo'}
      </Button>
    </Box>
  );
};

export default TodoForm;

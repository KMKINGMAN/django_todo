import React, { useState } from 'react';
import { Box, Button, TextField, Typography, Alert } from '@mui/material';

const TaskForm = ({ onAddTask }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
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
      await onAddTask({ title: title.trim(), description: description.trim() });
      setTitle('');
      setDescription('');
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000);
    } catch (error) {
      setError('Failed to create task. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mb: 3 }}>
      <Typography variant="h6" sx={{ mb: 2 }}>Add New Task</Typography>
      
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {success && <Alert severity="success" sx={{ mb: 2 }}>Task created successfully!</Alert>}
      
      <TextField
        label="Task Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        fullWidth
        margin="normal"
        required
        disabled={loading}
      />
      <TextField
        label="Task Description (Optional)"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        fullWidth
        margin="normal"
        multiline
        rows={4}
        disabled={loading}
      />
      <Button 
        type="submit" 
        variant="contained" 
        disabled={loading || !title.trim()}
        sx={{ mt: 2 }}
      >
        {loading ? 'Creating...' : 'Add Task'}
      </Button>
    </Box>
  );
};

export default TaskForm;

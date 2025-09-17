import React from 'react';
import { List, ListItem, ListItemText, Paper, Typography, Box, Chip, Button } from '@mui/material';
import { Visibility, Add } from '@mui/icons-material';

const TaskList = ({ tasks, onTaskClick, onQuickAddTodo }) => {
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
    </Paper>
  );
};

export default TaskList;

import React from 'react';
import { Drawer, List, ListItem, ListItemIcon, ListItemText, Toolbar, Box } from '@mui/material';
import { Inbox, Mail } from '@mui/icons-material';

const drawerWidth = 240;

const Sidebar = ({ setView }) => {
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
      }}
    >
      <Toolbar />
      <Box sx={{ overflow: 'auto' }}>
        <List>
          <ListItem button onClick={() => setView('tasks')}>
            <ListItemIcon>
              <Inbox />
            </ListItemIcon>
            <ListItemText primary="Tasks" />
          </ListItem>
          <ListItem button onClick={() => setView('todos')}>
            <ListItemIcon>
              <Mail />
            </ListItemIcon>
            <ListItemText primary="Todos" />
          </ListItem>
        </List>
      </Box>
    </Drawer>
  );
};

export default Sidebar;

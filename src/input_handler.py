"""
Handles mouse and keyboard input for the game.
"""


class InputHandler:
    """Manages user input and card interaction."""
    
    def __init__(self):
        """Initialize the input handler."""
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_clicked = False
        self.mouse_down = False
        self.dragged_card = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0
    
    def update(self, event):
        """
        Process input events.
        
        Args:
            event: Pygame event to process
        """
        if event.type == pygame.MOUSEMOTION:
            self.mouse_x, self.mouse_y = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.mouse_down = True
                self.mouse_clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                self.mouse_down = False
                self.end_drag()
    
    def start_drag(self, card):
        """
        Start dragging a card.
        
        Args:
            card: Card to drag
        """
        self.dragged_card = card
        card.dragging = True
        card.selected = True
        self.drag_offset_x = self.mouse_x - card.x
        self.drag_offset_y = self.mouse_y - card.y
    
    def update_drag(self):
        """Update position of card being dragged."""
        if self.dragged_card:
            self.dragged_card.x = self.mouse_x - self.drag_offset_x
            self.dragged_card.y = self.mouse_y - self.drag_offset_y
            self.dragged_card.update_rect()
    
    def end_drag(self):
        """End dragging operation."""
        if self.dragged_card:
            self.dragged_card.dragging = False
            self.dragged_card.selected = False
            self.dragged_card = None
    
    def reset_click(self):
        """Reset click flag after processing."""
        self.mouse_clicked = False


# Need to import pygame at module level
import pygame


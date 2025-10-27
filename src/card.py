"""
Card class representing individual playing cards.
Supports custom attributes for game-specific mechanics.
"""


class Card:
    """Represents a single card with customizable attributes."""
    
    def __init__(self, name, **attributes):
        """
        Initialize a card.
        
        Args:
            name: The card's identifier/name
            **attributes: Custom attributes for the card (e.g., attack=5, defense=3)
        """
        self.name = name
        self.attributes = attributes
        
        # Visual properties
        self.x = 0
        self.y = 0
        self.width = 100
        self.height = 140
        self.rect = None
        
        # State properties
        self.face_up = True
        self.selected = False
        self.dragging = False
        self.hovered = False
        
        # Styling properties
        self.face_color = (240, 240, 240)
        self.back_color = (50, 50, 150)
        self.border_color = (50, 50, 50)
        self.text_color = (0, 0, 0)
        
    def update_rect(self):
        """Update the card's rectangle for collision detection."""
        self.rect = (self.x, self.y, self.width, self.height)
    
    def set_position(self, x, y):
        """Set the card's position and update its rectangle."""
        self.x = x
        self.y = y
        self.update_rect()
    
    def is_point_inside(self, x, y):
        """Check if a point is inside the card."""
        if not self.rect:
            self.update_rect()
        rect_x, rect_y, width, height = self.rect
        return rect_x <= x <= rect_x + width and rect_y <= y <= rect_y + height
    
    def get_attribute(self, key, default=None):
        """Get a custom attribute value."""
        return self.attributes.get(key, default)
    
    def set_attribute(self, key, value):
        """Set a custom attribute value."""
        self.attributes[key] = value
    
    def flip(self):
        """Flip the card (face up/down)."""
        self.face_up = not self.face_up
    
    def __str__(self):
        attrs_str = ", ".join(f"{k}={v}" for k, v in self.attributes.items())
        return f"Card({self.name}" + (f", {attrs_str})" if attrs_str else ")")


"""
Card class representing individual playing cards.
Supports different card types with type-specific attributes.
"""

CARD_TYPES = ["Character", "Upgrade", "Plan", "Skill", "Location", "Encounter"]


class Card:
    """Represents a single card with customizable attributes."""
    
    def __init__(self, name, card_type="Character", **attributes):
        """
        Initialize a card.
        
        Args:
            name: The card's identifier/name
            card_type: Type of card (Character, Upgrade, Plan, Skill, Location, Encounter)
            **attributes: Custom attributes for the card
        """
        self.name = name
        self.card_type = card_type
        self.attributes = attributes
        
        # Initialize type-specific attributes with defaults
        self._initialize_type_attributes()
        
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
    
    def _initialize_type_attributes(self):
        """Initialize type-specific attributes based on card type."""
        if self.card_type == "Character":
            self.attributes.setdefault("level", 0)
            self.attributes.setdefault("class", "")
            self.attributes.setdefault("strength", 0)
            self.attributes.setdefault("agility", 0)
            self.attributes.setdefault("intelligence", 0)
            self.attributes.setdefault("wisdom", 0)
            self.attributes.setdefault("special_rules", "")
        elif self.card_type == "Upgrade":
            self.attributes.setdefault("level", 0)
            self.attributes.setdefault("strength_mod", 0)
            self.attributes.setdefault("agility_mod", 0)
            self.attributes.setdefault("intelligence_mod", 0)
            self.attributes.setdefault("wisdom_mod", 0)
            self.attributes.setdefault("special_rules", "")
        elif self.card_type == "Plan":
            self.attributes.setdefault("strength_req", 0)
            self.attributes.setdefault("agility_req", 0)
            self.attributes.setdefault("intelligence_req", 0)
            self.attributes.setdefault("wisdom_req", 0)
            self.attributes.setdefault("special_rules", "")
        elif self.card_type == "Skill":
            self.attributes.setdefault("strength_req", 0)
            self.attributes.setdefault("agility_req", 0)
            self.attributes.setdefault("intelligence_req", 0)
            self.attributes.setdefault("wisdom_req", 0)
            self.attributes.setdefault("special_rules", "")
        elif self.card_type == "Location":
            self.attributes.setdefault("level", 0)
            self.attributes.setdefault("strength_def", 0)
            self.attributes.setdefault("agility_def", 0)
            self.attributes.setdefault("intelligence_def", 0)
            self.attributes.setdefault("wisdom_def", 0)
            self.attributes.setdefault("hit_points", 0)
            self.attributes.setdefault("special_rules", "")
        elif self.card_type == "Encounter":
            self.attributes.setdefault("strength_def", 0)
            self.attributes.setdefault("agility_def", 0)
            self.attributes.setdefault("intelligence_def", 0)
            self.attributes.setdefault("wisdom_def", 0)
            self.attributes.setdefault("hit_points", 0)
            self.attributes.setdefault("special_rules", "")
    
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
        return f"Card({self.name}, type={self.card_type}" + (f", {attrs_str})" if attrs_str else ")")


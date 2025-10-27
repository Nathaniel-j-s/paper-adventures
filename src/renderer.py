"""
Rendering system for drawing cards and visual elements.
"""

import pygame


class CardRenderer:
    """Handles rendering of cards with different visual states."""
    
    def __init__(self, screen):
        """
        Initialize the card renderer.
        
        Args:
            screen: Pygame surface to render to
        """
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 28)
    
    def render_card(self, card):
        """
        Render a single card with appropriate visual state.
        
        Args:
            card: Card object to render
        """
        if not card.rect:
            card.update_rect()
        
        # Draw card background (face or back)
        if card.face_up:
            color = card.face_color
        else:
            color = card.back_color
        
        # Add elevation effect when dragging
        if card.dragging:
            # Draw shadow
            shadow_rect = (card.x + 3, card.y + 3, card.width, card.height)
            pygame.draw.rect(self.screen, (0, 0, 0, 50), shadow_rect)
            card_x = card.x + 2
            card_y = card.y + 2
        else:
            card_x = card.x
            card_y = card.y
        
        # Draw card body
        pygame.draw.rect(self.screen, color, 
                        (card_x, card_y, card.width, card.height))
        
        # Draw border
        if card.selected:
            border_color = (255, 200, 0)
            border_width = 3
        elif card.hovered:
            border_color = (255, 255, 255)
            border_width = 2
        else:
            border_color = card.border_color
            border_width = 1
        
        pygame.draw.rect(self.screen, border_color,
                        (card_x, card_y, card.width, card.height), border_width)
        
        # Draw card content if face up
        if card.face_up:
            # Draw card name
            text = self.font.render(card.name, True, card.text_color)
            text_rect = text.get_rect(center=(card_x + card.width // 2, 
                                             card_y + 20))
            self.screen.blit(text, text_rect)
            
            # Draw attributes
            y_offset = 50
            for key, value in card.attributes.items():
                attr_text = f"{key}: {value}"
                text = self.font.render(attr_text, True, card.text_color)
                text_rect = text.get_rect(center=(card_x + card.width // 2, 
                                                 card_y + y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 25


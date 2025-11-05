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

    def render_deck_pile(self, deck, x, y, width=100, height=140):
        """Render a deck pile at a fixed position with count label."""
        # Background for pile (use a darker back if there are cards)
        has_cards = deck.size() > 0
        pile_color = (60, 60, 100) if has_cards else (35, 35, 35)
        pygame.draw.rect(self.screen, pile_color, (x, y, width, height))
        # Border
        border_color = (200, 200, 200) if has_cards else (90, 90, 90)
        pygame.draw.rect(self.screen, border_color, (x, y, width, height), 2)
        # Count label
        count_text = self.title_font.render(f"Deck: {deck.size()}", True, (230, 230, 230))
        count_rect = count_text.get_rect(center=(x + width // 2, y + height + 14))
        self.screen.blit(count_text, count_rect)

    def render_hand_area(self, x, y, width, height):
        """Render the player's hand area background and label."""
        pygame.draw.rect(self.screen, (30, 30, 30), (x, y, width, height))
        pygame.draw.rect(self.screen, (120, 120, 120), (x, y, width, height), 2)
        label = self.title_font.render("Hand", True, (220, 220, 220))
        self.screen.blit(label, (x + 8, y + 6))

    def render_deck_debug_list(self, deck, x, y):
        """Render a simple list of card names from top to bottom for debugging."""
        # Panel metrics
        panel_width = 220
        line_height = 22
        padding = 8
        items = [card.name for card in deck.cards]  # index 0 is top
        panel_height = padding * 2 + max(1, len(items)) * line_height
        # Background panel
        pygame.draw.rect(self.screen, (25, 25, 25), (x, y, panel_width, panel_height))
        pygame.draw.rect(self.screen, (180, 180, 180), (x, y, panel_width, panel_height), 1)
        # Title
        title_text = self.title_font.render("Deck (top -> bottom)", True, (230, 230, 230))
        self.screen.blit(title_text, (x + padding, y + padding - 2))
        # Items
        list_y = y + padding + 20
        if not items:
            empty_text = self.font.render("<empty>", True, (200, 200, 200))
            self.screen.blit(empty_text, (x + padding, list_y))
            return
        for idx, name in enumerate(items):
            item_text = self.font.render(f"{idx+1}. {name}", True, (200, 200, 200))
            self.screen.blit(item_text, (x + padding, list_y + idx * line_height))


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
            # Draw card name and type
            name_text = self.font.render(card.name, True, card.text_color)
            name_rect = name_text.get_rect(center=(card_x + card.width // 2, 
                                                   card_y + 15))
            self.screen.blit(name_text, name_rect)
            
            # Draw card type
            type_text = self.font.render(f"({card.card_type})", True, card.text_color)
            type_rect = type_text.get_rect(center=(card_x + card.width // 2, 
                                                    card_y + 35))
            self.screen.blit(type_text, type_rect)
            
            # Draw type-specific attributes
            y_offset = 55
            card_type = card.card_type
            
            if card_type == "Character":
                if card.attributes.get("level", 0):
                    self._render_attribute(card_x, card_y, card.width, y_offset, "Lvl", card.attributes.get("level", 0), card.text_color)
                    y_offset += 20
                if card.attributes.get("class"):
                    self._render_attribute(card_x, card_y, card.width, y_offset, "Class", card.attributes.get("class"), card.text_color)
                    y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "STR", card.attributes.get("strength", 0), card.text_color)
                y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "AGI", card.attributes.get("agility", 0), card.text_color)
                y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "INT", card.attributes.get("intelligence", 0), card.text_color)
                y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "WIS", card.attributes.get("wisdom", 0), card.text_color)
                y_offset += 20
            elif card_type == "Upgrade":
                if card.attributes.get("level", 0):
                    self._render_attribute(card_x, card_y, card.width, y_offset, "Lvl", card.attributes.get("level", 0), card.text_color)
                    y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "STR+", card.attributes.get("strength_mod", 0), card.text_color)
                y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "AGI+", card.attributes.get("agility_mod", 0), card.text_color)
                y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "INT+", card.attributes.get("intelligence_mod", 0), card.text_color)
                y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "WIS+", card.attributes.get("wisdom_mod", 0), card.text_color)
                y_offset += 20
            elif card_type == "Plan":
                self._render_attribute(card_x, card_y, card.width, y_offset, "STR Req", card.attributes.get("strength_req", 0), card.text_color)
                y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "AGI Req", card.attributes.get("agility_req", 0), card.text_color)
                y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "INT Req", card.attributes.get("intelligence_req", 0), card.text_color)
                y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "WIS Req", card.attributes.get("wisdom_req", 0), card.text_color)
                y_offset += 20
            elif card_type == "Skill":
                self._render_attribute(card_x, card_y, card.width, y_offset, "STR Req", card.attributes.get("strength_req", 0), card.text_color)
                y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "AGI Req", card.attributes.get("agility_req", 0), card.text_color)
                y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "INT Req", card.attributes.get("intelligence_req", 0), card.text_color)
                y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "WIS Req", card.attributes.get("wisdom_req", 0), card.text_color)
                y_offset += 20
            elif card_type == "Location":
                if card.attributes.get("level", 0):
                    self._render_attribute(card_x, card_y, card.width, y_offset, "Lvl", card.attributes.get("level", 0), card.text_color)
                    y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "STR Def", card.attributes.get("strength_def", 0), card.text_color)
                y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "AGI Def", card.attributes.get("agility_def", 0), card.text_color)
                y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "INT Def", card.attributes.get("intelligence_def", 0), card.text_color)
                y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "WIS Def", card.attributes.get("wisdom_def", 0), card.text_color)
                y_offset += 20
                if card.attributes.get("hit_points", 0):
                    self._render_attribute(card_x, card_y, card.width, y_offset, "HP", card.attributes.get("hit_points", 0), card.text_color)
                    y_offset += 20
            elif card_type == "Encounter":
                self._render_attribute(card_x, card_y, card.width, y_offset, "STR Def", card.attributes.get("strength_def", 0), card.text_color)
                y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "AGI Def", card.attributes.get("agility_def", 0), card.text_color)
                y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "INT Def", card.attributes.get("intelligence_def", 0), card.text_color)
                y_offset += 20
                self._render_attribute(card_x, card_y, card.width, y_offset, "WIS Def", card.attributes.get("wisdom_def", 0), card.text_color)
                y_offset += 20
                if card.attributes.get("hit_points", 0):
                    self._render_attribute(card_x, card_y, card.width, y_offset, "HP", card.attributes.get("hit_points", 0), card.text_color)
                    y_offset += 20
            
            # Draw special rules if present
            special_rules = card.attributes.get("special_rules", "")
            if special_rules:
                # Truncate if too long for card
                rules_text = special_rules[:20] + "..." if len(special_rules) > 20 else special_rules
                rules_surface = self.font.render(rules_text, True, card.text_color)
                rules_rect = rules_surface.get_rect(center=(card_x + card.width // 2, 
                                                             card_y + card.height - 15))
                self.screen.blit(rules_surface, rules_rect)
    
    def _render_attribute(self, card_x, card_y, card_width, y_offset, label, value, color):
        """Render a single attribute line on a card."""
        attr_text = f"{label}: {value}"
        text = self.font.render(attr_text, True, color)
        text_rect = text.get_rect(center=(card_x + card_width // 2, 
                                         card_y + y_offset))
        self.screen.blit(text, text_rect)

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

    def render_play_area(self, x, y, width, height):
        """Render the in-play area background and label."""
        pygame.draw.rect(self.screen, (30, 30, 30), (x, y, width, height))
        pygame.draw.rect(self.screen, (120, 120, 120), (x, y, width, height), 2)
        label = self.title_font.render("In-Play Area", True, (220, 220, 220))
        self.screen.blit(label, (x + 8, y + 6))

    def render_hand_area(self, x, y, width, height):
        """Render the player's hand area background and label."""
        pygame.draw.rect(self.screen, (30, 30, 30), (x, y, width, height))
        pygame.draw.rect(self.screen, (120, 120, 120), (x, y, width, height), 2)
        label = self.title_font.render("Hand", True, (220, 220, 220))
        self.screen.blit(label, (x + 8, y + 6))

    def render_button(self, x, y, width, height, text, enabled=True):
        """Render a simple button."""
        bg = (70, 70, 70) if enabled else (45, 45, 45)
        border = (180, 180, 180) if enabled else (90, 90, 90)
        fg = (240, 240, 240) if enabled else (160, 160, 160)
        pygame.draw.rect(self.screen, bg, (x, y, width, height), border_radius=4)
        pygame.draw.rect(self.screen, border, (x, y, width, height), 2, border_radius=4)
        label = self.title_font.render(text, True, fg)
        label_rect = label.get_rect(center=(x + width // 2, y + height // 2))
        self.screen.blit(label, label_rect)

    def render_text_input(self, x, y, width, height, label_text, value_text, focused=False):
        """Render a labeled text input box."""
        # Label
        label_surface = self.font.render(label_text, True, (220, 220, 220))
        self.screen.blit(label_surface, (x, y))
        # Input box
        box_y = y + 18
        border_color = (255, 200, 0) if focused else (150, 150, 150)
        pygame.draw.rect(self.screen, (35, 35, 35), (x, box_y, width, height))
        pygame.draw.rect(self.screen, border_color, (x, box_y, width, height), 2)
        # Text
        text_surface = self.font.render(value_text, True, (230, 230, 230))
        self.screen.blit(text_surface, (x + 8, box_y + (height - text_surface.get_height()) // 2))

    def render_panel_with_title(self, x, y, width, height, title):
        """Render a simple panel with a border and title text."""
        pygame.draw.rect(self.screen, (25, 25, 25), (x, y, width, height))
        pygame.draw.rect(self.screen, (120, 120, 120), (x, y, width, height), 2)
        title_surface = self.title_font.render(title, True, (230, 230, 230))
        self.screen.blit(title_surface, (x + 8, y + 8))

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


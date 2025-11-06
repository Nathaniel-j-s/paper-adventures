"""
Main entry point for the PyGame card game.
"""

import pygame
import sys
from src.card import Card, CARD_TYPES
from src.deck import Deck
from src.renderer import CardRenderer
from src.input_handler import InputHandler
from src.deck_manager import DeckManager


class Game:
    """Main game class managing the game loop and state."""
    
    def __init__(self):
        """Initialize the game."""
        pygame.init()
        self.screen_width = 1280
        self.screen_height = 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Paper Adventures - Card Game")
        self.clock = pygame.time.Clock()
        
        # Initialize systems
        self.input_handler = InputHandler()
        self.renderer = CardRenderer(self.screen)
        self.deck_manager = DeckManager()
        self.table_deck = Deck("Table Deck")
        # Persistent deck for cards created via Card Creator
        loaded_created = self.deck_manager.load_deck("CreatedCards")
        self.created_cards_deck = loaded_created if loaded_created else Deck("CreatedCards")
        # Static deck placement and size (matches card size)
        self.deck_x = 10
        self.deck_y = 10
        self.deck_width = 100
        self.deck_height = 140
        # Debug view flag for deck contents
        self.view_deck_debug = False
        # Draw button under deck
        self.draw_btn_width = self.deck_width
        self.draw_btn_height = 36
        self.draw_btn_x = self.deck_x
        self.draw_btn_y = self.deck_y + self.deck_height + 20
        
        # Upper-right Card Creator inputs
        self.card_type_index = 0  # Index into CARD_TYPES
        self.card_name_input = ""
        # Fields for all card types
        self.level_input = ""
        self.class_input = ""
        self.strength_input = ""
        self.agility_input = ""
        self.intelligence_input = ""
        self.wisdom_input = ""
        self.strength_mod_input = ""
        self.agility_mod_input = ""
        self.intelligence_mod_input = ""
        self.wisdom_mod_input = ""
        self.strength_req_input = ""
        self.agility_req_input = ""
        self.intelligence_req_input = ""
        self.wisdom_req_input = ""
        self.strength_def_input = ""
        self.agility_def_input = ""
        self.intelligence_def_input = ""
        self.wisdom_def_input = ""
        self.hit_points_input = ""
        self.special_rules_input = ""
        self.input_focus = None  # Current focused input field
        self.card_name_input_width = 260
        self.card_name_input_height = 28
        self.card_name_input_x = self.screen_width - self.card_name_input_width - 10
        self.card_name_input_y = 10
        self.spacing = 40  # Spacing between input fields
        # Player hand area along bottom
        self.hand_x = 10
        self.hand_y = self.screen_height - 180
        self.hand_width = self.screen_width - 20
        self.hand_height = 170
        self.hand_cards = []
        
        # In-play area in the center of the window
        self.play_area_x = 10
        self.play_area_y = 200
        self.play_area_width = self.screen_width - 20
        self.play_area_height = self.hand_y - self.play_area_y - 20
        
        # Game state
        self.running = True
        self.cards = []
        
        # Add previously created cards (persisted) to the table
        for persisted_card in self.created_cards_deck.cards:
            # Ensure their rects are set and include in current table
            if not persisted_card.rect:
                persisted_card.update_rect()
            self.cards.append(persisted_card)

    def _get_visible_fields(self):
        """Get list of visible field names for current card type."""
        card_type = CARD_TYPES[self.card_type_index]
        fields = ['name']
        if card_type == "Character":
            fields.extend(['type_selector', 'level', 'class', 'strength', 'agility', 
                          'intelligence', 'wisdom', 'special_rules'])
        elif card_type == "Upgrade":
            fields.extend(['type_selector', 'level', 'strength_mod', 'agility_mod', 
                          'intelligence_mod', 'wisdom_mod', 'special_rules'])
        elif card_type == "Plan":
            fields.extend(['type_selector', 'strength_req', 'agility_req', 
                          'intelligence_req', 'wisdom_req', 'special_rules'])
        elif card_type == "Skill":
            fields.extend(['type_selector', 'strength_req', 'agility_req', 
                          'intelligence_req', 'wisdom_req', 'special_rules'])
        elif card_type == "Location":
            fields.extend(['type_selector', 'level', 'strength_def', 'agility_def', 
                          'intelligence_def', 'wisdom_def', 'hit_points', 'special_rules'])
        elif card_type == "Encounter":
            fields.extend(['type_selector', 'strength_def', 'agility_def', 
                          'intelligence_def', 'wisdom_def', 'hit_points', 'special_rules'])
        return fields
    
    def _get_field_y_position(self, field_name):
        """Get Y position for a field in the card creator."""
        card_type = CARD_TYPES[self.card_type_index]
        field_order = ['name']
        
        if card_type == "Character":
            field_order.extend(['type_selector', 'level', 'class', 'strength', 'agility', 
                               'intelligence', 'wisdom', 'special_rules'])
        elif card_type == "Upgrade":
            field_order.extend(['type_selector', 'level', 'strength_mod', 'agility_mod', 
                               'intelligence_mod', 'wisdom_mod', 'special_rules'])
        elif card_type == "Plan":
            field_order.extend(['type_selector', 'strength_req', 'agility_req', 
                               'intelligence_req', 'wisdom_req', 'special_rules'])
        elif card_type == "Skill":
            field_order.extend(['type_selector', 'strength_req', 'agility_req', 
                               'intelligence_req', 'wisdom_req', 'special_rules'])
        elif card_type == "Location":
            field_order.extend(['type_selector', 'level', 'strength_def', 'agility_def', 
                               'intelligence_def', 'wisdom_def', 'hit_points', 'special_rules'])
        elif card_type == "Encounter":
            field_order.extend(['type_selector', 'strength_def', 'agility_def', 
                               'intelligence_def', 'wisdom_def', 'hit_points', 'special_rules'])
        
        try:
            index = field_order.index(field_name)
            return self.card_name_input_y + index * self.spacing
        except ValueError:
            return None

    def handle_events(self):
        """Process all input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Update input handler
            self.input_handler.update(event)
            
            # Handle mouse clicks on cards
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                input_w = self.card_name_input_width
                input_h = self.card_name_input_height
                base_x = self.card_name_input_x
                handled = False
                
                # Check card type selector (dropdown)
                type_selector_y = self._get_field_y_position('type_selector')
                if type_selector_y is not None:
                    if (base_x <= mx <= base_x + input_w and
                        type_selector_y <= my <= type_selector_y + 32):
                        # Cycle through card types
                        self.card_type_index = (self.card_type_index + 1) % len(CARD_TYPES)
                        self.input_focus = None
                        handled = True
                
                if not handled:
                    # Check all visible fields
                    visible_fields = self._get_visible_fields()
                    for field_name in visible_fields:
                        if field_name == 'type_selector':
                            continue
                        field_y = self._get_field_y_position(field_name)
                        if field_y is not None:
                            if (base_x <= mx <= base_x + input_w and
                                field_y + 18 <= my <= field_y + 18 + input_h):
                                self.input_focus = field_name
                                handled = True
                                break
                
                if not handled:
                    # Check Submit button
                    visible_fields = self._get_visible_fields()
                    submit_y = self.card_name_input_y + len(visible_fields) * self.spacing
                    submit_w = self.card_name_input_width
                    submit_h = 32
                    if (base_x <= mx <= base_x + submit_w and
                        submit_y <= my <= submit_y + submit_h):
                        self._submit_creator_inputs()
                        handled = True
                
                if not handled:
                    # Draw button click
                    if (self.draw_btn_x <= mx <= self.draw_btn_x + self.draw_btn_width and
                        self.draw_btn_y <= my <= self.draw_btn_y + self.draw_btn_height):
                        # Draw top card into hand if available
                        drawn = self.table_deck.draw_card()
                        if drawn is not None:
                            if drawn in self.cards:
                                self.cards.remove(drawn)
                            if drawn in self.hand_cards:
                                self.hand_cards.remove(drawn)
                            self.hand_cards.append(drawn)
                        # Do not start dragging when clicking button
                        handled = True
                
                if not handled:
                    # Check which card was clicked
                    for card in reversed(self.cards + self.hand_cards):  # Check from top to bottom
                        if card.is_point_inside(*event.pos):
                            self.input_handler.start_drag(card)
                            # Clear input focus when clicking on cards
                            self.input_focus = None
                            handled = True
                            break
                
                if not handled:
                    # Clicking elsewhere clears focus
                    self.input_focus = None
            
            # Handle right-click on cards in hand to move to in-play area
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right mouse button
                # Check if a card in hand was right-clicked
                for card in reversed(self.hand_cards):  # Check from top to bottom
                    if card.is_point_inside(*event.pos):
                        # Remove from hand
                        self.hand_cards.remove(card)
                        # Position in center of play area
                        center_x = self.play_area_x + self.play_area_width // 2 - card.width // 2
                        center_y = self.play_area_y + self.play_area_height // 2 - card.height // 2
                        card.set_position(center_x, center_y)
                        # Add to in-play area (cards list)
                        self.cards.append(card)
                        break
            
            # Handle flip on 'F' key while hovering a card
            if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                # Avoid flipping while dragging a card
                if not self.input_handler.dragged_card:
                    mouse_pos = pygame.mouse.get_pos()
                    for card in reversed(self.cards):  # Top-most first
                        if card.is_point_inside(*mouse_pos):
                            card.flip()
                            break

            # Handle dropping onto the deck area
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                released = self.input_handler.released_card
                if released is not None:
                    mx, my = pygame.mouse.get_pos()
                    if (self.deck_x <= mx <= self.deck_x + self.deck_width and
                        self.deck_y <= my <= self.deck_y + self.deck_height):
                        # Remove from table if present
                        if released in self.cards:
                            self.cards.remove(released)
                        if released in self.hand_cards:
                            self.hand_cards.remove(released)
                        # Snap to deck position
                        released.set_position(self.deck_x, self.deck_y)
                        # Place on top of deck
                        self.table_deck.add_to_top(released)
                    elif (self.hand_x <= mx <= self.hand_x + self.hand_width and
                          self.hand_y <= my <= self.hand_y + self.hand_height):
                        # Drop into player hand
                        if released in self.cards:
                            self.cards.remove(released)
                        if released in self.hand_cards:
                            self.hand_cards.remove(released)
                        self.hand_cards.append(released)
                        # Positioning handled by layout in update()
                    # Clear the released reference
                    self.input_handler.released_card = None

            # Debug: show deck contents while holding V over deck
            if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
                mx, my = pygame.mouse.get_pos()
                self.view_deck_debug = (
                    self.deck_x <= mx <= self.deck_x + self.deck_width and
                    self.deck_y <= my <= self.deck_y + self.deck_height
                )
            if event.type == pygame.KEYUP and event.key == pygame.K_v:
                self.view_deck_debug = False
            
            # Typing into upper-right inputs when focused
            if event.type == pygame.KEYDOWN and self.input_focus is not None:
                # Helper to get/set value by focus key
                def get_val():
                    field_map = {
                        'name': self.card_name_input,
                        'level': self.level_input,
                        'class': self.class_input,
                        'strength': self.strength_input,
                        'agility': self.agility_input,
                        'intelligence': self.intelligence_input,
                        'wisdom': self.wisdom_input,
                        'strength_mod': self.strength_mod_input,
                        'agility_mod': self.agility_mod_input,
                        'intelligence_mod': self.intelligence_mod_input,
                        'wisdom_mod': self.wisdom_mod_input,
                        'strength_req': self.strength_req_input,
                        'agility_req': self.agility_req_input,
                        'intelligence_req': self.intelligence_req_input,
                        'wisdom_req': self.wisdom_req_input,
                        'strength_def': self.strength_def_input,
                        'agility_def': self.agility_def_input,
                        'intelligence_def': self.intelligence_def_input,
                        'wisdom_def': self.wisdom_def_input,
                        'hit_points': self.hit_points_input,
                        'special_rules': self.special_rules_input,
                    }
                    return field_map.get(self.input_focus, "")
                
                def set_val(v):
                    if self.input_focus == 'name': self.card_name_input = v
                    elif self.input_focus == 'level': self.level_input = v
                    elif self.input_focus == 'class': self.class_input = v
                    elif self.input_focus == 'strength': self.strength_input = v
                    elif self.input_focus == 'agility': self.agility_input = v
                    elif self.input_focus == 'intelligence': self.intelligence_input = v
                    elif self.input_focus == 'wisdom': self.wisdom_input = v
                    elif self.input_focus == 'strength_mod': self.strength_mod_input = v
                    elif self.input_focus == 'agility_mod': self.agility_mod_input = v
                    elif self.input_focus == 'intelligence_mod': self.intelligence_mod_input = v
                    elif self.input_focus == 'wisdom_mod': self.wisdom_mod_input = v
                    elif self.input_focus == 'strength_req': self.strength_req_input = v
                    elif self.input_focus == 'agility_req': self.agility_req_input = v
                    elif self.input_focus == 'intelligence_req': self.intelligence_req_input = v
                    elif self.input_focus == 'wisdom_req': self.wisdom_req_input = v
                    elif self.input_focus == 'strength_def': self.strength_def_input = v
                    elif self.input_focus == 'agility_def': self.agility_def_input = v
                    elif self.input_focus == 'intelligence_def': self.intelligence_def_input = v
                    elif self.input_focus == 'wisdom_def': self.wisdom_def_input = v
                    elif self.input_focus == 'hit_points': self.hit_points_input = v
                    elif self.input_focus == 'special_rules': self.special_rules_input = v
                
                current = get_val()
                if event.key == pygame.K_BACKSPACE:
                    set_val(current[:-1])
                elif event.key == pygame.K_RETURN:
                    # Ignore submit behavior for now
                    pass
                else:
                    if event.unicode:
                        # Text fields: name, class, special_rules
                        if self.input_focus in ['name', 'class', 'special_rules']:
                            max_len = 30 if self.input_focus == 'name' else 100
                            if len(current) < max_len:
                                set_val(current + event.unicode)
                        # Numeric fields
                        else:
                            if event.unicode.isdigit() or (event.unicode == '-' and len(current) == 0):
                                max_len = 3
                                if len(current) < max_len:
                                    set_val(current + event.unicode)
    
    def update(self):
        """Update game state."""
        # Update card positions
        self.input_handler.update_drag()
        
        # Reset click flag
        self.input_handler.reset_click()
        
        # Update card hover states
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for card in self.cards + self.hand_cards:
            card.hovered = card.is_point_inside(mouse_x, mouse_y)
        
        # Layout hand cards
        self._layout_hand()

    def _layout_hand(self):
        """Arrange cards in the player's hand neatly centered along the hand area."""
        if not self.hand_cards:
            return
        card_width = self.hand_cards[0].width
        card_height = self.hand_cards[0].height
        available_width = self.hand_width - 20
        count = len(self.hand_cards)
        if count == 1:
            gap = 0
        else:
            gap = (available_width - count * card_width) / (count - 1)
            gap = max(10, min(30, gap))
        total_width = count * card_width + (count - 1) * gap
        start_x = self.hand_x + (self.hand_width - total_width) / 2
        y = self.hand_y + (self.hand_height - card_height) / 2
        for idx, card in enumerate(self.hand_cards):
            if card.dragging:
                # Skip positioning dragged cards
                continue
            x = start_x + idx * (card_width + gap)
            card.set_position(int(x), int(y))
    
    def render(self):
        """Render the game."""
        # Clear screen
        self.screen.fill((40, 40, 40))
        
        # Render the in-play area first (background)
        self.renderer.render_play_area(self.play_area_x, self.play_area_y, 
                                       self.play_area_width, self.play_area_height)
        
        # Render the hand area (background)
        self.renderer.render_hand_area(self.hand_x, self.hand_y, self.hand_width, self.hand_height)

        # Render all cards
        for card in self.cards:
            self.renderer.render_card(card)
        # Render hand cards on top of hand area
        for card in self.hand_cards:
            self.renderer.render_card(card)
        
        # Render the deck pile
        self.renderer.render_deck_pile(self.table_deck, self.deck_x, self.deck_y,
                                       self.deck_width, self.deck_height)
        # Render draw button under deck
        self.renderer.render_button(
            self.draw_btn_x, self.draw_btn_y, self.draw_btn_width, self.draw_btn_height,
            "Draw", enabled=not self.table_deck.is_empty()
        )
        
        # Render Card Creator panel
        visible_fields = self._get_visible_fields()
        panel_x = self.card_name_input_x - 8
        panel_y = self.card_name_input_y - 8
        panel_w = self.card_name_input_width + 16
        # Bottom = submit button top + button height + padding
        panel_h = (self.card_name_input_y + len(visible_fields) * self.spacing + 32 + 12) - panel_y
        self.renderer.render_panel_with_title(panel_x, panel_y, panel_w, panel_h, "Card Creator")

        # Render card type selector
        type_selector_y = self._get_field_y_position('type_selector')
        if type_selector_y is not None:
            self.renderer.render_button(
                self.card_name_input_x,
                type_selector_y,
                self.card_name_input_width,
                32,
                f"Type: {CARD_TYPES[self.card_type_index]}",
                enabled=True
            )
        
        # Render fields based on card type
        field_labels = {
            'name': 'Card Name',
            'level': 'Level',
            'class': 'Class',
            'strength': 'Strength',
            'agility': 'Agility',
            'intelligence': 'Intelligence',
            'wisdom': 'Wisdom',
            'strength_mod': 'Strength Mod',
            'agility_mod': 'Agility Mod',
            'intelligence_mod': 'Intelligence Mod',
            'wisdom_mod': 'Wisdom Mod',
            'strength_req': 'Strength Req',
            'agility_req': 'Agility Req',
            'intelligence_req': 'Intelligence Req',
            'wisdom_req': 'Wisdom Req',
            'strength_def': 'Strength Def',
            'agility_def': 'Agility Def',
            'intelligence_def': 'Intelligence Def',
            'wisdom_def': 'Wisdom Def',
            'hit_points': 'Hit Points',
            'special_rules': 'Special Rules',
        }
        
        field_values = {
            'name': self.card_name_input,
            'level': self.level_input,
            'class': self.class_input,
            'strength': self.strength_input,
            'agility': self.agility_input,
            'intelligence': self.intelligence_input,
            'wisdom': self.wisdom_input,
            'strength_mod': self.strength_mod_input,
            'agility_mod': self.agility_mod_input,
            'intelligence_mod': self.intelligence_mod_input,
            'wisdom_mod': self.wisdom_mod_input,
            'strength_req': self.strength_req_input,
            'agility_req': self.agility_req_input,
            'intelligence_req': self.intelligence_req_input,
            'wisdom_req': self.wisdom_req_input,
            'strength_def': self.strength_def_input,
            'agility_def': self.agility_def_input,
            'intelligence_def': self.intelligence_def_input,
            'wisdom_def': self.wisdom_def_input,
            'hit_points': self.hit_points_input,
            'special_rules': self.special_rules_input,
        }
        
        for field_name in visible_fields:
            if field_name == 'type_selector':
                continue
            field_y = self._get_field_y_position(field_name)
            if field_y is not None:
                label = field_labels.get(field_name, field_name)
                value = field_values.get(field_name, "")
                self.renderer.render_text_input(
                    self.card_name_input_x,
                    field_y,
                    self.card_name_input_width,
                    self.card_name_input_height,
                    label,
                    value,
                    self.input_focus == field_name
                )
        
        # Render Submit button
        submit_y = self.card_name_input_y + len(visible_fields) * self.spacing
        self.renderer.render_button(
            self.card_name_input_x,
            submit_y,
            self.card_name_input_width,
            32,
            "Submit",
            enabled=True
        )
        
        # Render debug list if hovering deck and V is held
        if self.view_deck_debug:
            mx, my = pygame.mouse.get_pos()
            if (self.deck_x <= mx <= self.deck_x + self.deck_width and
                self.deck_y <= my <= self.deck_y + self.deck_height):
                self.renderer.render_deck_debug_list(
                    self.table_deck,
                    self.deck_x + self.deck_width + 12,
                    self.deck_y
                )
        
        # Update display
        pygame.display.flip()

    def _submit_creator_inputs(self):
        """Create a new Card from the upper-right inputs and add to table."""
        def to_int(s):
            try:
                return int(s)
            except Exception:
                return 0
        
        name = self.card_name_input.strip() or "Card"
        card_type = CARD_TYPES[self.card_type_index]
        attrs = {}
        
        # Collect attributes based on card type
        if card_type == "Character":
            attrs["level"] = to_int(self.level_input)
            attrs["class"] = self.class_input.strip()
            attrs["strength"] = to_int(self.strength_input)
            attrs["agility"] = to_int(self.agility_input)
            attrs["intelligence"] = to_int(self.intelligence_input)
            attrs["wisdom"] = to_int(self.wisdom_input)
            attrs["special_rules"] = self.special_rules_input.strip()
        elif card_type == "Upgrade":
            attrs["level"] = to_int(self.level_input)
            attrs["strength_mod"] = to_int(self.strength_mod_input)
            attrs["agility_mod"] = to_int(self.agility_mod_input)
            attrs["intelligence_mod"] = to_int(self.intelligence_mod_input)
            attrs["wisdom_mod"] = to_int(self.wisdom_mod_input)
            attrs["special_rules"] = self.special_rules_input.strip()
        elif card_type == "Plan":
            attrs["strength_req"] = to_int(self.strength_req_input)
            attrs["agility_req"] = to_int(self.agility_req_input)
            attrs["intelligence_req"] = to_int(self.intelligence_req_input)
            attrs["wisdom_req"] = to_int(self.wisdom_req_input)
            attrs["special_rules"] = self.special_rules_input.strip()
        elif card_type == "Skill":
            attrs["strength_req"] = to_int(self.strength_req_input)
            attrs["agility_req"] = to_int(self.agility_req_input)
            attrs["intelligence_req"] = to_int(self.intelligence_req_input)
            attrs["wisdom_req"] = to_int(self.wisdom_req_input)
            attrs["special_rules"] = self.special_rules_input.strip()
        elif card_type == "Location":
            attrs["level"] = to_int(self.level_input)
            attrs["strength_def"] = to_int(self.strength_def_input)
            attrs["agility_def"] = to_int(self.agility_def_input)
            attrs["intelligence_def"] = to_int(self.intelligence_def_input)
            attrs["wisdom_def"] = to_int(self.wisdom_def_input)
            attrs["hit_points"] = to_int(self.hit_points_input)
            attrs["special_rules"] = self.special_rules_input.strip()
        elif card_type == "Encounter":
            attrs["strength_def"] = to_int(self.strength_def_input)
            attrs["agility_def"] = to_int(self.agility_def_input)
            attrs["intelligence_def"] = to_int(self.intelligence_def_input)
            attrs["wisdom_def"] = to_int(self.wisdom_def_input)
            attrs["hit_points"] = to_int(self.hit_points_input)
            attrs["special_rules"] = self.special_rules_input.strip()
        
        new_card = Card(name, card_type=card_type, **attrs)
        # Place to the right of the deck at deck Y
        place_x = self.deck_x + self.deck_width + 20
        place_y = self.deck_y
        new_card.set_position(place_x, place_y)
        self.cards.append(new_card)
        
        # Add to persistent created-cards deck and save immediately
        self.created_cards_deck.add_card(new_card)
        self.deck_manager.save_deck(self.created_cards_deck)
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # Cap at 60 FPS
        
        # Save created cards before exiting
        try:
            self.deck_manager.save_deck(self.created_cards_deck)
        except Exception:
            pass
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()


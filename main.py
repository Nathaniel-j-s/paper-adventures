"""
Main entry point for the PyGame card game.
"""

import pygame
import sys
from src.card import Card
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
        # Player hand area along bottom
        self.hand_x = 10
        self.hand_y = self.screen_height - 180
        self.hand_width = self.screen_width - 20
        self.hand_height = 170
        self.hand_cards = []
        
        # Game state
        self.running = True
        self.cards = []
        
        # Create some test cards
        self._create_test_cards()
    
    def _create_test_cards(self):
        """Create sample cards for testing."""
        # Create a test deck with some cards
        card1 = Card("Fireball", attack=5, mana=3)
        card1.set_position(200, 300)
        self.cards.append(card1)
        
        card2 = Card("Shield", defense=3, mana=2)
        card2.set_position(350, 300)
        self.cards.append(card2)
        
        card3 = Card("Heal", healing=4, mana=1)
        card3.set_position(500, 300)
        self.cards.append(card3)
        
        card4 = Card("Lightning", attack=7, mana=4)
        card4.set_position(200, 100)
        self.cards.append(card4)
    
    def handle_events(self):
        """Process all input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Update input handler
            self.input_handler.update(event)
            
            # Handle mouse clicks on cards
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Draw button click
                if (self.draw_btn_x <= event.pos[0] <= self.draw_btn_x + self.draw_btn_width and
                    self.draw_btn_y <= event.pos[1] <= self.draw_btn_y + self.draw_btn_height):
                    # Draw top card into hand if available
                    drawn = self.table_deck.draw_card()
                    if drawn is not None:
                        if drawn in self.cards:
                            self.cards.remove(drawn)
                        if drawn in self.hand_cards:
                            self.hand_cards.remove(drawn)
                        self.hand_cards.append(drawn)
                    # Do not start dragging when clicking button
                    continue
                # Check which card was clicked
                for card in reversed(self.cards + self.hand_cards):  # Check from top to bottom
                    if card.is_point_inside(*event.pos):
                        self.input_handler.start_drag(card)
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
        
        # Render the hand area first (background)
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
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # Cap at 60 FPS
        
        pygame.quit()
        sys.exit()


def main():
    """Entry point."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()


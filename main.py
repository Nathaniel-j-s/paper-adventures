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
                # Check which card was clicked
                for card in reversed(self.cards):  # Check from top to bottom
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
    
    def update(self):
        """Update game state."""
        # Update card positions
        self.input_handler.update_drag()
        
        # Reset click flag
        self.input_handler.reset_click()
        
        # Update card hover states
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for card in self.cards:
            card.hovered = card.is_point_inside(mouse_x, mouse_y)
    
    def render(self):
        """Render the game."""
        # Clear screen
        self.screen.fill((40, 40, 40))
        
        # Render all cards
        for card in self.cards:
            self.renderer.render_card(card)
        
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


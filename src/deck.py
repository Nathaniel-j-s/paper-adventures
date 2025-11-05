"""
Deck class for managing collections of cards.
"""

import random


class Deck:
    """Manages a collection of cards."""
    
    def __init__(self, name="New Deck"):
        """
        Initialize an empty deck.
        
        Args:
            name: Name of the deck
        """
        self.name = name
        self.cards = []
    
    def add_card(self, card):
        """
        Add a card to the deck.
        
        Args:
            card: Card object to add
        """
        self.cards.append(card)
    
    def add_to_top(self, card):
        """
        Place a card on the top of the deck.
        The deck treats index 0 as the top for draws.
        
        Args:
            card: Card object to place on top
        """
        self.cards.insert(0, card)
    
    def remove_card(self, card):
        """
        Remove a card from the deck.
        
        Args:
            card: Card object to remove
        """
        if card in self.cards:
            self.cards.remove(card)
    
    def shuffle(self):
        """Shuffle the cards in the deck."""
        random.shuffle(self.cards)
    
    def draw_card(self):
        """
        Draw and remove the top card from the deck.
        
        Returns:
            Card object or None if deck is empty
        """
        if self.cards:
            return self.cards.pop(0)
        return None
    
    def draw_cards(self, count):
        """
        Draw multiple cards from the top of the deck.
        
        Args:
            count: Number of cards to draw
        
        Returns:
            List of Card objects
        """
        drawn = []
        for _ in range(min(count, len(self.cards))):
            card = self.draw_card()
            if card:
                drawn.append(card)
        return drawn
    
    def size(self):
        """Get the number of cards in the deck."""
        return len(self.cards)
    
    def is_empty(self):
        """Check if the deck is empty."""
        return len(self.cards) == 0
    
    def clear(self):
        """Remove all cards from the deck."""
        self.cards = []
    
    def __str__(self):
        return f"Deck({self.name}, {len(self.cards)} cards)"


"""
Save and load deck collections to/from JSON files.
"""

import json
import os


class DeckManager:
    """Handles persistence of deck collections."""
    
    def __init__(self, data_dir="data"):
        """
        Initialize the deck manager.
        
        Args:
            data_dir: Directory to store deck files
        """
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def save_deck(self, deck):
        """
        Save a deck to a JSON file.
        
        Args:
            deck: Deck object to save
        """
        from .card import Card
        
        # Prepare deck data
        deck_data = {
            "name": deck.name,
            "cards": []
        }
        
        for card in deck.cards:
            card_data = {
                "name": card.name,
                "card_type": card.card_type,
                "attributes": card.attributes,
                "x": card.x,
                "y": card.y,
                "face_up": card.face_up
            }
            deck_data["cards"].append(card_data)
        
        # Save to file
        filename = os.path.join(self.data_dir, f"{deck.name}.json")
        with open(filename, 'w') as f:
            json.dump(deck_data, f, indent=2)
    
    def load_deck(self, deck_name):
        """
        Load a deck from a JSON file.
        
        Args:
            deck_name: Name of the deck file (without .json extension)
        
        Returns:
            Deck object or None if file not found
        """
        from .deck import Deck
        from .card import Card
        
        filename = os.path.join(self.data_dir, f"{deck_name}.json")
        
        if not os.path.exists(filename):
            return None
        
        with open(filename, 'r') as f:
            deck_data = json.load(f)
        
        # Create deck
        deck = Deck(deck_data["name"])
        
        # Add cards
        for card_data in deck_data["cards"]:
            card_type = card_data.get("card_type", "Character")  # Default for backward compatibility
            card = Card(card_data["name"], card_type=card_type, **card_data["attributes"])
            card.set_position(card_data["x"], card_data["y"])
            card.face_up = card_data.get("face_up", True)
            deck.add_card(card)
        
        return deck
    
    def list_decks(self):
        """
        Get a list of all saved deck names.
        
        Returns:
            List of deck names
        """
        if not os.path.exists(self.data_dir):
            return []
        
        decks = []
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                deck_name = filename[:-5]  # Remove .json extension
                decks.append(deck_name)
        
        return decks
    
    def delete_deck(self, deck_name):
        """
        Delete a deck file.
        
        Args:
            deck_name: Name of the deck to delete
        
        Returns:
            True if deleted, False if not found
        """
        filename = os.path.join(self.data_dir, f"{deck_name}.json")
        if os.path.exists(filename):
            os.remove(filename)
            return True
        return False


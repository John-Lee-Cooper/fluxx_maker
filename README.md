# Fluxx Deck Maker #

This utility creates a printer ready images of cards for the game Fluxx.

![Fluxx](rsrc/fluxx.png)

### How it works ###

Currently, fluxx_maker reads in a template csv file,
where each row describes a card in three columns:
the card's Name, Type, and either a Description or (for a Keeper or Creeper type)
the name of an Image, or (for a Goal) the name of the required Keepers and Creepers.

![csv](csv.png)

flux_maker then uses the appropriate template for the card's Type,
and writes the Name at the top of the card 
and either writes the Description
or draws the card's Image
on the bottom of the card.

After flux_maker has written each card to the deck directory,
It copies 3 x 3 cards onto a printer-ready Page image,
generating as many Page images as necessary to print the entire deck.

![PageImage](rsrc/example_page.png)

### Todo ###

* Allow special powers to Keeper/Creeper cards.
* Allow unique images for Goal cards.
* Print a summary of Goals per Keeper/Creeper to aid in balancing the deck.

### How do I get set up? ###

```bash
python -m venv venv
pip install -r requirements.in
source venv/bin/activate

./flux_maker <input_directory>
```

### Written by ###

John Lee Cooper  
john.lee.cooper@gatech.edu
  

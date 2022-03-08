import os
from renderer.renderer import read_deck, read_library

import pytest

@pytest.mark.parametrize(
    "test_input,expected",
    [('unit_test/decks/happy/deck_3.txt', [('1', 'a'), ('1', 'b'), ('1', 'c')]), ('unit_test/decks/happy/deck_4.txt', [('1202020200202', 'sdmsfdopk'), ('6789789790', 'asjiasdidsa'), ('980898790', 'asjiasdi'), ('89078998999898', 'sadsadsasadkln'), ('877677667', 'biuashbuidsa'), ('87997898', 'sajiosdaioj')]), ('unit_test/decks/happy/deck_1.txt', [('1','adfasfdfsfddafdfafsd')]), ('unit_test/decks/happy/deck_2.txt', [('1', 'sdkmsa')]), ('unit_test/decks/happy/deck_0.txt', [('2', 'Healer Dork'), ('1', 'Regrowth'), ('12', 'Vicious Reaction'), ('2', 'Healer Dork'), ('1', 'Regrowth'), ('12', 'Vicious Reaction'), ('2', 'Healer Dork'), ('1', 'Regrowth'), ('12', 'Vicious Reaction'), ('2', 'Healer Dork'), ('1', 'Regrowth'), ('12', 'Vicious Reaction'), ('2', 'Healer Dork'), ('1', 'Regrowth'), ('12', 'Vicious Reaction'), ('2', 'Healer Dork'), ('1', 'Regrowth'), ('12', 'Vicious Reaction')])]
    )
def test_read_deck_happy(test_input, expected):
    assert read_deck(test_input) == expected

@pytest.mark.parametrize(
    "test_input", 
    ['unit_test/decks/wrong_regexp/deck_0.txt','unit_test/decks/wrong_regexp/deck_1.txt','unit_test/decks/wrong_regexp/deck_1.txt']
    )
def test_read_deck_wrong_regexp(test_input):
    with pytest.raises(ValueError):
        read_deck(test_input)

@pytest.mark.parametrize(
    "test_input", 
    ['unit_test/decks/empty/deck_0.txt']
    )
def test_read_deck_empty(test_input):
    with pytest.raises(ValueError):
        read_deck(test_input)


@pytest.mark.parametrize(
    "test_input", 
    ['unit_test/decks/wrong_regexp/deck_01212.txt','unit_test/decks/wrong_regexp/deck_1121.txt','unit_test/decks/wrong_regexp/...']
    )
def test_read_deck_file_not_found(test_input):
    with pytest.raises(FileNotFoundError):
        read_deck(test_input)

@pytest.mark.parametrize(
    "test_input", 
    ['unit_test/decks/wrong_regexp','unit_test/decks/happy','unit_test/decks']
    )
def test_read_deck_is_a_directory(test_input):
    with pytest.raises(IsADirectoryError):
        read_deck(test_input)


@pytest.mark.parametrize(
    "test_input", 
    ['unit_test/decks/wrong_regexp/deck_01212.txt','unit_test/decks/wrong_regexp/deck_1121.txt','unit_test/decks/wrong_regexp/...']
    )
def test_read_lib_file_not_found(test_input):
    with pytest.raises(FileNotFoundError):
        read_library(test_input)


@pytest.mark.parametrize(
    "test_input", 
    ['unit_test/decks/wrong_regexp/deck_0.txt','unit_test/decks/wrong_regexp/deck_1.txt','unit_test/decks/wrong_regexp/deck_1.txt']
    )
def test_read_lib_wrong_format(test_input):
    with pytest.raises(ValueError):
        read_library(test_input)

@pytest.mark.parametrize(
    "test_input", 
    ['unit_test/decks/wrong_regexp','unit_test/decks/happy','unit_test/decks']
    )
def test_read_lib_is_a_directory(test_input):
    with pytest.raises(IsADirectoryError):
        read_library(test_input)
@pytest.mark.parametrize(
    "test_input",
    ['unit_test/dataframes/empty/df_1.xlsx',
    'unit_test/dataframes/empty/df_1.csv',
    'unit_test/dataframes/empty/df_0.xlsx',
    'unit_test/dataframes/empty/df_0.csv'])
def test_read_lib_empty(test_input):
    with pytest.raises(ValueError):
        read_library(test_input)
@pytest.mark.parametrize(
    "test_input,expected",
    [('unit_test/dataframes/happy/df_1.xlsx', {'Healer Dork': {'ID': 5, 'Name': 'Healer Dork', 'Type': 'Creature', 'Qty': 2, 'Module': 'Nature', 'Cost': 1, 'Power': 1, 'Text': 'Whenever another permanent you control enters, gain 1 life.\nAction, tap, pay 1 life: gain 1 mana; Priority.', 'Image': 'https://99px.ru/sstorage/56/2013/06/10306130220478230.jpg', 'Tags': 'Heal, Mana, PayLife, Ability', 'Version_Tag': 1}}), ('unit_test/dataframes/happy/df_1.csv', {'Healer Dork': {'ID': '5', 'Name': 'Healer Dork', 'Type': 'Creature', 'Qty': '2', 'Module': 'Nature', 'Cost': '1', 'Power': '1', 'Text': 'Whenever another permanent you control enters, gain 1 life.\nAction, tap, pay 1 life: gain 1 mana; Priority.', 'Image': 'https://99px.ru/sstorage/56/2013/06/10306130220478230.jpg', 'Tags': 'Heal, Mana, PayLife, Ability', 'Version_Tag': '1'}}), ('unit_test/dataframes/happy/df_0.csv', {'Healer Dork': {'ID': '5', 'Name': 'Healer Dork', 'Type': 'Creature', 'Qty': '2', 'Module': 'Nature', 'Cost': '1', 'Power': '1', 'Text': 'Whenever another permanent you control enters, gain 1 life.\nAction, tap, pay 1 life: gain 1 mana; Priority.', 'Image': 'https://99px.ru/sstorage/56/2013/06/10306130220478230.jpg', 'Tags': 'Heal, Mana, PayLife, Ability', 'Version_Tag': '1'}, 'Regrowth': {'ID': '14', 'Name': 'Regrowth', 'Type': 'Action', 'Qty': '1', 'Module': 'Nature', 'Cost': '1', 'Power': '', 'Text': "Fuel -- return target card from your discard to your hand.\nChoose two (you can choose each mode multiple times):\n - return target card from any discard to it's owner's hand;\n - remove target card from any discard.", 'Image': 'https://c4.wallpaperflare.com/wallpaper/773/817/71/green-light-sake-girl-wallpaper-preview.jpg', 'Tags': 'Fuel, Recursion, Gravehate', 'Version_Tag': '3'}, 'Golem Liquidator': {'ID': '38', 'Name': 'Golem Liquidator', 'Type': 'Creature', 'Qty': '2', 'Module': 'Ice', 'Cost': 'X', 'Power': 'X+1', 'Text': 'During the upkeep, ~ gets +1 power.\nAction, kill ~: search for a Object with mana cost less than his power.', 'Image': '', 'Tags': 'Ability, PowerCounter, SearchToPlay', 'Version_Tag': '2'}, 'Vicious Reaction': {'ID': '50', 'Name': 'Vicious Reaction', 'Type': 'Object', 'Qty': '1', 'Module': 'Burn', 'Cost': '4', 'Power': '', 'Text': 'Double the damage dealt by cards you control.\nAction, tap: deal 1 damage to each opponent.', 'Image': '', 'Tags': 'DamageToOpponent, Ability, SpecialRule', 'Version_Tag': '1'}, 'Paincatcher': {'ID': '80', 'Name': 'Paincatcher', 'Type': 'Reaction', 'Qty': '2', 'Module': 'Veil', 'Cost': '1', 'Power': '', 'Text': 'Trigger: a player loses life.\nDraw that many cards.', 'Image': '', 'Tags': 'Draw', 'Version_Tag': '1'}, 'Thorn': {'ID': '73', 'Name': 'Thorn', 'Type': 'Action', 'Qty': '1', 'Module': 'Veil', 'Cost': '0', 'Power': '', 'Text': '~ deals 1 damage to any target.\nWhen a Creature dies, return ~ to hand.', 'Image': '', 'Tags': 'DamageToAny', 'Version_Tag': '5'}}), ('unit_test/dataframes/happy/df_0.xlsx', {'Healer Dork': {'ID': 5, 'Name': 'Healer Dork', 'Type': 'Creature', 'Qty': 2, 'Module': 'Nature', 'Cost': 1, 'Power': 1, 'Text': 'Whenever another permanent you control enters, gain 1 life.\nAction, tap, pay 1 life: gain 1 mana; Priority.', 'Image': 'https://99px.ru/sstorage/56/2013/06/10306130220478230.jpg', 'Tags': 'Heal, Mana, PayLife, Ability', 'Version_Tag': 1}, 'Regrowth': {'ID': 14, 'Name': 'Regrowth', 'Type': 'Action', 'Qty': 1, 'Module': 'Nature', 'Cost': 1, 'Power': '', 'Text': "Fuel -- return target card from your discard to your hand.\nChoose two (you can choose each mode multiple times):\n - return target card from any discard to it's owner's hand;\n - remove target card from any discard.", 'Image': 'https://c4.wallpaperflare.com/wallpaper/773/817/71/green-light-sake-girl-wallpaper-preview.jpg', 'Tags': 'Fuel, Recursion, Gravehate', 'Version_Tag': 3}, 'Golem Liquidator': {'ID': 38, 'Name': 'Golem Liquidator', 'Type': 'Creature', 'Qty': 2, 'Module': 'Ice', 'Cost': 'X', 'Power': 'X+1', 'Text': 'During the upkeep, ~ gets +1 power.\nAction, kill ~: search for a Object with mana cost less than his power.', 'Image': '', 'Tags': 'Ability, PowerCounter, SearchToPlay', 'Version_Tag': 2}, 'Vicious Reaction': {'ID': 50, 'Name': 'Vicious Reaction', 'Type': 'Object', 'Qty': 1, 'Module': 'Burn', 'Cost': 4, 'Power': '', 'Text': 'Double the damage dealt by cards you control.\nAction, tap: deal 1 damage to each opponent.', 'Image': '', 'Tags': 'DamageToOpponent, Ability, SpecialRule', 'Version_Tag': 1}, 'Paincatcher': {'ID': 80, 'Name': 'Paincatcher', 'Type': 'Reaction', 'Qty': 2, 'Module': 'Veil', 'Cost': 1, 'Power': '', 'Text': 'Trigger: a player loses life.\nDraw that many cards.', 'Image': '', 'Tags': 'Draw', 'Version_Tag': 1}, 'Thorn': {'ID': 73, 'Name': 'Thorn', 'Type': 'Action', 'Qty': 1, 'Module': 'Veil', 'Cost': 0, 'Power': '', 'Text': '~ deals 1 damage to any target.\nWhen a Creature dies, return ~ to hand.', 'Image': '', 'Tags': 'DamageToAny', 'Version_Tag': 5}})]
    )
def test_read_lib_happy(test_input, expected):
    assert read_library(test_input) == expected

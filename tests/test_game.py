import pytest
from game import Game
from app import create_app


def test_server_controls_positions_and_score():
    game = Game()
    identifier = game.join('Student')
    game.players[identifier]['x'],game.players[identifier]['y'] = 0,0
    game.coins.add((1,0))
    game.move(identifier,'left')
    assert game.players[identifier]['x'] == 0
    game.move(identifier,'right')
    assert game.players[identifier]['score'] == 1
    assert game.players[identifier]['x'] == 1
    assert len(game.coins) == 12
    game.move(identifier,'teleport')
    assert game.players[identifier]['x'] == 1


def test_room_capacity_and_cleanup():
    game = Game()
    ids = [game.join(str(i)) for i in range(8)]
    with pytest.raises(ValueError): game.join('Ninth')
    for identifier in ids: game.leave(identifier)
    assert not game.players
    assert create_app().test_client().get('/').status_code == 200

import sqlalchemy as sa

from data import db_session
from data.game import Game


def create_game(score, handicap, game_number, bowler_id):
    new_game = Game(score=score, handicap=handicap, game_number=game_number, bowler_id=bowler_id)
    session = db_session.create_session()

    try:
        session.add(new_game)
        session.commit()
        return new_game
    finally:
        session.close()


def modify_game(game_id, bowler_id=None, score=None, handicap=None, game_number=None):
    session = db_session.create_session()

    try:
        game = session.scalars(sa.select(Game).where(Game.id == game_id)).unique().one_or_none()
        if not game:
            return ""
        else:
            if bowler_id != "_":
                game.bowler_id = int(bowler_id)
            if score != "_" and score.isdigit():
                game.score = int(score)
            if handicap != "_" and handicap.isdigit():
                game.handicap = handicap
            if game_number != "" and game_number.isdigit():
                game.game_number = game_number
            session.commit()
            return game

    finally:
        session.close()


def delete_game(game_id):
    session = db_session.create_session()
    try:
        game = session.scalars(sa.select(Game).where(Game.id == game_id)).unique().one_or_none()
        if game:
            session.delete(game)
            session.commit()
            return True
        else:
            False
    finally:
        session.close()


def get_game_by_id(game_id):
    session = db_session.create_session()
    try:
        game = session.scalars(sa.select(Game).where(Game.id == game_id)).unique().one_or_none()
        return game
    finally:
        session.close()


def get_all_games():
    session = db_session.create_session()
    try:
        all_games = session.scalars(sa.Select(Game)).unique().all()
        return all_games
    finally:
        session.close()

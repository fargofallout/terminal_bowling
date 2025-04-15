import sqlalchemy as sa

from data import db_session
from data.bowler_head_to_head_game import Bowler_Head_To_Head_Game


def create_bowler_head_to_head_game(bowler_position=bowler_position,
                                    game_number=game_number,
                                    left_bowler_id=left_bowler_id,
                                    right_bowler_id=right_bowler_id,
                                    head_to_head_id=head_to_head_id,
                                    head_to_head_game_id=head_to_head_game_id):
    #CONTINUE HERE
    new_bowler_head_to_head_game = Bowler_Head_To_Head_Game(bowler_position=bowler_position,
                                                            game_number=game_number,
                                                            left_bowler_id=left_bowler_id,
                                                            right_bowler_id=right_bowler_id,
                                                            head_to_head_id=head_to_head_id,
                                                            head_to_head_game_id=head_to_head_game_id)
    session = db_session.create_session()

    try:
        session.add(new_bowler_head_to_head)
        session.commit()
        return new_bowler_head_to_head_game
    finally:
        session.close()


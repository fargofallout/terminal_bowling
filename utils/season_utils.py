import sqlalchemy as sa
import json

from data import db_session
from data.season import Season


def create_season(season_years, handicap_formula, league_id, games_per_week, players_per_team):
    # TODO: should I do this here, or should I do it before calling the function? I should probably do it before calling it, right? 
    formula_as_json = json.dumps(handicap_formula)
    print(f"this is the json version of the token list: {handicap_formula}")
    new_season = Season(season_years=season_years,
                        handicap_formula=formula_as_json,
                        league_id=league_id,
                        games_per_week=games_per_week,
                        players_per_team=players_per_team,
                        is_complete=False)
    session = db_session.create_session()

    try:
        session.add(new_season)
        session.commit()
        league_name = new_season.league.league_name
        return new_season
    finally:
        session.close()


def get_season_by_id(season_id):
    session = db_session.create_session()
    try:
        season = session.scalars(sa.select(Season).where(Season.id==season_id)).unique().one_or_none()
        return season
    finally:
        session.close()


def get_all_seasons():
    session = db_session.create_session()
    try:
        all_seasons = session.scalars(sa.select(Season).order_by(Season.id)).unique().all()
        return all_seasons
    finally:
        session.close()


def update_season(season_id, season_timeframe=None, handicap_formula=None, league_id=None, games_per_week=None, players_per_team=None):
    session = db_session.create_session()
    try:
        season = session.scalars(sa.select(Season).where(Season.id == season_id)).unique().one_or_none()
        if season_timeframe:
            season.season_years = season_timeframe
            session.commit()
            return season
        elif handicap_formula:
            season.handicap_formula = handicap_formula
            session.commit()
            return season
        elif league_id:
            season.league_id = league_id
            league_name = season.league.league_name
            session.commit()
            return season
        elif games_per_week:
            season.games_per_week = games_per_week
            session.commit()
            return season
        elif players_per_team:
            season.players_per_team = players_per_team
            session.commit()
            return season
    finally:
        session.close()


def delete_season(season_id):
    session = db_session.create_session()
    try:
        season = session.scalars(sa.select(Season).where(Season.id == season_id)).unique().one_or_none()
        if season:
            session.delete(season)
            session.commit()
            return True
        else:
            return False
    finally:
        session.close()


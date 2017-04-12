# Ceopardy
# https://github.com/obilodeau/ceopardy/
#
# Olivier Bilodeau <olivier@bottomlesspit.org>
# Copyright (C) 2017 Olivier Bilodeau
# All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
from enum import Enum

from flask import current_app as app

from ceopardy import db
from config import NB_TEAMS, CATEGORIES_PER_GAME, QUESTIONS_PER_CATEGORY

# TODO save a game in progress
# TODO load a game in progress
# TODO refactor to GameModel?
class Game():
    def __init__(self):
        self.config = {
            'NB_TEAMS': NB_TEAMS
        }
        self.state = GameState.uninitialized
        self.teams = []


    def setup(self, teamnames):
        if self.state is GameState.uninitialized:
            self.teams = [Team(team) for team in teamnames]
            self.state = GameState.setup
        else:
            raise GameProblem("Trying to setup a game that is already started")



    def start(self):
        if self.state is GameState.setup:
            self.state = GameState.started
            return True
        else:
            raise GameProblem("Trying to start a game that isn't ready to start")


    def get_team_stats(self):
        return [{team.name: team.score} for team in self.teams]

    # TODO randomly pick a team


class GameState(Enum):
    uninitialized = 0
    setup = 1
    started = 2


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    handicap = db.Column(db.Integer)

    def __init__(self, name, handicap=0):
        self.name = name
        self.handicap = handicap
        app.logger.debug("Team created: name is {}, handicap is {}"
                         .format(self.name, self.handicap))

    def __repr__(self):
        return '<Team %r>' % self.name


class GameBoard():
    def __init__(self):
        self.config = {
            'CATEGORIES_PER_GAME': CATEGORIES_PER_GAME,
            'QUESTIONS_PER_CATEGORY': QUESTIONS_PER_CATEGORY
        }
        self.questions = []
        for column in range(CATEGORIES_PER_GAME):
            l = []
            for row in range(QUESTIONS_PER_CATEGORY):
                question = Question("Nothing!", (row + 1) * 100, [row + 1, column + 1])
                l.append(question)
            self.questions.append(l)
        self.categories = []
        for column in range(CATEGORIES_PER_GAME):
            category = Category("This is C%d" % (column + 1), column + 1)
            self.categories.append(category)


class Category():
    def __init__(self, value, column):
        self.value = value
        self.column = column


class Question():
    def __init__(self, value, amount, coordinates):
        self.value = value
        self.amount = amount
        self.coordinates = coordinates
        self.solved = False


class GameProblem(Exception):
    pass

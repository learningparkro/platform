import logging
from django.utils.translation import ugettext_noop
from wouso.core.scoring.models import *
from wouso.core.user.models import Player
from wouso.core.god import God
from wouso.interface.activity import signals

class NotSetupError(Exception): pass
class InvalidFormula(Exception): pass
class FormulaParsingError(Exception): pass
class InvalidScoreCall(Exception): pass

CORE_POINTS = ('points',)

#def __init__(self):
#    if not Scoring.check_setup():
#        raise NotSetupError('Please setup the Scoring Module, using '+
#        '\n\t'+'python core/scoring/default_setup.py')

def check_setup():
    """ Check if the module has been setup """
    
    if Coin.get('points') is None:
        return False
    return True

def setup():
    """ Prepare database for Scoring """
    for cc in CORE_POINTS:
        if not Coin.get(cc):
            Coin.add(cc, name=cc)
    
    # iterate through games and register formulas
    for game in get_games():
        for formula in game.get_formulas():
            if not Formula.get(formula.id):
                Formula.add(formula)

def calculate(formula, **params):
    """ Calculate formula """
    formula = Formula.get(formula)
    if formula is None:
        raise InvalidFormula(formula)
    
    ret = {}
    try:    
        frml = formula.formula.format(**params)
        # Apparently, Python does not allow assignments inside eval
        # Using this workaround for now
        ass = frml.split(',')
        for a in ass:
            asp = a.split('=')
            coin = asp[0].strip()
            expr = '='.join(asp[1:])
            result = eval(expr)
            ret[coin] = result
    except Exception as e:
        raise FormulaParsingError(e)
        
    return ret
    
def score(user, game, formula, external_id=None, **params):
    ret = calculate(formula, **params)

    if isinstance(ret, dict):
        for coin, amount in ret.items():
            score_simple(user, coin, amount, game, formula, external_id)

def score_simple(player, coin, amount, game=None, formula=None,
    external_id=None):

    if not isinstance(game, Game):
        game = game.get_instance()

    if not isinstance(player, Player):
        raise InvalidScoreCall()

    user = player.user

    coin = Coin.get(coin)
    formula = Formula.get(formula) 

    hs = History.objects.create(user=user, coin=coin, amount=amount,
        game=game, formula=formula, external_id=external_id)

    # update user.points asap
    if coin.name == 'points':
        player.points += amount
        level = God.get_level_for_points(player.points)
        if level != player.level_no:
            if level < player.level_no:
                signal_msg = ugettext_noop("{user} downgraded to level {level}")
            else:
                signal_msg = ugettext_noop("{user} upgraded to level {level}")

            signals.addActivity.send(sender=None, user_from=player,
                                 user_to=player, message=signal_msg,
                                 arguments=dict(user=player, level=level),
                                 game=game)
            player.level_no = level
        player.save()

    logging.debug("Scored %s with %f %s" % (user, amount, coin))
    return hs

def history_for(user, game, external_id=None, formula=None, coin=None):
    fltr = {}
    if external_id:
        fltr['external_id'] = external_id
    if formula:
        fltr['formula'] = Formula.get(formula)
    if coin:
        fltr['coin'] = Coin.get(coin)
    
    if not isinstance(game, Game):
        game = game.get_instance()
    
    if not isinstance(user, User):
        user = user.user
        
    try:
        return History.objects.filter(user=user, game=game, **fltr)
    except History.DoesNotExist:
        return None
        
def user_coins(user):
    """ Returns a dictionary with user coins """
    if not isinstance(user, User):
        user = user.user
    return History.user_coins(user)

def sync_user(player):
    """ Synchronise user points with database
    """
    coin = Coin.get('points')
    result = History.objects.filter(user=player.user,coin=coin).aggregate(total=models.Sum('amount'))
    points = result['total'] if result['total'] is not None else 0
    if player.points != points:
        logging.debug('%s had %d instead of %d points' % (player, player.points, points))
        player.points = points
        player.level_no = God.get_level_for_points(player.points)
        player.save()

def sync_all_user_points():
    for player in Player.objects.all():
        sync_user(player)
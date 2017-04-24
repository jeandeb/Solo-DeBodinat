from soccersimulator.strategies  import Strategy
from soccersimulator.mdpsoccer import SoccerTeam, Simulation, SoccerAction
from soccersimulator.gui import SimuGUI,show_state,show_simu
from soccersimulator.utils import Vector2D
from soccersimulator import golf


GAME_WIDTH = 150 # Longueur du terrain
GAME_HEIGHT = 90 # Largeur du terrain
GAME_GOAL_HEIGHT = 10 # Largeur des buts
PLAYER_RADIUS = 1. # Rayon d un joueur
BALL_RADIUS = 0.65 # Rayon de la balle
MAX_GAME_STEPS = 2000 # duree du jeu par defaut
maxPlayerSpeed = 1. # Vitesse maximale d un joueur
maxPlayerAcceleration = 0.2 # Acceleration maximale
maxBallAcceleration = 5 # Acceleration maximale de la balle

class properties( object ):
    def __init__( self,state,idteam,idplayer ):
        self.state = state
        self.key = ( idteam, idplayer )
        if self.key[0] == 1 : 
            self.owngoal =  Vector2D( 0, GAME_HEIGHT/2 )
            self.adgoal =  Vector2D( GAME_WIDTH, GAME_HEIGHT/2. )
        else : 
            self.adgoal =  Vector2D( 0, GAME_HEIGHT/2 )
            self.owngoal =  Vector2D( GAME_WIDTH, GAME_HEIGHT/2. )
        self.my_position =  self.state.player_state( self.key[0], self.key[1] ).position
        self.ball_position = self.state.ball.position
        self.ball_vitesse = self.state.ball.vitesse
        self.my_vitesse =  self.state.player_state( self.key[0], self.key[1] ).vitesse

    @property
    def pos_x( self ):
        return self.my_position.x

    @property
    def pos_y( self ):
        return self.my_position.y

    @property
    def vector_ball( self ) :
        return  self.ball_position - self.my_position

    def passe( self,p ):
        
        dir_conduite = p - self.my_position
        angle_con = dir_conduite.angle
        norm = dir_conduite.norm / 2

        return SoccerAction( Vector2D( ), Vector2D( angle = angle_con, norm = norm ) )
    
    @property
    def ball_move( self ):
        return self.state.ball.vitesse.x > 0 or self.state.ball.vitesse.y > 0  

    def go( self,p ):
        dist_p = p - self.my_position
        if dist_p.norm < 1:
            return SoccerAction( Vector2D( ),Vector2D( ) )
        return SoccerAction( p - self.my_position,Vector2D( ) )

    @property    
    def go_ball( self ) : 
        return SoccerAction( self.vector_ball,Vector2D( ) )

    @property
    def ball_center( self ):
        if self.ball_position.x == GAME_WIDTH/2 and self.ball_position.y == GAME_HEIGHT/2 :
            return True
        return False

    @property
    def can_shoot( self ) :
        if ( self.vector_ball ).norm >= PLAYER_RADIUS + BALL_RADIUS:
                return False
        return True

    def is_in_rect( self, p ) :
    	position = p - self.ball_position
        if position.norm >= 3 or self.ball_vitesse >= 0.01 :
                return False
        return True

    def in_rect( self, p ) :
    	position = p - self.ball_position
        if position.norm >= 5 :
                return False
        return True

    @property
    def shoot_goal( self ):
        vector_shoot = self.adgoal - self.my_position
        return SoccerAction( Vector2D( ), vector_shoot.normalize()*2 )

    def conduire( self, point_direction, norm ):

        dir_conduite = point_direction - self.my_position
        angle_con = dir_conduite.angle

        if not self.can_shoot : 
           return self.go_ball
        return SoccerAction( Vector2D( ), Vector2D( angle = angle_con, norm = norm ) )

	@property
	def anticipe_dir(self): #Anticipe la direction de la balle 
		return self.vector_ball + 15*self.ball_vitesse

    @property
    def go_anticipe_ball( self ) : 
        return SoccerAction( self.anticipe_dir, Vector2D() ) 
        
    def anticipe_ball(self,rayon):
        if self.ball_vitesse.norm > rayon : 
            return self.go_anticipe_ball
        return self.go_ball

	



class GolfStrategy( Strategy ) : 
    def __init__( self ):

    	self.i = 0
        Strategy.__init__( self, "Golf" )
        

    def compute_strategy( self, state, id_team, id_player ):
  		

  		prop = properties(state,id_team,id_player)
  		zones = state.get_zones( id_team )

  		if self.i >= len(zones) : 
  			return prop.shoot_goal + prop.go_ball

  		zone_pos = zones[self.i].position + Vector2D( zones[self.i].l, zones[self.i].l )/2


  		if (zone_pos - prop.ball_position).norm < 10 : 
  			return SoccerAction( Vector2D(), Vector2D() )

  		elif not prop.is_in_rect( zone_pos ) : 
  			return prop.conduire( zone_pos, 0.5 ) 
    	
  		elif self.i <= len(zones)-1:
  			self.i = self.i + 1

 
		return SoccerAction( Vector2D(), Vector2D() )


class StaticStrategy( Strategy ) : 
    def __init__( self ):

        Strategy.__init__( self, "Random" )

    def compute_strategy( self, state, id_team, id_player ):
  
        return SoccerAction( Vector2D(), Vector2D() )



class SlalomStrategy( Strategy ) : 
    def __init__( self ):

    	self.i = 0
        Strategy.__init__( self, "Golf" )
        
     
    def compute_strategy( self, state, id_team, id_player ):
  		

  		prop = properties(state,id_team,id_player)
  		zones = state.get_zones( id_team )

  		if self.i >= len(zones) : 
  			return prop.shoot_goal + prop.go_ball


  		zone_pos = zones[self.i].position + Vector2D( zones[self.i].l, zones[self.i].l )/2

  		if not prop.is_in_rect( zone_pos ) : 
  			return prop.conduire( zone_pos, 0.5 ) 
    	
  		elif self.i <= len(zones):
  			self.i = self.i + 1

		return prop.go_ball


















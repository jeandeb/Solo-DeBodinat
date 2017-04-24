from soccersimulator.mdpsoccer import SoccerTeam, Simulation, SoccerAction
import tools


def get_golf_team( i ):

    Jean = GolfTeam( name = "Jean"  )

    Jean.add( "Cavani", strategy.GolfStrategy( ) ) 
   
    return Jean
    
def get_slalom_team( i ):
    
    Jean = GolfTeam( name = "Jean"  )

    Jean.add( "Cavani", strategy.SlalomStrategy( ) ) 
   
    return Jean
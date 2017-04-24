import tools
import strategy
from soccersimulator import golf

team1 = strategy.SoccerTeam( name = "AS FORBACH" ,login = "etu1" )
team2 = strategy.SoccerTeam( name = "MFC", login = "etu2" )

team1.add( "Woods", tools.GolfStrategy() )
team2.add( "Rien", tools.StaticStrategy() )

simu = golf.Parcours4( team1=team1, vitesse = 0.01 )
#Jouer et afficher la partie
strategy.show_simu( simu )
#Jouer sans afficher
simu.start( )


import random
import uuid

SIZE = 20
COLORS = ['#2859d9','#e65c2b','#8a43c5','#16815d','#bc3168','#bd8909','#24909b','#545875']


class Game:
    def __init__(self):
        self.players = {}
        self.coins = set()
        self.refill_coins()

    def refill_coins(self):
        occupied = {(p['x'],p['y']) for p in self.players.values()}
        available = [(x,y) for x in range(SIZE) for y in range(SIZE) if (x,y) not in self.coins and (x,y) not in occupied]
        random.shuffle(available)
        self.coins.update(available[:max(0,12-len(self.coins))])

    def join(self, name):
        if len(self.players) >= 8:
            raise ValueError('Room is full (eight players).')
        identifier = uuid.uuid4().hex[:12]
        occupied = {(p['x'],p['y']) for p in self.players.values()}
        free = [(x,y) for x in range(SIZE) for y in range(SIZE) if (x,y) not in occupied and (x,y) not in self.coins]
        x,y = random.choice(free)
        self.players[identifier] = {'name':name[:20] or 'Player','x':x,'y':y,'score':0,'color':COLORS[len(self.players)]}
        return identifier

    def move(self, identifier, direction):
        player = self.players[identifier]
        directions = {'up':(0,-1),'down':(0,1),'left':(-1,0),'right':(1,0)}
        if not isinstance(direction,str) or direction not in directions:
            return
        dx,dy = directions[direction]
        x = max(0,min(SIZE-1,player['x']+dx))
        y = max(0,min(SIZE-1,player['y']+dy))
        if any(p['x']==x and p['y']==y for key,p in self.players.items() if key!=identifier):
            return
        player['x'],player['y'] = x,y
        if (x,y) in self.coins:
            self.coins.remove((x,y))
            player['score'] += 1
            self.refill_coins()

    def leave(self, identifier):
        self.players.pop(identifier,None)

    def snapshot(self, identifier):
        return {'you':identifier,'size':SIZE,'players':self.players,'coins':sorted(self.coins)}

# Real-Time Multiplayer Game notes

A multiplayer game where players collect coins in the same room.

I used WebSockets to send player positions between the server and browsers. A lock keeps shared game state consistent when players move at the same time.

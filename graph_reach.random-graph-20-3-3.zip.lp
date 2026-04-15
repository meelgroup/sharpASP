{ in(X) } :- node(X).

reached(1) :- in(1).
reached(Y) :- in(Y), reached(X), edge(X,Y).

first(X) :- X = #min { Y: node(Y) }.
last(X) :- X = #max { Y: node(Y) }.
:- last(X), not reached(X).
:- first(X), not reached(X). 


% Display
#show in/1.
#show reached/1.
#show first/1.
#show last/1.


node(1).
node(2).
node(3).
node(4).
node(5).
node(6).
node(7).
node(8).
node(9).
node(10).
node(11).
node(12).
node(13).
node(14).
node(15).
node(16).
node(17).
node(18).
node(19).
node(20).
edge(1, 15).
edge(15, 1).
edge(19, 1).
edge(2, 3).
edge(9, 2).
edge(17, 2).
edge(3, 2).
edge(6, 3).
edge(16, 3).
edge(4, 12).
edge(10, 4).
edge(17, 4).
edge(5, 9).
edge(7, 5).
edge(10, 5).
edge(6, 18).
edge(13, 6).
edge(7, 6).
edge(7, 16).
edge(11, 7).
edge(18, 7).
edge(8, 17).
edge(7, 8).
edge(13, 8).
edge(9, 19).
edge(2, 9).
edge(7, 9).
edge(10, 4).
edge(12, 10).
edge(6, 10).
edge(11, 6).
edge(6, 11).
edge(8, 11).
edge(12, 7).
edge(6, 12).
edge(9, 12).
edge(13, 16).
edge(2, 13).
edge(15, 13).
edge(14, 12).
edge(1, 14).
edge(2, 14).
edge(15, 12).
edge(13, 15).
edge(3, 15).
edge(16, 8).
edge(4, 16).
edge(18, 16).
edge(17, 20).
edge(6, 17).
edge(2, 17).
edge(18, 11).
edge(5, 18).
edge(19, 18).
edge(19, 10).
edge(1, 19).
edge(3, 19).
edge(20, 8).
edge(10, 20).
edge(12, 20).

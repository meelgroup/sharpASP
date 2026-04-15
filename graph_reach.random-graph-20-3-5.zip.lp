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
edge(1, 11).
edge(18, 1).
edge(17, 1).
edge(2, 16).
edge(8, 2).
edge(10, 2).
edge(3, 4).
edge(7, 3).
edge(8, 3).
edge(4, 12).
edge(6, 4).
edge(20, 4).
edge(5, 8).
edge(13, 5).
edge(14, 5).
edge(6, 9).
edge(3, 6).
edge(4, 6).
edge(7, 4).
edge(20, 7).
edge(16, 7).
edge(8, 3).
edge(2, 8).
edge(7, 8).
edge(9, 15).
edge(14, 9).
edge(18, 9).
edge(10, 18).
edge(11, 10).
edge(14, 10).
edge(11, 13).
edge(14, 11).
edge(10, 11).
edge(12, 19).
edge(3, 12).
edge(2, 12).
edge(13, 19).
edge(18, 13).
edge(15, 13).
edge(14, 3).
edge(13, 14).
edge(16, 14).
edge(15, 8).
edge(5, 15).
edge(16, 15).
edge(16, 14).
edge(6, 16).
edge(19, 16).
edge(17, 7).
edge(5, 17).
edge(1, 17).
edge(18, 3).
edge(2, 18).
edge(17, 18).
edge(19, 12).
edge(18, 19).
edge(1, 19).
edge(20, 19).
edge(4, 20).
edge(5, 20).

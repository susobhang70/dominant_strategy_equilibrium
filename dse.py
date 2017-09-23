#!/usr/bin/python
import sys
if len(sys.argv) < 2:
    print "Please pass the name of the game file to be analyzed"

f = open(sys.argv[1], "r")
gameinfo = f.readline()
data = f.readline().split(" ")
data = data[data.index("{") + 1: data.index("}\n")]
data = data[data.index("{") + 1:]
num_players = len(data)
strategies = map(int, data)
multiplier = []
temp = 1
for i in range(len(strategies)):
    multiplier.append(temp)
    temp = temp * strategies[i]

f.readline()
data = f.readline().split(" ")
# print data
gamedata = map(float, data)

def intersect(a, b):
    return list(set(a) & set(b))

def sel_index(player, args):
    result = 0
    i = 0
    # print "Args ", args
    for arg in args:
        result = result + (arg * multiplier[i])
        i = i + 1
    result = result * num_players
    result += player
    return result

def find_strongly_dominant_eq(playerno, totalplayer, topplayer, strategyarr = [], eqindex = -1):
    if(len(totalplayer) >= 1):
        cur_player = totalplayer[0]
        temp = 0
        totalplayer = totalplayer[1:]
        for strategy in range(strategies[cur_player]):
            # print "First eqindex ", eqindex
            temparray = strategyarr[:]
            # print "Tempar ", temparray
            temparray.append(strategy)
            temp = find_strongly_dominant_eq(playerno, totalplayer, topplayer, temparray, eqindex)
            # print "Temp value ", temp
            if( temp == -sys.maxint):
                return temp
            else:
                eqindex = temp

        return temp

    else:
        # print "Eqindex ", eqindex
        max_payoff = -sys.maxint
        max_index = -1
        other_payoffs = []
        other_index = []
        for strategy in range(strategies[playerno]):
            temp1 = strategyarr[:]
            # print "T1 ", temp1
            temp1.insert(playerno, strategy)
            cur_payoff = gamedata[sel_index(playerno, temp1)]
            if( max_payoff < cur_payoff):
                max_payoff = cur_payoff
                max_index = strategy
            else:
                other_payoffs.append(cur_payoff)
                other_index = strategy
        if(max_payoff in other_payoffs):
            return -sys.maxint
        if( eqindex == -1 ):
            eqindex = max_index
        elif( eqindex != max_index ):
            return -sys.maxint
        return eqindex

def find_weakly_dominant_eq(playerno, totalplayer, topplayer, eqindex, strategyarr = []):
    if(len(totalplayer) >= 1):
        cur_player = totalplayer[0]
        temp = 0
        totalplayer = totalplayer[1:]
        for strategy in range(strategies[cur_player]):
            # print "First eqindex ", eqindex
            temparray = strategyarr[:]
            # print "Tempar ", temparray
            temparray.append(strategy)
            temp, eqindex = find_weakly_dominant_eq(playerno, totalplayer, topplayer, eqindex, temparray)
            # print "Temp value ", temp
            if( temp == -sys.maxint):
                return temp, eqindex

        return temp, eqindex

    else:
        # print "Eqindex ", eqindex
        max_payoff = -sys.maxint
        other_payoffs = []
        max_index = []
        for strategy in range(strategies[playerno]):
            temp1 = strategyarr[:]
            # print "T1 ", temp1
            temp1.insert(playerno, strategy)
            cur_payoff = gamedata[sel_index(playerno, temp1)]
            if( max_payoff < cur_payoff):
                max_payoff = cur_payoff
                max_index = []
                max_index.append(strategy)
            elif max_payoff == cur_payoff:
                max_index.append(strategy)
        if eqindex[0] == -1:
            eqindex = max_index
        else:
            temp_index = intersect(eqindex, max_index)
            eqindex = temp_index[:]
        if not eqindex:
            return -sys.maxint, eqindex
        else:
            return eqindex[0], eqindex

def print_weak(indexes, valueindexes = [], start = 0):
    if start < num_players - 1:
        for i in indexes[start]:
            tempvalues = valueindexes[:]
            tempvalues.append(i)
            print_weak(indexes, tempvalues, start + 1)

    else:
        for i in indexes[start]:
            tempresult = valueindexes[:]
            tempresult.append(i)
            for v in tempresult:
                print v, 
            print
        print


# print find_strongly_dominant_eq(0, [1, 2], 1)

playerslist = list(xrange(num_players))
return_value = -1
strong_eq = []
for i in range(num_players):
    tempplayerlist = playerslist[:]
    tempplayerlist.remove(i)
    # print i, tempplayerlist, tempplayerlist[0]
    value = find_strongly_dominant_eq(i, tempplayerlist, tempplayerlist[0])
    if value == -sys.maxint:
        print "No Strongly Dominant Strategy equilibrium exists"
        return_value = 0
        break
    else:
        strong_eq.append(value)

if return_value == -1:
    print "Strongly dominant strategy equilibrium (in order of P1, P2, ... ,Pn) is (0 based indexing):",
    for i in strong_eq:
        print i, 

else:
    min_eq_list = []
    for i in range(num_players):
        tempplayerlist = playerslist[:]
        tempplayerlist.remove(i)
        result_index = [-1]
        value, result_index = find_weakly_dominant_eq(i, tempplayerlist, tempplayerlist[0], result_index)
        if value == -sys.maxint or len(result_index) == strategies[i]:
            print "No Weakly Dominant Strategy equilibrium exists as well"
            return_value = -2
            break
        else:
            min_eq_list.append(result_index)

    if return_value != -2:
        print "Weakly dominant strategy equilibrium(s) is (are) (0 based indexing): "
        print_weak(min_eq_list)
        # print min_eq_list

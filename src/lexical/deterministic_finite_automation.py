from hashlib import new

from sqlalchemy import false
from src.lexical.finite_automation import FA
from src.lexical.state import State

class DFA(FA):

    @staticmethod
    def init_by_fa(fa: FA):  # TODO:根据FA构造最小DFA
        return dfa_minimize(
            fa_2_dfa(fa))


# def epsilon_closure(s0:State): #传进：初始状态s0；返回：一个由s0的epsilon闭包组成的状态集合
#     return s0.epsilonTransitions
#     pass

def epsilon_closure_Move (I: list, letter: str, fa: FA):  # 将集合I转为J=move(I,letter)，再转为Ia=epsilon_closure{j}
    J = []
    I_letter = []
    for state in I:          #move动作
        key = (state, str)
        if (fa.f[key] != None):
            J.append(fa.f[key])

    for state in J:          #得到Ia
        for state_2 in state.epsilonTransitions:
            if not (I_letter.__contains__(state_2)):
                I_letter.append[state_2]

    return I_letter
    pass



def fa_2_dfa(fa: FA) -> DFA:  # NFA确定化
    ListOfNewStateList = []
    dict1 = {}
    state =  State(False)    
    Allstate = state.get_state_all    #get_state_all是不是改成静态方法好点？
    
    
    for state1 in Allstate:
     if(fa.s == state1.get_flag):
      S0 = state1

    for letter in fa.letters:
      SL=epsilon_closure_Move(S0.epsilonTransitions,letter,fa)
      ListOfNewStateList.append(SL)
      state2 = State(false)
      dict1[SL]=state2
      
    
    for StateList in ListOfNewStateList:
      for letter in fa.letters:    
        if not (ListOfNewStateList.__contains__(epsilon_closure_Move(StateList, letter, fa))):
          ListOfNewStateList.append(epsilon_closure_Move(StateList, letter, fa))

          dict()
    
    for StateList in ListOfNewStateList:
    NewState = StateList 
    
    
    return Dfa
    pass



def dfa_minimize(dfa) -> DFA:  # DFA最小化
    # 1.区分初态和末态，各分为一个集合

    # 2.判断集合是否可“区分”

    # 3.对两个集合根据是否可再分继续划分集合，直到不可再划分为止

    pass  

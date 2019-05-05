# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 10:22:33 2019

@author: belbert
"""

def contains(entry,tupleList):
    for tL in tupleList: # iterate over list of tuples
        matched = 1
        for t in tL: # iterate over tuple items
            if t not in entry:
                matched = 0
                break
        if matched==1:
            return True
    return False # did not find a match

def generate_keys(Fkeys,F1_keys,curr_k):
    C = []
    for i in range(len(Fkeys)):
        for j in range(len(F1_keys)):
            poss_C = tuple(set([Fk for Fk in Fkeys[i]]+[F1k for F1k in F1_keys[j]])) # Will always create sorted list of items (useful for downward closure checks later)
            if len(poss_C)==curr_k+1:
                    C.append(poss_C)

    midC = [list(set(c)) for c in C]
    C = []
    for m in midC:
        if m not in C:
            C.append(m)
    C = [tuple(c) for c in C]
    return C


class Apriori(object):
    def __init__(self):
        self.DataList = []  # DataList expects elements of form [item1,item2,...itemZ]
        self.kLengthSets = {} # Placeholder for kLengthSets generated with support = S; will build dict of form {support0: ItemSets, support1: ItemSets}
        self.ItemCounts = {}
        
    def addEntry(self,entry):
        if not(isinstance(entry,list)):
            raise Exception("DataList can only be given list entries; please pass in a non-empty list.")
        
        if len(entry) == 0:
            raise Exception("DataList can only be given list entries; please pass in a non-empty list.")
            
        self.DataList.append(entry)
        for item in entry:
            self.ItemCounts[item] = self.ItemCounts.get(item,0) + 1
        
    def validate(self):
        valid=True
        if not(isinstance(self.DataList,list)):
            return False
        if len(self.DataList) > 0:
            for d in self.DataList:
                if not(isinstance(d,list)):
                    valid=False
                    return valid
            return valid
        else:
            return valid
        
    def kLengthSet(self,support):
        if not(self.validate()):
            print("There appears to be an issue with self.DataList...")
        else:
            # Generate Length-1 list
            self.kLengthSets[support] = {}
            F = {tuple([item]):self.ItemCounts[item] for item in self.ItemCounts.keys() if self.ItemCounts[item] >= support}
            F1_keys = list(F.keys()) # Need list of Length-1 supported items for Add-1 building of sets
            Fkeys = list(F.keys())
            if len(Fkeys) > 0:
                self.kLengthSets[support][1] = {'items':F, 'entries':[d for d in self.DataList if contains(d,Fkeys)]}
                curr_k = 1
                C = generate_keys(Fkeys, F1_keys, curr_k)
                C_counts = {}
                for entry in self.kLengthSets[support][curr_k]['entries']:
                    for poss_F in C:
                        if contains(entry,[poss_F]):
                            C_counts[poss_F] = C_counts.get(poss_F,0)+1
                # Create, if exists, Length-2 list, enter loop
                F = {item:C_counts[item] for item in C_counts.keys() if C_counts[item] >= support}
                while bool(F):
                    Fkeys = list(F.keys())
                    curr_k += 1
                    if curr_k % 10 == 0:
                        print("Made it through Length-"+str(curr_k)+" item sets...")
                    self.kLengthSets[support][curr_k] = {'items':F, 'entries':[d for d in self.kLengthSets[support][curr_k-1]['entries'] if contains(d,Fkeys)]}
                    C = generate_keys(Fkeys, F1_keys, curr_k)
                    C_counts = {}
                    for entry in self.kLengthSets[support][curr_k]['entries']:
                        for poss_F in C:
                            if contains(entry,[poss_F]):
                                C_counts[poss_F] = C_counts.get(poss_F,0)+1
                    
                    # Create, if exists, Length-k+1 list, continue loop
                    F = {item:C_counts[item] for item in C_counts.keys() if C_counts[item] >= support}
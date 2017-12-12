from Bio import Phylo
with open('/home/bwsq/Downloads/draftversion4.tre','r') as f:
    GiantFuckoffTree=Phylo.parse(f,'newick').__next__()
    
tree={}
duplicates={}
for clade in GiantFuckoffTree.find_clades():
        if clade.name:
            n=' '.join(clade.name.split('_')[:-1])
            if n in tree:
                if n in duplicates:
                    duplicates[n].append(clade)
                else:
                    duplicates[n]=[clade]
            else:
                tree[n]=clade
                
def _subclades(clade,depth):
    if clade.name:
        n=' '.join(clade.name.split('_')[:-1])
    else:
        n=None
    ret=Phylo.BaseTree.Clade(name=n,confidence=clade.count_terminals())
        
    if depth:
        for c in clade:
            ret.clades.append(_subclades(c,depth-1))
    return ret
def subclades(name,depth):
    ret=Phylo.BaseTree.Tree()
    ret.root.clades.append(_subclades(tree[name],depth))
    return ret


    


def placetree(terminalpositions,rootposition,tree):
    terms=tree.get_terminals()
    if len(terminalpositions)!=len(terms):
        raise IndexError('need'+str(len(terms))+'terminal positions, only got '+str(len(terminalpositions)))
    depths=tree.depths(unit_branch_lengths=True)
    pos={}
    termpos=iter(terminalpositions)
    for t in terms:
        pos[t]=next(termpos)
    for t in reversed(list(tree.find_clades(order='level'))):
        p=tree.get_path(t)
        if len(p)<=1:
            parent=tree.root
        else:
            parent=p[-2]
        if parent not in pos:
            siblings=parent.clades
            centroid=sum(pos[s] for s in siblings)*(1/len(siblings))
            ray=rootposition-centroid
            pos[parent]=ray*(1/depths[t])+centroid
    return pos
    

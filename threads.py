def Ropeify(tree):
    ''' generative rope texture.  given a vector path (x,y,theta)(t) and a thickness, or number of strands, 
                                                     _______2
    ok. i want the strands to branch off. 0========1<
                                                     \
                                                      -------3
    so at node 1, we know how many subbranches there are (2) so that tells us the thickness from 1-2. working up from tips
    
    think in terms of threads. there we are.
    one thread per terminal. might end up looking cluttered, we might join threads into larger threads in a bundle as we traverse the tree (less random orientation/tangling)
    
    !!flyaways.  occasionally, theres a chance of a new thread being created
    
    traverse the tree.
        at terminal: new thread
                    draw thread to parent (base path plus jitter)
        at node: connect
    
def postorder(clade):
    for subclade in clade:
        p=postorder(subclade)
        for i in p:
            yield i
    yield clade

class Thread():
    def __init__(here,theta):
        self.here=here
        self.theta=theta
        self.paths=[]
    def append(basepath,jitter):
        for i in segmentation:
            self.paths.append(PrettyPath(self.here,self.theta, blay blay
for node in postorder(phylotree):
    if node._is_terminal:
        #new thread
        threads[node]=Thread()
    for thread in threads[node]:
        thread.append jittered path from here to node.parent
    
    '''

'''Code adapted from https://github.com/stevenhalim/cpbook-code/blob/027f77933428d7688f935800ffa9109794e429b1/ch9/mcmf.py'''

INF = 10**18

class min_cost_max_flow:
  def __init__(self, V):
    self.V = V
    self.EL = []
    self.AL = [list() for _ in range(V)]
    self.vis = [False] * V 
    self.total_cost = 0
    self.d = None 
    self.last = None 
    self.edge_in_result = []

  def SPFA(self, s, t):
    self.d = [INF] * self.V
    self.d[s] = 0 # distance from source to source is 0
    self.vis[s] = True # source is in the queue
    q = [s] # queue of vertices to visit
    while len(q) != 0:
      u = q[0]
      q.pop(0)
      self.vis[u] = False # u is no longer in the queue
      for idx in self.AL[u]: # for each edge (u,v)
        v, cap, flow, cost = self.EL[idx] # self.El is to store edge v's capacity, current flow, and cost
        if cap-flow > 0 and self.d[v] > self.d[u]+cost: # if there is still capacity and the cost is lower
          self.d[v] = self.d[u]+cost # update the cost
          if not self.vis[v]: # if v is not in the queue
            q.append(v) # add v to the queue
            self.vis[v] = True # v is now in the queue
    return self.d[t] != INF

  def DFS(self, u, t, f=INF):
    if u == t or f == 0:
      return f
    self.vis[u] = True
    for i in range(self.last[u], len(self.AL[u])): # for each edge (u,v)
      v, cap, flow, cost = self.EL[self.AL[u][i]] 
      if not self.vis[v] and self.d[v] == self.d[u]+cost:
        pushed = self.DFS(v, t, min(f, cap-flow))
        if pushed != 0:
          self.total_cost += pushed * cost
          flow += pushed
          self.EL[self.AL[u][i]][2] = flow
          rv, rcap, rflow, rcost = self.EL[self.AL[u][i]^1]
          rflow -= pushed
          self.EL[self.AL[u][i]^1][2] = rflow
          self.vis[u] = False
          self.last[u] = i
          self.edge_in_result.append((u, v)) # add the edge to the result
          # print(u, v) # desired output, aka all the edges that are selected for the problem
          return pushed
    self.vis[u] = False
    return 0

  def add_edge(self, u, v, w, c, directed=True):
    if u == v:
      return
    self.EL.append([v, w, 0, c])
    self.AL[u].append(len(self.EL)-1)
    self.EL.append([u, 0 if directed else w, 0, -c])
    self.AL[v].append(len(self.EL)-1)

  def mcmf(self, s, t):
    mf = 0
    while self.SPFA(s, t):
      self.last = [0] * self.V
      f = self.DFS(s, t)
      while f != 0:
        mf += f
        f = self.DFS(s, t)
    # return mf, self.total_cost
    return self.edge_in_result


# def main():
    
#   V, E, s, t = map(int, input().split()) # Number of vertices, edges, source node index, sink node index
#   mf = min_cost_max_flow(V) # Create a min_cost_max_flow object
#   for _ in range(E): # Add edges
#     u, v, w, c = map(int, input().split()) # u, v, capacity, cost
#     mf.add_edge(u, v, w, c) # Add edge from u to v with capacity w and cost c
  
#   res = mf.mcmf(s, t) # Get the max flow and min cost
#   print('%d %d' % (res[0], res[1]))


# main()

'''
Input: 
1) Number of vertices, edges, source node index, sink node index
2) For each edge:
    start node, target node, capacity, cost
Desired Output is in DFS
'''
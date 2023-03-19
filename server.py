from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from pyvis.network import Network
import pickle

app = FastAPI()

def getKB(keyword):
    
    with open('relations.pkl', 'rb') as r:
           kb = pickle.load(r)
            
    if keyword != "full":
        new_kb = []

        for each in kb:
            if ((keyword.lower() in each['head'].lower()) or (keyword.lower() in each['tail'].lower())) and (each not in new_kb):
                new_kb.append(each)

        nodes = []
        for r in new_kb:
            nodes.extend([r["head"], r["tail"]])

        #unique nodes to plot in the knowledge base
        nodes = list(set(nodes))

        return new_kb, nodes
    else:
        nodes = []
        for r in new_kb:
            nodes.extend([r["head"], r["tail"]])
        return kb, nodes

    
def save_network_html(kb, nodes):
    # create network
    net = Network(directed=True, width="1500px", height="900px", bgcolor="#eeeeee")

    # nodes
    color_entity = "#00FF00"
    for e in nodes:
        net.add_node(e, shape="circle", color=color_entity)

    # edges
    for r in kb:
        net.add_edge(r["head"], r["tail"],
                    title=r["type"], label=r["type"])
        
    # save network
    net.repulsion(
        node_distance=200,
        central_gravity=0.2,
        spring_length=200,
        spring_strength=0.05,
        damping=0.09
    )
    net.set_edge_smooth('dynamic')
    net.show('file.html')
    

@app.get("/{keyword}")
async def root(keyword:str):
    kb, nodes = getKB(keyword)
    save_network_html(kb, nodes)
    f = open('file.html', 'r')
    return HTMLResponse(f.read())

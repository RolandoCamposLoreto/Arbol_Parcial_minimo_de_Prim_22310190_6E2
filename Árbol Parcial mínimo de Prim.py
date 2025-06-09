# Se requiere instalar estas librerías antes de ejecutar el código:
# pip install matplotlib networkx

import networkx as nx           # Para manejar grafos
import matplotlib.pyplot as plt # Para graficar los nodos y conexiones
import heapq                    # Para usar una cola de prioridad (mínimo primero)
import random                   # Para generar pesos aleatorios

# Función que genera un grafo representando las casas y tuberías posibles entre ellas
def generar_grafo_coto(num_casas):
    grafo = {}  # Diccionario que representará el grafo
    for i in range(num_casas):
        nodo = f"Casa {i+1}"   # Nombre de cada casa, por ejemplo "Casa 1"
        grafo[nodo] = {}       # Inicializa las conexiones de cada casa
    
    # Conexiones aleatorias entre casas con pesos (costos) aleatorios
    for i in range(num_casas):
        casa_actual = f"Casa {i+1}"
        # Selecciona entre 2 y 4 casas aleatorias para conectar (sin conectar consigo misma)
        conexiones = random.sample(range(num_casas), k=random.randint(2, 4))
        for j in conexiones:
            if j != i:
                casa_vecina = f"Casa {j+1}"
                peso = random.randint(1, 20)  # Costo aleatorio entre 1 y 20
                # Se agrega la conexión (grafo no dirigido, es simétrico)
                grafo[casa_actual][casa_vecina] = peso
                grafo[casa_vecina][casa_actual] = peso
    return grafo

# Función para mostrar gráficamente el árbol parcial mínimo
def mostrar_arbol_prim(grafo, mst_edges, titulo="Árbol Parcial Mínimo (Prim)"):
    G = nx.Graph()  # Crea un grafo de NetworkX
    # Agrega todas las aristas y sus pesos al grafo
    for nodo, vecinos in grafo.items():
        for vecino, peso in vecinos.items():
            G.add_edge(nodo, vecino, weight=peso)
    pos = nx.spring_layout(G, seed=42)  # Posiciones fijas para los nodos
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800, font_size=7)  # Dibuja nodos
    etiquetas = nx.get_edge_attributes(G, 'weight')  # Etiquetas de pesos
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas)  # Muestra los pesos
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges, edge_color='red', width=3)  # Dibuja el árbol de Prim
    plt.title(titulo)  # Título del gráfico
    plt.show()         # Muestra el gráfico

# Función que implementa el algoritmo de Prim con impresión paso a paso
def prim_con_pasos(grafo, inicio):
    visitados = set([inicio])  # Conjunto de nodos visitados (inicia con el nodo raíz)
    # Lista de aristas candidatas al árbol, formateadas como tuplas (peso, nodo_origen, nodo_destino)
    aristas_posibles = [(peso, inicio, vecino) for vecino, peso in grafo[inicio].items()]
    heapq.heapify(aristas_posibles)  # Convierte la lista en una cola de prioridad (mínimo primero)
    mst_edges = []   # Lista de aristas del árbol parcial mínimo
    costo_total = 0  # Costo acumulado

    # Imprime el grafo completo (todos los nodos y conexiones)
    print("\n=== GRAFO GENERADO ===")
    for nodo, vecinos in grafo.items():
        print(f"{nodo}:")
        for vecino, peso in vecinos.items():
            print(f"  - conectado a {vecino} con costo {peso}")
    print("======================\n")

    # Inicia la ejecución del algoritmo de Prim
    print(f"\n>>> Inicio del algoritmo de Prim desde {inicio}")
    print(f"Cola de prioridad inicial con las aristas desde {inicio}:")
    for peso, desde, hasta in aristas_posibles:
        print(f"  - {desde} --({peso})--> {hasta}")

    # Mientras haya aristas y no hayamos visitado todos los nodos
    while aristas_posibles and len(visitados) < len(grafo):
        peso, desde, hasta = heapq.heappop(aristas_posibles)  # Saca la arista más barata
        if hasta not in visitados:
            # Imprime el paso actual
            print(f"\n✔ Se selecciona la arista: {desde} --({peso})--> {hasta}")
            visitados.add(hasta)              # Agrega el nodo al conjunto visitado
            mst_edges.append((desde, hasta))  # Agrega la arista al árbol
            costo_total += peso               # Suma el costo
            print(f"{hasta} se agrega al árbol.")
            print(f"Se agregan nuevas aristas desde {hasta}:")

            # Agrega nuevas aristas posibles desde el nuevo nodo
            for vecino, costo in grafo[hasta].items():
                if vecino not in visitados:
                    heapq.heappush(aristas_posibles, (costo, hasta, vecino))
                    print(f"  - {hasta} --({costo})--> {vecino}")

    # Imprime el resultado final
    print("\n===== ÁRBOL PARCIAL MÍNIMO FINAL =====")
    for desde, hasta in mst_edges:
        peso = grafo[desde][hasta]
        print(f"  - {desde} --({peso})--> {hasta}")
    print(f"\n💰 Costo total de la instalación de plomería: {costo_total}")
    print("=======================================\n")

    return mst_edges  # Retorna las aristas del árbol de Prim

# -------------------- EJECUCIÓN PRINCIPAL ------------------------

grafo_coto = generar_grafo_coto(33)               # Genera un grafo aleatorio de 33 casas
mst_resultado = prim_con_pasos(grafo_coto, "Casa 1")  # Ejecuta el algoritmo desde Casa 1
mostrar_arbol_prim(grafo_coto, mst_resultado)     # Muestra el resultado gráficamente

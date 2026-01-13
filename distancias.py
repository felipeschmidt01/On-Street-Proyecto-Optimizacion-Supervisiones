from geopy.distance import geodesic
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import AgglomerativeClustering

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)  # Esto asegura que al imprimir el dataframe no se trunque
# es decir, se muestre completo en la consola

# Cargar los datos en un DataFrame
data = {
    "Móvil": [
        "La Araucana Móvil Promoción La Serena", "La Araucana Móvil Promoción Quillota",
        "La Araucana Móvil Agencia Quillota", "La Araucana Móvil Agencia Viña del Mar",
        "La Araucana Móvil Promoción Viña del Mar", "La Araucana Móvil Agencia San Antonio",
        "La Araucana Móvil Promoción Merced 1", "La Araucana Móvil Promoción Merced 2",
        "La Araucana Móvil Promoción Merced 3", "La Araucana Móvil Promoción Merced 4",
        "La Araucana Móvil Promoción Maipú 1", "La Araucana Móvil Promoción Maipu 2",
        "La Araucana Móvil Promoción Maipu 3", "La Araucana Móvil Agencia San Bernardo",
        "La Araucana Móvil Agencia Talagante", "La Araucana Móvil Promoción Maipu 4",
        "La Araucana Móvil Agencia Rancagua", "La Araucana Móvil Promoción Rancagua",
        "La Araucana Móvil Agencia San Fernando", "La Araucana Móvil Promoción San Fernando",
        "Caja 18 RM 3", "Caja 18 RM 4", "Caja 18 Rancagua 2", "La Araucana Móvil Agencia Curicó",
        "La Araucana Móvil Promoción Talca", "La Araucana Móvil Agencia Linares",
        "La Araucana Móvil Promoción Linares", "La Araucana Móvil Promoción Chillán",
        "La Araucana Móvil Agencia Chillán", "La Araucana Móvil Agencia Concepción",
        "La Araucana Móvil Promoción Concepción", "Habitat Móvil Talca", "Habitat Móvil Chillán",
        "Habitat Móvil Los Ángeles", "Habitat Móvil Concepción", "CGE Móvil Maule", "CGE Móvil Ñuble",
        "Punto Caja Los Andes Móvil San Clemente", "Punto Caja Los Andes Móvil Cauquenes",
        "Punto Caja Los Andes Móvil San Carlos", "La Araucana Móvil Agencia Los Ángeles",
        "La Araucana Móvil Promoción Los Ángeles", "La Araucana Móvil Agencia Coronel",
        "La Araucana Móvil Agencia Coyhaique", "La Araucana Móvil Agencia Temuco 1",
        "La Araucana Móvil Agencia Temuco 2", "La Araucana Móvil Promoción Temuco 1",
        "La Araucana Móvil Agencia Temuco 3", "La Araucana Móvil Promoción Temuco 2",
        "La Araucana Móvil Promoción Valdivia", "La Araucana Móvil Agencia Valdivia",
        "La Araucana Móvil Promoción Puerto Montt", "La Araucana Móvil Promoción Castro",
        "Habitat Móvil Temuco", "Habitat Móvil Valdivia", "Habitat Móvil Osorno",
        "Habitat Móvil Puerto Montt", "Punto Caja Los Andes Móvil Panguipulli", "Punto Caja Los Andes Móvil Ancud",
        "Habitat Móvil Iquique", "Habitat Móvil Calama", "Habitat Móvil Copiapó", "Habitat Móvil La Serena",
        "Habitat Móvil V Cordillera", "Habitat Móvil Santiago 1", "Habitat Móvil Santiago 2",
        "Habitat Móvil V Costa", "Habitat Móvil Rancagua", "CGE Móvil Coquimbo", "CGE Móvil RM",
        "Mutual Bus de capacitación", "Punto Caja Los Andes Móvil Tocopilla", "Punto Caja Los Andes Móvil Taltal",
        "Punto Caja Los Andes Móvil Los Vilos", "Punto Caja Los Andes Móvil Cabildo",
        "Punto Caja Los Andes Móvil Limache", "Punto Caja Los Andes Móvil Llay Llay", "Los Pelambres Móvil"
    ],
    "Latitud": [
        -29.9045, -32.8833, -32.8833, -33.0246, -33.0246, -33.5930, -33.4088, -33.4088, -33.3670, -33.3670, -33.5080,
        -33.6117, -33.5922, -33.5922, -33.6633, -33.6896, -34.1708, -34.1708, -34.5857, -34.5857, -33.5922, -33.4489,
        -34.1708, -34.9828, -35.4264, -35.8466, -35.8466, -36.6066, -36.6066, -36.8201, -36.8201, -35.4264, -36.6066,
        -37.4693, -36.8201, -35.4264, -36.6000, -35.5399, -35.9667, -36.4222, -37.4693, -37.4693, -37.0302, -45.4024,
        -38.7397, -38.7397, -38.7397, -38.7397, -38.7397, -39.8196, -39.8196, -41.4693, -42.4804, -38.7397, -39.8196,
        -40.5743, -41.4693, -39.6450, -41.8697, -20.2133, -22.4567, -27.3668, -29.9045, -32.8833, -33.4489, -33.4489,
        -33.5930, -34.1708, -29.9533, -33.4489, -33.4489, -22.0869, -25.4057, -31.9136, -32.4263, -33.0167, -32.8417,
        -31.7753
    ],
    "Longitud": [
        -71.2489, -71.2489, -71.2489, -71.5518, -71.5518, -71.6210, -70.5670, -70.5670, -70.7330, -70.7330, -70.7617,
        -70.5758, -70.6996, -70.6996, -70.9270, -71.2150, -70.7444, -70.7444, -70.9923, -70.9923, -70.6996, -70.6693,
        -70.7444, -71.2406, -71.6554, -71.5936, -71.5936, -72.1034, -72.1034, -73.0443, -73.0443, -71.6554, -72.1034,
        -72.3537, -73.0443, -71.6554, -71.8000, -71.4884, -72.3167, -71.9583, -72.3537, -72.3537, -73.1405, -72.6920,
        -72.5984, -72.5984, -72.5984, -72.5984, -72.5984, -73.2452, -73.2452, -72.9424, -73.7620, -72.5984, -73.2452,
        -73.1338, -72.9424, -72.3306, -73.8203, -70.1503, -68.9237, -70.3322, -71.2489, -71.2489, -70.6693, -70.6693,
        -71.6210, -70.7444, -71.3395, -70.6693, -70.6693, -70.1979, -70.4859, -71.5070, -71.0638, -71.2667, -70.9561,
        -70.9725
    ]
}

df = pd.DataFrame(data) # el diccionario se convierte en un data frame

# Crear una lista de coordenadas (latitud, longitud)
coords = list(zip(df["Latitud"], df["Longitud"])) # se crea una lista de tuplas con las coordenadas

# Calcular la matriz de distancias
dist_matrix = squareform(pdist(coords, lambda u, v: geodesic(u, v).km)) # se obtiene la matriz de distancias entre los móviles

# Usar AgglomerativeClustering para construir los cúmulos
# 

clustering = AgglomerativeClustering( # crear los clusters
    n_clusters=None,  # Número de cúmulos será definido por la distancia
    distance_threshold=300,  # Distancia máxima para crear cúmulos. Es decir, los clusteres no se juntan si es que la distancia máxima entre alguno de los elementos de cada cluster es mayor a 300 km
    metric="precomputed", # usa la matriz de distancias ya calculada
    linkage="complete" # la distancia entre los clusters se define como la máxima distancia entre cualquier par de elementos de esos clusters
)
labels = clustering.fit_predict(dist_matrix) # Se ejecuta el clustering en la matriz de distancais creada anteriormente
# labels es un array de numeros enteros. Tiene la forma [0,0,1,1,2,2,...] donde cada número es el número del cluster donde se ubica cada móvil.
# por ejemplo, el primer móvil es del cluster cero, el segundo también, el tercero y el cuarto son del cluster 1, y así.

# Agregar los clústeres al DataFrame
df["Cluster"] = labels # aquí se crea la nueva columna con los id de cada cluster, con lo que cada móvil queda asignado a un cluster

# print(df)

# Obtener los clusters válidos (siempre será todo el conjunto en este caso)
valid_clusters = df["Cluster"].unique() # se obtiene los id de los clusters creados
# por ejemplo, si antes era [0,0,1,1,2,2,...], ahora valid_clusters es [0,1,2,...]

subclusters = []

for cluster_id in valid_clusters:
    cluster_df = df[df["Cluster"] == cluster_id].copy()  # Crear una copia para evitar problemas de asignación
    cluster_coords = list(zip(cluster_df["Latitud"], cluster_df["Longitud"]))
    cluster_dist_matrix = squareform(pdist(cluster_coords, lambda u, v: geodesic(u, v).km)) # se crea de nuevo la matriz de distancias para este cluster específico
    
    if len(cluster_coords) > 1:  # Aplicar lógica solo si hay más de un móvil en el clúster
        # Crear subclústeres basados en cercanía relativa
        subclustering_labels = []
        used_indices = set()
        
        for i, coord in enumerate(cluster_coords):
            if i not in used_indices:
                subcluster = [i] # inicio greedy, se recorre cada móvil; si no está usado, se inicia un nuevo subcluster con ese movil
                used_indices.add(i) # se añade a los usados
                
                # Encontrar los más cercanos no utilizados
                while len(subcluster) < 4:  # Intentar agrupar hasta 3
                    remaining_indices = [j for j in range(len(cluster_coords)) if j not in used_indices]
                    if not remaining_indices:
                        break
                    
                    # Buscar el más cercano al último móvil añadido
                    closest_idx = min(remaining_indices, key=lambda j: cluster_dist_matrix[subcluster[-1], j])
                    subcluster.append(closest_idx)
                    used_indices.add(closest_idx)
                
                subclustering_labels.append(subcluster)
        
        # Asignar subclústeres
        for subcluster_id, indices in enumerate(subclustering_labels):
            cluster_df.loc[cluster_df.index[indices], "SubCluster"] = subcluster_id
    else:
        # Si solo hay un móvil, asignar un subclúster único
        cluster_df["SubCluster"] = 0

    subclusters.append(cluster_df)

# Combinar todos los subgrupos en un DataFrame final
df_result = pd.concat(subclusters)

# Mostrar subclústeres
print("Subclústeres creados dentro de cada clúster:")
for cluster_id in sorted(df_result["Cluster"].unique()):
    print(f"\nClúster {cluster_id}:")
    for subcluster_id in sorted(df_result[df_result["Cluster"] == cluster_id]["SubCluster"].unique()):
        print(f"  Subclúster {subcluster_id}:")
        print(df_result[(df_result["Cluster"] == cluster_id) & (df_result["SubCluster"] == subcluster_id)][["Móvil", "Latitud", "Longitud"]])

# Verificar si todos los móviles están en el resultado final
if len(df_result) == len(df):
    print("✅ Todos los móviles han sido asignados correctamente a subclústeres.")
else:
    print("⚠️ Atención: No todos los móviles han sido asignados.")
    print("Móviles no asignados:")
    print(df[~df.index.isin(df_result.index)])
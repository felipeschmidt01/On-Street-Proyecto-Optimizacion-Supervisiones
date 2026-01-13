from collections import defaultdict
import math
from pulp import LpVariable, LpProblem, LpMaximize, lpSum, LpBinary

clusters = {
    "Cluster 1": ["Habitat Móvil Iquique", "Habitat Móvil Calama", "Punto Caja Los Andes Móvil Tocopilla"],
    "Cluster 2": ["La Araucana Móvil Promoción Talca", "Habitat Móvil Talca", "CGE Móvil Maule", "Punto Caja Los Andes Móvil San Clemente"],
    "Cluster 3": ["La Araucana Móvil Agencia Linares", "La Araucana Móvil Promoción Linares", "Punto Caja Los Andes Móvil Cauquenes", "Punto Caja Los Andes Móvil San Carlos"],
    "Cluster 4": ["La Araucana Móvil Promoción Chillán", "La Araucana Móvil Agencia Chillán", "Habitat Móvil Chillán", "CGE Móvil Ñuble"],
    "Cluster 5": ["La Araucana Móvil Agencia Concepción", "La Araucana Móvil Promoción Concepción", "Habitat Móvil Concepción", "La Araucana Móvil Agencia Coronel"],
    "Cluster 6": ["Habitat Móvil Los Ángeles", "La Araucana Móvil Agencia Los Ángeles", "La Araucana Móvil Promoción Los Ángeles"],
    "Cluster 7": ["La Araucana Móvil Agencia San Antonio", "La Araucana Móvil Agencia Talagante", "La Araucana Móvil Promoción Maipú 4", "Habitat Móvil V Costa"],
    "Cluster 8": ["La Araucana Móvil Promoción Merced 1", "La Araucana Móvil Promoción Merced 2", "Caja 18 RM 4", "Habitat Móvil Santiago 1"],
    "Cluster 9": ["La Araucana Móvil Promoción Merced 3", "La Araucana Móvil Promoción Merced 4", "Habitat Móvil Santiago 2", "CGE Móvil RM"],
    "Cluster 10": ["La Araucana Móvil Promoción Maipú 1", "La Araucana Móvil Promoción Maipú 3", "La Araucana Móvil Agencia San Bernardo", "Mutual Bus de capacitación"],
    "Cluster 11": ["La Araucana Móvil Promoción Maipú 2", "La Araucana Móvil Agencia Rancagua", "La Araucana Móvil Promoción Rancagua", "Caja 18 RM 3"],
    "Cluster 12": ["La Araucana Móvil Agencia San Fernando", "La Araucana Móvil Promoción San Fernando", "Caja 18 Rancagua 2", "La Araucana Móvil Agencia Curicó"],
    "Cluster 13": ["Habitat Móvil Rancagua"],
    "Cluster 14": ["La Araucana Móvil Promoción Puerto Montt", "La Araucana Móvil Promoción Castro", "Habitat Móvil Puerto Montt", "Punto Caja Los Andes Móvil Ancud"],
    "Cluster 15": ["Habitat Móvil Osorno"],
    "Cluster 16": ["Habitat Móvil Copiapó", "Punto Caja Los Andes Móvil Taltal"],
    "Cluster 17": ["La Araucana Móvil Agencia Coyhaique"],
    "Cluster 18": ["La Araucana Móvil Promoción Quillota", "La Araucana Móvil Agencia Quillota", "Habitat Móvil V Cordillera", "Punto Caja Los Andes Móvil Limache"],
    "Cluster 19": ["La Araucana Móvil Agencia Viña del Mar", "La Araucana Móvil Promoción Viña del Mar", "Punto Caja Los Andes Móvil Cabildo", "Punto Caja Los Andes Móvil Llay Llay"],
    "Cluster 20": ["Punto Caja Los Andes Móvil Los Vilos", "Los Pelambres Móvil"],
    "Cluster 21": ["La Araucana Móvil Agencia Temuco 1", "La Araucana Móvil Agencia Temuco 2", "La Araucana Móvil Promoción Temuco 1", "La Araucana Móvil Agencia Temuco 3"],
    "Cluster 22": ["La Araucana Móvil Promoción Temuco 2", "La Araucana Móvil Promoción Valdivia", "Habitat Móvil Temuco", "Punto Caja Los Andes Móvil Panguipulli"],
    "Cluster 23": ["La Araucana Móvil Agencia Valdivia", "Habitat Móvil Valdivia"],
    "Cluster 24": ["La Araucana Móvil Promoción La Serena", "Habitat Móvil La Serena", "CGE Móvil Coquimbo"]
}


# Resultados del primer modelo: visitas por lugar
visitas_por_lugar = {
    "La Araucana Móvil Promoción La Serena": 4,
    "La Araucana Móvil Promoción Quillota": 6,
    "La Araucana Móvil Agencia Quillota": 6,
    "La Araucana Móvil Agencia Viña del Mar": 6,
    "La Araucana Móvil Promoción Viña del Mar": 6,
    "La Araucana Móvil Agencia San Antonio": 6,
    "La Araucana Móvil Promoción Merced 1": 7,
    "La Araucana Móvil Promoción Merced 2": 6,
    "La Araucana Móvil Promoción Merced 3": 6,
    "La Araucana Móvil Promoción Merced 4": 6,
    "La Araucana Móvil Promoción Maipú 1": 6,
    "La Araucana Móvil Promoción Maipú 2": 6,
    "La Araucana Móvil Promoción Maipú 3": 6,
    "La Araucana Móvil Agencia San Bernardo": 7,
    "La Araucana Móvil Agencia Talagante": 6,
    "La Araucana Móvil Promoción Maipú 4": 6,
    "La Araucana Móvil Agencia Rancagua": 6,
    "La Araucana Móvil Promoción Rancagua": 6,
    "La Araucana Móvil Agencia San Fernando": 6,
    "La Araucana Móvil Promoción San Fernando": 6,
    "Caja 18 RM 3": 6,
    "Caja 18 RM 4": 6,
    "Caja 18 Rancagua 2": 6,
    "La Araucana Móvil Agencia Curicó": 5,
    "La Araucana Móvil Promoción Talca": 5,
    "La Araucana Móvil Agencia Linares": 6,
    "La Araucana Móvil Promoción Linares": 6,
    "La Araucana Móvil Promoción Chillán": 6,
    "La Araucana Móvil Agencia Chillán": 6,
    "La Araucana Móvil Agencia Concepción": 7,
    "La Araucana Móvil Promoción Concepción": 6,
    "Habitat Móvil Talca": 6,
    "Habitat Móvil Chillán": 7,
    "Habitat Móvil Los Ángeles": 7,
    "Habitat Móvil Concepción": 7,
    "CGE Móvil Maule": 6,
    "CGE Móvil Ñuble": 6,
    "Punto Caja Los Andes Móvil San Clemente": 7,
    "Punto Caja Los Andes Móvil Cauquenes": 8,
    "Punto Caja Los Andes Móvil San Carlos": 8,
    "La Araucana Móvil Agencia Los Ángeles": 6,
    "La Araucana Móvil Promoción Los Ángeles": 6,
    "La Araucana Móvil Agencia Coronel": 6,
    "La Araucana Móvil Agencia Coyhaique": 4,
    "La Araucana Móvil Agencia Temuco 1": 7,
    "La Araucana Móvil Agencia Temuco 2": 7,
    "La Araucana Móvil Promoción Temuco 1": 6,
    "La Araucana Móvil Agencia Temuco 3": 6,
    "La Araucana Móvil Promoción Temuco 2": 6,
    "La Araucana Móvil Promoción Valdivia": 6,
    "La Araucana Móvil Agencia Valdivia": 6,
    "La Araucana Móvil Promoción Puerto Montt": 5,
    "La Araucana Móvil Promoción Castro": 4,
    "Habitat Móvil Temuco": 7,
    "Habitat Móvil Valdivia": 6,
    "Habitat Móvil Osorno": 6,
    "Habitat Móvil Puerto Montt": 5,
    "Punto Caja Los Andes Móvil Panguipulli": 7,
    "Punto Caja Los Andes Móvil Ancud": 6,
    "Habitat Móvil Iquique": 3,
    "Habitat Móvil Calama": 3,
    "Habitat Móvil Copiapó": 3,
    "Habitat Móvil La Serena": 5,
    "Habitat Móvil V Cordillera": 6,
    "Habitat Móvil Santiago 1": 7,
    "Habitat Móvil Santiago 2": 7,
    "Habitat Móvil V Costa": 7,
    "Habitat Móvil Rancagua": 6,
    "CGE Móvil Coquimbo": 5,
    "CGE Móvil RM": 7,
    "Mutual Bus de capacitación": 6,
    "Punto Caja Los Andes Móvil Tocopilla": 3,
    "Punto Caja Los Andes Móvil Taltal": 4,
    "Punto Caja Los Andes Móvil Los Vilos": 7,
    "Punto Caja Los Andes Móvil Cabildo": 7,
    "Punto Caja Los Andes Móvil Limache": 7,
    "Punto Caja Los Andes Móvil Llay Llay": 6,
    "Los Pelambres Móvil": 6,
}

# Datos de los KAM y sus móviles
kams_moviles = {
    "Nicolás Villaseca": [
        "La Araucana Móvil Promoción La Serena", "La Araucana Móvil Promoción Quillota",
        "La Araucana Móvil Agencia Quillota", "La Araucana Móvil Agencia Viña del Mar",
        "La Araucana Móvil Promoción Viña del Mar", "La Araucana Móvil Agencia San Antonio",
        "La Araucana Móvil Promoción Merced 1", "La Araucana Móvil Promoción Merced 2",
        "La Araucana Móvil Promoción Merced 3", "La Araucana Móvil Promoción Merced 4",
        "La Araucana Móvil Promoción Maipú 1", "La Araucana Móvil Promoción Maipú 2",
        "La Araucana Móvil Promoción Maipú 3", "La Araucana Móvil Agencia San Bernardo",
        "La Araucana Móvil Agencia Talagante", "La Araucana Móvil Promoción Maipú 4",
        "La Araucana Móvil Agencia Rancagua", "La Araucana Móvil Promoción Rancagua",
        "La Araucana Móvil Agencia San Fernando", "La Araucana Móvil Promoción San Fernando",
        "Caja 18 RM 3", "Caja 18 RM 4", "Caja 18 Rancagua 2"
    ],
    "José Ocampos": [
        "La Araucana Móvil Agencia Curicó", "La Araucana Móvil Promoción Talca",
        "La Araucana Móvil Agencia Linares", "La Araucana Móvil Promoción Linares",
        "La Araucana Móvil Promoción Chillán", "La Araucana Móvil Agencia Chillán",
        "La Araucana Móvil Agencia Concepción", "La Araucana Móvil Promoción Concepción",
        "Habitat Móvil Talca", "Habitat Móvil Chillán", "Habitat Móvil Los Ángeles",
        "Habitat Móvil Concepción", "CGE Móvil Maule", "CGE Móvil Ñuble",
        "Punto Caja Los Andes Móvil San Clemente", "Punto Caja Los Andes Móvil Cauquenes",
        "Punto Caja Los Andes Móvil San Carlos"
    ],
    "Cristobal Aniñir": [
        "La Araucana Móvil Agencia Los Ángeles", "La Araucana Móvil Promoción Los Ángeles",
        "La Araucana Móvil Agencia Coronel", "La Araucana Móvil Agencia Coyhaique",
        "La Araucana Móvil Agencia Temuco 1", "La Araucana Móvil Agencia Temuco 2",
        "La Araucana Móvil Promoción Temuco 1", "La Araucana Móvil Agencia Temuco 3",
        "La Araucana Móvil Promoción Temuco 2", "La Araucana Móvil Promoción Valdivia",
        "La Araucana Móvil Agencia Valdivia", "La Araucana Móvil Promoción Puerto Montt",
        "La Araucana Móvil Promoción Castro", "Habitat Móvil Temuco", "Habitat Móvil Valdivia",
        "Habitat Móvil Osorno", "Habitat Móvil Puerto Montt", "Punto Caja Los Andes Móvil Panguipulli",
        "Punto Caja Los Andes Móvil Ancud"
    ],
    "Nathalie Galaz": [
        "Habitat Móvil Iquique", "Habitat Móvil Calama", "Habitat Móvil Copiapó",
        "Habitat Móvil La Serena", "Habitat Móvil V Cordillera", "Habitat Móvil Santiago 1",
        "Habitat Móvil Santiago 2", "Habitat Móvil V Costa", "Habitat Móvil Rancagua",
        "CGE Móvil Coquimbo", "CGE Móvil RM", "Mutual Bus de capacitación",
        "Punto Caja Los Andes Móvil Tocopilla", "Punto Caja Los Andes Móvil Taltal",
        "Punto Caja Los Andes Móvil Los Vilos", "Punto Caja Los Andes Móvil Cabildo",
        "Punto Caja Los Andes Móvil Limache", "Punto Caja Los Andes Móvil Llay Llay",
        "Los Pelambres Móvil"
    ]
}

moviles_por_cliente = {
    "La Araucana móvil": [
        "La Araucana Móvil Promoción La Serena", "La Araucana Móvil Promoción Quillota",
        "La Araucana Móvil Agencia Quillota", "La Araucana Móvil Agencia Viña del Mar",
        "La Araucana Móvil Promoción Viña del Mar", "La Araucana Móvil Agencia San Antonio",
        "La Araucana Móvil Promoción Merced 1", "La Araucana Móvil Promoción Merced 2",
        "La Araucana Móvil Promoción Merced 3", "La Araucana Móvil Promoción Merced 4",
        "La Araucana Móvil Promoción Maipú 1", "La Araucana Móvil Promoción Maipú 2",
        "La Araucana Móvil Promoción Maipú 3", "La Araucana Móvil Agencia San Bernardo",
        "La Araucana Móvil Agencia Talagante", "La Araucana Móvil Promoción Maipú 4",
        "La Araucana Móvil Agencia Rancagua", "La Araucana Móvil Promoción Rancagua",
        "La Araucana Móvil Agencia San Fernando", "La Araucana Móvil Promoción San Fernando",
        "La Araucana Móvil Agencia Curicó", "La Araucana Móvil Promoción Talca",
        "La Araucana Móvil Agencia Linares", "La Araucana Móvil Promoción Linares",
        "La Araucana Móvil Promoción Chillán", "La Araucana Móvil Agencia Chillán",
        "La Araucana Móvil Agencia Concepción", "La Araucana Móvil Promoción Concepción",
        "La Araucana Móvil Agencia Los Ángeles", "La Araucana Móvil Promoción Los Ángeles",
        "La Araucana Móvil Agencia Coronel", "La Araucana Móvil Agencia Coyhaique",
        "La Araucana Móvil Agencia Temuco 1", "La Araucana Móvil Agencia Temuco 2",
        "La Araucana Móvil Promoción Temuco 1", "La Araucana Móvil Agencia Temuco 3",
        "La Araucana Móvil Promoción Temuco 2", "La Araucana Móvil Promoción Valdivia",
        "La Araucana Móvil Agencia Valdivia", "La Araucana Móvil Promoción Puerto Montt",
        "La Araucana Móvil Promoción Castro"
    ],
    "Caja 18": [
        "Caja 18 RM 3", "Caja 18 RM 4", "Caja 18 Rancagua 2"
    ],
    "Habitat Móvil": [
        "Habitat Móvil Talca", "Habitat Móvil Chillán", "Habitat Móvil Los Ángeles",
        "Habitat Móvil Concepción", "Habitat Móvil Temuco", "Habitat Móvil Valdivia",
        "Habitat Móvil Osorno", "Habitat Móvil Puerto Montt", "Habitat Móvil Iquique",
        "Habitat Móvil Calama", "Habitat Móvil Copiapó", "Habitat Móvil La Serena",
        "Habitat Móvil V Cordillera", "Habitat Móvil Santiago 1", "Habitat Móvil Santiago 2",
        "Habitat Móvil V Costa", "Habitat Móvil Rancagua"
    ],
    "CGE": [
        "CGE Móvil Maule", "CGE Móvil Ñuble", "CGE Móvil Coquimbo", "CGE Móvil RM"
    ],
    "Caja los Andes": [
        "Punto Caja Los Andes Móvil San Clemente", "Punto Caja Los Andes Móvil Cauquenes",
        "Punto Caja Los Andes Móvil San Carlos", "Punto Caja Los Andes Móvil Panguipulli",
        "Punto Caja Los Andes Móvil Ancud", "Punto Caja Los Andes Móvil Tocopilla",
        "Punto Caja Los Andes Móvil Taltal", "Punto Caja Los Andes Móvil Los Vilos",
        "Punto Caja Los Andes Móvil Cabildo", "Punto Caja Los Andes Móvil Limache",
        "Punto Caja Los Andes Móvil Llay-Llay"
    ],
    "Mutual": [
        "Mutual Bus de capacitación"
    ],
    "Pelambres": [
        "Los Pelambres Móvil"
    ]
}

# Inicializar x_dicts para almacenar las variables x de todos los KAM
globals()["x_dicts"] = []

# Parámetros principales
meses = range(1, 13)  # Meses del año
lugares = list(visitas_por_lugar.keys())  # Lista de lugares

def resolver_para_conjunto(conjunto, nombre_conjunto):
    lugares_conjunto = [lugar for lugar in lugares if lugar in conjunto]
    limite_mensual = math.ceil(0.55 * len(lugares_conjunto))  # Relajamos el límite mensual
    minimo_mensual = math.floor(0.45 * len(lugares_conjunto))  # Relajamos el mínimo mensual

    # Variables de decisión
    x = LpVariable.dicts(f"visita_{nombre_conjunto}", [(l, m) for l in lugares_conjunto for m in meses], cat=LpBinary)
    globals()["x_dicts"].append(x)  # Agregar las variables x al global x_dicts

    z = LpVariable.dicts(f"mes_activo_{nombre_conjunto}", meses, cat=LpBinary)
    w = LpVariable.dicts(f"visita_conjunta_{nombre_conjunto}",
                         [(l1, l2, m) for c, cluster in clusters.items()
                          for l1 in cluster if l1 in conjunto
                          for l2 in cluster if l2 in conjunto and l1 != l2
                          for m in meses],
                         cat=LpBinary)

    # Modelo
    modelo = LpProblem(f"Plan_Anual_Visitas_{nombre_conjunto}", LpMaximize)

    # Función objetivo ajustada
    modelo += (
        50000 * lpSum(w[(l1, l2, m)] for c, cluster in clusters.items()
                for l1 in cluster if l1 in conjunto
                for l2 in cluster if l2 in conjunto and l1 != l2
                for m in meses)  # Incentivar visitas conjuntas
        - 100 * lpSum(x.get((l, m), 0) + x.get((l, m + 1), 0) for l in lugares_conjunto for m in range(1, 12))  # Penalizar visitas consecutivas
    )

    # Restricciones
    for m in meses:
        modelo += lpSum(x[l, m] for l in lugares_conjunto) <= limite_mensual, f"Límite_mensual_{nombre_conjunto}_{m}"
        modelo += lpSum(x[l, m] for l in lugares_conjunto) >= minimo_mensual, f"Mínimo_mensual_{nombre_conjunto}_{m}"

    for l in lugares_conjunto:
        modelo += lpSum(x[l, m] for m in meses) == visitas_por_lugar[l], f"Cobertura_{nombre_conjunto}_{l}"

    for m in meses:
        modelo += z[m] == 1, f"Mes_activo_{nombre_conjunto}_{m}"
        modelo += lpSum(x[l, m] for l in lugares_conjunto) >= z[m], f"Visitas_activan_mes_{nombre_conjunto}_{m}"

    for l in lugares_conjunto:
        frecuencia = max(1, 12 // visitas_por_lugar[l])
        for m1 in range(1, 13):
            for m2 in range(m1 + 1, min(13, m1 + frecuencia)):
                modelo += x[l, m1] + x[l, m2] <= 1, f"Frecuencia_ajustada_{nombre_conjunto}_{l}_{m1}_{m2}"

    # Nueva restricción: Al menos el 47% de los móviles supervisados cada mes
    for cliente, moviles_cliente in moviles_por_cliente.items():
        lugares_cliente = [l for l in lugares_conjunto if l in moviles_cliente]
        if lugares_cliente:  # Solo aplica si hay móviles de este cliente en el conjunto
            min_supervisiones_por_mes = math.ceil(0.47 * len(lugares_cliente))
            for m in meses:
                modelo += lpSum(x[l, m] for l in lugares_cliente) >= min_supervisiones_por_mes, f"Min_supervisiones_{cliente}_{nombre_conjunto}_{m}"

    # Resolver modelo
    modelo.solve()

    # Mostrar resultados
    print(f"\n=== Plan Anual de Visitas para {nombre_conjunto} ===\n")
    plan_anual = defaultdict(list)
    for l in lugares_conjunto:
        for m in meses:
            if x[l, m].value() == 1:
                plan_anual[m].append(l)

    for mes, visitas in sorted(plan_anual.items()):
        print(f"Mes {mes}:")
        for lugar in visitas:
            print(f"  - {lugar}")
        print()

# Resolver para cada KAM
for nombre, conjunto in kams_moviles.items():
    resolver_para_conjunto(conjunto, nombre)

# Supervisión global mes a mes para cada cliente
print("\n=== Supervisión Global Mes a Mes por Cliente ===\n")
for cliente, moviles_cliente in moviles_por_cliente.items():
    if len(moviles_cliente) > 1:  # Aplica solo si el cliente tiene más de un móvil
        print(f"Cliente: {cliente}")
        for m in meses:
            # Contar supervisados globalmente para este mes
            supervisados = sum(
                1
                for l in moviles_cliente
                if any((l, m) in x and x[(l, m)].value() == 1 for x in globals()["x_dicts"])
            )
            total_mobiles = len(moviles_cliente)
            porcentaje = (supervisados / total_mobiles) * 100 if total_mobiles > 0 else 0
            print(f"  Mes {m}: {porcentaje:.2f}% supervisado")
        print()

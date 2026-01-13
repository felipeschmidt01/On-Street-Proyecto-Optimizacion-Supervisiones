
from pulp import LpMaximize,LpStatus, LpProblem, LpVariable, lpSum, PULP_CBC_CMD
import numpy as np
import math 

# Lista de lugares y sus costos

lugares = [
    ("La Araucana Móvil Promoción La Serena", 66231),
    ("La Araucana Móvil Promoción Quillota", 32380),
    ("La Araucana Móvil Agencia Quillota", 32380),
    ("La Araucana Móvil Agencia Viña del Mar", 30605),
    ("La Araucana Móvil Promoción Viña del Mar", 30605),
    ("La Araucana Móvil Agencia San Antonio", 28485),
    ("La Araucana Móvil Promoción Merced 1", 17000),
    ("La Araucana Móvil Promoción Merced 2", 17000),
    ("La Araucana Móvil Promoción Merced 3", 17000),
    ("La Araucana Móvil Promoción Merced 4", 17000),
    ("La Araucana Móvil Promoción Maipú 1", 18000),
    ("La Araucana Móvil Promoción Maipú 2", 19000),
    ("La Araucana Móvil Promoción Maipú 3", 19000),
    ("La Araucana Móvil Agencia San Bernardo", 19000),
    ("La Araucana Móvil Agencia Talagante", 21000),
    ("La Araucana Móvil Promoción Maipú 4", 22000),
    ("La Araucana Móvil Agencia Rancagua", 29000),
    ("La Araucana Móvil Promoción Rancagua", 29000),
    ("La Araucana Móvil Agencia San Fernando", 40000),
    ("La Araucana Móvil Promoción San Fernando", 40000),
    ("Caja 18 RM 3", 19000),
    ("Caja 18 RM 4", 19000),
    ("Caja 18 Rancagua 2", 29000),
    ("La Araucana Móvil Agencia Curicó", 49500),
    ("La Araucana Móvil Promoción Talca", 42000),
    ("La Araucana Móvil Agencia Linares", 38000),
    ("La Araucana Móvil Promoción Linares", 38000),
    ("La Araucana Móvil Promoción Chillán", 28000),
    ("La Araucana Móvil Agencia Chillán", 28000),
    ("La Araucana Móvil Agencia Concepción", 17000),
    ("La Araucana Móvil Promoción Concepción", 17000),
    ("Habitat Móvil Talca", 42000),
    ("Habitat Móvil Chillán", 28000),
    ("Habitat Móvil Los Ángeles", 28000),
    ("Habitat Móvil Concepción", 17000),
    ("CGE Móvil Maule", 42000),
    ("CGE Móvil Ñuble", 28000),
    ("Punto Caja Los Andes Móvil San Clemente", 41000),
    ("Punto Caja Los Andes Móvil Cauquenes", 27500),
    ("Punto Caja Los Andes Móvil San Carlos", 29500),
    ("La Araucana Móvil Agencia Los Ángeles", 35000),
    ("La Araucana Móvil Promoción Los Ángeles", 35000),
    ("La Araucana Móvil Agencia Coronel", 39500),
    ("La Araucana Móvil Agencia Coyhaique", 103000),
    ("La Araucana Móvil Agencia Temuco 1", 17000),
    ("La Araucana Móvil Agencia Temuco 2", 17000),
    ("La Araucana Móvil Promoción Temuco 1", 17000),
    ("La Araucana Móvil Agencia Temuco 3", 17000),
    ("La Araucana Móvil Promoción Temuco 2", 17000),
    ("La Araucana Móvil Promoción Valdivia", 34500),
    ("La Araucana Móvil Agencia Valdivia", 34500),
    ("La Araucana Móvil Promoción Puerto Montt", 55500),
    ("La Araucana Móvil Promoción Castro", 70500),
    ("Habitat Móvil Temuco", 17000),
    ("Habitat Móvil Valdivia", 34500),
    ("Habitat Móvil Osorno", 45000),
    ("Habitat Móvil Puerto Montt", 55500),
    ("Punto Caja Los Andes Móvil Panguipulli", 32500),
    ("Punto Caja Los Andes Móvil Ancud", 65000),
    ("Habitat Móvil Iquique", 245000),
    ("Habitat Móvil Calama", 245000),
    ("Habitat Móvil Copiapó", 235000),
    ("Habitat Móvil La Serena", 66231),
    ("Habitat Móvil V Cordillera", 32380),
    ("Habitat Móvil Santiago 1", 17000),
    ("Habitat Móvil Santiago 2", 17000),
    ("Habitat Móvil V Costa", 28500),
    ("Habitat Móvil Rancagua", 29000),
    ("CGE Móvil Coquimbo", 66231),
    ("CGE Móvil RM", 20000),
    ("Mutual Bus de capacitación", 19000),
    ("Punto Caja Los Andes Móvil Tocopilla", 270000),
    ("Punto Caja Los Andes Móvil Taltal", 260000),
    ("Punto Caja Los Andes Móvil Los Vilos", 42000),
    ("Punto Caja Los Andes Móvil Cabildo", 34213),
    ("Punto Caja Los Andes Móvil Limache", 31600),
    ("Punto Caja Los Andes Móvil Llay Llay", 30000),
    ("Los Pelambres Móvil", 47000),
]

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
# Crear el modelo de optimización
modelo = LpProblem(name="asignacion_visitas", sense=LpMaximize)

n = len(lugares)  # Total de lugares

# Variables de decisión: 6 posibles cantidades de visitas (3, 4, 5, 6, 7, 8)
y = {
    (i, v): LpVariable(f"y_{i}_{v}", cat="Binary")
    for i in range(n) for v in [3, 4, 5, 6, 7, 8]
}

# Restricción: cada lugar debe tener exactamente una cantidad de visitas
for i in range(n):
    modelo += lpSum([y[i, v] for v in [3, 4, 5, 6, 7, 8]]) == 1, f"eleccion_unica_{i}"

# Restricción explícita: ningún móvil debe quedarse con menos de 3 supervisiones
for i in range(n):
    modelo += lpSum([y[i, v] for v in [3, 4, 5, 6, 7, 8]]) >= 1, f"restriccion_min_supervisiones_{i}"

# Función objetivo: Maximizar visitas equilibradas
target_visitas = 6  # Valor objetivo para penalización
alpha = 0.3  # Penalización para desviarse del objetivo
beta = 0.7   # Incentivo para maximizar visitas
modelo += lpSum([
    -alpha * (v - target_visitas)**2 * y[i, v] + beta * v * y[i, v]
    for i in range(n) for v in [3, 4, 5, 6, 7, 8]
]), "Maximizar_visitas_equilibradas"

# Restricciones de presupuesto
presupuesto_total = 1800000 * 10
modelo += lpSum([
    y[i, v] * v * lugares[i][1] for i in range(n) for v in [3, 4, 5, 6, 7, 8]
]) <= presupuesto_total, "restriccion_presupuesto"

# Proporciones mínimas y máximas por valor
modelo += lpSum([y[i, 4] for i in range(n)]) >= 0.05 * n, "restriccion_min_5_por_ciento_4"
modelo += lpSum([y[i, 5] for i in range(n)]) >= 0.05 * n, "restriccion_min_10_por_ciento_5"
modelo += lpSum([y[i, 6] for i in range(n)]) >= 0.15 * n, "restriccion_min_20_por_ciento_6"
modelo += lpSum([y[i, 3] for i in range(n)]) <= 0.11 * n, "restriccion_max_10_por_ciento_3"
modelo += lpSum([y[i, 7] for i in range(n)]) <= 0.3 * n, "restriccion_max_30_por_ciento_7"
modelo += lpSum([y[i, 8] for i in range(n)]) <= 0.07 * n, "restriccion_max_5_por_ciento_8"

# Restricción: Supervisiones por cliente entre 48% y 50% de sus móviles
for cliente, moviles_cliente in moviles_por_cliente.items():
    indices_cliente = [i for i, (lugar, _) in enumerate(lugares) if lugar in moviles_cliente]
    num_moviles = len(moviles_cliente)
    min_supervisiones = math.ceil(0.48 * num_moviles * 12)  # 48% del total
    max_supervisiones = math.ceil(0.49 * num_moviles * 12)  # 50% del total

    modelo += (
        lpSum(y[i, v] * v for i in indices_cliente for v in [3, 4, 5, 6, 7, 8]) >= min_supervisiones,
        f"restriccion_min_supervisiones_{cliente}"
    )

    modelo += (
        lpSum(y[i, v] * v for i in indices_cliente for v in [3, 4, 5, 6, 7, 8]) <= max_supervisiones,
        f"restriccion_max_supervisiones_{cliente}"
    )

# Resolver el modelo
solver = PULP_CBC_CMD(msg=True)
modelo.solve(solver)

# Validar los resultados
print("\n=== Resultados del Modelo ===\n")
print(f"Estado del Modelo: {modelo.status}, {LpStatus[modelo.status]}")
print(f"Valor Objetivo: {modelo.objective.value()}")

# Calcular presupuesto utilizado
presupuesto_utilizado = sum(
    y[i, v].value() * v * lugares[i][1] for i in range(n) for v in [3, 4, 5, 6, 7, 8]
)
print(f"Presupuesto Total Disponible: {presupuesto_total}")
print(f"Presupuesto Utilizado: {presupuesto_utilizado:.2f}")
print(f"Porcentaje de Presupuesto Utilizado: {(presupuesto_utilizado / presupuesto_total) * 100:.2f}%")
# Mostrar asignación de visitas por lugar
print("\n=== Asignación de Visitas por Móvil ===\n")
for i in range(n):
    asignado = False
    for v in [3, 4, 5, 6, 7, 8]:
        if y[i, v].value() == 1:
            print(f"{lugares[i][0]}: {v} visitas")
            asignado = True
            break
    if not asignado:
        print(f"{lugares[i][0]}: Sin asignación")

# Supervisiones totales por cliente con límites
print("\n=== Supervisiones Totales por Cliente ===\n")
for cliente, moviles_cliente in moviles_por_cliente.items():
    indices_cliente = [i for i, (lugar, _) in enumerate(lugares) if lugar in moviles_cliente]
    total_supervisiones_cliente = sum(
        (y[i, v].value() or 0) * v for i in indices_cliente for v in [3, 4, 5, 6, 7, 8]
    )
    min_supervisiones = math.ceil(0.48 * len(moviles_cliente) * 12)
    max_supervisiones = math.ceil(0.49 * len(moviles_cliente) * 12)
    print(f"Cliente: {cliente}, Supervisiones totales: {total_supervisiones_cliente:.2f}, Mínimo requerido: {min_supervisiones}, Máximo permitido: {max_supervisiones}")

# Calcular y mostrar porcentaje de móviles con 7 y 8 visitas
total_moviles_7 = sum(1 for i in range(n) if y[i, 7].value() == 1)
total_moviles_8 = sum(1 for i in range(n) if y[i, 8].value() == 1)
print("\n=== Porcentajes de Visitas Altas ===\n")
print(f"Porcentaje de móviles con 7 visitas: {(total_moviles_7 / n) * 100:.2f}%")
print(f"Porcentaje de móviles con 8 visitas: {(total_moviles_8 / n) * 100:.2f}%")
